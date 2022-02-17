#!/bin/bash

mkdir -p /home/ec2-user/listener-app
pwd
tar -xzvf /home/ec2-user/artifact.tar.gz -C /home/ec2-user/listener-app
echo "unpack complete"