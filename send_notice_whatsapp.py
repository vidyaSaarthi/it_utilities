import glob
import os
import time
import asyncio
import telegram
import datetime

def send_telegram(grp, token_str, msg):
    try:
        telegram_msg = msg
        telegram_group_id = grp
        bot = telegram.Bot(token=token_str)
        asyncio.run(bot.send_message(chat_id=telegram_group_id, text=telegram_msg))
        os.remove(file_name)
    except:
        pass

def send_error_notices():
    msg_list=[]
    list_of_error_files = glob.glob(r'.\error_notices\*')
    for file_name in list_of_error_files:
        f = open(file_name, "r")
        notice_txt = f.read()
        # print(notice_txt)
        grp = notice_txt.split(",")[0]
        msg = notice_txt.split(",")[1]
        msg_list.append(msg)
        f.close()
        os.remove(file_name)

    mylist = list(dict.fromkeys(msg_list))
    # print(mylist)

    for each_error_msg in mylist:
        send_telegram("@VS_Error_Notices", '7253352863:AAGS62qdzNVJtoL3UmAvcji9haevrm0GapY', each_error_msg)

while 1:
    list_of_files = glob.glob(r'.\new_notices\*')

    for file_name in list_of_files:
        print("file_name is {0}".format(file_name))
        time.sleep(5)

        f = open(file_name, "r")

        notice_txt = f.read()
        # print("notice_txt is {0}".format(notice_txt))
        grp = notice_txt.split(",")[0]
        # print("grp is {0}".format(grp))
        msg = notice_txt.split(",")[1]
        # print(grp, msg)
        f.close()
        send_telegram('@VS_Notices', '7873667251:AAFoZVUhEM5cbLsvCTrpuJ6BxJy-WmvWY14', msg)

    curr_time = datetime.datetime.now().minute

    if str(curr_time) in ('29','59'):
        send_error_notices()
