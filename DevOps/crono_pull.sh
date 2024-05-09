#!/bin/bash

# Usage: This script is used to pull the latest changes from the repository each minute (CI/CD)
cd ~/Project-1-analitica
git pull

# Setup: 
# sudo yum install cronie cronie-anacron
# sudo systemctl start crond
# sudo systemctl enable crond
# chmod +x crono_pull.sh
# crontab -e
# Add the following line to the crontab file
# */1 * * * * /home/ec2-user/Project-1-analitica/DevOps/crono_pull.sh >/dev/null 2>&1
