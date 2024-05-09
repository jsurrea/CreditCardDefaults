#!/bin/bash

# Usage: This script is used to setup the environment in the server

sudo apt update
sudo apt install python3-pip -y
sudo apt install git -y
sudo apt install screen -y
sudo apt install python3-virtualenv

virtualenv myenv
source myenv/bin/activate

git clone https://github.com/jsurrea/CreditCardDefaults.git
cd CreditCardDefaults/Despliegue

pip install -r requirements.txt
screen -S dashboard_session -d -m python app.py
