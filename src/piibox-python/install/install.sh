#!/bin/bash
# Loader for the deploy script

# Run with wget http://pastebin.com/raw.php?i=sgXjZNkk -O - | tr -d '\015' | sh

# Check we have the following up to date
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install ca-certificates ssh git build-essential python fabric rpi-update python-virtualenv supervisor -y
sudo apt-get install python-dev python-gtk2-dev git automake libtool espeak python-django python-simplejson -y
sudo service ssh start

# Update the firmware
read -p "Do you want to update the firmware on this machine (y/n)?"
[ "$REPLY" == "y" ] && sudo rpi-update && sudo reboot

reponame=piibox-python

# check out the repo with our fabric script in
git clone https://piibox-readonly:2Nr_cr2GA6Dy9XRnWDSEHzh-FQ_U2ehv@bitbucket.org/chrispbailey/$reponame $reponame

# run deploy
fab -f $reponame/install/fabfile.py install

# Clean up
rm -rf $reponame