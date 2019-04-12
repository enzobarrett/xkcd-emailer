from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import mysql.connector as mariadb
import smtplib
import random
import os
import re

# Pick random file
random = random.choice(os.listdir("xkcd"))

# Find comic number for explain link
reElem = re.findall('\d+?\d*', random)
number = reElem[len(reElem)-1]

# From
From = 'enzobarrett@gmail.com'

# Setup message
msg = MIMEMultipart('related')
msg['Subject'] = 'Daily XKCD'
msg['From'] = From

# Alternate message
msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

# Alternate message text
msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# Give html with image and explain link and unsub with format string
msgText = MIMEText('<img src="cid:image1"><br><h3><a href="explainxkcd.com/' + number + '">Explain XKCD</a></h3><a href="xkcd.enzob.xyz/{key}">unsubscribe</a>', 'html')
msgAlternative.attach(msgText)

# Open image
fp = open(os.path.join('xkcd', random), 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Add proper header and name, attach image
msgImage.add_header('Content-ID', '<image1>')
msgImage.add_header('Content-Disposition', 'inline', filename=random)
msg.attach(msgImage)

# Start connection
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()

# Get pass
with open('pass.txt', 'r') as myfile:
    password=myfile.read().replace('\n', '')

# Fetch all people to email to
mariadb_connection = mariadb.connect(user='dailyxkcd', password='nA-C/]eB1}', database='dailyxkcd')
cursor = mariadb_connection.cursor()
cursor.execute("SELECT * from emails")
result = cursor.fetchall()

# Login
smtp.login('enzobarrett@gmail.com', password)

# Loop trough emails and send with key in unsub link
for to, key in result:
    print('sending to : ', to)
    msg['To'] = to
    smtp.sendmail(From, to, msg.as_string().format(key=key))

smtp.quit()
