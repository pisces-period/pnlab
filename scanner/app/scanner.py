#!/usr/bin/python3

# import statements

import nmap
import ipaddress
import os
import sys

# ideally this constant should be assigned via os.environ.get("${ENV}") - possibly deployed by Ansible via jinja2 templates or 'lineinfile' replacements of the appropriate bash profile
# environment variables. However I'm simply hard-coding it because yes =)

FILE_DIFF_PATH="/vagrant/scanner/app"
os.chdir(FILE_DIFF_PATH)

if __name__=="__main__":

    # scan result
    scan_output=""
    # previous scan
    previous_scan=""

    # get NMAP PortScanner
    scanner=nmap.PortScanner()

    # show NMAP version

    # for each IP Address(es) from STDIN *OBS: argv[0] == path to the script
    for argument in range(1, len(sys.argv)):

        print("attempting to scan host {}".format(sys.argv[argument]))

        target_ip=str(sys.argv[argument])

        # sS (SYN/TCP) - UDP is available but disabled by default due to scanning performance issues inherent to UDP scanning
        scanner.scan(target_ip, '22-443', 'v -sS')
        
        if scanner.all_hosts():
            pass
        else:
            print("No hosts found. Are you sure you are using valid IPv4/IPv6 IP addresses and or CIDR networks?")
            exit(0)
        
        # get data for each host:
        for host in scanner.all_hosts():
            print("Scanning {} ...".format(host))
            # get TCP data for each port:
            for port in scanner[host].all_tcp():
                scan_output+= "{}:{}   {}/{}/{}\n".format('Target', host, port,scanner[host]['tcp'][port]['state'], 'tcp')

            # get UDP data for each port:
            #for port in scanner[host].all_udp():
            #    scan_output+= "{}:{}    {}/{}/{}\n".format('Target', host, port,scanner[host]['udp'][port]['state'], "udp")

            if not scan_output:
                print("No ports found. Scanned ports on {} host might have been filtered".format(host))


            # check if a previous scan exists
            if os.path.isfile(FILE_DIFF_PATH + "/{}_scanner.log".format(host)):
                # if a previous scan exists, load the previous scan file
                with open (FILE_DIFF_PATH + "/{}_scanner.log".format(host), "r") as previous:
                    previous_scan=previous.read()
                    # if the scan_output is equal to the previous_scan, then no changes occurred:
                    if scan_output==previous_scan:
                        print("Target {}: no new records found since last scan.\n".format(host))
                    # else there's been a change since the last scan
                    else:
                        # dump the output to STDOUT
                        print("{}".format(scan_output))
                        # replace the previous scan file with current file
                        with open(FILE_DIFF_PATH + "/{}_scanner.log".format(host), "w") as current:
                            current.write(scan_output)

            # if no previous scan was detected, write the output to a file
            else:
                with open(FILE_DIFF_PATH + "/{}_scanner.log".format(host), "w") as current:
                    # dump the output to STDOUT
                    print("{}".format(scan_output))
                    # write the output to a file
                    current.write(scan_output)
            scan_output=""
