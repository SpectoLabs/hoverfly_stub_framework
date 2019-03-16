#!/usr/bin/env bash

##############################################################################################
# Name  : install_hoverfly.sh
# Brief : Script to install Hoverfly on Linux Machine and set Path Variables
# Author: Navdit Sharma
# Date  : 13th, March, 2019
# Notes : 13/03/2019 -- Created Version 1 of Script
##############################################################################################

echo "CUSTOM INFO: Installing Hoverfly"
LINUX_BIT="$(getconf LONG_BIT)"

echo "CUSTOM INFO: Create Hoverfly Folder"
mkdir $HOME/Hoverfly

cd $HOME/Hoverfly
mkdir archive
mkdir hoverfly_home


if [ ${LINUX_BIT} -eq 64 ]; then
    echo "CUSTOM INFO: Getting Linux 64 bit hoverfly_stub bundle"
    wget -P $HOME/Hoverfly/archive https://github.com/SpectoLabs/hoverfly/releases/download/v1.0.0-rc.2/hoverfly_bundle_linux_amd64.zip
    echo "CUSTOM INFO: Unzip the bundle to hoverfly_home"
    unzip archive/hoverfly_bundle_linux_amd64.zip -d  hoverfly_home/
else
    echo "CUSTOM INFO: Getting Linux 32 bit hoverfly_stub bundle"
    wget -P $HOME/Hoverfly/archive https://github.com/SpectoLabs/hoverfly/releases/download/v0.17.7/hoverfly_bundle_linux_386.zip
    echo "CUSTOM INFO: Unzip the bundle to hoverfly_home"
    unzip archive/hoverfly_bundle_linux_386.zip -d  hoverfly_home/
fi

echo "CUSTOM INFO: Set Path variable"
export PATH=$PATH:$HOME/Hoverfly/hoverfly_home/

