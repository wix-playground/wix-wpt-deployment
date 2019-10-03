#!/bin/bash

AGENT_LOCATION=$1


function log () {
	echo "$(date) : $1"
}


function restart_host () {
	log "Stopping WPT agent ..."
	sudo systemctl stop wptagent

	log "Rebooting host ..."
	sudo reboot
}


function update_agent () {
	log "Checking if there is an update for the WPT agent ..."
	git remote update

	UPSTREAM=${1:-'@{u}'}
	LOCAL=$(git rev-parse @)
	REMOTE=$(git rev-parse "$UPSTREAM")

	if [ $LOCAL = $REMOTE ]; then
	    log "WPT agent is up-to-date"
	else
	    log "WPT agent needs to be updated"
	    log "Starting to update WPT agent ..."
	    git pull origin master
	    restart_host
	fi
}


if [ $# -eq 0 ]; then
	echo "No arguments provided."
	echo "You must pass the path to the location of the wptagent repository."
	exit 1
fi

cd $AGENT_LOCATION
update_agent