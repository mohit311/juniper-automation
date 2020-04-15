import sys, time
from jnpr.junos import Device
from jnpr.junos.utils.sw import SW
from jnpr.junos.exception import ConnectError

dev_ip_address = '192.168.124.39'
dev_username = 'xxxx'
dev_password = 'xxxx'
package = '/var/tmp/jinstall-ppc-17.1R2.7-signed.tgz'
validate = False

dev = Device(host=dev_ip_address, user=dev_username, passwd=dev_password, mode='telnet', port='23')

try:
    dev.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)
except Exception as err:
    print (err)
    sys.exit(1)

sw = SW(dev)

try:
    ok = sw.install(no_copy=True, package=package, validate=validate)
except Exception as err:
    print ('Unable to install software')
    ok = False

if ok is True:
    sw.reboot()
else:
    print ('Unable to install software')

for i in xrange(1020, 0, -1):
    time.sleep(1)


dev.open()

re0_version = dev.cli('show version', warning=False)

re1_version = dev.cli('show version invoke-on other-routing-engine', warning=False)

for i in xrange(5, 0, -1):
    time.sleep(1)

re0_version_check = re0_version.find('17.1R2.7')

re1_version_check = re1_version.find('17.1R2.7')

if re0_version_check >= 0 and re1_version_check >= 0:
    print "JunOS Upgrade is successful to 17.1R2.7"
else:
    print "JunOS Upgrade is NOT successful - Abort"
    sys.exit(1)


dev.close()
