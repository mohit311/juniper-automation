from jnpr.junos.exception import ConnectTimeoutError
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectClosedError
from jnpr.junos.exception import ConnectAuthError
from jnpr.junos import Device
import subprocess
import datetime
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

dev_username = 'xxxxx'
dev_password = 'xxxxxx'

f = open('results-' + str(datetime.date.today()) + '.txt', 'w+')

with open('device_list.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        p1 = subprocess.Popen(["ping", "-n", "1", row["ip_address"]], stdout=subprocess.PIPE)
        p1.wait()
        result = p1.poll()
        if result == 0:
            with Device(host=row["ip_address"], user=dev_username, passwd=dev_password, port='830') as dev:
                try:
                    dev.open()
                    dev.timeout = 45
                except ConnectTimeoutError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                except ConnectClosedError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                except ConnectError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                except ConnectAuthError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                fpc_details = dev.rpc.get_fpc_information({'format': 'json'})
                fpc_status = str(fpc_details["fpc-information"][0]['fpc'])

                chassis_alarms = dev.rpc.get_alarm_information({'format': 'json'})
                chassis_alarms_status = str(chassis_alarms["alarm-information"][0])

                system_alarms = dev.rpc.get_system_alarm_information({'format': 'json'})
                system_alarms_status = str(system_alarms["alarm-information"][0])

                f = open('results-' + str(datetime.date.today()) + '.txt', 'a+')
                if 'Bad Voltage' in fpc_status or 'Offline' in fpc_status or 'Unresponsive' in fpc_status or 'Present' in fpc_status:
                    f.write(row["ip_address"] + ' ' + dev.facts['hostname'])
                    f.write('\n')
                    fpc_output = str(dev.cli("show chassis fpc", warning=False))
                    f.write(fpc_output)
                    f.write('\n')
                    chassis_alarm_output = str(dev.cli("show chassis alarms", warning=False))
                    f.write(chassis_alarm_output)
                    f.write('******************************************************')
                    f.write('\n')
                elif ('active-alarm-count') in chassis_alarms_status:
                    f.write(row["ip_address"] + ' ' +  dev.facts['hostname'])
                    f.write('\n')
                    chassis_alarm_output = str(dev.cli("show chassis alarms", warning=False))
                    f.write(chassis_alarm_output)
                    f.write('******************************************************')
                    f.write('\n')
                elif ('active-alarm-count') in system_alarms_status:
                    f.write(row["ip_address"] + ' ' +  dev.facts['hostname'])
                    f.write('\n')
                    system_alarm_output = str(dev.cli("show system alarms", warning=False))
                    f.write(system_alarm_output)
                    f.write('******************************************************')
                    f.write('\n')
            dev.close()
        else:
            print('Cannot connect to {}'.format((row["ip_address"])))
            pass
email = 'do-not-reply@xxxx.com'
send_to_emails = ['xxxx.xxxx@xx.com', 'xxx2xxx@xxxx.net']

subject = "<Subject - Line> -- " + str(datetime.date.today())
message = 'Please find Attached Router Chassis Alarms and FPCs Status \n\n\n\n Regards \n Mohit Mittal'
file_location = 'results-' + str(datetime.date.today()) + '.txt'

# Setup the attachment
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# Attach the attachment to the MIMEMultipart object
server = smtplib.SMTP('<server-ip>')
for send_to_email in send_to_emails:
    # Setup MIMEMultipart for each email address (if we don't do this, the emails will concat on each email sent)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))
    # Attach the attachment file
    msg.attach(part)

    # Send the email to this specific email address
    server.sendmail(email, send_to_email, msg.as_string())
    print("Mail Sent Successfully")

f.close()
dev.close()
