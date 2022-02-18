#!/bin/bash
# executed as a first thing after files copy
mkdir -p /home/ec2-user/listener-app
pwd
tar -xzvf /home/ec2-user/artifact.tar.gz -C /home/ec2-user/listener-app
echo 'unpack complete, refreshing supervisor config'

sudo mv /home/ec2-user/listener.ini /etc/supervisord.d/
sudo supervisorctl reread
sudo supervisorctl update
