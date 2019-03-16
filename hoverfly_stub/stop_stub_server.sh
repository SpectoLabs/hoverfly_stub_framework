#!/usr/bin/env bash

##############################################################################################
# Name  : stop_stub_server.sh
# Brief : Script to Stop Hoverfly Stub Server
# Author: Navdit Sharma
# Date  : 13th, March, 2019
# Notes : 13/03/2019 -- Created Version 1 of Script
##############################################################################################

if [ ! -d "$HOME/Hoverfly/hoverfly_home" ]; then
    echo "CUSTOM INFO: Hoverfly is not installed!"
    ./install_hoverfly.sh
fi

export PATH=$PATH:$HOME/Hoverfly/hoverfly_home/

hoverctl stop
echo "CUSTOM INFO: Server Stopped"