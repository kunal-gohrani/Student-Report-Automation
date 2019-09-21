#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Simple Mail transfer protocol(SMTP) is an internet standard for electronic mail (email) transmission.
#smtplib:- the smtplib module defines an SMTP client session object that can be used to send mail to any internet machine with an SMTP or ESMTP listener
import smtplib 
from getpass import getpass
#mime is shortform form multipurpose internet mail extention.
# mime is an internet standard which just  specify the format to support text , attachments etc in a email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
class EmailSender:
    def __init__(self):
        self.username= "hellgod112@gmail.com"
        self.password=getpass()
        self.mail= smtplib.SMTP('smtp.gmail.com',587)
        self.mail.starttls()
        self.mail.login(self.username,self.password)
        del self.password
    def send_mail(self,name,month,email):
       
        #mail.ehlo() # saying hello to your server that you wnt to use their service 
        #secure tranfer protocol
        #msg='Milestone'
        #mail.sendmail(username,'gohrani.kunal8@gmail.com',msg)
        #MIMEMultipart will contain all the parts of  email body 
        msg= MIMEMultipart()

        msg['From']=self.username

        msg['To']= email

        msg['Subject']= "CampusX Monthly Report"

        text="Hi "+name+", here is your report card for the month of "+month

        msg.attach(MIMEText(text))

        #function to check how my current email look like 
        #print(msg.as_string())
        file_name=name+'_'+month+'.pdf'
        path=os.path.join('pdfs',file_name)
        with open(path , 'rb') as f:
            part=MIMEApplication(f.read())
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)

        _=self.mail.sendmail(msg['From'], msg['To'], msg.as_string())


# In[ ]:


if __name__=='__main__':
    obj=EmailSender()
    obj.send_mail(name='Kunal',month='September',email='gohranikunal25@outlook.com')


# In[ ]:




