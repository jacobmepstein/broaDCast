import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from datetime import date
import time
import schedule


def text_menu():
    url = 'https://www.haverford.edu/dining-services/dining-center'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    menu = soup.find(class_='container today_menu_1')

    if date.today().weekday() == 5 or 6:
        # check if it's the weekend
        brunch = menu.find('h4', string='Brunch ').parent.p
        dinner = menu.find('h4', string='Dinner ').parent.p

        brunch_list = str(brunch).replace('<br/>', '\n').replace('<p>', '').replace('</p>', '')
        dinner_list = str(dinner).replace('<br/>', '\n').replace('<p>', '').replace('</p>', '')

        today_menu = f"Hello Jacob! Here is today's menu at the Dining Center:\n\nBrunch:\n{brunch_list}\n\nDinner:\n{dinner_list}"

    else:
        breakfast = menu.find('h4', string='Breakfast').parent.p
        lunch = menu.find('h4', string='Lunch').parent.p
        dinner = menu.find('h4', string='Dinner').parent.p

        breakfast_list = str(breakfast).replace('<br/>', '\n').replace('<p>', '').replace('</p>', '')
        lunch_list = str(lunch).replace('<br/>', '\n').replace('<p>', '').replace('</p>', '')
        dinner_list = str(dinner).replace('<br/>', '\n').replace('<p>', '').replace('</p>', '')

        today_menu = f"Hello Jacob! Here is today's menu at the Dining Center:\n\nBreakfast:\n{breakfast_list}\n\nLunch:\n{lunch_list}\n\nDinner:\n{dinner_list}"

    account_sid = 'XXX'
    auth_token = 'XXX'
    client = Client(account_sid, auth_token)

    message = client.messages.create(body=today_menu, from_='+12223334444', to='+12223334444')

    print(message.sid)


schedule.every().day.at("09:00").do(text_menu)
while True:
    schedule.run_pending()
    time.sleep(1)
