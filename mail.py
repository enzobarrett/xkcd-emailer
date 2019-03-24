from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import random
import os
import re

# Pick random file
random = random.choice(os.listdir("xkcd"))
print(random)

# Find comic number for explain link
reElem = re.findall('\d+?\d*', random)
number = reElem[len(reElem)-1]
print(number)

# Who to?
From = 'enzobarrett@gmail.com'
To = ['enzobarrett@gmail.com']

# Setup message
msg = MIMEMultipart('related')
msg['Subject'] = 'Daily XKCD'
msg['From'] = From
msg['To'] = ', '.join(To)

# Alternate message
msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

# Alternate message text
msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# Give html with image and explain link
msgText = MIMEText('<img src="cid:image1"><br><h3><a href="explainxkcd.com/' + number + '">Explain XKCD</a></h3>', 'html')
msgAlternative.attach(msgText)

# Open image
fp = open(os.path.join('xkcd', random), 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Add proper header and name, attach image
msgImage.add_header('Content-ID', '<image1>')
msgImage.add_header('Content-Disposition', 'inline', filename=random)
print('Attaching image...')
msg.attach(msgImage)

# Login
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()

# Get pass
with open('pass.txt', 'r') as myfile:
    password=myfile.read().replace('\n', '')

# Login and send
smtp.login('enzobarrett@gmail.com', password)
smtp.sendmail(From, To, msg.as_string())
smtp.quit()

