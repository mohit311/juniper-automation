import paramiko
import time
import sys
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError

class AllowAllKeys(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

############################        Terminal Server credentials      #############################################################

hostname = 'xx.xx.xx.xx'
#username = raw_input("Terminal Server username: ")
#password = raw_input("Terminal Server password: ")
username = 'XXXX'
password = 'XXXXX'

port = 22

try:

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AllowAllKeys())

    client.connect(hostname, port=port, username=username, password=password)
    #print "Connected to %s" % hostname

############################        Opening the shell and sending individual set commands     ######################################

    channel = client.invoke_shell()
    channel.send('1\n')
    #channel.send('\n')
    #channel.send('\n')
    channel.send('root\n')
    channel.send('\n')
    channel.send('cli\n')
    channel.send('edit\n')
    channel.send('set groups re0 system host-name re0.ZTP_1.mx104\n')
    channel.send('set groups re0 interfaces fxp0 description "10/100 Management Interface"\n')
    channel.send('set groups re0 interfaces fxp0 unit 0 family inet address 192.168.124.37/25\n')
    channel.send('set groups re0 interfaces fxp0 unit 0 family inet address 192.168.124.39/25 master-only\n')

    channel.send('set groups re1 system host-name re1.ZTP_1.mx104\n')
    channel.send('set groups re1 interfaces fxp0 description "10/100 Management Interface"\n')
    channel.send('set groups re1 interfaces fxp0 unit 0 family inet address 192.168.124.38/25\n')
    channel.send('set groups re1 interfaces fxp0 unit 0 family inet address 192.168.124.39/25 master-only\n')

    channel.send('set apply-groups re0\n')
    channel.send('set apply-groups re1\n')

    channel.send('set system ports console type vt100\n')
    channel.send('set system root-authentication encrypted-password "$6$bRoFt3nI$xVEJ6Q9.yWr/2gSNI1VO37byIJB4W2wHWE.6rRY/J36g5InIlakIcLRPlOcuKCc67oZvuuqSTKgB5SxK92JKd/"\n')

    channel.send('set system services ftp connection-limit 1\n')
    channel.send('set system services telnet connection-limit 1\n')

    channel.send('set system login class su-class idle-timeout 15\n')
    channel.send('set system login class su-class permissions all\n')
    channel.send('set system login user write full-name "Read/write fallback access user"\n')
    channel.send('set system login user write uid 100\n')
    channel.send('set system login user write class su-class\n')
    channel.send('set system login user write authentication encrypted-password "$1$iZQNJgB1$G3HrM/.ZMpg54qle6uSGq/"\n')

    channel.send('set routing-options static route 0.0.0.0/0 next-hop 192.168.124.1\n')
    channel.send('set routing-options static route 0.0.0.0/0 retain\n')
    channel.send('set routing-options static route 0.0.0.0/0 no-readvertise\n')
    channel.send('set routing-options static route 0.0.0.0/0 preference 240\n')

    channel.send('commit synchronize and-quit\n')

    while not channel.recv_ready():
      time.sleep(3)
    out = channel.recv(9999)
    #print out

    for i in xrange(75, 0, -1):
        time.sleep(1)
        #sys.stdout.write(str(i) + ' ')
        #sys.stdout.flush()

    ##################         Getting Juniper device credentials   ######################################


    dev_ip_address = '192.168.124.39'
    dev_username = 'xxxx'
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

    command1 = dev.cli('show configuration groups', warning=False)
    check1 = command1.find('fxp0')

    command2 = dev.cli('show configuration system root-authentication', warning=False)
    check2 = command2.find('encrypted-password')

    command3 = dev.cli('show configuration system services', warning=False)
    check3 = command3.find('telnet')

    command4 = dev.cli('show configuration system login', warning=False)
    check4 = command4.find('write')

    command5 = dev.cli('show configuration routing-options static', warning=False)
    check5 = command5.find('preference')

    if check1 >= 0 & check2 >= 0 & check3 >= 0 & check4 >= 0 & check5 >= 0:
        print "Configuration Successful"
    else:
        print "Configuration Unsuccessful - Abort"
        sys.exit(1)

except:
    print ("Failure")
    sys.exit(1)


finally:
    client.close()

