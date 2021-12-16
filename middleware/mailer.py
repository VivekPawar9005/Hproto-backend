import os
from smtplib import SMTP, SMTPException 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from models import admin_config
from configs import settings
import ssl

class mailer():
    def __init__(self):
        self.absolute_path=os.path.abspath(__file__)
        admin_config_obj=admin_config.adminConfig()
        self.smtp_config=admin_config_obj.mail_configs()    
    def send_mail(self,data):
        if data['attachment_flag']:
            message = MIMEMultipart()
        else:
            message = MIMEMultipart("alternative")    
        message['Subject'] = data['subject']
        message['From'] = self.smtp_config['details']['communicationFromAddress']['emailAddress']
        message['To'] = data['to_email']
        pdf_path=settings.TXN_FILES_PATH
        message.attach(MIMEText(data['content'], "html"))
        if data['attachment_flag']:
            with open(pdf_path+'/'+data['attachment'], "rb") as f:
                attach = MIMEApplication(f.read(),_subtype="pdf")
            attach.add_header('Content-Disposition','attachment',filename=data['attachment'])
            message.attach(attach)
            os.remove(pdf_path+'/'+data['attachment'])
        try:
            msgBody = message.as_string()
            context = ssl.create_default_context()
            server = SMTP(self.smtp_config['details']['hostName'],self.smtp_config['details']['port'])
            server.set_debuglevel(2)
            server.starttls(context = context)
            server.login(self.smtp_config['details']['authentication']['user'], self.smtp_config['details']['authentication']['password'])
            server.sendmail(self.smtp_config['details']['communicationFromAddress']['emailAddress'], data['to_email'], msgBody)
            server.quit()            
        except SMTPException as e:
            return e
