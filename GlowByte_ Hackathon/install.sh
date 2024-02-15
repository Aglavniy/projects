#!/bin/bash

trap 'echo "Exit, (Ctrl+C) pressed!"; exit 1' 2

username=$(id -nu)
if [[ "$username" != "root" ]]; then
	echo "Please, use another user with sudo... exit."
	exit 1
fi

chmod +x install.sh
apt install python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# after install use:
# source venv/bin/activate
# main.py <name_csv>
# deactivate