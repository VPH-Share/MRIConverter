#!/bin/bash
set -o nounset
set -o errexit
shopt -s expand_aliases
#######################################
# Source helper utilities
source manage/utils.sh
log "Updating OS packages"
pkgupdate
log "Setting GB locale"
setlocales
#######################################
log  "Installing MRIConverter commandline application and dependencies"
pkginstall libgtk2.0-0 libsm-dev libjpeg62-dev
sudo tar xzf $REPO_DIR/vendors/MRIConvert-2.0.7-x86_64.tar.gz -C vendors
#######################################
log "Installing SOAPlib Commandline Wrapper dependencies"
pkginstall python-pip
pkginstall python-dev python-lxml
sudo pip install -r $REPO_DIR/manage/requirements.txt
#######################################
log "Configure SOAPLib to autostart"
sudo cat $REPO_DIR/manage/initd.mriconverter > /etc/init.d/mriconverter
sudo chmod +x /etc/init.d/mriconverter
sudo update-rc.d mriconverter defaults
#######################################
log "Starting application"
sudo service mriconverter start
#######################################
log "Cleaning up..."
pkgclean
pkgautoremove
history -c
#######################################
