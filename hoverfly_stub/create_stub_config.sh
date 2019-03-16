#!/usr/bin/env bash

##############################################################################################
# Name  : create_stub_config.sh
# Brief : Script to create Hoverfly stub config jason from Postman Collection and optional
#         Postman Environment File.

# Pre-requisites:
# 1. Hoverfly
# 2. Node.js
# 3. Newman (npm install -g newman)

# Author: Navdit Sharma
# Date  : 13th, March, 2019
# Notes : 13/03/2019 -- Created Version 1 of Script
##############################################################################################

# Function - Exports the captured requests by Hoverfly to Simulation and then stops the Hoverfly
export_simulation_and_stop_hoverfly(){

        echo "CUSTOM INFO: Exporting Simulation or Hoverfly Config"
        hoverctl export hoverfly_config_${TIME}.json

        echo "CUSTOM INFO: Stopping Hoverfly"
        hoverctl stop
}


# Validate Postman Collection
if [ -z "$1" ]; then
    echo "CUSTOM ERROR: Please provide Postman Collection"
    exit 1
elif [ ! -f "$1" ]; then
    echo "CUSTOM ERROR: Postman Collection not found at given location - $1"
    exit 1
else
    echo "CUSTOM INFO: Given Postman Collection is valid!"
fi

# Validate Postman Environment File
if [ -z "$2" ]; then
    echo "NOTE: No Postman Environment File has been provided."
else
    if [ ! -f "$2" ]; then
    echo "CUSTOM ERROR: Postman Environment File not found at given location - $2"
    exit 1
else
    echo "CUSTOM INFO: Given Postman Environment File is valid!"
    fi
fi


# Set Global Variables
POSTMAN_COLLECTION=$1
POSTMAN_ENV=$2
TIME=`date '+%Y_%m_%d_%H%M%S'`

echo "CUSTOM INFO: Starting Hoverfly"
hoverctl start

echo "CUSTOM INFO: Setting Capture mode"
hoverctl mode capture

echo "CUSTOM INFO: Setting up proxies"
export HTTP_PROXY=http://localhost:8500
export HTTPS_PROXY=http://localhost:8500

echo "CUSTOM INFO: Running Postman Collection"
# No Postman Environment file given
if [ -z "$2" ]; then
    if (newman run ${POSTMAN_COLLECTION} --insecure); then
        echo "CUSTOM INFO: Postman Collection Run SUCCESS!"
        export_simulation_and_stop_hoverfly
    else
        echo "CUSTOM ERROR: Please investigate your Postman Collection Run"
        exit 1
    fi

# Postman Env file given
else [ ! -f "$2" ]
    if (newman run ${POSTMAN_COLLECTION} --insecure -e ${POSTMAN_ENV}); then
        echo "CUSTOM INFO: Postman Collection Run was SUCCESSFUL!"
        export_simulation_and_stop_hoverfly
    else
        echo "CUSTOM ERROR: Please investigate your Postman Collection Run"
        exit 1
    fi
fi