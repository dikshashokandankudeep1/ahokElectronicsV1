
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


def sendEmail(sender_email, receiver_email, password, subject, messageContent):
    print("Send_Email started")

    '''
    subject = "Product Purchased"
    messageContent = '<p>Hi User,<br> \
                    Purchased Item is:<br> \
                    <a href="http://127.0.0.1:8000/product/""" + productTitle + """">""" + productTitle + """</a> \
                    </p>'
    '''

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
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return "MSG SENT"

class myThreadPool:
 
    # state shared by each instance
    __shared_state = dict()
 
    # constructor method
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.isthreadPoolActive = 0
        self.executor = ""
 
    def __str__(self):
        return self.state

    def threadPoolInit(self):
        if self.isthreadPoolActive == 0:
            max_workers = 1
            self.executor = ThreadPoolExecutor(max_workers)
            self.isthreadPoolActive = 1
        else:
            print("threadPoolInit::ERROR")

    def addTaskToThreadPool(self, taskType, taskDataDict):
        self.threadPoolInit()
        if taskType == "sentEmail":
            self.executor.submit(sendEmail, taskDataDict["senderEmail"], taskDataDict["emailaddress"], 
                        taskDataDict["password"], taskDataDict["subject"], taskDataDict["messageContent"])
        else:
            print("addTaskToThreadPool::ERROR")

def setSession(request, key, value):
    request.session[key] = value

def getSession(request, key):
    if request.session.__contains__(key):
        print("getSession key contains....",key, request.session[key])
        return request.session[key]
    else:
        print("getSession key not contains....")
        return ""

def toCamelCase(stringData):
    if stringData:
        vect = stringData.split(" ")
        outputString = ""
        for vec in vect:
            outputString += vec[0].upper() + vec[1:].lower() + " "
        return outputString.strip()
    else:
        return ""
def toCommaSeperatedCurrency(number):
    commaSeparatedCurrency = "{:,}".format(number)
    if '.' not in commaSeparatedCurrency:
        commaSeparatedCurrency += ".00"
    return commaSeparatedCurrency