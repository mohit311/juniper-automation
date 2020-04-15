#!/usr/bin/env python

import paramiko
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import sys
import time

class AllowAllKeys(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

############################        Terminal Server credentials      ######################################

hostname = 'xx.xx.xx.xx'
#username = raw_input("Terminal Server username: ")
#password = raw_input("Terminal Server password: ")

username = 'xxxxx'
password = 'xxxx'

port = 22

try:

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AllowAllKeys())

    client.connect(hostname, port=port, username=username, password=password)
    #print "Connected to %s" % hostname

    ##################        Opening the shell and sending individual set commands     ######################################

    channel = client.invoke_shell()

    channel.send('1\n')
    channel.send('\n')
    channel.send('file copy ftp://<username:pwd>@192.168.127.238/jinstall-ppc-17.1R2.7-signed.tgz /var/tmp/')
    channel.send('\n')

    dev_ip_address = '192.168.124.39'
    dev_username = 'xxxx'
    dev_password = 'xxxx'

    dev = Device(host=dev_ip_address, user=dev_username, passwd=dev_password, mode='telnet', port='23')

    try:
        dev.open()
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        sys.exit(1)
    except Exception as err:
        print (err)
        sys.exit(1)

    for i in xrange(80, 0, -1):
        time.sleep(1)

    file_check = dev.cli('file checksum md5 /var/tmp/jinstall-ppc-17.1R2.7-signed.tgz', warning=False)
    #print file_check
    md5_check = file_check.find('85faa16a131a54eaad9cc61ec14c65f4')


    file_copy_other_re = dev.rpc.file_copy(source="/var/tmp/jinstall-ppc-17.1R2.7-signed.tgz", destination="re1:/var/tmp/")
    #print file_copy_other_re

    for i in xrange(30, 0, -1):
        time.sleep(1)

    file_check_other_re = dev.cli('file checksum md5 re1:/var/tmp/jinstall-ppc-17.1R2.7-signed.tgz', warning=False)
    #print file_check_other_re
    md5_check_other_re = file_check_other_re.find('85faa16a131a54eaad9cc61ec14c65f4')


    if md5_check >= 0 & md5_check_other_re >= 0:
        print "File Transfer Successful on both REs"
    else:
        print "File Transfer UN-Successful - Abort"
        sys.exit(1)

    dev.close()

finally:
    client.close()
