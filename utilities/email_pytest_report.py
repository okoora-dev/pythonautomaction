import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes
from email import encoders



class Email_Pytest_Report:
    "Class to email pytest report"

    def __init__(self):
        self.smtp_lib=smtplib.SMTP('okoora-com.mail.protection.outlook.com')
        self.smtp_lib_port = 25
        self.sender ="qa@okoora.com"
        self.targets =["danielh@okoora.com"]


    def get_test_report_data(self,html_body_flag= True,report_file_path= 'default'):
        "get test report data from pytest_report.html or pytest_report.txt or from user provided file"
        if html_body_flag == True and report_file_path == 'default':
            #To generate pytest_report.html file use following command e.g. py.test --html = log/pytest_report.html
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Tests','report.html'))#Change report file name & address here
        elif html_body_flag == False and report_file_path == 'default':
            #To generate pytest_report.log file add ">pytest_report.log" at end of py.test command e.g. py.test -k example_form -r F -v > log/pytest_report.log
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Tests','pytest_report.log'))#Change report file name & address here
        else:
            test_report_file = report_file_path
        #check file exist or not
        if not os.path.exists(test_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file"%test_report_file)

        with open(test_report_file, "r") as in_file:
            testdata = ""
            for line in in_file:
                testdata = testdata + '\n' + line

        return testdata


    def get_attachment(self,attachment_file_path = 'default'):
        "Get attachment and attach it to mail"
        if attachment_file_path == 'default':
            #To generate report.html file use following command e.g. py.test --html = log/report.html
            attachment_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','Tests','report.html'))#Change report file name & address here
        else:
            attachment_report_file = attachment_file_path
        #check file exist or not
        if not os.path.exists(attachment_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file"%attachment_report_file)

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


    def send_test_report_email(self,html_body_flag = True,attachment_flag = False,report_file_path = 'default'):
        "send test report email"
        #1. Get html formatted email body data from report_file_path file (log/report.html) and do not add it as an attachment
        if html_body_flag == True and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,report_file_path) #get html formatted test report data from log/report.html
            message = MIMEText(testdata,"html") # Add html formatted test data to email

        #2. Get text formatted email body data from report_file_path file (log/pytest_report.log) and do not add it as an attachment
        elif html_body_flag == False and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,report_file_path) #get html test report data from log/pytest_report.log
            message  = MIMEText(testdata) # Add text formatted test data to email

        #3. Add html formatted email body message along with an attachment file
        elif html_body_flag == True and attachment_flag == True:
            message = MIMEMultipart()
            #add html formatted body message to email
            html_body = MIMEText('''<p>Hello,</p>
                                     <p>&nbsp; &nbsp; &nbsp; &nbsp; Please check the attachment to see test built report.</p>
                                     <p><strong>Note: For best UI experience, download the attachment and open using Chrome browser.</strong></p>
                                 ''',"html") # Add/Update email body message here as per your requirement
            message.attach(html_body)
            #add attachment to email
            attachment = self.get_attachment(report_file_path)
            message.attach(attachment)

        #4. Add text formatted email body message along with an attachment file
        else:
            message = MIMEMultipart()
            #add test formatted body message to email
            plain_text_body = MIMEText('''Hello,\n\tPlease check attachment to see test built report.
                                       \n\nNote: For best UI experience, download the attachment and open  using Chrome browser.''')# Add/Update email body message here as per your requirement
            message.attach(plain_text_body)
            #add attachment to email
            attachment = self.get_attachment(report_file_path)
            message.attach(attachment)

            message['From'] = self.sender
            message['To'] = ', '.join(self.targets)
            message['Subject'] = 'Script generated test report' # Update email subject here
            time.sleep(5)
        #Send Email

        server = smtplib.SMTP('okoora-com.mail.protection.outlook.com', 25)
        server.sendmail(self.sender, self.targets, message.as_string())
        server.quit()
