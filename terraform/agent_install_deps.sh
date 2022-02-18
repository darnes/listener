#!/bin/bash
# sudo apt-get update -y

# code deploy agent
sudo yum install ruby -y
sudo yum install wget -y
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent start
rm install

# supervisor
# epel needed for supervisor
sudo amazon-linux-extras install epel -y
sudo yum install supervisor -y
sudo service supervisord start