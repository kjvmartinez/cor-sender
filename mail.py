import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import csv
import time

sender_email = "youremail@gmail.com"
# receiver_email = "receiver_mail@gmail.com"
password = 'yourpassword'

message = MIMEMultipart("alternative")
message["Subject"] = "Certificate of Registration"
message["From"] = sender_email

context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
server.ehlo()
server.login(sender_email, password)

with open('mail.html', 'r', encoding="utf8") as file:
    data = file.read().replace('\n', '')
count = 0

with open("mail_list.csv") as file:
    reader = csv.reader(file)
    next(reader)
    for name, email, cor in reader:
        # Create the plain-text and HTML version of your message
        html = data.format(name=name, link='http://www.google.com')

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(MIMEText(html, "html"))

        with open(cor, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(cor)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(cor)
        message.attach(part)        

        server.sendmail(
            sender_email, email, message.as_string()
        )


        count += 1
        print(str(count) + ". Sent to " + email)

        if(count%80 == 0):
            server.quit()
            print("Server cooldown for 100 seconds")
            time.sleep(100)
            server.ehlo()
            server.login(sender_email, password)

server.quit()