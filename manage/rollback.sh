#!/bin/bash
set -o nounset
set -o errexit
shopt -s expand_aliases
#######################################
# Source helper utilities
source $REPO_DIR/manage/utils.sh
log "Updating OS packages"
pkgupdate
#######################################
log "Stopping application"
sudo service mriconverter stop
#######################################
log "Deconfigure SOAPLib to autostart"
sudo update-rc.d mriconverter disable
sudo rm /etc/init.d/mriconverter
#######################################
log "Uninstalling SOAPlib Commandline Wrapper dependencies"
sudo pip uninstall -r $REPO_DIR/manage/requirements.txt
pkgremove python-dev python-lxml
pkgremove python-pip
#######################################
sudo rm -rf /webapp
sudo rm /root/$REPO_NAME-install.log
