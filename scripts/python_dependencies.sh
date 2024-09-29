#!/usr/bin/env bash

sudo chown -R ubuntu:ubuntu ~/Elearn
virtualenv /home/ubuntu/Elearn/venv
source /home/ubuntu/Elearn/venv/bin/activate
pip install -r /home/ubuntu/Elearn/requirements.txt