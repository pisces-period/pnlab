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
