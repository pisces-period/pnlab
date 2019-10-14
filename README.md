# PN-LAB
---

Welcome to the PN lab. This file contains general instructions to start up the lab and run the tests.

The PN lab includes an Ansible playbook, 2 ansible roles and a "detached" task (declared in the playbook), all designed to tackle the 3 challenges which have been proposed.

A few words regarding the setup:

2 Vagrant Boxes are created and automatically provisioned via Vagrant, for your convenience.
They are both running ubuntu/xenial64 - Ubuntu 16.04:
* pan-peter (IP 192.168.50.10) - Ansible controller/slave (ansible is installed via bootstrap script)
* peter-pan (IP 192.168.50.11) - Test VM (for port scanning and logging)

The VMs share a private network and can ping each other.

You can configure peter-pan box to send logs to pan-peter, and also use peter-pan as a target of port scanning. Please notice that peter-pan box is __*NOT*__ managed by Ansible.

The ansible-playbook runs on pan-peter at boot-time via Vagrant provisioning, but you can re-run it at any time or change the Vagrantfile to remove this step from provisioning.

To start up the lab, run the following command at the root directory of the repo (where Vagrantfile should be):

` vagrant up `

Then, log into the box of your choosing by invoking the following command (replace with the box name):

`vagrant ssh $(box)`

I strongly recommend you immediately run `sudo -i` everytime you log into the boxes, so root permissions won't be a problem.

Though the box logs into the / root folder by default, you'll want to `cd /vagrant` as this is the _de facto_ root folder of the pn lab.

I'm assuming a target environment with VirtualBox and Vagrant installed. If you wish to use a different provider other than VirtualBox, please override the `config.vm.provider=virtualbox` directive on the `Vagrantfile` along with any other VirtualBox-specific settings and replace them with the vendor of your choosing (https://www.vagrantup.com/docs/providers/).

Please read the 'Component Version' section to ensure this lab will run on your environment.

### Overview
---
When you log into __*pan-peter*__ box (192.168.50.10), you *shouldn't* need to run Ansible playbooks (unless you want to). Vagrant executes `ansible-playbook play.yml` command as part of the provisioning process, upon first boot, to streamline the provisioning of the box.

As a result, the following roles are automatically created:
* Syslog (for exercise III) - Syslog configuration (default, custom and remote logs)
* Docker (for exercise I) - weather app and Docker logging driver

Additionally, a __*install NMAP and dependencies*__ task is triggered by Ansible (as specified in the play.yml file). This task is simple enough to not need a dedicated role and prepares the environment for exercise II (port scanning).

This box is the main box where all the Ansible roles and apps are installed.

You should see the following folder structure on pan-peter VM (relative to /vagrant):
```
.
├── ansible
│   ├── inventory.txt
│   ├── play.yml
│   └── roles
│       ├── docker
│       │   ├── defaults
│       │   │   └── main.yml
│       │   ├── files
│       │   │   └── daemon.json
│       │   ├── handlers
│       │   │   └── main.yml
│       │   ├── meta
│       │   │   └── main.yml
│       │   ├── README.md
│       │   ├── tasks
│       │   │   └── main.yml
│       │   ├── templates
│       │   ├── tests
│       │   │   ├── inventory
│       │   │   └── test.yml
│       │   └── vars
│       │       └── main.yml
│       └── rsyslog
│           ├── defaults
│           │   └── main.yml
│           ├── files
│           ├── handlers
│           │   └── main.yml
│           ├── meta
│           │   └── main.yml
│           ├── README.md
│           ├── tasks
│           │   └── main.yml
│           ├── templates
│           │   ├── 50-default.conf.j2
│           │   └── rsyslog.conf.j2
│           ├── tests
│           │   ├── inventory
│           │   └── test.yml
│           └── vars
│               └── main.yml
├── bootstrap.sh
├── getweather
│   ├── app
│   │   ├── getweather.py
│   │   └── __init__.py
│   ├── Dockerfile
│   ├── README.md
│   ├── requirements.txt
│   └── setup.py
├── README.md
├── scanner
│   ├── app
│   │   ├── __init__.py
│   │   └── scanner.py
│   ├── README.md
│   ├── requirements.txt
│   └── setup.py
└── Vagrantfile
```
Onto the exercises.

### Rsyslog Role (Exercise III)
---

Please read the [_README_](https://github.com/pisces-period/pnlab/blob/master/ansible/roles/rsyslog/README.md) file included with this ansible role for further information on how it is implemented.

### Docker Role (Exercise I)
---

Please read the [_README_](https://github.com/pisces-period/pnlab/blob/master/ansible/roles/docker/README.md) file included with this ansible role for further information on how it is implemented.

### NMAP Task (Exercise II)
---

The objective of this exercise is to create a port scanner (via programming language or third party app) which takes parameters via CLI and displays differences between subsequent scans.

This task is accomplished via a combination of Python-NMAP module and NMAP application. You need to use sudo -i so that the app will run (NMAP requires elevation). Though not requested to be deployed via Ansible, I'm using the APT module to install NMAP and dependencies.

You can read the __*README.md*__ file for specifics on how the app works.

UDP port scanning is disabled by default (but written into the source code, if you would like to test it too).

#### Testing Exercise II

Simply invoke the executable script (if you are not directly within the __*/vagrant/scanner/app*__ folder, you'll have to invoke the full path) and make sure you have root privileges. Pass the parameters via CLI, like so (use valid IP addresses and/or networks):

` cd /vagrant/scanner/app `
` ./scanner.py 127.0.0.1/32 192.168.50.10 192.168.50.11 192.168.50.0/28 8.8.8.8* `

###### \*please avoid scanning ports outside of the LAN as it is illegal in some countries

You can use peter-pan to install applications (e.g. Apache2) and verify if the new open ports have been scanned correctly. As you'll remember, peter-pan's IP address is 192.168.50.11 (provisioned by Vagrant).

` vagrant ssh peter-pan `
` sudo -i `
` apt-get install apache2 `
` systemctl start apache2 `

Wait a while and re-run the scan. You should see an output similar to the following:
```
attempting to scan host 192.168.50.10
Scanning 192.168.50.10 ...
Target 192.168.50.10: no new records found since last scan.
attempting to scan host 192.168.50.11
Scanning 192.168.50.11 ...
Target:192.168.50.11   22/open/tcp
Target:192.168.50.11   80/open/tcp
```

###### Component Version:
The following component versions have been used to create this lab:
###### _VirtualBox: 6.0.12_
###### _Vagrant: 2.2.5_
###### _Ansible: 2.8.5_
###### _Docker: 18.09.7, build 2d0083d_
###### _NMAP: 7.1_
