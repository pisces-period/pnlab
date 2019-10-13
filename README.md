# PN-LAB

Welcome to the PN lab. This file describes the proposed solutions to the exercises, as well as general instructions to start up the lab and run tests.

2 Vagrant Boxes are created and automatically provisioned via Vagrant, for your convenience.
They are both running ubuntu/xenial64 - Ubuntu 16.04:
* pan-peter (IP 192.168.50.10) - Ansible controller/slave
* peter-pan (IP 192.168.50.11) - Test VM (for port scanning and logging)

The VMs share a private network and can ping each other.
You can configure peter-pan box to send logs to pan-peter, and also use peter-pan as a target of port scanning. Please notice that peter-pan box is __*NOT*__ managed by Ansible.

The ansible-playbook runs on pan-peter at boot-time via Vagrant provisioning, but you can re-run it at any time or change the Vagrantfile to remove this step from provisioning.

To start up the lab, run the following command at the root directory of the repo (where Vagrantfile should be):

` vagrant up `

Then, log into the box of your choosing by invoking the following command (replace with the box name):

`vagrant ssh $(box)`

I strongly recommend you immediately run `sudo -i` everytime you log into the boxes, so root permissions won't be a problem.

Though the box logs into the / root folder by default, you'll want to `cd /vagrant` as this is the __de facto__ root folder of the pan-net lab.

I'm assuming a target environment with VirtualBox and Vagrant installed. If you wish to use a different provider other than VirtualBox, please override the __*config.vm.provider=virtualbox*__ directive on the __*Vagrantfile*__ along with any other VirtualBox-specific settings and replace them with the vendor of your choosing (https://www.vagrantup.com/docs/providers/).

Please read the 'Component Version' section to ensure this lab will run on your environment.

Below I detail the solutions to the exercises, and how the Ansible roles relate to them.

### Overview
When you log into __*pan-peter*__ box (192.168.50.10), you *shouldn't* need to run Ansible playbooks (unless you want to). Vagrant executes `ansible-playbook play.yml` command as part of the provisioning process, upon first boot, to streamline the provisioning of the box.

As a result, the following roles are automatically created:
* Syslog (for exercise III) - Syslog configuration (default, custom and remote logs)
* Docker (for exercise I) - weather app and Docker logging driver

Additionally, a __*install NMAP and dependencies*__ task is triggered by Ansible (as specified in the play.yml file). This task is simple enough to not need a dedicated role and prepares the environment for exercise II (port scanning).

This box is the main box where all the Ansible roles and apps are installed.

You should see the following folder structure on pan-peter VM (relative to /vagrant):
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
│   │   ├── 192.168.50.10_scanner.log
│   │   ├── 192.168.50.11_scanner.log
│   │   ├── __init__.py
│   │   └── scanner.py
│   ├── README.md
│   ├── requirements.txt
│   └── setup.py
├── ubuntu-xenial-16.04-cloudimg-console.log
└── Vagrantfile

Let's discuss a bit further about the roles.

### Syslog Role (Exercise III)

The objective of this exercise is to configure an rsyslog server, capable of logging default log files, as well as custom log files, and relaying logs to an external log server. This role is deployed first because it makes more sense to prepare the syslog server before sending Docker logs.

To accomplish this task, I'm dedicating a role for this configuration, along with 2 tasks, both using jinja2 and Ansible template module, and a notify-hook to restart services when appropriate. Please notice the configuration is based on group/root 644 permissions and you'll need to perform sudo -i to be able to navigate the log files.

Within the __*rsyslog*__ role folder structure, the __*defaults*__ folder contains a __*main.yml*__ file, which stores the desired configuration for the rsyslog server. Therefore, any desired configuration change __*MUST*__ be set here and here only (e.g., adding remote syslog servers to relay logs, custom syslog rules, etc.).

