
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def Send_Email(productTitle, sender_email, receiver_email, password):
    print("Send_Email")
    #if request.method == 'POST':
        #print("Nothing ....")

    #sender_email = "ashokElectronicsWeb@gmail.com"
    #receiver_email = "pradeepkumawat91@gmail.com"
    #password = "akgmail@@1993@"
    subject = "Product Purchased"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """\
    <html>
    <body>
        <p>Hi User,<br>
        Purchased Item is:<br>
        <a href="http://127.0.0.1:8000/product/""" + productTitle + """">""" + productTitle + """</a>
        </p>
    </body>
    </html>
    """
    # Turn these into plain/html MIMEText objects
    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    #message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    #return render(request, "product/adminPage.html", {})
    return "MSG SENT"


#def error_404(request):
#        return render(request, '404.html')

def setSession(request, key, value):
    request.session[key] = value

def getSession(request, key):
    return request.session[key]
