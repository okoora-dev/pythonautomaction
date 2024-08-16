import mimetypes
import os
import smtplib
import time
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utilities.email_pytest_report import Email_Pytest_Report


def pytest_terminal_summary(terminalreporter, exitstatus):
    report_file_path = 'C:/Users/Administrator/Automation/Tests/report.html'
    "add additional section in terminal summary reporting."
    if not hasattr(terminalreporter.config, 'workerinput'):
        if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
            send_test_report_email()

            #Initialize the Email_Pytest_Report object
            # email_obj = Email_Pytest_Report()
            # # Send html formatted email body message with pytest report as an attachment
            # email_obj.send_test_report_email(html_body_flag=True,attachment_flag=True,report_file_path= report_file_path)
def send_test_report_email():

    sender = "qa@okoora.com"
    targets = ["danielh@okoora.com", "racheli.list@okoora.com", "sanazt@okoora.com", "daniel.shalamov@okoora.com",
                    "yuval@okoora.com", "dork@okoora.com"]
    report_file_path = 'C:/Users/Administrator/Automation/Tests/report.html'
    "send test report email"

    # 3. Add html formatted email body message along with an attachment file
    message = MIMEMultipart()
    # add html formatted body message to email
    html_body = MIMEText(
        '''Hello,Please check the attachment to see test built report.<strong>Note: For best UI experience, download the attachment and open using Chrome browser.</strong>''',
        "html")  # Add/Update email body message here as per your requirement
    message.attach(html_body)
    # add attachment to email
    attachment = get_attachment(report_file_path)
    message.attach(attachment)
    message['From'] = sender
    message['To'] = ', '.join(targets)
    message['Subject'] = 'Script generated test report'  # Update email subject here
    time.sleep(5)
    server = smtplib.SMTP('okoora-com.mail.protection.outlook.com', 25)
    server.sendmail(sender, targets, message.as_string())
    server.quit()

    # Send Email

    # 4. Add text formatted email body message along with an attachment file



def get_attachment(attachment_file_path):
    "Get attachment and attach it to mail"
    attachment_report_file = attachment_file_path
    # check file exist or not
    if not os.path.exists(attachment_report_file):
        raise Exception("File '%s' does not exist. Please provide valid file" % attachment_report_file)

    # Guess encoding type
    ctype, encoding = mimetypes.guess_type(attachment_report_file)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'  # Use a binary type as guess couldn't made

    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        fp = open(attachment_report_file)
        attachment = MIMEText(fp.read(), subtype)
        fp.close()
    elif maintype == 'image':
        fp = open(attachment_report_file, 'rb')
        attachment = MIMEImage(fp.read(), subtype)
        fp.close()
    elif maintype == 'audio':
        fp = open(attachment_report_file, 'rb')
        attachment = MIMEAudio(fp.read(), subtype)
        fp.close()
    else:
        fp = open(attachment_report_file, 'rb')
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        encoders.encode_base64(attachment)
    # Set the filename parameter
    attachment.add_header('Content-Disposition',
                          'attachment',
                          filename=os.path.basename(attachment_report_file))

    return attachment


