import datetime
import os
import re
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from dotenv import load_dotenv
from pyvirtualdisplay import Display

from constants import SENDER

load_dotenv()
firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = "/usr/bin/firefox"
recipients = ["jameskelly2411@gmail.com"]
password = os.environ.get("PASSWORD")


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def get_post_info(url:str, class_name:str, web)-> str:
    web.get(url)
    soup = BeautifulSoup(web.page_source)
    return soup.find(class_=class_name).text

# def new_post_today(date:str) -> bool:
#     post_time = date.split('at')[0]
#     raw_date = datetime.datetime.strptime(post_time, '%B %d, %Y ')
#     todays_date = datetime.datetime.strftime(raw_date, '%Y-%m-%d %H:%M:%S').split(' ')[0]
#     date_parsed = datetime.datetime.strptime(todays_date, '%Y-%m-%d')
#     #if blog post from today
#     if date_parsed.date() == datetime.datetime.today().date():
#         return True
#     return False


def find_winds_reference(content):
    return re.search(r'\winds\b', content.lower())


def same_post(last_date:str) -> bool:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/last_date.txt') as f:
        date = f.read()
    if last_date.strip() == date:
        return True


def update_last_date(date:str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(f'{dir_path}/last_date.txt', 'w') as f:
        f.write(date)



if __name__ == '__main__':

    display = Display(visible=0, size=(1600, 1200))
    display.start()
    todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
    web = webdriver.Chrome()
    date = get_post_info('https://georgerrmartin.com/notablog/', 'thedate', web)
    if not same_post(date):
        print('New post found!')
        content = get_post_info('https://georgerrmartin.com/notablog/', 'post', web)
        if find_winds_reference(content):
            send_email(f'{ todays_date} New potential Winds of winter Reference !',f'Check \n https://georgerrmartin.com/notablog/ \n Quick!! \n\n{content}',
                       SENDER,
                       recipients, password
                       )
        else:
            send_email(f'{ todays_date} New blog post no winds though','Check \n https://georgerrmartin.com/notablog/ \n Words are wind',
                       SENDER,
                       recipients, password
                       )
        update_last_date(date)
    else:
        send_email(f'{ todays_date} No new blog post today',
                   'Keep watching on the wall',
                   SENDER,
                   recipients, password
                   )

    web.close()


