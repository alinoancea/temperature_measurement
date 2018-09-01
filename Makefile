APPPATH=/var/temp_measurement
USER=pi
SSHSRV?=raspi
SSH=ssh $(SSHSRV)
SHELL=/bin/bash

dependencies: push-app
	$(SSH) "sudo apt update"
	$(SSH) "sudo apt install -y build-essential python3-dev python3-pip"
	$(SSH) "sudo python3 -m pip install --upgrade pip setuptools wheel"
	$(SSH) "sudo pip3 install -r $(APPPATH)/requirements.txt"

push-app:
	$(SSH) "sudo mkdir -p $(APPPATH)/templates"
	$(SSH) "sudo chown -R $(USER):$(USER) $(APPPATH)"
	scp *.py requirements.txt $(SSHSRV):$(APPPATH)/
	scp templates/* $(SSHSRV):$(APPPATH)/templates/

push-service:
	cat temp_measurement.service|$(SSH) "sudo tee /etc/systemd/system/multi-user.target.wants/temp_measurement.service > /dev/null"
	$(SSH) sudo systemctl daemon-reload

restart-service:
	$(SSH) "sudo systemctl stop temp_measurement; sudo systemctl start temp_measurement"
	$(SSH) "sudo systemctl status temp_measurement"

deploy: push-app push-service restart-service