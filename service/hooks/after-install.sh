#!/bin/bash
# executed as a first thing after files copy
mkdir -p /home/ec2-user/listener-app
pwd
tar -xzvf /home/ec2-user/artifact.tar.gz -C /home/ec2-user/listener-app

echo 'setting up envirounment'
python3 -m venv /home/ec2-user/venv
/home/ec2-user/venv/bin/pip install -r /home/ec2-user/requirements.txt

echo 'unpack complete, refreshing supervisor config'

#sudo chmod a+x /home/ec2-user/listener-app/src/start.sh # no need 

sudo mv /home/ec2-user/listener.ini /etc/supervisord.d/
sudo supervisorctl reread
sudo supervisorctl update
