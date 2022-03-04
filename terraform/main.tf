terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "app_server" {
  ami = "ami-038b3df3312ddf25d"
  instance_type = "t2.medium"
  vpc_security_group_ids = [aws_security_group.listener-sg.id]

  user_data = file("agent_install_deps.sh")
  
  tags = {
    Name = "ListenerInstance"
  }
  key_name = "MasterKey"
  # tbd: attach role https://stackoverflow.com/questions/41997426/instanceagentpluginscodedeployplugincommandpoller-missing-credentials
  # so CodeDeployAgent can connect
  # + attach CodeDeploy policies.... 
  iam_instance_profile = "ListenerAgentRole"
  security_groups = [
    "listener-sg"
  ]
}

resource "aws_security_group" "listener-sg" {
  name = "listener-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


# resource "aws_key_pair" "master_key" {
#   key_name   = "deployer-key"
#   public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD3F6tyPEFEzV0LX3X8BsXdMsQz1x2cEikKDEY0aIj41qgxMCP/iteneqXSIFZBp5vizPvaoIR3Um9xK7PGoW8giupGn+EPuxIA4cDM4vzOqOkiMPhz5XK0whEjkVzTo4+S0puvDZuwIsdiW9mxhJc7tgBNL0cYlWSYVkz4G/fslNfRPW5mYAM49f4fhtxPb5ok4Q2Lg9dPKVHO/Bgeu5woMc7RY0p1ej6D4CKFE6lymSDJpW0YHX/wqE9+cfEauh7xZcG0q9t2ta6F6fmX0agvpFyZo8aFbXeUBr7osSCJNgvavWbM/06niWrOvYX2xwWdhXmXSrbX8ZbabVohBK41 email@example.com"
# }

#TBD: make output with DNS name
# cloudwatch logs perms:
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": [
#         "logs:Create*",
#         "logs:PutLogEvents"
#         ],
#       "Effect": "Allow",
#       "Resource": "arn:aws:logs:*:*:*"
#     },
#     {
#       "Action": [
#         "ecs:CreateCluster",
#         "ecs:DeregisterContainerInstance",
#         "ecs:DiscoverPollEndpoint",
#         "ecs:RegisterContainerInstance",
#         "ecs:Submit*",
#         "ecs:Poll"
#       ],
#       "Effect": "Allow",
#       "Resource": "*"
#     }
#   ]
# }