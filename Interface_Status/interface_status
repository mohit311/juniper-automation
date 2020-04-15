from jnpr.junos.exception import ConnectTimeoutError
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectClosedError
from jnpr.junos.exception import ConnectAuthError
from jnpr.junos import Device
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import subprocess
import datetime
import csv
import smtplib
import os.path


dev_username = 'xxxxxxx'
dev_password = 'xxxxxxx'

f = open('Interfaces_Status-' + str(datetime.date.today()) + '.txt', 'w+')

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
                interface_details = str(dev.cli('show interface descriptions', warning=False))

                f = open('Interfaces_Status-' + str(datetime.date.today()) + '.txt', 'a+')
                if 'down' in interface_details:
                    f.write(row["ip_address"] + ' ' + dev.facts['hostname'])
                    f.write('\n')
                    f.write(interface_details)
                    f.write('\n')
                    f.write('**************************************************************************')
                    f.write('\n')
                    f.close()
            dev.close()
        else:
            print('Cannot connect to {}'.format((row["ip_address"])))
            pass
email = 'do-not-reply@xxxxx.com'
send_to_emails = ['xxxxx@xx.com']

subject = "<Subject Line --> " + str(datetime.date.today())
message = 'Please find Attached Router Interfaces Status which looks to be down \n\n\n\n Regards \n Mohit Mittal'
file_location = 'Interfaces_Status-' + str(datetime.date.today()) + '.txt'

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