When you run the Ansible playbook, these defaults are evaluated and copied to the __*rsyslog.conf*__ and __*50-default.conf*__ files respectively, using Ansible __*template*__ module. The changes (if there is any) are written to the template files, which are located in __*rsyslog/templates*__ (OBS - this is relative to the roles folder, the actual full path is /vagrant/ansible/roles/rsyslog/templates).

These template files contain jinja2 expressions, which add/update/remove lines according to the defaults specified. The original file is then replaced by a new version that contains all the changes.

The first task evaluates/re-writes the __*rsyslog.conf*__ file (general settings, custom rules).

The second task evaluates/re-writes the __*50-default.conf*__ file (log relay settings).

#### Testing Exercise III
If you want, you can use the readily available peter-pan box to test remote log settings, by logging into the box (do not forget to escalate privilege) and appending the following line at the end of the __*/etc/rsyslog.d/50-default.conf*__ file:
`*.*   @192.168.50.10:514 `

Next,restart the rsyslog service:
` systemctl restart rsyslog `

Execute the following commnand (or any other log-related one, really):
` logger -n 192.168.50.10 "log" `

Then, SSH into Pan-Peter and verify the contents of /etc/var/log/syslog:
` vagrant ssh pan-peter `
` cat /etc/var/log/syslog `

Output example:
```
Oct 13 17:31:22 peter-pan apache2[3322]:  * Starting Apache httpd web server apache2
Oct 13 17:31:22 peter-pan apache2[3322]: AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.1.1. Set the 'ServerName' directive globally to suppress this message
Oct 13 17:31:23 peter-pan apache2[3322]:  *
Oct 13 17:31:23 peter-pan systemd[1]: Started LSB: Apache2 web server.
Oct 13 17:31:25 peter-pan systemd[1]: Reloading.
Oct 13 17:31:25 peter-pan systemd[1]: Started ACPI event daemon.
Oct 13 17:31:34 peter-pan systemd[1]: Started LSB: Apache2 web server.
Oct 13 17:32:47 peter-pan kernel: [ 4265.748603] DCCP: Activated CCID 2 (TCP-like)
Oct 13 17:50:03 peter-pan vagrant log
```

### Docker Role (Exercise I)

The objective of this exercise is to deploy a python app inside a docker container that forwards logs to the syslog server. This configuration is to be deployed by Ansible. The app takes parameters from CLI in the form of environment variables.

You can read the __*README.md*__ file for specifics on how the app works.

To accomplish this task, I'm dedicating a role for this configuration, along with 4 tasks and a notify-hook to restart services, when appropriate. __*Please notice that I'm NOT creating nor adding a Docker group to sudo list. Make sure you use sudo -i command before running containers*__.

The first task installs Docker.io and dependencies.

The second task enables the Docker service startup on boot.

The third task configures the Docker logging driver.

The fourth task uses the __*docker_image*__ module to build an image based on the Dockerfile. By default, this image is named __*getweather:v1.0*__. You'll need to use this name when you run your container.

The Dockerfile describes the necessary actions to install the dependencies and copy the /getweather directory into the container and run the app (notice that the app does not run as root, but as a random user ID 5000).

###### For further information regarding security of docker, please check these out:
https://docs.docker.com/engine/security/security/

#### Testing Exercise I

SSH into pan-peter and run the following command, replacing the ${API_KEY} and ${CITY} variables with a valid API key and a city whose weather you would like to inspect:
` vagrant ssh pan-peter `
` sudo -i `
` docker run --rm -e OPENWEATHER_API_KEY=="${API_KEY}" -e CITY_NAME="${CITY}" getweather:v1.0 `

Verify the output with the following command:
` cat /var/log/syslog | grep "openweather" `

You should see something like:
```
Oct 13 16:42:16 localhost 50d091e7a6b4[6808]: source:openweathermap,location:New York,description:clear sky,temp:16.58,humidity:45
```
### NMAP Task (Exercise II)

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
