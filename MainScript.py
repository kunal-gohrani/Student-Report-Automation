#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PdfMaker
import MailSender
import json
import datetime
import argparse


# In[2]:


def load_json():
    with open('user_list.json') as f:
        return json.load(f)


def get_prev_month():
    month = datetime.datetime.now()
    month = month.strftime('%B')
    previous_month = {'January': 'December', 'February': 'January', 'March': 'February', 'April': 'March',
                      'May': 'April', 'June': 'May', 'July': 'June', 'August': 'July', 'September': 'August',
                      'October': 'September', 'November': 'October', 'December': 'November'}
    return previous_month[month]


# In[ ]:


def init():
    args = argSetter()  # stores arguments passed through command line in dictionary format
    pdf = PdfMaker.PdfMaker()
    mail = MailSender.EmailSender()
    users = load_json()

    if args['month'] == None:  # if a month is explicitly passed through command line
        month = get_prev_month()
    else:
        month = args['month']

    for i in users['People']:  # PDF generation part, generates pdf by iterating over names stored in json
        print('PDF Generation:')
        print('Name:', i['Name'])
        pdf.generate_report_monthly(month, i['Name'])

    if args['sendmail'] == True:  # check if the program should run the mail sender part
        print('Email Sender: ')
        for i in users['People']:
            if args['sendall'] == False:  # check if we need to send to all people,
                # if False, then only send to teammates
                if i['Name'] == 'Bhavna' or i['Name'] == 'Apurwa' or i['Name'] == 'Kunal':
                    print('Sending to', i['Name'])
                    mail.send_mail(name=i['Name'], month=month, email=i['Email'])

            elif args['sendall'] == True:  # send mail to all people
                print('Sending to', i['Name'])
                mail.send_mail(name=i['Name'], month=month, email=i['Email'])


def argSetter():
    my_parser = argparse.ArgumentParser(description='Run the CampusX Project generator mailer')
    my_parser.add_argument('-a', '--sendall', action='store_true', default=False)
    my_parser.add_argument('-s', '--sendmail', action='store_true', default=False)
    my_parser.add_argument('-m', '--month', action='store')
    args = my_parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    init()

# In[ ]:
