from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import sys
import time
from jnpr.junos.utils.config import Config

##################        Opening the device     ######################################

dev_ip_address = '192.168.124.39'
dev_username = 'xxxxx'
dev_password = 'xxxxx'

dev_ssh = Device(host=dev_ip_address, user=dev_username, passwd=dev_password, port='22')


try:
    dev_ssh.open()
    dev_ssh.timeout = 300
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1)

with Config(dev_ssh, mode='private') as cu:
    cu.load(url="mx104_baseconfig.conf", overwrite=True)
    #cu.pdiff()
    cu.commit()

for i in xrange(40, 0, -1):
    time.sleep(1)

command1 = dev_ssh.cli('show configuration groups', warning=False)
check1 = command1.find('fxp0')

command2 = dev_ssh.cli('show configuration system login', warning=False)
check2 = command2.find('dmas-su')

command3 = dev_ssh.cli('show configuration system services', warning=False)
check3 = command3.find('netconf')

command4 = dev_ssh.cli('show configuration chassis', warning=False)
check4 = command4.find('graceful-switchover')

command5 = dev_ssh.cli('show configuration class-of-service forwarding-classes', warning=False)
check5 = command5.find('Network-Control')

if check1 >= 0 & check2 >= 0 & check3 >= 0 & check4 >= 0 & check5 >= 0:
    print "Base configuration is applied Successfully"
else:
    print "Base configuration is NOT Applied - Abort"
    sys.exit(1)

dev_ssh.close()

