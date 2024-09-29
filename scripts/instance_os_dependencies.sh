#!/usr/bin/env bash

sudo apt update
# Install Python3 pip
sudo apt install -y python3-pip

# Install Nginx
sudo apt install -y nginx

sudo apt install -y gunicorn

# Install Virtualenv
sudo apt install -y virtualenv