import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import webCredentialsTable

class emailWrapper:

    def credentialsOperation(self, taskDataDict):
        websiteUrl = ""
        for obj in webCredentialsTable.objects.filter(credentialType="sentEmail"):
            websiteUrl = obj.websiteUrl
            
        subject = "User credentials"
        messageContent = "<p><b><span style='color:green'> Congratulations!</b> now you are member of "+  websiteUrl +" </b></p>"
        messageContent += "<p> Below are your login credentials </p>"
        messageContent += "<p> Username : "+ taskDataDict["username"] +" </p>"
        messageContent += "<p> Password : "+ taskDataDict["userPassword"] +" </p>"
        self.sendEmail(taskDataDict["useremail"], subject, messageContent)

    def sendEmail(self, receiver_email, subject, messageContent):
        sender_email = ""
        sender_password = ""
        for obj in webCredentialsTable.objects.filter(credentialType="sentEmail"):
            sender_email = obj.senderEmail
            sender_password = obj.password

        #print("sender_email::", sender_email, sender_password)
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        html = """\
        <html>
        <body>""" + \
            messageContent + \
        """</body>
        </html>
        """
        part2 = MIMEText(html, "html")

        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        return "MSG SENT"