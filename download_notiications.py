from bs4 import BeautifulSoup
import requests, re
import pandas as pd
import pywhatkit
import time
import datetime
import os

# importing module
import logging

# Create and configure logger
logging.basicConfig(filename="download_notiications.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)


def web_crawler(paging, paging_count, url_link, element_to_find, attr, attr_value, sub_attr, caption, sub_attr_attr='',
                sub_attr_attr_value=''):
    count = 0

    try:
        if paging:
            for i in range(1, paging_count):
                url = url_link.format(i)
                reqs = requests.get(url, verify=False)
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
        logging.info("Exception for {0}:- {1}".format(caption, str(e)))
        count = -1

    return count


def send_whatsapp(caption_msg, state):
    logging.info("New Notiication Found in {0}".format(state))
    # pywhatkit.sendwhats_image(receiver='+918377837545', \
    #                           img_path=r"Vidya Saarthi Edu-Specialist Logo.jpeg", \
    #                           caption=caption_msg, tab_close=True, wait_time=40, close_time=5)

    filename = r'.\new_notices\{0}_'.format(state) + str(datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"

    if state not in ['JEE MAINS 1', 'JEE MAINS 2', 'JEE MAINS 3', 'VITEEE', 'JEE Advanced']:
        with open(filename, "w") as f:
            f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format(caption_msg))

        # pywhatkit.sendwhatmsg_to_group_instantly(group_id='G9nAAne3vq5EhGQEAfe3bA',
        #                                          message=caption_msg,
        #                                          tab_close=True, wait_time=40, close_time=5)

    else:

        with open(filename, "w") as f:
            f.write("LroI0bTcnjG050Vgl6TF2L,{0}".format(caption_msg))

        # pywhatkit.sendwhatmsg_to_group_instantly(group_id='LroI0bTcnjG050Vgl6TF2L',
        #                                          message=caption_msg,
        #                                          tab_close=True, wait_time=40, close_time=5)


def check_new_notification(old_count, new_count, state, url):
    if old_count == -1 or new_count == -1:
        logging.info("Issue in Reading notice for {0}\n{1}".format(state, url))
        caption_msg = "LroI0bTcnjG050Vgl6TF2L,*Issue in Reading notice for {0}*\n{1}".format(state, url)

        # pywhatkit.sendwhats_image(receiver='+918377837545',
        #                           img_path=r"Vidya Saarthi Edu-Specialist Logo.jpeg",
        #                           caption=caption_msg, tab_close=True, wait_time=40, close_time=5)

        filename = r'.\error_notices\{0}_error_notice_'.format(state) + str(
            datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"
        with open(filename, "w") as f:
            f.write(caption_msg)

        return
        exit

    if old_count != new_count and new_count > old_count:
        caption_msg = "**New Notification Alert** in **{0}**\n{1}\n**Number Of Notices** : **{2}**\n".format(
            state, url, new_count - old_count)
        send_whatsapp(caption_msg, state)


iter = 0

while 1:
    logging.info(datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))
    dict_counts = {}

    old_df = pd.read_csv("neet_notifications_count.csv")

    kerala_old_count = old_df[old_df.State.isin(['kerala_count'])]['Counts'][0]
    tamil_nadu_old_count = old_df[old_df.State.isin(['tamil_nadu_count'])]['Counts'][1]
    haryana_1_old_count = old_df[old_df.State.isin(['haryana_1_count'])]['Counts'][2]
    haryana_2_old_count = old_df[old_df.State.isin(['haryana_2_count'])]['Counts'][3]
    karnataka_old_count = old_df[old_df.State.isin(['karnataka_count'])]['Counts'][4]
    hp_old_count = old_df[old_df.State.isin(['hp_count'])]['Counts'][5]
    uk_old_count = old_df[old_df.State.isin(['uk_count'])]['Counts'][6]
    pb_old_count = old_df[old_df.State.isin(['pb_count'])]['Counts'][7]
    up_old_count = old_df[old_df.State.isin(['up_count'])]['Counts'][8]
    jk_old_count = old_df[old_df.State.isin(['jk_count'])]['Counts'][9]
    rajasthan_old_count = old_df[old_df.State.isin(['rajasthan_count'])]['Counts'][10]
    mp_old_count = old_df[old_df.State.isin(['mp_count'])]['Counts'][11]
    cg_old_count = old_df[old_df.State.isin(['cg_count'])]['Counts'][12]
    jh_old_count = old_df[old_df.State.isin(['jh_count'])]['Counts'][13]
    wb1_old_count = old_df[old_df.State.isin(['wb_count1'])]['Counts'][14]
    wb2_old_count = old_df[old_df.State.isin(['wb_count2'])]['Counts'][15]
    wb3_old_count = old_df[old_df.State.isin(['wb_count3'])]['Counts'][16]
    mcc1_old_count = old_df[old_df.State.isin(['mcc1_count'])]['Counts'][17]
    mcc2_old_count = old_df[old_df.State.isin(['mcc2_count'])]['Counts'][18]
    mcc3_old_count = old_df[old_df.State.isin(['mcc3_count'])]['Counts'][19]
    mcc4_old_count = old_df[old_df.State.isin(['mcc4_count'])]['Counts'][20]
    mcc5_old_count = old_df[old_df.State.isin(['mcc5_count'])]['Counts'][21]
    gujju_old_count = old_df[old_df.State.isin(['gujju_count'])]['Counts'][22]
    mh_old_count = old_df[old_df.State.isin(['mh_count'])]['Counts'][23]
    assam_old_count = old_df[old_df.State.isin(['assam_count'])]['Counts'][24]
    telangana_old_count = old_df[old_df.State.isin(['telangana_count'])]['Counts'][25]
    ap_old_count = old_df[old_df.State.isin(['ap_count'])]['Counts'][26]
    gmch_old_count = old_df[old_df.State.isin(['gmch_count'])]['Counts'][27]
    pudu_old_count = old_df[old_df.State.isin(['pudu_count'])]['Counts'][28]
    bihar_old_count = old_df[old_df.State.isin(['bihar_count'])]['Counts'][29]
    odisha_old_count = old_df[old_df.State.isin(['odisha_count'])]['Counts'][30]
    manipur_old_count = old_df[old_df.State.isin(['manipur_count'])]['Counts'][31]
    meghalaya_old_count = old_df[old_df.State.isin(['meghalaya_count'])]['Counts'][32]
    nagaland_old_count = old_df[old_df.State.isin(['nagaland_count'])]['Counts'][33]
    ipu_1_old_count = old_df[old_df.State.isin(['ipu_1_count'])]['Counts'][34]
    ipu_2_old_count = old_df[old_df.State.isin(['ipu_2_count'])]['Counts'][35]
    tripura_old_count = old_df[old_df.State.isin(['tripura_count'])]['Counts'][36]

    ##############################################################################

    mcc_pg_1_old_count = old_df[old_df.State.isin(['mcc_pg_1_count'])]['Counts'][37]
    mcc_pg_2_old_count = old_df[old_df.State.isin(['mcc_pg_2_count'])]['Counts'][38]
    mcc_pg_3_old_count = old_df[old_df.State.isin(['mcc_pg_3_count'])]['Counts'][39]
    mcc_pg_4_old_count = old_df[old_df.State.isin(['mcc_pg_4_count'])]['Counts'][40]
    mcc_pg_5_old_count = old_df[old_df.State.isin(['mcc_pg_5_count'])]['Counts'][41]
    pb_pg_old_count = old_df[old_df.State.isin(['pb_pg_count'])]['Counts'][42]
    rj_pg_old_count = old_df[old_df.State.isin(['rj_pg_count'])]['Counts'][43]
    karnataka_pg_old_count = old_df[old_df.State.isin(['karnataka_pg_count'])]['Counts'][44]
    uk_pg_old_count = old_df[old_df.State.isin(['uk_pg_count'])]['Counts'][45]
    mp_pg_old_count = old_df[old_df.State.isin(['mp_pg_count'])]['Counts'][46]
    wb_1_pg_old_count = old_df[old_df.State.isin(['wb_1_pg_count'])]['Counts'][47]
    wb_2_pg_old_count = old_df[old_df.State.isin(['wb_2_pg_count'])]['Counts'][48]
    wb_3_pg_old_count = old_df[old_df.State.isin(['wb_3_pg_count'])]['Counts'][49]
    gujju_pg_old_count = old_df[old_df.State.isin(['gujju_pg_count'])]['Counts'][50]
    mh_pg_old_count = old_df[old_df.State.isin(['mh_pg_count'])]['Counts'][51]
    gmch_pg_old_count = old_df[old_df.State.isin(['gmch_pg_count'])]['Counts'][52]
    kerala_pg_old_count = old_df[old_df.State.isin(['kerala_pg_count'])]['Counts'][53]
    bihar_pg_old_count = old_df[old_df.State.isin(['bihar_pg_count'])]['Counts'][54]
    wb_1_ayush_old_count = old_df[old_df.State.isin(['wb_1_ayush_count'])]['Counts'][55]
    wb_2_ayush_old_count = old_df[old_df.State.isin(['wb_2_ayush_count'])]['Counts'][56]
    wb_3_ayush_old_count = old_df[old_df.State.isin(['wb_3_ayush_count'])]['Counts'][57]
    up_ayush_old_count = old_df[old_df.State.isin(['up_ayush_count'])]['Counts'][58]
    rj_ayush_old_count = old_df[old_df.State.isin(['rj_ayush_count'])]['Counts'][59]
    skau_ayush_old_count = old_df[old_df.State.isin(['skau_ayush_count'])]['Counts'][60]

    ##############################################################################
    ##############################################################################

    jee_main_ac_old_count = old_df[old_df.State.isin(['jee_main_ac_count'])]['Counts'][61]
    jee_main_nic_old_count = old_df[old_df.State.isin(['jee_main_nic_count'])]['Counts'][62]
    nta_ac_old_count = old_df[old_df.State.isin(['nta_ac_count'])]['Counts'][63]
    viteee_old_count = old_df[old_df.State.isin(['viteee_count'])]['Counts'][64]
    odisha_pg_old_count = old_df[old_df.State.isin(['odisha_pg_count'])]['Counts'][65]
    aiims_old_count = old_df[old_df.State.isin(['aiims_count'])]['Counts'][66]
    nbems_old_count = old_df[old_df.State.isin(['nbems_count'])]['Counts'][67]
    jee_adv_old_count = old_df[old_df.State.isin(['jee_adv_count'])]['Counts'][68]
    goa_old_count = old_df[old_df.State.isin(['goa_count'])]['Counts'][69]
    sikkim_old_count = old_df[old_df.State.isin(['sikkim_count'])]['Counts'][70]
    jnims_old_count = old_df[old_df.State.isin(['jnims_count'])]['Counts'][71]
    jh_pg_old_count = old_df[old_df.State.isin(['jh_pg_count'])]['Counts'][72]
    dme_assam_old_count = old_df[old_df.State.isin(['dme_assam_count'])]['Counts'][73]
    dnb_kerala_old_count = old_df[old_df.State.isin(['dnb_kerala_count'])]['Counts'][74]
    aaccc_current_events_ayush_ug_old_count = \
    old_df[old_df.State.isin(['aaccc_current_events_ayush_ug_count'])]['Counts'][75]
    aaccc_news_events_ayush_ug_old_count = old_df[old_df.State.isin(['aaccc_news_events_ayush_ug_count'])]['Counts'][76]
    ipu_ayush_old_count = old_df[old_df.State.isin(['ipu_ayush_count'])]['Counts'][77]
    uttarakhand_ayush_old_count = old_df[old_df.State.isin(['uttarakhand_ayush_count'])]['Counts'][78]
    fmsc_bhms_old_count = old_df[old_df.State.isin(['fmsc_bhms_count'])]['Counts'][79]
    fmsc_bams_bums_old_count = old_df[old_df.State.isin(['fmsc_bams_bums_count'])]['Counts'][80]

    ##Kerala#########################################################################
    try:
        logger.info("Checking Kerala")
        kerala_count = 0
        for i in range(1, 20):

            url = 'https://cee.kerala.gov.in/keam2024/notification?page=' + str(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'card-body'})

            for div in table.find_all('div', attrs={'class': 'row'}):
                kerala_count = kerala_count + 1

    except Exception as e:
        logging.info("Exception for Kerala:- " + str(e))
        kerala_count = -1

    check_new_notification(old_count=kerala_old_count,
                           new_count=kerala_count,
                           state='Kerala',
                           url='https://cee.kerala.gov.in/keam2024/notification')

    dict_counts['kerala_count'] = kerala_count

    ##Tamil Nadu################################################################
    logger.info("Checking Tamil Nadu")
    try:
        tamil_nadu_count = 0
        url = 'https://tnmedicalselection.net/Notification.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'col-sm-8 box_inner'})
        # rows=[]
        #

        for div in table.find_all('p'):
            #     logging.info('https://tnmedicalselection.net/' + div.get("href"))
            tamil_nadu_count = tamil_nadu_count + 1


    except Exception as e:
        logging.info("Exception for Tamil Nadu:- " + str(e))
        tamil_nadu_count = -1

    check_new_notification(old_count=tamil_nadu_old_count,
                           new_count=tamil_nadu_count,
                           state='Tamil Nadu',
                           url='https://tnmedicalselection.net/Notification.aspx')

    dict_counts['tamil_nadu_count'] = tamil_nadu_count

    ###Haryana 1###############################################################
    logger.info("Checking Haryana 1")

    try:
        haryana_1_count = 0
        url = 'https://uhsrugcounselling.com/Notice.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'container'})

        for each_row in table.find_all('div', attrs={'class': 'row'}):
            haryana_1_count += 1

    except Exception as e:
        logging.info("Exception for Haryana 1:- " + str(e))
        haryana_1_count = -1

    check_new_notification(old_count=haryana_1_old_count,
                           new_count=haryana_1_count,
                           state='Haryana 1',
                           url='https://uhsrugcounselling.com/Notice.aspx')

    dict_counts['haryana_1_count'] = haryana_1_count

    ###Haryana 2###############################################################

    logging.info("Checking Haryana 2")
    try:
        haryana_2_count = 0
        url = 'https://uhsr.ac.in/detail.aspx?artid=79&menuid=12'
        reqs = requests.get(url, verify=False, timeout=None)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table', attrs={'style': 'border-collapse: collapse; width: 100.561%; height: 37632px;'})

        # logging.info(table)
        date_element = []
        text_element = []
        href_element = []

        for each_row in table.find_all('tr'):
            haryana_2_count += 1

    except Exception as e:
        logging.info("Exception for Haryana 2:- " + str(e))
        haryana_2_count = -1

    check_new_notification(old_count=haryana_2_old_count,
                           new_count=haryana_2_count,
                           state='Haryana 2',
                           url='https://uhsr.ac.in/detail.aspx?artid=79&menuid=12')

    dict_counts['haryana_2_count'] = haryana_2_count

    ####Karnataka##############################################################
    logging.info("Checking Karnataka")
    try:
        karnataka_count = 0
        url = 'https://cetonline.karnataka.gov.in/kea/ugneet24'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'ContentPlaceHolder1_req_accordion'})

        for each_row in table.find_all('div', attrs={'class': 'card'}):
            karnataka_count += 1

    except Exception as e:
        logging.info("Exception for Karnataka:- " + str(e))
        karnataka_count = -1

    check_new_notification(old_count=karnataka_old_count,
                           new_count=karnataka_count,
                           state='Karnataka UG',
                           url='https://cetonline.karnataka.gov.in/kea/ugneet24')

    dict_counts['karnataka_count'] = karnataka_count

    #################################################################
    ####Himachal Pradesh##############################################################
    logging.info("Checking Himachal Pradesh")
    # try:
    #     hp_count = 0
    #
    #     for i in range(1, 200):
    #         url = 'https://amruhp.ac.in/notices/page/{0}/'.format(i)
    #         reqs = requests.get(url)
    #         soup = BeautifulSoup(reqs.text, 'html.parser')
    #         table = soup.find('div', attrs={'class': 'et_pb_text_inner'})
    #         if table is not None:
    #             for each_row in table.find_all('a', attrs={'class': 'text-white'}):
    #                 hp_count += 1
    #
    # except Exception as e:
    #     logging.info("Exception for HP:- " + str(e))
    #     hp_count = -1
    #
    # check_new_notification(old_count = hp_old_count,
    #                        new_count = hp_count,
    #                        state = 'Himachal Pradesh',
    #                        url = 'https://amruhp.ac.in/notices/')

    try:

        url = 'https://amruhp.ac.in/notices/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'et_pb_text_inner'})
        first_row = table.find('a', attrs={'class': 'text-white'})

        new_hp_text = first_row.text

        if iter == 0:
            old_hp_text = new_hp_text

        if new_hp_text != old_hp_text:
            hp_count = hp_old_count + 1
        else:
            hp_count = hp_old_count

        old_hp_text = new_hp_text

    except Exception as e:
        logging.info("Exception for HP:- " + str(e))
        hp_count = -1

    dict_counts['hp_count'] = hp_count

    #################################################################

    ####Uttarakhand##############################################################
    logging.info("Checking Uttarakhand")
    try:
        uk_count = 0

        url = 'https://meta-secure.com/HNBUMU_NEETUG'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'style': 'text-align: left; padding-left: 5px;'})
        for each_row in table.find_all('li'):
            uk_count += 1

    except Exception as e:
        logging.info("Exception for UK:- " + str(e))
        uk_count = -1

    check_new_notification(old_count=uk_old_count,
                           new_count=uk_count,
                           state='Uttarakhand UG',
                           url='https://meta-secure.com/HNBUMU_NEETUG')

    dict_counts['uk_count'] = uk_count

    ####Punjab##############################################################
    logging.info("Checking Punjab")
    try:
        pb_count = 0

        url = 'https://bfuhs.ac.in/MBBS_BDS/MBBSBDS.asp'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table', attrs={'class': 'table table-bordered border-success'})
        for each_row in table.find_all('a'):
            pb_count += 1

    except Exception as e:
        logging.info("Exception for Punjab:- " + str(e))
        pb_count = -1

    check_new_notification(old_count=pb_old_count,
                           new_count=pb_count,
                           state='Punjab UG',
                           url='https://bfuhs.ac.in/MBBS_BDS/MBBSBDS.asp')

    dict_counts['pb_count'] = pb_count

    #################################################################
    ####UP##############################################################
    logging.info("Checking UP")

    try:
        up_count = 0

        url = 'http://dgme.up.gov.in/Welcome/linkfiles?catid=news'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table')
        tbody = table.find('tbody')
        for each_row in tbody.find_all('tr'):
            up_count += 1

    except Exception as e:
        logging.info("Exception for UP:- " + str(e))
        up_count = -1

    check_new_notification(old_count=up_old_count,
                           new_count=up_count,
                           state='Uttar Pradesh',
                           url='http://dgme.up.gov.in/Welcome/linkfiles?catid=news')

    dict_counts['up_count'] = up_count

    ####J & K##############################################################

    logging.info("Checking J & K")
    try:
        jk_count = 0

        url = 'https://www.jkbopee.gov.in/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table', attrs={'class': 'table table-bordered table-striped table-responsive'})
        for each_row in table.find_all('tr'):
            jk_count += 1

    except Exception as e:
        logging.info("Exception for J & K:- " + str(e))
        jk_count = -1

    check_new_notification(old_count=jk_old_count,
                           new_count=jk_count,
                           state='J & K',
                           url='https://www.jkbopee.gov.in/')

    dict_counts['jk_count'] = jk_count

    ####Rajasthan##############################################################

    logging.info("Checking Rajasthan")
    try:

        rajasthan_count = 0

        url = 'https://www.rajugneet2024.org/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('td', attrs={'style': 'width: 543px; text-align: left;'})
        for each_row in table.find_all('tr'):
            rajasthan_count += 1

    except Exception as e:
        logging.info("Exception for Rajasthan:- " + str(e))
        rajasthan_count = -1

    check_new_notification(old_count=rajasthan_old_count,
                           new_count=rajasthan_count,
                           state='Rajasthan UG',
                           url='https://www.rajugneet2024.org/')

    dict_counts['rajasthan_count'] = rajasthan_count

    ####MP##############################################################

    logging.info("Checking MP")

    try:
        mp_count = 0
        url = 'https://dme.mponline.gov.in/Portal/Services/DMEMP/DMEUG/Profile/Instructions.aspx?tab=tab1'
        reqs = requests.get(url, verify=False)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'tab1'})
        for each_row in table.find_all('li'):
            mp_count += 1

    except Exception as e:
        logging.info("Exception for MP:- " + str(e))
        mp_count = -1

    check_new_notification(old_count=mp_old_count,
                           new_count=mp_count,
                           state='Madhya Pradesh UG',
                           url='https://dme.mponline.gov.in/Portal/Services/DMEMP/DMEUG/Profile/Instructions.aspx?tab=tab1')

    dict_counts['mp_count'] = mp_count

    ####Chhatisgarh##############################################################

    logging.info("Checking Chattisgah")
    try:
        cg_count = 0

        url = 'https://cgdme.in/Notice_24.php'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'text-widget2'})
        for each_row in table.find_all('tr'):
            cg_count += 1

    except Exception as e:
        logging.info("Exception for Chhattisgarh:- " + str(e))
        cg_count = -1

    check_new_notification(old_count=cg_old_count,
                           new_count=cg_count,
                           state='Chhattisgarh',
                           url='https://cgdme.in/Notice_24.php')

    dict_counts['cg_count'] = cg_count

    ####Jharkhand##############################################################

    logging.info("Checking Jharkhand UG")
    try:
        jh_count = 0

        url = 'https://jceceb.jharkhand.gov.in/Links/counselling.aspx'
        reqs = requests.get(url, verify=False)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'page_inner'})
        for each_row in table.find_all('tr'):
            jh_count += 1

    except Exception as e:
        logging.info("Exception for Jharkhand UG:- " + str(e))
        jh_count = -1

    check_new_notification(old_count=jh_old_count,
                           new_count=jh_count,
                           state='Jharkhand UG',
                           url='https://jceceb.jharkhand.gov.in/Links/counselling.aspx')

    dict_counts['jh_count'] = jh_count

    ####West Bengal##############################################################

    logging.info("Checking West Bengal 1")
    try:
        wb_count1 = 0

        url = 'https://wbmcc.nic.in/UGMedDen/UGMedDenNotices.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'boxdesignCurrentEvents'})
        for each_row in table.find_all('li'):
            wb_count1 += 1

    except Exception as e:
        logging.info("Exception for West Bengal 1:- " + str(e))
        wb_count1 = -1

    check_new_notification(old_count=wb1_old_count,
                           new_count=wb_count1,
                           state='West Bengal 1',
                           url='https://wbmcc.nic.in/UGMedDen/UGMedDenNotices.aspx')

    dict_counts['wb_count1'] = wb_count1

    logging.info("Checking West Bengal 2")
    try:
        wb_count2 = 0

        url = 'https://wbmcc.nic.in/UGMedDen/ugmeddenland.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'boxdesignImpLinks'})
        for each_row in table.find_all('li'):
            wb_count2 += 1

    except Exception as e:
        logging.info("Exception for West Bengal 2:- " + str(e))
        wb_count2 = -1

    check_new_notification(old_count=wb2_old_count,
                           new_count=wb_count2,
                           state='West Bengal 2',
                           url='https://wbmcc.nic.in/UGMedDen/ugmeddenland.aspx')

    dict_counts['wb_count2'] = wb_count2

    logging.info("Checking West Bengal 3")
    try:

        wb_count3 = 0

        url = 'https://wbmcc.nic.in/UGMedDen/UGMedDenNewsEvents.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'boxdesignCurrentEvents'})
        for each_row in table.find_all('li'):
            wb_count3 += 1

    except Exception as e:
        logging.info("Exception for West Bengal 3:- " + str(e))
        wb_count3 = -1

    check_new_notification(old_count=wb3_old_count,
                           new_count=wb_count3,
                           state='West Bengal 3',
                           url='https://wbmcc.nic.in/UGMedDen/UGMedDenNewsEvents.aspx')

    dict_counts['wb_count3'] = wb_count3

    ####MCC##############################################################

    logging.info("Checking MCC 1")
    try:
        mcc1_count = 0

        for i in range(1, 10):
            url = 'https://mcc.nic.in/current-events-ug/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'wpb_column vc_column_container vc_col-sm-12'})
            for each_row in table.find_all('tr'):
                mcc1_count += 1

    except Exception as e:
        logging.info("Exception for MCC 1:- " + str(e))
        mcc1_count = -1

    check_new_notification(old_count=mcc1_old_count,
                           new_count=mcc1_count,
                           state='MCC 1 UG',
                           url='https://mcc.nic.in/current-events-ug')

    dict_counts['mcc1_count'] = mcc1_count

    logging.info("Checking MCC 2")
    try:
        mcc2_count = 0

        url = 'https://mcc.nic.in/eservices-schedule-ug/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_row wpb_row vc_row-fluid'})

        for each_row in table.find_all('tr'):
            mcc2_count += 1

    except Exception as e:
        logging.info("Exception for MCC 2:- " + str(e))
        mcc2_count = -1

    check_new_notification(old_count=mcc2_old_count,
                           new_count=mcc2_count,
                           state='MCC 2 UG',
                           url='https://mcc.nic.in/eservices-schedule-ug/')

    dict_counts['mcc2_count'] = mcc2_count

    logging.info("Checking MCC 3")
    try:
        mcc3_count = 0

        for i in range(1, 10):
            url = 'https://mcc.nic.in/news-events-ug-medical/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'wpb_column vc_column_container vc_col-sm-12'})

            for each_row in table.find_all('tr'):
                mcc3_count += 1

    except Exception as e:
        logging.info("Exception for MCC 3:- " + str(e))
        mcc3_count = -1

    check_new_notification(old_count=mcc3_old_count,
                           new_count=mcc3_count,
                           state='MCC 3 UG',
                           url='https://mcc.nic.in/news-events-ug-medical/')

    dict_counts['mcc3_count'] = mcc3_count

    logging.info("Checking MCC 4")
    try:
        mcc4_count = 0

        url = 'https://mcc.nic.in/ug-medical-counselling/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_column-inner vc_custom_1647862263119'})

        for each_row in table.find_all('li'):
            mcc4_count += 1

    except Exception as e:
        logging.info("Exception for MCC 4:- " + str(e))
        mcc4_count = -1

    check_new_notification(old_count=mcc4_old_count,
                           new_count=mcc4_count,
                           state='MCC 4 UG',
                           url='https://mcc.nic.in/ug-medical-counselling/')

    dict_counts['mcc4_count'] = mcc4_count

    logging.info("Checking MCC 5")
    try:
        mcc5_count = 0

        url = 'https://mcc.nic.in/ug-medical-counselling/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_column-inner vc_custom_1647861778410'})

        for each_row in table.find_all('li'):
            mcc5_count += 1

    except Exception as e:
        logging.info("Exception for MCC 5:- " + str(e))
        mcc5_count = -1

    check_new_notification(old_count=mcc5_old_count,
                           new_count=mcc5_count,
                           state='MCC 5 UG',
                           url='https://mcc.nic.in/ug-medical-counselling/')

    dict_counts['mcc5_count'] = mcc5_count

    ####Gujarat##############################################################

    logging.info("Checking Gujarat")
    try:
        gujju_count_1 = 0

        url = 'https://www.medadmgujarat.org/ug/home.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'post'})

        for each_row in table.find_all('div', attrs={'style': 'border: 2px solid purple;'}):
            gujju_count_1 += 1

    except Exception as e:
        logging.info("Exception for Gujarat:- " + str(e))
        gujju_count_1 = -1

    gujju_count_2 = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://www.medadmgujarat.org/ug/home.aspx',
                                element_to_find='div',
                                attr='class',
                                attr_value='post',
                                sub_attr='div',
                                caption='Gujarat',
                                sub_attr_attr='style',
                                sub_attr_attr_value='border: 2px solid purple; font-size: 20px;')

    gujju_count = gujju_count_1 + gujju_count_2

    check_new_notification(old_count=gujju_old_count,
                           new_count=gujju_count,
                           state='Gujarat',
                           url='https://www.medadmgujarat.org/ug/home.aspx')

    dict_counts['gujju_count'] = gujju_count

    ####Maharashtra##############################################################

    logging.info("Checking Maharashtra")
    try:
        mh_count = 0

        url = 'https://medical2024.mahacet.org/NEET-UG-2024/login'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'd-lg-flex pos-relative col-lg-4 card pb-20 m-4px'})

        for each_div in table[1].find_all_next('li'):
            mh_count += 1

    except Exception as e:
        logging.info("Exception for Maharashtra:- " + str(e))
        mh_count = -1

    check_new_notification(old_count=mh_old_count,
                           new_count=mh_count,
                           state='Maharashtra',
                           url='https://medical2024.mahacet.org/NEET-UG-2024/login')

    dict_counts['mh_count'] = mh_count

    ####Assam##############################################################

    logging.info("Checking Assam")
    try:
        assam_count = 0

        url = 'https://dme.assam.gov.in/latest/admission-notice-ugpg-and-others'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'region region-content'})

        for each_div in table.find_all('tr'):
            assam_count += 1

    except Exception as e:
        logging.info("Exception for Assam:- " + str(e))
        assam_count = -1

    check_new_notification(old_count=assam_old_count,
                           new_count=assam_count,
                           state='Assam',
                           url='https://dme.assam.gov.in/latest/admission-notice-ugpg-and-others')

    dict_counts['assam_count'] = assam_count

    ####Telangana##############################################################

    logging.info("Checking Telangana")
    try:
        telangana_count = 0
        for i in range(1, 100):
            url = 'https://www.knruhs.telangana.gov.in/all-notifications/?cpage={0}'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={
                'class': 'fusion-fullwidth fullwidth-box fusion-builder-row-7 fusion-flex-container nonhundred-percent-fullwidth non-hundred-percent-height-scrolling'})

            for each_div in table.find_all('tr'):
                telangana_count += 1

    except Exception as e:
        logging.info("Exception for Telangana:- " + str(e))
        telangana_count = -1

    check_new_notification(old_count=telangana_old_count,
                           new_count=telangana_count,
                           state='Telangana',
                           url='https://www.knruhs.telangana.gov.in/all-notifications/')

    dict_counts['telangana_count'] = telangana_count

    ####Telangana##############################################################

    logging.info("Checking Andhra Pradesh")
    try:
        ap_count = 0

        url = 'https://drntr.uhsap.in/index/index.html'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_tta-panels-container'})

        for each_div in table.find_all('li'):
            ap_count += 1

    except Exception as e:
        logging.info("Exception for Andhra Pradesh:- " + str(e))
        ap_count = -1

    check_new_notification(old_count=ap_old_count,
                           new_count=ap_count,
                           state='Andhra Pradesh',
                           url='https://drntr.uhsap.in/index/index.html')

    dict_counts['ap_count'] = ap_count

    ####GMCH##############################################################

    logging.info("Checking GMCH")
    try:
        gmch_count = 0

        url = 'https://gmch.gov.in/centralized-admission-prospectus-mbbsbdsbhms-courses-session-2024'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'node node--type-page node--view-mode-full clearfix'})

        for each_div in table.find_all('tr'):
            gmch_count += 1

    except Exception as e:
        logging.info("Exception for GMCH:- " + str(e))
        gmch_count = -1

    check_new_notification(old_count=gmch_old_count,
                           new_count=gmch_count,
                           state='GMCH',
                           url='https://gmch.gov.in/centralized-admission-prospectus-mbbsbdsbhms-courses-session-2024')

    dict_counts['gmch_count'] = gmch_count
    ####Puducherry##############################################################

    logging.info("Checking Puducherry")
    try:
        pudu_count = 0

        url = 'https://www.centacpuducherry.in/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'nav-overall_news-home'})

        for each_div in table.find_all('div', attrs={'class': 'content text-danger font-weight-bold text-justify'}):
            pudu_count += 1

    except Exception as e:
        logging.info("Exception for Puducherry:- " + str(e))
        pudu_count = -1

    check_new_notification(old_count=pudu_old_count,
                           new_count=pudu_count,
                           state='Puducherry',
                           url='https://www.centacpuducherry.in/')

    dict_counts['pudu_count'] = pudu_count

    ####Bihar##############################################################

    logging.info("Checking Bihar UG")
    try:
        bihar_count = 0

        url = 'https://bceceboard.bihar.gov.in/UGMACIndex.php'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'SubDiv'})

        for each_div in table.find_all('li'):
            bihar_count += 1

    except Exception as e:
        logging.info("Exception for Bihar UG:- " + str(e))
        bihar_count = -1

    check_new_notification(old_count=bihar_old_count,
                           new_count=bihar_count,
                           state='Bihar UG',
                           url='https://bceceboard.bihar.gov.in/UGMACIndex.php')

    dict_counts['bihar_count'] = bihar_count

    ####Odisha##############################################################

    logging.info("Checking Odisha")
    try:
        odisha_count = 0

        for i in range(1, 10):
            url = 'https://ojee.nic.in/medical-notice/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'wpb_column vc_column_container vc_col-sm-12'})

            for each_row in table.find_all('tr'):
                odisha_count += 1

    except Exception as e:
        logging.info("Exception for Odisha:- " + str(e))
        odisha_count = -1

    check_new_notification(old_count=odisha_old_count,
                           new_count=odisha_count,
                           state='Odisha',
                           url='https://ojee.nic.in/medical-notice/')

    dict_counts['odisha_count'] = odisha_count

    ####Manipur##############################################################

    logging.info("Checking Manipur")
    try:
        manipur_count = 0
        url = 'https://manipurhealthdirectorate.mn.gov.in/notifications'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'col-md-8'})

        for each_row in table.find_all('li'):
            manipur_count += 1

    except Exception as e:
        logging.info("Exception for Manipur:- " + str(e))
        manipur_count = -1

    check_new_notification(old_count=manipur_old_count,
                           new_count=manipur_count,
                           state='Manipur',
                           url='https://manipurhealthdirectorate.mn.gov.in/notifications')

    dict_counts['manipur_count'] = manipur_count

    ####Meghalaya##############################################################

    logging.info("Checking Meghalaya")
    try:
        meghalaya_count = 0
        url = 'https://meghealth.gov.in/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'col-lg-3 col-md-3 col-sm-6'})

        for each_row in table.find_all('li'):
            meghalaya_count += 1

    except Exception as e:
        logging.info("Exception for Meghalaya:- " + str(e))
        meghalaya_count = -1

    check_new_notification(old_count=meghalaya_old_count,
                           new_count=meghalaya_count,
                           state='Meghalaya',
                           url='https://meghealth.gov.in/')

    dict_counts['meghalaya_count'] = meghalaya_count

    ####Nagaland##############################################################

    logging.info("Checking Nagaland")
    try:
        nagaland_count = 0
        url = 'https://dte.nagaland.gov.in/index.php/dept-2/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'entry themeform'})

        for each_row in table.find_all('tr'):
            nagaland_count += 1

    except Exception as e:
        logging.info("Exception for Nagaland:- " + str(e))
        nagaland_count = -1

    check_new_notification(old_count=nagaland_old_count,
                           new_count=nagaland_count,
                           state='Nagaland',
                           url='https://dte.nagaland.gov.in/index.php/dept-2/')

    dict_counts['nagaland_count'] = nagaland_count

    ####IPU 1 ##############################################################

    logging.info("Checking IPU News")
    try:
        ipu_1_count = 0
        for i in range(1, 50):
            url = 'https://ipu.admissions.nic.in/news-events/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'data-table-container'})

            for each_row in table.find_all('tr'):
                ipu_1_count += 1

    except Exception as e:
        logging.info("Exception for IPU News:- " + str(e))
        ipu_1_count = -1

    check_new_notification(old_count=ipu_1_old_count,
                           new_count=ipu_1_count,
                           state='IPU News & Events',
                           url='https://ipu.admissions.nic.in/news-events/')

    dict_counts['ipu_1_count'] = ipu_1_count

    ####IPU 2 ##############################################################

    logging.info("Checking IPU Current Events")
    try:
        ipu_2_count = 0
        for i in range(1, 50):
            url = 'https://ipu.admissions.nic.in/current-events/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'wpb_column vc_column_container vc_col-sm-12'})

            for each_row in table.find_all('tr'):
                ipu_2_count += 1

    except Exception as e:
        logging.info("Exception for IPU Current Events:- " + str(e))
        ipu_2_count = -1

    check_new_notification(old_count=ipu_2_old_count,
                           new_count=ipu_2_count,
                           state='IPU Current Events',
                           url='https://ipu.admissions.nic.in/current-events/')

    dict_counts['ipu_2_count'] = ipu_2_count

    ####Tripura ##############################################################

    logging.info("Checking Tripura")
    try:
        tripura_count = 0
        for i in range(1, 20):
            url = 'https://dme.tripura.gov.in/notification?page={0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'row content'})

            for each_row in table.find_all('tr'):
                tripura_count += 1

    except Exception as e:
        logging.info("Exception for Tripura:- " + str(e))
        tripura_count = -1

    check_new_notification(old_count=tripura_old_count,
                           new_count=tripura_count,
                           state='Tripura',
                           url='https://dme.tripura.gov.in/notification')

    dict_counts['tripura_count'] = tripura_count

    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################

    logging.info("Checking MCC PG Current Events ")

    mcc_pg_1_count = web_crawler(paging=True,
                                 paging_count=10,
                                 url_link='https://mcc.nic.in/current-events-pg/page/{0}/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='wpb_column vc_column_container vc_col-sm-12',
                                 sub_attr='tr',
                                 caption='MCC PG Current Events'
                                 )

    check_new_notification(old_count=mcc_pg_1_old_count,
                           new_count=mcc_pg_1_count,
                           state='MCC PG Current Events',
                           url='https://mcc.nic.in/current-events-pg')

    dict_counts['mcc_pg_1_count'] = mcc_pg_1_count

    logging.info("Checking MCC eService Schedule")

    mcc_pg_2_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://mcc.nic.in/eservices-schedule-pg/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='vc_row wpb_row vc_row-fluid',
                                 sub_attr='tr',
                                 caption='MCC PG eService Schedule'
                                 )

    check_new_notification(old_count=mcc_pg_2_old_count,
                           new_count=mcc_pg_2_count,
                           state='MCC PG eService Schedule',
                           url='https://mcc.nic.in/eservices-schedule-pg/')

    dict_counts['mcc_pg_2_count'] = mcc_pg_2_count

    logging.info("Checking MCC PG News Events")

    mcc_pg_3_count = web_crawler(paging=True,
                                 paging_count=10,
                                 url_link='https://mcc.nic.in/news-events-pg/page/{0}/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='wpb_column vc_column_container vc_col-sm-12',
                                 sub_attr='tr',
                                 caption='MCC PG News Events'
                                 )

    check_new_notification(old_count=mcc_pg_3_old_count,
                           new_count=mcc_pg_3_count,
                           state='MCC PG News Events',
                           url='https://mcc.nic.in/news-events-pg/')

    dict_counts['mcc_pg_3_count'] = mcc_pg_3_count

    logging.info("Checking MCC PG Candidate Board")

    mcc_pg_4_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://mcc.nic.in/pg-medical-counselling/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='vc_column-inner vc_custom_1647862263119',
                                 sub_attr='li',
                                 caption='MCC PG Candidate Board'
                                 )

    check_new_notification(old_count=mcc_pg_4_old_count,
                           new_count=mcc_pg_4_count,
                           state='MCC PG Candidate Board',
                           url='https://mcc.nic.in/pg-medical-counselling/')

    dict_counts['mcc_pg_4_count'] = mcc_pg_4_count

    logging.info("Checking MCC PG Important Link")

    mcc_pg_5_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://mcc.nic.in/pg-medical-counselling/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='vc_column-inner vc_custom_1647861778410',
                                 sub_attr='li',
                                 caption='MCC PG Important Link'
                                 )

    check_new_notification(old_count=mcc_pg_5_old_count,
                           new_count=mcc_pg_5_count,
                           state='MCC PG Important Link',
                           url='https://mcc.nic.in/ug-medical-counselling/')

    dict_counts['mcc_pg_5_count'] = mcc_pg_5_count

    ####Punjab PG##############################################################
    logging.info("Checking Punjab PG")

    pb_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://bfuhs.ac.in/MDMS/MDMS.asp',
                              element_to_find='table',
                              attr='class',
                              attr_value='table table-bordered border-success',
                              sub_attr='a',
                              caption='Punjab PG'
                              )

    check_new_notification(old_count=pb_pg_old_count,
                           new_count=pb_pg_count,
                           state='Punjab PG',
                           url='https://bfuhs.ac.in/MDMS/MDMS.asp')

    dict_counts['pb_pg_count'] = pb_pg_count

    ####Rajasthan PG##############################################################

    logging.info("Checking Rajasthan PG")

    rj_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://www.rajpgneet2024.org/',
                              element_to_find='td',
                              attr='style',
                              attr_value='width: 543px; text-align: left;',
                              sub_attr='tr',
                              caption='Rajasthan PG'
                              )

    check_new_notification(old_count=rj_pg_old_count,
                           new_count=rj_pg_count,
                           state='Rajasthan PG',
                           url='https://www.rajpgneet2024.org/')

    dict_counts['rj_pg_count'] = rj_pg_count

    ####Karnataka PG##############################################################
    logging.info("Checking Karnataka PG")

    karnataka_pg_count = web_crawler(paging=False,
                                     paging_count=0,
                                     url_link='https://cetonline.karnataka.gov.in/kea/pget2024',
                                     element_to_find='div',
                                     attr='id',
                                     attr_value='ContentPlaceHolder1_req_accordion',
                                     sub_attr='div',
                                     caption='Karnataka PG',
                                     sub_attr_attr='class',
                                     sub_attr_attr_value='card')

    check_new_notification(old_count=karnataka_pg_old_count,
                           new_count=karnataka_pg_count,
                           state='Karnataka PG',
                           url='https://cetonline.karnataka.gov.in/kea/pget2024')

    dict_counts['karnataka_pg_count'] = karnataka_pg_count

    ####Uttarakhand PG##############################################################
    logging.info("Checking Uttarakhand PG")

    uk_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://meta-secure.com/HNBUMU_MDMS',
                              element_to_find='div',
                              attr='style',
                              attr_value='height: 300px; overflow-y: scroll;',
                              sub_attr='li',
                              caption='Uttarakhand PG')

    check_new_notification(old_count=uk_pg_old_count,
                           new_count=uk_pg_count,
                           state='Uttarakhand PG',
                           url='https://meta-secure.com/HNBUMU_MDMS')

    dict_counts['uk_pg_count'] = uk_pg_count

    ####MP PG##############################################################

    logging.info("Checking MP PG")

    mp_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://dme.mponline.gov.in/portal/services/dmemp/DMEPG/Profile/Instructions.aspx?tab=tab1',
                              element_to_find='div',
                              attr='id',
                              attr_value='tab1',
                              sub_attr='li',
                              caption='MP PG')

    try:
        mp_pg_count = 0
        url = 'https://dme.mponline.gov.in/portal/services/dmemp/DMEPG/Profile/Instructions.aspx?tab=tab1'
        reqs = requests.get(url, verify=False)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'tab1'})
        for each_row in table.find_all('li'):
            mp_pg_count += 1

    except Exception as e:
        logging.info("Exception for MP PG:- " + str(e))
        mp_pg_count = -1

    check_new_notification(old_count=mp_pg_old_count,
                           new_count=mp_pg_count,
                           state='Madhya Pradesh PG',
                           url='https://dme.mponline.gov.in/portal/services/dmemp/DMEPG/Profile/Instructions.aspx?tab=tab1')

    dict_counts['mp_pg_count'] = mp_pg_count

    ####West Bengal PG##############################################################

    logging.info("Checking West Bengal PG Notices")

    wb_1_pg_count = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://wbmcc.nic.in/PGMed/PGMedNotices.aspx',
                                element_to_find='div',
                                attr='class',
                                attr_value='boxdesignCurrentEvents',
                                sub_attr='li',
                                caption='West Bengal PG Notices')

    check_new_notification(old_count=wb_1_pg_old_count,
                           new_count=wb_1_pg_count,
                           state='West Bengal PG Notices',
                           url='https://wbmcc.nic.in/PGMed/PGMedNotices.aspx')

    dict_counts['wb_1_pg_count'] = wb_1_pg_count

    logging.info("Checking West Bengal PG Downloads")

    wb_2_pg_count = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://wbmcc.nic.in/PGMed/pgmedland.aspx',
                                element_to_find='div',
                                attr='class',
                                attr_value='boxdesignImpLinks',
                                sub_attr='li',
                                caption='West Bengal PG Download')

    check_new_notification(old_count=wb_2_pg_old_count,
                           new_count=wb_2_pg_count,
                           state='West Bengal PG Download',
                           url='https://wbmcc.nic.in/PGMed/pgmedland.aspx')

    dict_counts['wb_2_pg_count'] = wb_2_pg_count

    logging.info("Checking West Bengal PG News & Events")

    wb_3_pg_count = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://wbmcc.nic.in/PGMed/pgmedland.aspx',
                                element_to_find='div',
                                attr='class',
                                attr_value='boxdesignNews',
                                sub_attr='li',
                                caption='West Bengal PG News & Events')

    check_new_notification(old_count=wb_3_pg_old_count,
                           new_count=wb_3_pg_count,
                           state='West Bengal PG News & Events',
                           url='https://wbmcc.nic.in/PGMed/pgmedland.aspx')

    dict_counts['wb_3_pg_count'] = wb_3_pg_count

    ####Gujarat PG##############################################################

    logging.info("Checking Gujarat PG")

    gujju_pg_count_1 = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://www.medadmgujarat.org/pg/home.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='post',
                                   sub_attr='div',
                                   caption='Gujarat PG',
                                   sub_attr_attr='style',
                                   sub_attr_attr_value='border: 2px solid purple;')

    gujju_pg_count_2 = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://www.medadmgujarat.org/pg/home.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='post',
                                   sub_attr='div',
                                   caption='Gujarat PG',
                                   sub_attr_attr='style',
                                   sub_attr_attr_value='border: 1px solid purple; margin-top: 5px;')

    gujju_pg_count = gujju_pg_count_1 + gujju_pg_count_2

    check_new_notification(old_count=gujju_pg_old_count,
                           new_count=gujju_pg_count,
                           state='Gujarat PG',
                           url='https://www.medadmgujarat.org/pg/home.aspx')

    dict_counts['gujju_pg_count'] = gujju_pg_count

    ####Maharashtra PG##############################################################

    logging.info("Checking Maharashtra PG")

    try:
        mh_pg_count = 0

        url = 'https://medical2024.mahacet.org/NEET-PGM-2024/login'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'd-lg-flex pos-relative col-lg-4 card pb-20 m-4px'})

        for each_div in table[1].find_all_next('li'):
            mh_pg_count += 1

    except Exception as e:
        logging.info("Exception for Maharashtra PG:- " + str(e))
        mh_pg_count = -1

    check_new_notification(old_count=mh_pg_old_count,
                           new_count=mh_pg_count,
                           state='Maharashtra PG',
                           url='https://medical2024.mahacet.org/NEET-PGM-2024/login')

    dict_counts['mh_pg_count'] = mh_pg_count

    ####GMCH PG #############################################################

    logging.info("Checking GMCH PG")

    gmch_pg_count = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://gmch.gov.in/admission-mdms-2024',
                                element_to_find='div',
                                attr='class',
                                attr_value='node node--type-page node--view-mode-full clearfix',
                                sub_attr='tr',
                                caption='MCH PG')

    check_new_notification(old_count=gmch_pg_old_count,
                           new_count=gmch_pg_count,
                           state='GMCH PG',
                           url='https://gmch.gov.in/admission-mdms-2024')

    dict_counts['gmch_pg_count'] = gmch_pg_count

    ##Kerala#########################################################################

    logging.info("Checking Kerala PG")

    kerala_pg_count = web_crawler(paging=False,
                                  paging_count=0,
                                  url_link='https://cee.kerala.gov.in/pgm2024/notification',
                                  element_to_find='div',
                                  attr='class',
                                  attr_value='container',
                                  sub_attr='div',
                                  caption='Kerala PG',
                                  sub_attr_attr='class',
                                  sub_attr_attr_value='row')

    check_new_notification(old_count=kerala_pg_old_count,
                           new_count=kerala_pg_count,
                           state='Kerala PG',
                           url='https://cee.kerala.gov.in/pgm2024/notification')

    dict_counts['kerala_pg_count'] = kerala_pg_count

    ####Bihar PG##############################################################

    logging.info("Checking Bihar PG")

    bihar_pg_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://bceceboard.bihar.gov.in/PGMACIndex.php',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='SubDiv',
                                 sub_attr='li',
                                 caption='Bihar PG')

    check_new_notification(old_count=bihar_pg_old_count,
                           new_count=bihar_pg_count,
                           state='Bihar PG',
                           url='https://bceceboard.bihar.gov.in/PGMACindex.php#')

    dict_counts['bihar_pg_count'] = bihar_pg_count

    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################

    ####West Bengal Ayush##############################################################

    logging.info("Checking West Bengal Ayush Notices")

    wb_1_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://wbmcc.nic.in/UGAyushW/UGAYUSHNotices.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='boxdesignCurrentEvents',
                                   sub_attr='li',
                                   caption='West Bengal Ayush Notices')

    check_new_notification(old_count=wb_1_ayush_old_count,
                           new_count=wb_1_ayush_count,
                           state='West Bengal AYUSH Notices',
                           url='https://wbmcc.nic.in/UGAyushW/UGAYUSHNotices.aspx')

    dict_counts['wb_1_ayush_count'] = wb_1_ayush_count

    logging.info("Checking West Bengal Ayush Downloads")

    wb_2_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://wbmcc.nic.in/UGAyushW/ugayushland.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='boxdesignImpLinks',
                                   sub_attr='li',
                                   caption='West Bengal Ayush Download')

    check_new_notification(old_count=wb_2_ayush_old_count,
                           new_count=wb_2_ayush_count,
                           state='West Bengal AYUSH Download',
                           url='https://wbmcc.nic.in/UGAyushW/ugayushland.aspx')

    dict_counts['wb_2_ayush_count'] = wb_2_ayush_count

    logging.info("Checking West Bengal Ayush News & Events")

    wb_3_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://wbmcc.nic.in/UGAyushW/ugayushland.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='boxdesignNews',
                                   sub_attr='li',
                                   caption='West Bengal Ayush News & Events')

    check_new_notification(old_count=wb_3_ayush_old_count,
                           new_count=wb_3_ayush_count,
                           state='West Bengal AYUSH News & Events',
                           url='https://wbmcc.nic.in/UGAyushW/ugayushland.aspx')

    dict_counts['wb_3_ayush_count'] = wb_3_ayush_count

    ####UP PG##############################################################

    logging.info("Checking UP Ayush Notices")

    up_ayush_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://upayushcounseling.upsdc.gov.in/Newsandevent1.aspx#',
                                 element_to_find='form',
                                 attr='name',
                                 attr_value='form1',
                                 sub_attr='tr',
                                 caption='UP AYUSH Notices')

    check_new_notification(old_count=up_ayush_old_count,
                           new_count=up_ayush_count,
                           state='UP AYUSH Notices',
                           url='https://upayushcounseling.upsdc.gov.in/Newsandevent1.aspx#')

    dict_counts['up_ayush_count'] = up_ayush_count

    ####Rajasthan AYUSH##############################################################

    logging.info("Checking Rajasthan Ayush Notices")

    rj_ayush_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://rajayushcounselling.com/Notice.aspx',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='container',
                                 sub_attr='a',
                                 caption='Rajasthan AYUSH Notices')

    check_new_notification(old_count=rj_ayush_old_count,
                           new_count=rj_ayush_count,
                           state='Rajasthan AYUSH Notices',
                           url='https://rajayushcounselling.com/Notice.aspx')

    dict_counts['rj_ayush_count'] = rj_ayush_count

    ####Haryana AYUSH##############################################################

    logging.info("Checking Haryana Ayush Notices")

    skau_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://skau.ac.in/U.G_Admission_2025',
                                   element_to_find='section',
                                   attr='class',
                                   attr_value='bg_color_box1',
                                   sub_attr='tr',
                                   caption='Sri Krishna Kurukshetra AYUSH')

    check_new_notification(old_count=skau_ayush_old_count,
                           new_count=skau_ayush_count,
                           state='Sri Krishna KURUKSHETRA AYUSH Notices',
                           url='https://skau.ac.in/U.G_Admission_2025')

    dict_counts['skau_ayush_count'] = skau_ayush_count
    ##################################################################
    ##################################################################

    ############### JEE   ############################################

    logging.info("Checking JEE Main 1 Notices")

    jee_main_ac_count = web_crawler(paging=False,
                                    paging_count=0,
                                    url_link='https://jeemain.nta.ac.in/',
                                    element_to_find='div',
                                    attr='class',
                                    attr_value='news-eve-scroll pr-2',
                                    sub_attr='li',
                                    caption='JEE Mains 1')

    check_new_notification(old_count=jee_main_ac_old_count,
                           new_count=jee_main_ac_count,
                           state='JEE MAINS 1',
                           url='https://jeemain.nta.ac.in/')

    dict_counts['jee_main_ac_count'] = jee_main_ac_count

    logging.info("Checking JEE Main 2 Notices")

    jee_main_nic_count = web_crawler(paging=False,
                                     paging_count=0,
                                     url_link='https://jeemain.nta.nic.in/',
                                     element_to_find='div',
                                     attr='class',
                                     attr_value='vc_tta-panel vc_active',
                                     sub_attr='li',
                                     caption='JEE Mains 2')

    check_new_notification(old_count=jee_main_nic_old_count,
                           new_count=jee_main_nic_count,
                           state='JEE MAINS 2',
                           url='https://jeemain.nta.nic.in/')

    dict_counts['jee_main_nic_count'] = jee_main_nic_count

    logging.info("Checking JEE Main 3 Notices")

    nta_ac_count = web_crawler(paging=False,
                               paging_count=0,
                               url_link='https://nta.ac.in/NoticeBoardArchive',
                               element_to_find='div',
                               attr='class',
                               attr_value='col-md-12 col-sm-12 col-xs-12',
                               sub_attr='tr',
                               caption='JEE Mains 3')

    check_new_notification(old_count=nta_ac_old_count,
                           new_count=nta_ac_count,
                           state='JEE MAINS 3',
                           url='https://nta.ac.in/NoticeBoardArchive')

    dict_counts['nta_ac_count'] = nta_ac_count

    ##################################################################

    logging.info("Checking VITEEE Notices")

    viteee_count = web_crawler(paging=False,
                               paging_count=0,
                               url_link='https://vit.ac.in/all-events',
                               element_to_find='div',
                               attr='class',
                               attr_value='elementor-element elementor-element-aba2809 elementor-align-left elementor-icon-list--layout-traditional elementor-list-item-link-full_width exad-sticky-section-no exad-glass-effect-no elementor-widget elementor-widget-icon-list',
                               sub_attr='li',
                               caption='VITEEE',
                               sub_attr_attr='class',
                               sub_attr_attr_value='elementor-icon-list-item'
                               )

    check_new_notification(old_count=viteee_old_count,
                           new_count=viteee_count,
                           state='VITEEE',
                           url='https://vit.ac.in/all-events')

    dict_counts['viteee_count'] = viteee_count

    ########ODISHA PG##########################################################

    logging.info("Checking ODISHA PG Notices")

    odisha_pg_count = web_crawler(paging=False,
                                  paging_count=0,
                                  url_link='https://dmetodisha.in/PGMCC_Static/MEDICAL%20COUNSELLING%201/Notifications.html',
                                  element_to_find='table',
                                  attr='class',
                                  attr_value='border_bottom_dotted',
                                  sub_attr='td',
                                  caption='Odisha PG',
                                  sub_attr_attr='class',
                                  sub_attr_attr_value='Step_font')

    check_new_notification(old_count=odisha_pg_old_count,
                           new_count=odisha_pg_count,
                           state='ODISHA PG',
                           url='https://dmetodisha.in/PGMCC_Static/MEDICAL%20COUNSELLING%201/Notifications.html')

    dict_counts['odisha_pg_count'] = odisha_pg_count

    ##################################################################

    logging.info("Checking AIIMS EXAMS Notices")

    aiims_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://aiimsexams.ac.in/',
                              element_to_find='div',
                              attr='class',
                              attr_value='faq',
                              sub_attr='li',
                              caption='AIIMS EXAMS')

    check_new_notification(old_count=aiims_old_count,
                           new_count=aiims_count,
                           state='AIIMS EXAMS',
                           url='https://aiimsexams.ac.in/')

    dict_counts['aiims_count'] = aiims_count

    #####################################################################

    logging.info("Checking NBEMS")
    try:
        nbems_count = 0

        for i in range(1, 100):
            url = 'https://www.natboard.edu.in/allnotice.php?page={0}&s='.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('table', attrs={'class': 'customers'})
            if table is not None:
                for each_row in table.find_all('tr'):
                    nbems_count += 1

    except Exception as e:
        logging.info("Exception for NBEMS:- " + str(e) + "    " + str(url))
        nbems_count = -1

    check_new_notification(old_count=nbems_old_count,
                           new_count=nbems_count,
                           state='NBEMS',
                           url='https://www.natboard.edu.in/allnotice.php')

    dict_counts['nbems_count'] = nbems_count

    ############################################################################

    logging.info("Checking JEE Advanced Notices")

    jee_adv_count = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://jeeadv.ac.in/',
                                element_to_find='div',
                                attr='class',
                                attr_value='display-6 fs-6 text-start border rounded-1 border-success mt-3 p-2',
                                sub_attr='div',
                                caption='JEE Advanced')

    check_new_notification(old_count=jee_adv_old_count,
                           new_count=jee_adv_count,
                           state='JEE Advanced',
                           url='https://jeeadv.ac.in/')

    dict_counts['jee_adv_count'] = jee_adv_count

    #############################################################################
    logging.info("Checking Goa Notices")

    try:

        url = 'https://dte.goa.gov.in'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'views-field views-field-title'})

        new_goa_text = table.text

        if iter == 0:
            old_goa_text = new_goa_text

        if new_goa_text != old_goa_text:
            goa_count = goa_old_count + 1
        else:
            goa_count = goa_old_count

        old_goa_text = new_goa_text

    except Exception as e:
        logging.info("Exception for Goa:- " + str(e))
        goa_count = -1

    check_new_notification(old_count=goa_old_count,
                           new_count=goa_count,
                           state='GOA',
                           url='https://dte.goa.gov.in')

    dict_counts['goa_count'] = goa_count

    ##############################################################################

    logging.info("Checking Sikkim Notices")

    try:
        sikkim_count = 0
        url = 'https://smu.edu.in/smu/miscellaneous/smu-notice-board0.html'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table')
        for each_row in table.find_all('td'):
            sikkim_count += 1
    except Exception as e:
        logging.info("Exception for Sikkim:- " + str(e))
        sikkim_count = -1

    check_new_notification(old_count=sikkim_old_count,
                           new_count=sikkim_count,
                           state='SIKKIM',
                           url='https://smu.edu.in/smu/miscellaneous/smu-notice-board0.html')

    dict_counts['sikkim_count'] = sikkim_count
    ##############################################################################
    logging.info("Checking JNIMS Manipur Notices")

    try:
        jnims_count = 0
        url = 'https://jnims.nic.in/notification/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'entry-content'})
        for each_row in table.find_all('article'):
            jnims_count += 1
    except Exception as e:
        logging.info("Exception for JNIMS:- " + str(e))
        jnims_count = -1

    check_new_notification(old_count=jnims_old_count,
                           new_count=jnims_count,
                           state='JNIMS Manipur',
                           url='https://jnims.nic.in/notification/')

    dict_counts['jnims_count'] = jnims_count

    ##############################################################################

    logging.info("Checking Jharkhand PG")
    try:
        jh_pg_count = 0

        url = 'https://neetpg.jceceb.org.in/Public/Home#parentHorizontalTab2'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('ul', attrs={'class': 'notification-list date-list'})
        for each_row in table.find_all('li'):
            jh_pg_count += 1


    except Exception as e:

        logging.info("Exception for Jharkhand PG:- " + str(e))
        jh_pg_count = -1

    check_new_notification(old_count=jh_pg_old_count,
                           new_count=jh_pg_count,
                           state='Jharkhand PG',
                           url='https://neetpg.jceceb.org.in/Public/Home#parentHorizontalTab2')

    dict_counts['jh_pg_count'] = jh_pg_count

    ##############################################################################
    logging.info("Checking DME ASSAM")

    try:
        dme_assam_count = 0

        url = 'https://dme.assam.gov.in/latest/admission-notice-ugpgothersnew'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'panel-pane pane-views pane-latest'})
        for each_row in table.find_all('div', attrs={'class': 'field-content'}):
            for each_row_further in each_row.find_all('tr'):
                dme_assam_count += 1

    except Exception as e:
        print("Exception for DME ASSAM:- " + str(e))
        dme_assam_count = -1

    check_new_notification(old_count=dme_assam_old_count,
                           new_count=dme_assam_count,
                           state='DME ASSAM',
                           url='https://dme.assam.gov.in/latest/admission-notice-ugpgothersnew')

    dict_counts['dme_assam_count'] = dme_assam_count

    ##############################################################################
    logging.info("Checking DNB KERALA")

    try:
        dnb_kerala_count = 0

        url = 'https://cee.kerala.gov.in/dnbmbbs2024/notification'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'card border-light mb-3'})

        for each_div in table.find_all('div', attrs={'class': 'col-sm-10'}):
            dnb_kerala_count += 1

    except Exception as e:
        logging.info("Exception for DNB Kerala:- " + str(e))
        dnb_kerala_count = -1

    check_new_notification(old_count=dnb_kerala_old_count,
                           new_count=dnb_kerala_count,
                           state='DNB KERALA',
                           url='https://cee.kerala.gov.in/dnbmbbs2024/notification')

    dict_counts['dnb_kerala_count'] = dnb_kerala_count

    ####AACCC AYUSH Current Events##############################################################

    logging.info("Checking AACCC AYUSH Current Events UG")
    try:
        aaccc_current_events_ayush_ug_count = 0

        for i in range(1, 10):
            url = 'https://aaccc.gov.in/current-events-ug/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'data-table-container'})
            for each_row in table.find_all('tr'):
                aaccc_current_events_ayush_ug_count += 1

    except Exception as e:
        logging.info("Exception for AACCC AYUSH Current Events UG:- " + str(e))
        aaccc_current_events_ayush_ug_count = -1

    check_new_notification(old_count=aaccc_current_events_ayush_ug_old_count,
                           new_count=aaccc_current_events_ayush_ug_count,
                           state='AACCC AYUSH Current Events UG',
                           url='https://aaccc.gov.in/current-events-ug')

    dict_counts['aaccc_current_events_ayush_ug_count'] = aaccc_current_events_ayush_ug_count

    ####AACCC AYUSH News Events##############################################################

    logging.info("Checking AACCC AYUSH News Events UG")
    try:
        aaccc_news_events_ayush_ug_count = 0

        for i in range(1, 10):
            url = 'https://aaccc.gov.in/news-events-ug/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'data-table-container'})
            for each_row in table.find_all('tr'):
                aaccc_news_events_ayush_ug_count += 1

    except Exception as e:
        logging.info("Exception for AACCC AYUSH News Events UG:- " + str(e))
        aaccc_news_events_ayush_ug_count = -1

    check_new_notification(old_count=aaccc_news_events_ayush_ug_old_count,
                           new_count=aaccc_news_events_ayush_ug_count,
                           state='AACCC AYUSH News Events UG',
                           url='https://aaccc.gov.in/news-events-ug')

    dict_counts['aaccc_news_events_ayush_ug_count'] = aaccc_news_events_ayush_ug_count

    ################IPU AYUSH##############################################################

    ipu_ayush_count = 0
    try:
        for i in range(1, 10):
            url = 'https://ipu.admissions.nic.in/cutt-off-2024-25/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'data-table-container'})

            for each_row in table.find_all('tr'):
                ipu_ayush_count += 1

    except Exception as e:
        logging.info("Exception for IPU AYUSH:- " + str(e))
        ipu_ayush_count = -1

    check_new_notification(old_count=ipu_ayush_old_count,
                           new_count=ipu_ayush_count,
                           state='IPU AYUSH',
                           url='https://ipu.admissions.nic.in/cutt-off-2024-25')

    dict_counts['ipu_ayush_count'] = ipu_ayush_count

    ##############Uttarakhand Ayush ################################################################

    uttarakhand_ayush_count = 0
    try:
        url = 'https://octopod.co.in/uaucc/counselling/ec2648895c9864dce4df875968f228ef'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'col-lg-3 col-md-6'})

        for each_row in table.find_all('div', attrs={'class': 'd-flex bg-soft-dark align-items-center mt-3'}):
            uttarakhand_ayush_count += 1

    except Exception as e:
        logging.info("Exception for Uttarakhand Ayush:- " + str(e))
        uttarakhand_ayush_count = -1

    check_new_notification(old_count=uttarakhand_ayush_old_count,
                           new_count=uttarakhand_ayush_count,
                           state='Uttarakhand Ayush',
                           url='https://octopod.co.in/uaucc/counselling/ec2648895c9864dce4df875968f228ef')

    dict_counts['uttarakhand_ayush_count'] = uttarakhand_ayush_count

    ####FMSC BHMS##############################################################
    fmsc_bhms_count = 0
    try:
        url = 'https://fmsc.du.ac.in/homoeopathic.htm'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('p')

        for each in table:
            if each.text == 'BHMS Course 2024-25':
                fmsc_bhms_count = 0
            if each.text == 'BHMS Course 2023-24':
                break

            fmsc_bhms_count += 1


    except Exception as e:
        logging.info("Exception for FMSC BHMS:- " + str(e))
        fmsc_bhms_count = -1

    check_new_notification(old_count=fmsc_bhms_old_count,
                           new_count=fmsc_bhms_count,
                           state='FMSC BHMS',
                           url='https://fmsc.du.ac.in/homoeopathic.htm')

    dict_counts['fmsc_bhms_count'] = fmsc_bhms_count

    ####FMSC BAMS BUMS##############################################################
    fmsc_bams_bums_count = 0
    try:
        url = 'https://fmsc.du.ac.in/unani.htm'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('p')

        for each in table:
            if each.text == 'BAMS and BUMS Course 2024-25':
                fmsc_bhms_count = 0
            if each.text == 'BAMS and BUMS Course 2023-24':
                break

            fmsc_bams_bums_count += 1


    except Exception as e:
        logging.info("Exception for FMSC BAMS BUMS:- " + str(e))
        fmsc_bams_bums_count = -1

    check_new_notification(old_count=fmsc_bams_bums_old_count,
                           new_count=fmsc_bams_bums_count,
                           state='FMSC BAMS BUMS',
                           url='https://fmsc.du.ac.in/unani.htm')

    dict_counts['fmsc_bams_bums_count'] = fmsc_bams_bums_count

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################

    try:
        old_mcc_list = pd.read_csv("mcc_notices.csv", encoding='utf-8')['Notices'].tolist()
        old_mcc_ug_list = pd.read_csv("mcc_ug_notices.csv", encoding='utf-8')['Notices'].tolist()
        old_mcc_mds_list = pd.read_csv("mcc_mds_notices.csv", encoding='utf-8')['Notices'].tolist()
        old_mcc_pg_list = pd.read_csv("mcc_pg_notices.csv", encoding='utf-8')['Notices'].tolist()
        old_mcc_ss_list = pd.read_csv("mcc_ss_notices.csv", encoding='utf-8')['Notices'].tolist()

        new_mcc_list = []
        url = 'https://mcc.nic.in/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'with-urlchange'})

        for each in table:
            new_mcc_list.append((each.get_text().strip()))

        for index, each_item in enumerate(new_mcc_list):
            if each_item not in old_mcc_list:
                filename = r'.\new_notices\{0}_'.format("mcc") + str(index) + "_" + str(
                    datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"
                caption_msg = "** New Notification Alert ** in ** MCC Flash News ** \n{0}".format(url)

                with open(filename, "w") as f:
                    f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format(caption_msg))

        old_mcc_list = new_mcc_list

        df = pd.DataFrame(new_mcc_list, columns=['Notices'])
        df.to_csv('mcc_notices.csv', index=False, encoding='utf-8')

        ################################################

        new_mcc_ug_list = []
        url = "https://mcc.nic.in/ug-medical-counselling/"
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'with-urlchange'})

        for each in table:
            new_mcc_ug_list.append((each.get_text().strip()))

        for index, each_item in enumerate(new_mcc_ug_list):
            if each_item not in old_mcc_ug_list:
                filename = r'.\new_notices\{0}_'.format("mcc_ug") + str(index) + "_" + str(
                    datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"
                caption_msg = "** New Notification Alert ** in ** MCC NEET UG Flash News ** \n{0}".format(url)

                with open(filename, "w") as f:
                    f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format(caption_msg))

        old_mcc_ug_list = new_mcc_ug_list

        df = pd.DataFrame(new_mcc_ug_list, columns=['Notices'])
        df.to_csv('mcc_ug_notices.csv', index=False, encoding='utf-8')

        ################################################

        new_mcc_mds_list = []
        url = "https://mcc.nic.in/mds-counselling/"
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'with-urlchange'})

        for each in table:
            new_mcc_mds_list.append((each.get_text().strip()))

        for index, each_item in enumerate(new_mcc_mds_list):
            if each_item not in old_mcc_mds_list:
                filename = r'.\new_notices\{0}_'.format("mcc_mds") + str(index) + "_" + str(
                    datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"
                caption_msg = "** New Notification Alert ** in ** MCC MDS Flash News ** \n{0}".format(url)

                with open(filename, "w") as f:
                    f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format(caption_msg))

        old_mcc_mds_list = new_mcc_mds_list

        df = pd.DataFrame(new_mcc_mds_list, columns=['Notices'])
        df.to_csv('mcc_mds_notices.csv', index=False, encoding='utf-8')

        ################################################

        new_mcc_pg_list = []
        url = "https://mcc.nic.in/pg-medical-counselling/"
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'with-urlchange'})

        for each in table:
            new_mcc_pg_list.append((each.get_text().strip()))

        for index, each_item in enumerate(new_mcc_pg_list):
            if each_item not in old_mcc_pg_list:
                filename = r'.\new_notices\{0}_'.format("mcc_pg") + str(index) + "_" + str(
                    datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"
                caption_msg = "** New Notification Alert ** in ** MCC NEET PG Flash News ** \n{0}".format(url)

                with open(filename, "w") as f:
                    f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format(caption_msg))

        old_mcc_pg_list = new_mcc_pg_list

        df = pd.DataFrame(new_mcc_pg_list, columns=['Notices'])
        df.to_csv('mcc_pg_notices.csv', index=False, encoding='utf-8')

        ################################################

        new_mcc_ss_list = []
        url = "https://mcc.nic.in/super-speciality-counselling/"
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'with-urlchange'})

        for each in table:
            new_mcc_ss_list.append((each.get_text().strip()))

        for index, each_item in enumerate(new_mcc_ss_list):
            if each_item not in old_mcc_ss_list:
                filename = r'.\new_notices\{0}_'.format("mcc_ss") + str(index) + "_" + str(
                    datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"
                caption_msg = "** New Notification Alert ** in ** MCC NEET SS Flash News ** \n{0}".format(url)

                with open(filename, "w") as f:
                    f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format(caption_msg))

        old_mcc_ss_list = new_mcc_ss_list

        df = pd.DataFrame(new_mcc_ss_list, columns=['Notices'])
        df.to_csv('mcc_ss_notices.csv', index=False, encoding='utf-8')


    except Exception as e:
        filename = r'.\new_notices\{0}_'.format("mcc_error") + str(index) + "_" + str(
            datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"

        caption_msg = "** Error Notification Alert ** in ** MCC Flash Notices **\n. Exception - {0}".format(e)

        with open(filename, "w") as f:
            f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format(caption_msg))

    ################################################################################
    ################################################################################
    ################################################################################

    ################################################################################
    ################################################################################
    ################################################################################

    new_df = pd.DataFrame(dict_counts.items(), columns=['State', 'Counts'])
    new_df.to_csv("neet_notifications_count.csv", index=False)

    iter += 1
