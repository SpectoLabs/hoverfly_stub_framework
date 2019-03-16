#!/usr/bin/env bash
##############################################################################################
# Name  : start_stub_server.sh
# Brief : Script to Start Hoverfly Stub Server
# Author: Navdit Sharma
# Date  : 13th, March, 2019
# Notes : 13/03/2019 -- Created Version 1 of Script
##############################################################################################

# ToDo: Uncomment Following code in case you would like to check for installation
#if [ ! -d "$HOME/Hoverfly/hoverfly_home" ]; then
#    echo "CUSTOM INFO: Hoverfly is not installed!"
#    ./install_hoverfly.sh
#fi

export PATH=$PATH:$HOME/Hoverfly/hoverfly_home/

echo "CUSTOM INFO: Starting Hoverfly webserver..."
hoverctl start --listen-on-host 0.0.0.0 webserver
hoverctl import stub_final_config.json

echo "CUSTOM INFO: Setting correct mode..."
hoverctl mode simulate

echo "CUSTOM INFO: Adding middleware..."
hoverctl middleware --binary python --script latency_middleware.py



