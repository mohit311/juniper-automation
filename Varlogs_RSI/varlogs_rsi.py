from jnpr.junos.exception import ConnectError
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
import sys
import os
import datetime
import time
#import logging
import pysftp


folder_name = '<folder-name>'  # Add Folder Name Here, preferably in JTAC Case format i.e 2020-0116-0389
router_ip = '<router-ip>'    # Add IP address of Router

dev_username = '<dev_username>'
dev_password = '<dev_pwd>'
myHostname = '<sftp-server-ip>'
myUsername = '<sftp-user-name>'
myPassword = '<sftp-pwd>'

x = datetime.datetime.now()
current_date = str(x.strftime("%d") + '-' + x.strftime("%m") + '-' + x.strftime("%y"))

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

if not os.path.exists("<path_on_windows>" + folder_name):
    os.makedirs("<path_on_windows>" + folder_name)

with Device(host=router_ip, user=dev_username, passwd=dev_password, port='830') as dev:
    try:
        dev.open()
        dev.timeout = 300
    except ConnectError as err:
        print("Cannot connect to device: {0}".format(err))
        sys.exit(1)
    except Exception as err:
        print(err)
        sys.exit(1)
    hostname = dev.facts['hostname']
    print(hostname)
    if (dev.facts['RE0'] == None or dev.facts['RE0']['mastership_state'] == 'Present') and (dev.facts['RE1']['mastership_state']) == 'master':
        print ("Only RE1 is Available on this Router")
        with StartShell(dev, timeout=100) as ss:
            if ss.run('cli', '>')[0]:
                ss.run('request support information | save RSI_' + hostname + '_' + current_date + '.txt', '>')
                ss.run('file archive compress source /var/log/* destination re1_var_logs' + '_' + hostname + '_' + current_date + '.tgz', '>')
                if ss.run('sftp '<sftp-server-username>@<sftp-server-ip>', 'password:')[0] or ss.run('sftp <sftp-server-username>@<sftp-server-ip>', '(yes/no)?')[0]:
                    data0 = ss.run('yes', 'password:')
                    print(data0)
                    data3= ss.run('<sftp-server-pwd>', '>')
                    print(data3)
                    data4 = ss.run('cd <sftp-server-folder>', '>')
                    print(data4)
                    data5 = ss.run('put RSI_' + hostname + '_' + current_date + '.txt', '>')
                    print(data5)
                    data6 = ss.run('put re1_var_logs_' + hostname + '_' + current_date + '.tgz', '>')
                    print(data6)
            ss.close()
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
            print("Connection succesfully established ... ")
            # Define the file that you want to download from the remote directory
            remoteFilePath1 = "/<sftp-server-folder>/" + 'RSI_' + hostname + '_' + current_date + '.txt'
            remoteFilePath2 = "/<sftp-server-folder>/" + 're1_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            # Define the local path where the file will be saved
            localFilePath1 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 'RSI_' + hostname + '_' + current_date + '.txt'
            localFilePath2 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 're1_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            sftp.get(remoteFilePath1, localFilePath1)
            sftp.get(remoteFilePath2, localFilePath2)
    elif (dev.facts['RE1'] == None or dev.facts['RE1']['mastership_state'] == 'Present') and (dev.facts['RE0']['mastership_state']) == 'master':
        print ("Only RE0 is Available on Router")
        with StartShell(dev, timeout=100) as ss:
            if ss.run('cli', '>')[0]:
                ss.run('request support information | save RSI_' + hostname + '_' + current_date + '.txt', '>')
                ss.run('file archive compress source /var/log/* destination re0_var_logs' + '_' + hostname + '_' + current_date + '.tgz', '>')
                if ss.run('sftp '<sftp-server-username>@<sftp-server-ip>', 'password:')[0] or ss.run('sftp <sftp-server-username>@<sftp-server-ip>', '(yes/no)?')[0]:
                    data0 = ss.run('yes', 'password:')
                    print(data0)
                    data3= ss.run('<sftp-server-pwd>', '>')
                    print(data3)
                    data4 = ss.run('cd <sftp-server-folder>', '>')
                    print(data4)
                    data5 = ss.run('put RSI_' + hostname + '_' + current_date + '.txt', '>')
                    print(data5)
                    data6 = ss.run('put re0_var_logs_' + hostname + '_' + current_date + '.tgz', '>')
                    print(data6)
        ss.close()
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
            print("Connection succesfully established ... ")
            # Define the file that you want to download from the remote directory
            remoteFilePath1 = "/<sftp-server-folder>/" + 'RSI_' + hostname + '_' + current_date + '.txt'
            remoteFilePath2 = "/<sftp-server-folder>/" + 're0_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            # Define the local path where the file will be saved
            # or absolute "C:\Users\sdkca\Desktop\TUTORIAL.txt"
            localFilePath1 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 'RSI_' + hostname + '_' + current_date + '.txt'
            localFilePath2 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 're0_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            sftp.get(remoteFilePath1, localFilePath1)
            sftp.get(remoteFilePath2, localFilePath2)
    elif (dev.facts['RE0']['mastership_state']) == 'master' and (dev.facts['RE1']['mastership_state']) == 'backup':
        print("RE0 is Master and RE1 is Backup RE")
        with StartShell(dev, timeout=100) as ss:
            if ss.run('cli', '>')[0]:
                print(ss.run('request support information | save RSI_' + hostname + '_' + current_date + '.txt', '>'))
                print(ss.run('file archive compress source /var/log/* destination re0_var_logs' + '_' + hostname + '_' + current_date + '.tgz', '>'))
                if ss.run("request routing-engine login other-routing-engine", '>')[0]:
                    # if ss.run('cli', '>'):  # if last command request session me… goes to cli, this line is not required
                    data1 = ss.run('file archive compress source /var/log/* destination re1_var_logs' + '_' + hostname + '_' + current_date + '.tgz', '>')
                    print(data1)
                    data2 = ss.run('file copy re1_var_logs' + '_' + hostname + '_' + current_date + '.tgz' + ' ' + 're0:', '>')
                    print(data2)
                    data4 = ss.run('exit', '>')
                    print(data4)
                    if ss.run('sftp <sftp-server-username>@<sftp-server-ip>', 'password:')[0] or ss.run('sftp <sftp-server-username>@<sftp-server-ip>', '(yes/no)?')[0]:
                        data0 = ss.run('yes', 'password:')
                        print(data0)
                        data5 = ss.run('<sftp-server-pwd>', '>')
                        print(data5)
                        data6 = ss.run('cd <sftp-server-folder>', '>')
                        print(data6)
                        data7 = ss.run('put RSI_' + hostname + '_' + current_date + '.txt', '>')
                        print(data7)
                        data8 = ss.run('put re1_var_logs_' + hostname + '_' + current_date + '.tgz', '>')
                        print(data8)
                        data9 = ss.run('put re0_var_logs_' + hostname + '_' + current_date + '.tgz', '>')
                        print(data9)
            ss.close()
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
            print("Connection succesfully established ... ")
            # Define the file that you want to download from the remote directory
            remoteFilePath1 = "/<sftp-server-folder>/" + 'RSI_' + hostname + '_' + current_date + '.txt'
            remoteFilePath2 = "/<sftp-server-folder>/" + 're0_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            remoteFilePath3 = "/<sftp-server-folder>/" + 're1_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            # Define the local path where the file will be saved
            localFilePath1 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 'RSI_' + hostname + '_' + current_date + '.txt'
            localFilePath2 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 're0_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            localFilePath3 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 're1_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            sftp.get(remoteFilePath1, localFilePath1)
            sftp.get(remoteFilePath2, localFilePath2)
            sftp.get(remoteFilePath3, localFilePath3)
        ss.close()
    elif (dev.facts['RE0']['mastership_state']) == 'backup' and (dev.facts['RE1']['mastership_state']) == 'master':
        print("RE1 is Master and RE0 is Backup RE")
        with StartShell(dev, timeout=100) as ss:
            if ss.run('cli', '>')[0]:
                print(ss.run('request support information | save RSI_' + hostname + '_' + current_date + '.txt', '>'))
                print(ss.run('file archive compress source /var/log/* destination re1_var_logs' + '_' + hostname + '_' + current_date + '.tgz', '>'))
                if ss.run("request routing-engine login other-routing-engine", '>')[0]:
                    # if ss.run('cli', '>'):  # if last command request session me… goes to cli, this line is not required
                    data1 = ss.run('file archive compress source /var/log/* destination re0_var_logs' + '_' + hostname + '_' + current_date + '.tgz', '>')
                    print(data1)
                    data2 = ss.run('file copy re0_var_logs' + '_' + hostname + '_' + current_date + '.tgz' + ' ' + 're1:', '>')
                    print(data2)
                    data4 = ss.run('exit', '>')
                    print(data4)
                    if ss.run('sftp <sftp-server-username>@<sftp-server-ip>', 'password:')[0] or ss.run('sftp <sftp-server-username>@<sftp-server-ip>', '(yes/no)?')[0]:
                        data0 = ss.run('yes', 'password:')
                        print(data0)
                        data5 = ss.run('<sftp-server-pwd>', '>')
                        print(data5)
                        data6 = ss.run('cd <sftp-server-folder>', '>')
                        print(data6)
                        data7 = ss.run('put RSI_' + hostname + '_' + current_date + '.txt', '>')
                        print(data7)
                        data8 = ss.run('put re1_var_logs_' + hostname + '_' + current_date + '.tgz', '>')
                        print(data8)
                        data9 = ss.run('put re0_var_logs_' + hostname + '_' + current_date + '.tgz', '>')
                        print(data9)
            ss.close()
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
            print("Connection succesfully established ... ")
            # Define the file that you want to download from the remote directory
            remoteFilePath1 = "/<sftp-server-folder>/" + 'RSI_' + hostname + '_' + current_date + '.txt'
            remoteFilePath2 = "/<sftp-server-folder>/" + 're0_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            remoteFilePath3 = "/<sftp-server-folder>/" + 're1_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            # Define the local path where the file will be saved
            localFilePath1 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 'RSI_' + hostname + '_' + current_date + '.txt'
            localFilePath2 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 're0_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            localFilePath3 = 'C' + ':' + '\\' + 'Users' + '\\' + 'mmittal' + '\\' + 'Downloads' + '\\' + folder_name + '\\' + 're1_var_logs' + '_' + hostname + '_' + current_date + '.tgz'
            sftp.get(remoteFilePath1, localFilePath1)
            sftp.get(remoteFilePath2, localFilePath2)
            sftp.get(remoteFilePath3, localFilePath3)
        ss.close()
    dev.close()
