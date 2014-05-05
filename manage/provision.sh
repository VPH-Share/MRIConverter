#!/bin/bash
set -o nounset
set -o errexit
shopt -s expand_aliases
#######################################
# Source helper utilities
source manage/utils.sh
setlocales
pkgupdate
#######################################
# Install MRIConverter and dependencies
pkginstall libgtk2.0-0 libsm-dev libjpeg62-dev
sudo tar xzf vendors/MRIConvert-2.0.7-x86_64.tar.gz -C vendors
#######################################
# Install Webservices Dependencies
pkginstall python-pip
pkginstall python-dev python-lxml
sudo pip install -r manage/requirements.txt
#######################################
# Configure init.d to autostart
sudo cat manage/initd.mriconverter > /etc/init.d/mriconverter
sudo chmod +x /etc/init.d/mriconverter
sudo update-rc.d mriconverter defaults
#######################################
# Start application
sudo service mriconverter start
