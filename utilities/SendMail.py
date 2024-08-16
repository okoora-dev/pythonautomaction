from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email():

    msg = MIMEMultipart()
    server = smtplib.SMTP('okoora-com.mail.protection.outlook.com', 25)
    server.starttls()
    path_to_pdf = "C:/Users/DanielHasid/PycharmProjects/Automation/utilities/report.pdf"
    message = "Regression result"
    msg['Subject'] = "Regression report"
    msg['From'] = 'qa@okoora.com'
    recipients = ["danielh@okoora.com","racheli.list@ofakim-group.com","sanazt@okoora.com","daniel.shalamov@okoora.com"]
    msg['To'] = ", ".join(recipients)
    # Insert the text to the msg going by e-mail
    html = open("C:/Users/DanielHasid/PycharmProjects/Automation/Tests/report.html")
    msg = MIMEText(html.read(), 'html')
    msg.attach(MIMEText(message, "plain"))
    text = msg.as_string()
    # Attach the pdf to the msg going by e-mail
    #
    # with open(path_to_pdf, "rb") as f:
    #     attach = MIMEApplication(f.read(), _subtype="pdf")
    # attach.add_header('Content-Disposition', 'attachment', filename=str(path_to_pdf))
    # msg.attach(attach)
    # send msg
    server.send_message(msg)

send_email()


