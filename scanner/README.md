# PORT SCANNER

This app uses Python-NMAP module to probe known ports and compare subsequent scans for observable changes.

This app is designed to get IPv4/IPv6 and/or CIDR networks as arguments directly from CLI and pass them to NMAP for port scanning.

Port scanning is __illegal__ in some countries. Please be careful using this app.

## Variables

You can pass one or multiple arguments, separated by a whitespace, to the CLI.

e.g. ./scanner.py 127.0.0.1 192.168.0/32 

## Assumptions

This app makes the following assumptions:
* NMAP requires root privileges (make sure to escalate privilege before running it)
* For efficiency, only known ports [1-1024] are scanned
* UDP is disabled by default (the app does however include commented lines for UDP scanning)

###### For further information regarding Python-NMAP module, please check these out:
###### https://pypi.org/project/python-nmap/