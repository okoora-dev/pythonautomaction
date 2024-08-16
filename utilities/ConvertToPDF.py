import os
import datetime
import time

from pyhtml2pdf import converter


path = os.path.abspath('C:/Users/DanielHasid/PycharmProjects/Automation/Tests/report.html')
def convrtPDF():

        target_path = os.path.abspath('C:/Users/DanielHasid/PycharmProjects/Automation/utilities')
        # now = datetime.datetime.now()
        pdf_name = '/report.pdf'
        converter.convert(f'file:///{path}',f"{target_path}{pdf_name}")


convrtPDF()