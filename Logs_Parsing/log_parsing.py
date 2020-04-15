from jnpr.junos.exception import ConnectTimeoutError
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectClosedError
from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos import Device
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import subprocess
import csv
import datetime
import smtplib
import os.path

dev_username = 'xxxxx'
dev_password = 'xxxxx'

f = open('results_logs.rtf', 'w+')

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
                except ConnectTimeoutError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                except ConnectClosedError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                except ConnectError as err:
                    print("Cannot connect to device: {0}".format(err))
                    pass
                f = open('results_logs.rtf', 'a+')
                f.write(row["ip_address"] + ' ' + dev.facts['hostname'])
                f.write('\n')
                with StartShell(dev, timeout=45) as ss:
                    if ss.run('cli', '>')[0]:
                        x = ss.run('show log messages|last 200|except "bgp|snmp|cmlc|icmp|ping|last|sshd|auto|turned|jam|craftd|auditd|ffp|handler|profile|mib2d"|no-more')
                        data1 = x[1].replace('\x08', '')
                        y = ss.run('show log messages.0.gz|last 200|except "bgp|snmp|cmlc|icmp|ping|last|sshd|auto|turned|jam|craftd|auditd|ffp|handler|profile|mib2d"|no-more')
                        data2 = y[1].replace('\x08', '')
                        if 'fpc' in data1 or 'pic' in data1 or 'interface' in data1 or 'fail' in data1 or 'power' in data1 or 'error' in data1 or 'voltage' in data1 or 'critical' in data1:
                            f.write(data1)
                            f.write('\n\n')
                            f.write(data2)
                            f.write('\n\n')
                        elif 'fpc' in data2 or 'pic' in data2 or 'interface' in data2 or 'fail' in data2 or 'power' in data2 or 'error' in data2 or 'voltage' in data2 or 'critical' in data2:
                            f.write(data2)
                            f.write('\n\n')
                        else:
                            f.write("Nothing to worry here")
                f.write('\n\n')
                dev.close()
        else:
            print('Cannot connect to {}'.format((row["ip_address"])))
            pass
f.close()
dev.close()

email = 'do-not-reply@xxxx.com'
send_to_emails = ['xx.xxx@xx.com']

subject = "<<<subject-line>>> -- " + str(datetime.date.today())
message = 'Please find Attached Router Logs Scrap \n\n\n\n Regards \n Mohit Mittal'
file_location = 'results_logs.rtf'

# Setup the attachment
filename = os.path.basename(file_location)
attachment = open(file_location, "r+")
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
