from bs4 import BeautifulSoup
import requests, re
import pandas as pd
import datetime
import time

dict_counts={}

def web_crawler(paging, paging_count, url_link, element_to_find, attr, attr_value, sub_attr, caption, sub_attr_attr = '', sub_attr_attr_value=''):
    count = 0

    try:
        if paging:
            for i in range(1, paging_count):
                url = url_link.format(i)
                print(url)
                reqs = requests.get(url)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                table = soup.find(element_to_find, attrs={attr: attr_value})
                if sub_attr_attr == '':
                    for each_row in table.find_all(sub_attr):
                        count += 1
                else:
                    for each_row in table.find_all(sub_attr, attrs={sub_attr_attr: sub_attr_attr_value}):
                        count += 1
        else:
            url = url_link
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find(element_to_find, attrs={attr: attr_value})

            if sub_attr_attr == '':
                for each_row in table.find_all(sub_attr):
                    count += 1
            else:
                for each_row in table.find_all(sub_attr, attrs={sub_attr_attr: sub_attr_attr_value}):
                    count += 1
    except Exception as e:
        print("Exception for {0}:- {1}".format(caption, str(e)))
        count = -1

    return count


url = 'https://dte.goa.gov.in'
reqs = requests.get(url, verify=False)
soup = BeautifulSoup(reqs.text, 'html.parser')
table = soup.find('div', attrs={'class': 'views-field views-field-title'})


######################################################################################3
########################################################################################
df=pd.read_csv(r"C:\Finchiktsak\ClientListExcel_2827_2023-06-30 (2).csv")

for index, row in df.iterrows():
    nbr = '+91' + str(row['nbr'])

msg1= '''
🎯 *NEET & IIT-JEE Counselling*

✨ Forms, Cut-Offs, College Preference list, College Study, Seminars, Placements, India & Abroad admissions etc.✨

*Join Our Whatsapp Groups to get latest updates and notifications:-*
- *NEET Whatsapp* - https://chat.whatsapp.com/BEVWFpnOTKBIdAWBiYMywG
- *IIT-JEE Whatsapp* - https://chat.whatsapp.com/D2c3qwnMRQ44gsyksxBpTz

*Subscribe to Our YouTube Channels*
- *NEET Youtube* - https://www.youtube.com/channel/UCSe4bTh0PxHzCxFhXooPzFA
- *IIT-JEE Youtube* - https://www.youtube.com/channel/UCmWyK-zZw7idj3p4DoTK4pg

Turn your dreams into reality with us! 🚀

*Contact us today at*:-
+91 8484849630,
+91 8600164008

🌟 *VidyaSaarthi Pvt Ltd, Kurukshetra* 🌟
'''

msg='''
*Are you a 12th grader worried for NEET & IIT-JEE admissions?* From forms to cut-offs and college choices, it is not easy to crack the right strategy.

This is where we come in!

At *VidyaSaarthi* Pvt. Ltd., Kurukshetra, we offer:-

✅ *Personalized Counselling* for NEET & IIT-JEE
✅ Assistance with *forms, cut-offs* , and *college preferences*
✅ Expert guidance on c *ollege studies* , *seminars* , and *placements*
✅ Help with *India* & *Abroad* *admissions* to top-tier institutions

🚀 Let us guide you every step of the way to ensure you achieve your goals!

*Join Our WhatsApp Groups to get latest updates and notifications:-*
* *NEET WhatsApp* - https://chat.whatsapp.com/BEVWFpnOTKBIdAWBiYMywG
* *IIT-JEE WhatsApp* - https://chat.whatsapp.com/D2c3qwnMRQ44gsyksxBpTz

*Subscribe to Our YouTube Channels*
* *NEET YouTube* - https://www.youtube.com/channel/UCSe4bTh0PxHzCxFhXooPzFA
* *IIT-JEE YouTube* - https://www.youtube.com/channel/UCmWyK-zZw7idj3p4DoTK4pg

📞 *Contact* us today: 8484849630 | 8600164008
✨ *VidyaSaarthi Pvt. Ltd., Kurukshetra* – *Where your future takes flight!* 🚀
'''

pywhatkit.sendwhatmsg_instantly(phone_no = '+918377837545', message=msg, tab_close=True, wait_time=8)
pywhatkit.sendwhats_image(receiver='+918377837545',
                          img_path=r"C:\Users\Shubham Aggarwal\Downloads\VS services.png",
                          caption=msg, tab_close=True, wait_time=40, close_time=5)


import telegram


# use token generated in first step
bot = telegram.Bot(token='7817142696:AAGuAROypBqqeDelZzk7sglopV6A6ridH_Q')
status = bot.send_message(chat_id="@@VidyaSaarthiNEETUG", text='hello..this is python bot for VS neetug', parse_mode=telegram.ParseMode.HTML)
bot.sendPhoto(chat_id="@VSNEETUGTEST", photo= open('H:\My Drive\Business\Vidya Saarthi\Logo\Vidya Saarthi Edu-Specialist Logo.jpg', 'rb'), caption='test')
bot.send_document(chat_id="@@VidyaSaarthiNEETUG", document=open(r"C:\Users\Shubham Aggarwal\Downloads\qw.pdf", 'rb') , caption = "Check this document!")
print(status)

import os, glob
import telegram
import time
path=r'C:\Users\Shubham Aggarwal\Downloads\WhatsApp Chat - VidyaSaarthi NEET Guidance'
files = list(filter(os.path.isfile, glob.glob(path + "\*")))
files.sort(key=os.path.getctime)
bot = telegram.Bot(token='7817142696:AAGuAROypBqqeDelZzk7sglopV6A6ridH_Q')
i=0
for each in files:
    ext=each[-4:]
    i=i+1
    try:
        if ext=='.jpg':
            bot.send_photo(chat_id="@VidyaSaarthiNEETUG", photo=open(each,'rb'), timeout=60)
        elif ext=='.pdf':
            bot.send_document(chat_id="@VidyaSaarthiNEETUG", document=open(each,'rb'), timeout=60)
        elif ext in ('.mp4','.mov'):
            bot.send_video(chat_id="@VidyaSaarthiNEETUG", video=open(each,'rb'), timeout=60)
        elif ext in ('.m4a'):
            bot.send_audio(chat_id="@VidyaSaarthiNEETUG", audio=open(each,'rb'), timeout=60)
        else:
            print("File not supported - {0}".format(each))

        if i%10==0:
            time.sleep(30)
    except Exception as e:
        print(e)





# The process name to be terminated
