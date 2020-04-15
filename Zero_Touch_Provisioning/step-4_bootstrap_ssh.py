from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import sys
import time
from jnpr.junos.utils.config import Config

##################        Opening the device     ######################################

dev_ip_address = '192.168.124.39'
dev_username = 'xxxxx'
dev_password = 'xxxxx'

dev = Device(host=dev_ip_address, user=dev_username, passwd=dev_password, mode='telnet', port='23')

try:
    dev.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1)

with Config(dev, mode='private') as cu:
    cu.load(url="ftp://<username:pwd>@192.168.127.238/bootstrap_ssh.conf", overwrite=True)
    #cu.pdiff()
    cu.commit()

for i in xrange(40, 0, -1):
    time.sleep(1)

dev_ssh = Device(host=dev_ip_address, user=dev_username, passwd=dev_password, port='22')

try:
    dev_ssh.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1)

command1 = dev_ssh.cli('show configuration groups', warning=False)
check1 = command1.find('fxp0')

command2 = dev_ssh.cli('show configuration system root-authentication', warning=False)
check2 = command2.find('encrypted-password')

command3 = dev_ssh.cli('show configuration system services', warning=False)
check3 = command3.find('ssh')

command4 = dev.cli('show configuration system login', warning=False)
check4 = command4.find('write')

command5 = dev.cli('show configuration routing-options static', warning=False)
check5 = command5.find('preference')

if check1 >= 0 & check2 >= 0 & check3 >= 0 & check4 >= 0 & check5 >= 0:
    print "Bootstrap with SSH Configuration is Successful"
else:
    print "Bootstrap with SSH Configuration is Unsuccessful - Abort"
    sys.exit(1)

dev_ssh.close()
