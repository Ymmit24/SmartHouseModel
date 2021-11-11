import os
import re
import socket
import sys
from datetime import datetime
from fabric.api import *
from fabric.contrib import files
from fabric.context_managers import settings
from fabric import operations

APP_NAME = 'piiboxweb'

# Project paths
root = os.path.splitdrive(sys.executable)[0] or '/'
PROJECTS = os.path.join(root, 'usr','local','projects')
WWWPY_ROOT = os.path.join(PROJECTS,APP_NAME)
SRC_DIR = os.path.join(WWWPY_ROOT, 'src')
LOG_DIR = os.path.join(WWWPY_ROOT, 'logs')
CONF_DIR = os.path.join(WWWPY_ROOT, 'conf')
BIN_DIR = os.path.join(WWWPY_ROOT, 'bin')

# Bitbucket account details
USER = 'piibox-readonly'
PWD = '2Nr_cr2GA6Dy9XRnWDSEHzh-FQ_U2ehv'

BITBUCKETS = [('chrispbailey','piibox-python'),]

# pip-installable dependencies
PIP = ['bottle','cherrypy']

# default user account to use
env.user = 'pi'

def install(site='localhost'):
    """ Run secure_pi, deploy and setup_service to build whole project """
    secure_pi(site)
    deploy(site, restart=False)
    setup_piface(site)
    register_webserver(site)
    restart_webserver(site)

def deploy(site='localhost', restart=False):
    """
    Build project directory, install required dependencies and checkout the source code
    """
    
    with settings(host_string=site):
        
        pip_cmd = os.path.join('.','bin','pip')
        
        if not files.exists(PROJECTS):
            sudo('mkdir -p %s' % PROJECTS)
        
        for d in [WWWPY_ROOT,SRC_DIR, LOG_DIR, CONF_DIR]:
            if not files.exists(d):
                sudo('mkdir -p %s' % d)
                sudo('chown %s %s' % (env.user, d))

        with cd(WWWPY_ROOT):
            if not files.exists(os.path.join(BIN_DIR)):
                run('virtualenv --setuptools %s' % (WWWPY_ROOT))
        
            for egg in PIP:
                run('%s install %s' % (pip_cmd, egg))
        
            # fetch code
            for (repo, egg) in BITBUCKETS:
                if not files.exists(os.path.join(SRC_DIR,egg)):
                    run('%s install --no-dependencies -e git+https://%s:%s@bitbucket.org/%s/%s.git#egg=%s' % (pip_cmd, USER, PWD, repo, egg, egg))

                    # force push requests to use alternative credentials
                    with cd(os.path.join(SRC_DIR,egg)):
                        run('git config remote.origin.pushurl https://bitbucket.org/%s/%s.git' % (repo, egg))
                else:
                    with cd(os.path.join(SRC_DIR,egg)):
                        run('git pull')
                
            if restart:
                restart_webserver(site)
            else:
                print 'Installation finished'
                print 'Run the server with:'
                print '$>bin/bottle.py rpi.controller:app'


# Functions for running in production

def register_webserver(site='localhost'):
    """ Register the webserver with supervisord to be run as a background process on startup """
    with hide('output'), settings(host_string=site):
        ip = _get_ip(site)
        
        conf_file = '/etc/supervisor/supervisord.conf'
        if '[program:%s]' % APP_NAME not in sudo('cat %s' % conf_file):
            script = """
[program:%s]
command=%s/bin/bottle.py --server cherrypy --bind 0.0.0.0:80 rpi.controller:app
process_name=%s
user=root
priority=999
autorestart=true
redirect_stderr=true
stdout_logfile=%s/rpi_out.txt
stderr_logfile=%s/rpi_err.txt""" % \
(APP_NAME, WWWPY_ROOT, '%(program_name)s', LOG_DIR, LOG_DIR)
            filedict = {conf_file:script,}
            for file, lines in filedict.items():
                files.append(file, lines, use_sudo=True)
            
            # make sure supervisord is running
            sudo('supervisord')
            sudo('supervisorctl update')
        else:
            sudo('supervisorctl restart %s' % APP_NAME)
        
        status = sudo('supervisorctl status')
        if 'RUNNING' in status:
            print 'Server running. Access the site at:'
            print 'http://%s/' % ip
        else:
            print 'WARNING: Service not started!'

def restart_webserver(site='localhost'):
    """ Restart the supervisord-controlled webserver process """
    with hide('output'), settings(host_string=site):
        status = sudo('supervisorctl restart %s' % APP_NAME)
        if 'RUNNING' in status:
            print 'Server restarted. Access the site at:'
            print 'http://%s/' % _get_ip(site)


# Initial setup functions

def secure_pi(site='localhost',force=False):
    """
    Set up iptables to allow all traffic from the internal LAN but block ssh coming from your firewall
    Taken from http://simonthepiman.com/how_to_setup_your_pi_for_the_internet.php
    """
    
    with hide('output'), settings(host_string=site):
        if 'PermitRootLogin yes' in run('cat /etc/ssh/sshd_config'):
            print 'Disabling root login'
            files.sed('/etc/ssh/sshd_config','PermitRootLogin yes','PermitRootLogin no', use_sudo=True)
            sudo('/etc/init.d/sshd restart')
        
        gateway = _get_gateway(site)
        if not re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',gateway):
            print 'No gateway found, halting...'
            return
        
        ip = _get_ip(site)
        
        sudo('chmod 0600 /etc/network/interfaces')
        
        if force:
            sudo('rm /etc/network/iptables')
        
        if files.exists('/etc/network/iptables', use_sudo=True):
            print 'iptables already configured'
            return
        
        if 'iptables-restore' not in sudo('cat /etc/network/interfaces'):
            sudo('echo "pre-up iptables-restore < /etc/network/iptables" >> /etc/network/interfaces')
        
        iptables = """*filter
:INPUT DROP [23:2584]                                             -m comment --comment "dont accept any incoming network traffic unless a following rule overrides"
:FORWARD ACCEPT [0:0]                                             -m comment --comment "accept any forwarding requests"
:OUTPUT ACCEPT [1161:105847]                                      -m comment --comment "Allow any outbound network traffic"
-A INPUT -i lo -j ACCEPT                                          -m comment --comment "Allow any connections from the local host"
-A INPUT -i eth0 -p tcp -m tcp --dport 80 -j ACCEPT               -m comment --comment "Allow all traffic via port 80 (http) over ethernet"
-A INPUT -i eth0 -p tcp -m tcp --dport 443 -j ACCEPT              -m comment --comment "Allow all traffic via port 443 (https) over ethernet"
-A INPUT -i wlan0 -p tcp -m tcp --dport 80 -j ACCEPT              -m comment --comment "Allow all traffic via port 80 (http) over wifi"
-A INPUT -i wlan0 -p tcp -m tcp --dport 443 -j ACCEPT             -m comment --comment "Allow all traffic via port 443 (https) over wifi"
-A INPUT -s %s/24 -j ACCEPT                                       -m comment --comment "Allow all traffic from the internal LAN"
-A INPUT -s %s/32 -i tcp -p tcp -m tcp --dport 22 -j DROP         -m comment --comment "However block any traffic to port 22 (ssh) coming from your firewall"
-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT                  -m comment --comment "Allow ping traffic so you can test from outside - this can be deleted for extra security"
-A INPUT -i eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT   -m comment --comment "allow inbound access to any internally generated requests via ethernet"
-A INPUT -i wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT  -m comment --comment "allow inbound access to any internally generated requests via wifi"
COMMIT                                                            -m comment --comment "Finally commit the entries to the firewall"
""" % (ip, gateway)

        filedict = {'/etc/network/iptables':iptables,}
        for file, lines in filedict.items():
            if files.exists(file):
                sudo('rm -f %s' % file)
            sudo('touch %s' % file)
            files.append(file, lines, use_sudo=True)
        
        sudo('iptables-restore /etc/network/iptables')
        if ip in sudo('iptables-save'):
            print 'Tables loaded successfully'
        
        _add_to_startup(site, 'iptables-restore /etc/network/iptables')

def setup_piface(site='localhost'):
    with settings(host_string=site):
        sudo("sed -i 's/blacklist spi-bcm2708/#blacklist spi-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf")
        sudo('modprobe spi-bcm2708')
        
        if not files.exists(os.path.join(SRC_DIR,'piface')):
            with cd(WWWPY_ROOT):
                run('git clone https://github.com/thomasmacpherson/piface.git %s/piface' % SRC_DIR)
                run('bin/pip install -e %s/piface/python/' % SRC_DIR)
                sudo('%s/piface/scripts/spidev-setup' % SRC_DIR)
        else:
            print 'PiFace already installed'

# Utility commands

def shutdown(site='localhost', reboot=False):
    """ Remotely shutdown the machine """
    with hide('output'), settings(host_string=site):
        if reboot:
            from fabric import operations
            operations.reboot(0)
        else:
            sudo('halt -p')

def rpi_update(site='localhost'):
    """ Update the firmware on the PI """
    sudo('rpi-update')
    sudo('reboot')


# Private functions

def _add_to_startup(site, command):
    with hide('output'), settings(host_string=site):
        if command not in run('cat /etc/rc.local'):
            files.sed('/etc/rc.local','^exit 0','%s\\n\\nexit 0' % command, use_sudo=True)

def _get_gateway(site):
    
    with hide('output'), settings(host_string=site):
        gateway = sudo('grep nameserver /etc/resolv.conf ').split(" ")[1]
        print 'Gateway is %s' % gateway
        return gateway

def _get_ip(site):
    
    with hide('output'), settings(host_string=site):
        ip = socket.gethostbyname(socket.getfqdn())
        print 'IP is %s' % ip
        return ip
