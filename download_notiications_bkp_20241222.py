from bs4 import BeautifulSoup
import requests, re
import pandas as pd
import pywhatkit
import time
import os


def web_crawler(paging, paging_count, url_link, element_to_find, attr, attr_value, sub_attr, caption, sub_attr_attr = '', sub_attr_attr_value=''):
    count = 0

    try:
        if paging:
            for i in range(1, paging_count):
                url = url_link.format(i)
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


def send_whatsapp(caption_msg, state):
    print("New Notiication Found in {0}".format(state))
    # pywhatkit.sendwhats_image(receiver='+918377837545', \
    #                           img_path=r"Vidya Saarthi Edu-Specialist Logo.jpeg", \
    #                           caption=caption_msg, tab_close=True, wait_time=40, close_time=5)

    pywhatkit.sendwhatmsg_to_group_instantly(group_id='G9nAAne3vq5EhGQEAfe3bA',
                                             message=caption_msg,
                                             tab_close=True, wait_time=40, close_time=5)


def check_new_notification(old_count, new_count, state, url):
    if old_count == -1 or new_count == -1:
        print("Issue in Reading notice for {0} - {1}".format(state, url))
        caption_msg = "*Issue in Reading notice for {0}* - {1}".format(state, url)

        pywhatkit.sendwhats_image(receiver='+918377837545',
                                  img_path=r"Vidya Saarthi Edu-Specialist Logo.jpeg",
                                  caption=caption_msg, tab_close=True, wait_time=40, close_time=5)



        return

    if old_count != new_count and new_count > old_count:
        caption_msg = "*New Notification Alert* in *{0}*\n{1}\n*Number Of Notices* : *{2}*\n".format(
            state,url,new_count - old_count)
        send_whatsapp(caption_msg, state)

while 1:
    dict_counts = {}

    ##Kerala#########################################################################
    try:
        print("Checking Kerala")
        kerala_count = 0
        for i in range(1, 20):

            url = 'https://cee.kerala.gov.in/keam2024/notification?page=' + str(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'class': 'card-body'})

            for div in table.find_all('div', attrs={'class': 'row'}):
                kerala_count = kerala_count + 1

    except Exception as e:
        print("Exception for Kerala:- " + str(e))
        kerala_count = -1

    dict_counts['kerala_count'] = kerala_count

    ##Tamil Nadu################################################################
    print("Checking Tamil Nadu")
    try:
        tamil_nadu_count = 0
        url = 'https://tnmedicalselection.net/Notification.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'col-sm-8 box_inner'})
        # rows=[]
        #

        for div in table.find_all('p'):
            #     print('https://tnmedicalselection.net/' + div.get("href"))
            tamil_nadu_count = tamil_nadu_count + 1


    except Exception as e:
        print("Exception for Tamil Nadu:- " + str(e))
        tamil_nadu_count = -1

    dict_counts['tamil_nadu_count'] = tamil_nadu_count

    ###Haryana 1###############################################################
    print("Checking Haryana 1")

    try:
        haryana_1_count = 0
        url = 'https://uhsrugcounselling.com/Notice.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'container'})

        for each_row in table.find_all('div', attrs={'class': 'row'}):
            haryana_1_count += 1

    except Exception as e:
        print("Exception for Haryana 1:- " + str(e))
        haryana_1_count = -1

    dict_counts['haryana_1_count'] = haryana_1_count

    ###Haryana 2###############################################################

    print("Checking Haryana 2")
    try:
        haryana_2_count = 0
        url = 'https://uhsr.ac.in/detail.aspx?artid=79&menuid=12'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table', attrs={'style': 'border-collapse: collapse; width: 100.561%; height: 27165px;'})

        # print(table)
        date_element = []
        text_element = []
        href_element = []

        for each_row in table.find_all('tr'):
            haryana_2_count += 1

    except Exception as e:
        print("Exception for Haryana 2:- " + str(e))
        haryana_2_count = -1

    dict_counts['haryana_2_count'] = haryana_2_count

    ####Karnataka##############################################################
    print("Checking Karnataka")
    try:
        karnataka_count = 0
        url = 'https://cetonline.karnataka.gov.in/kea/ugneet24'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'ContentPlaceHolder1_req_accordion'})

        for each_row in table.find_all('div', attrs={'class': 'card'}):
            karnataka_count += 1

    except Exception as e:
        print("Exception for Karnataka:- " + str(e))
        karnataka_count = -1

    dict_counts['karnataka_count'] = karnataka_count

    #################################################################
    ####Himachal Pradesh##############################################################
    print("Checking Himachal Pradesh")
    try:
        hp_count = 0

        for i in range(1, 200):
            url = 'https://amruhp.ac.in/notices/page/{0}/'.format(i)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            table = soup.find('div', attrs={'id': 'et-main-area'})
            for each_row in table.find_all('a', attrs={'class': 'text-white'}):
                hp_count += 1

    except Exception as e:
        print("Exception for HP:- " + str(e))
        hp_count = -1

    dict_counts['hp_count'] = hp_count

    #################################################################

    ####Uttarakhand##############################################################
    print("Checking Uttarakhand")
    try:
        uk_count = 0

        url = 'https://meta-secure.com/HNBUMU_NEETUG'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'style': 'text-align: left; padding-left: 5px;'})
        for each_row in table.find_all('li'):
            uk_count += 1

    except Exception as e:
        print("Exception for UK:- " + str(e))
        uk_count = -1

    dict_counts['uk_count'] = uk_count

    ####Punjab##############################################################
    print("Checking Punjab")
    try:
        pb_count = 0

        url = 'https://bfuhs.ac.in/MBBS_BDS/MBBSBDS.asp'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table', attrs={'class': 'table table-bordered border-success'})
        for each_row in table.find_all('a'):
            pb_count += 1

    except Exception as e:
        print("Exception for Punjab:- " + str(e))
        pb_count = -1

    dict_counts['pb_count'] = pb_count

    #################################################################
    ####UP##############################################################
    print("Checking UP")

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
        print("Exception for UP:- " + str(e))
        up_count = -1

    dict_counts['up_count'] = up_count

    ####J & K##############################################################

    print("Checking J & K")
    try:
        jk_count = 0

        url = 'https://www.jkbopee.gov.in/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('table', attrs={'class': 'table table-bordered table-striped table-responsive'})
        for each_row in table.find_all('tr'):
            jk_count += 1

    except Exception as e:
        print("Exception for J & K:- " + str(e))
        jk_count = -1

    dict_counts['jk_count'] = jk_count

    ####Rajasthan##############################################################

    print("Checking Rajasthan")
    try:

        rajasthan_count = 0

        url = 'https://www.rajugneet2024.org/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('td', attrs={'style': 'width: 543px; text-align: left;'})
        for each_row in table.find_all('tr'):
            rajasthan_count += 1

    except Exception as e:
        print("Exception for Rajasthan:- " + str(e))
        rajasthan_count = -1

    dict_counts['rajasthan_count'] = rajasthan_count

    ####MP##############################################################

    print("Checking MP")

    try:
        mp_count = 0
        url = 'https://dme.mponline.gov.in/Portal/Services/DMEMP/DMEUG/Profile/Instructions.aspx?tab=tab1'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'tab1'})
        for each_row in table.find_all('li'):
            mp_count += 1
    except Exception as e:
        print("Exception for MP:- " + str(e))
        mp_count = -1

    dict_counts['mp_count'] = mp_count

    ####Chhatisgarh##############################################################

    print("Checking Chattisgah")
    try:
        cg_count = 0

        url = 'https://cgdme.in/Notice_24.php'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'text-widget2'})
        for each_row in table.find_all('tr'):
            cg_count += 1

    except Exception as e:
        print("Exception for Chhattisgarh:- " + str(e))
        cg_count = -1

    dict_counts['cg_count'] = cg_count

    ####Jharkhand##############################################################

    print("Checking Jharkhand")
    try:
        jh_count = 0

        url = 'https://jceceb.jharkhand.gov.in/Links/counselling.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'page_inner'})
        for each_row in table.find_all('tr'):
            jh_count += 1

    except Exception as e:
        print("Exception for Jharkhand:- " + str(e))
        jh_count = -1

    dict_counts['jh_count'] = jh_count

    ####West Bengal##############################################################

    print("Checking West Bengal 1")
    try:
        wb_count1 = 0

        url = 'https://wbmcc.nic.in/UGMedDen/UGMedDenNotices.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'boxdesignCurrentEvents'})
        for each_row in table.find_all('li'):
            wb_count1 += 1

    except Exception as e:
        print("Exception for West Bengal 1:- " + str(e))
        wb_count1 = -1

    dict_counts['wb_count1'] = wb_count1

    print("Checking West Bengal 2")
    try:
        wb_count2 = 0

        url = 'https://wbmcc.nic.in/UGMedDen/ugmeddenland.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'boxdesignImpLinks'})
        for each_row in table.find_all('li'):
            wb_count2 += 1

    except Exception as e:
        print("Exception for West Bengal 2:- " + str(e))
        wb_count2 = -1

    dict_counts['wb_count2'] = wb_count2

    print("Checking West Bengal 3")
    try:

        wb_count3 = 0

        url = 'https://wbmcc.nic.in/UGMedDen/UGMedDenNewsEvents.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'boxdesignCurrentEvents'})
        for each_row in table.find_all('li'):
            wb_count3 += 1

    except Exception as e:
        print("Exception for West Bengal 3:- " + str(e))
        wb_count3 = -1

    dict_counts['wb_count3'] = wb_count3

    ####MCC##############################################################

    print("Checking MCC 1")
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
        print("Exception for MCC 1:- " + str(e))
        mcc1_count = -1

    dict_counts['mcc1_count'] = mcc1_count

    print("Checking MCC 2")
    try:
        mcc2_count = 0

        url = 'https://mcc.nic.in/eservices-schedule-ug/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_row wpb_row vc_row-fluid'})

        for each_row in table.find_all('tr'):
            mcc2_count += 1

    except Exception as e:
        print("Exception for MCC 2:- " + str(e))
        mcc2_count = -1

    dict_counts['mcc2_count'] = mcc2_count

    print("Checking MCC 3")
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
        print("Exception for MCC 3:- " + str(e))
        mcc3_count = -1

    dict_counts['mcc3_count'] = mcc3_count

    print("Checking MCC 4")
    try:
        mcc4_count = 0

        url = 'https://mcc.nic.in/ug-medical-counselling/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_column-inner vc_custom_1647862263119'})

        for each_row in table.find_all('li'):
            mcc4_count += 1

    except Exception as e:
        print("Exception for MCC 4:- " + str(e))
        mcc4_count = -1

    dict_counts['mcc4_count'] = mcc4_count

    print("Checking MCC 5")
    try:
        mcc5_count = 0

        url = 'https://mcc.nic.in/ug-medical-counselling/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_column-inner vc_custom_1647861778410'})

        for each_row in table.find_all('li'):
            mcc5_count += 1

    except Exception as e:
        print("Exception for MCC 5:- " + str(e))
        mcc5_count = -1

    dict_counts['mcc5_count'] = mcc5_count

    ####Gujarat##############################################################

    print("Checking Gujarat")
    try:
        gujju_count_1 = 0

        url = 'https://www.medadmgujarat.org/ug/home.aspx'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'post'})

        for each_row in table.find_all('div', attrs={'style': 'border: 2px solid purple;'}):
            gujju_count_1 += 1

    except Exception as e:
        print("Exception for Gujarat:- " + str(e))
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
    dict_counts['gujju_count'] = gujju_count

    ####Maharashtra##############################################################

    print("Checking Maharashtra")
    try:
        mh_count = 0

        url = 'https://medical2024.mahacet.org/NEET-UG-2024/login'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'd-lg-flex pos-relative col-lg-4 card pb-20 m-4px'})

        for each_div in table[1].find_all_next('li'):
            mh_count += 1

    except Exception as e:
        print("Exception for Maharashtra:- " + str(e))
        mh_count = -1

    dict_counts['mh_count'] = mh_count

    ####Assam##############################################################

    print("Checking Assam")
    try:
        assam_count = 0

        url = 'https://dme.assam.gov.in/latest/admission-notice-ugpg-and-others'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'region region-content'})

        for each_div in table.find_all('tr'):
            assam_count += 1

    except Exception as e:
        print("Exception for Assam:- " + str(e))
        assam_count = -1

    dict_counts['assam_count'] = assam_count

    ####Telangana##############################################################

    print("Checking Telangana")
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
        print("Exception for Telangana:- " + str(e))
        telangana_count = -1

    dict_counts['telangana_count'] = telangana_count

    ####Telangana##############################################################

    print("Checking Andhra Pradesh")
    try:
        ap_count = 0

        url = 'https://drntr.uhsap.in/index/index.html'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'vc_tta-panels-container'})

        for each_div in table.find_all('li'):
            ap_count += 1

    except Exception as e:
        print("Exception for Andhra Pradesh:- " + str(e))
        ap_count = -1

    dict_counts['ap_count'] = ap_count

    ####GMCH##############################################################

    print("Checking GMCH")
    try:
        gmch_count = 0

        url = 'https://gmch.gov.in/centralized-admission-prospectus-mbbsbdsbhms-courses-session-2024'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'node node--type-page node--view-mode-full clearfix'})

        for each_div in table.find_all('tr'):
            gmch_count += 1

    except Exception as e:
        print("Exception for GMCH:- " + str(e))
        gmch_count = -1

    dict_counts['gmch_count'] = gmch_count
    ####Puducherry##############################################################

    print("Checking Puducherry")
    try:
        pudu_count = 0

        url = 'https://www.centacpuducherry.in/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'id': 'nav-overall_news-home'})

        for each_div in table.find_all('div', attrs={'class': 'content text-danger font-weight-bold text-justify'}):
            pudu_count += 1

    except Exception as e:
        print("Exception for Puducherry:- " + str(e))
        pudu_count = -1

    dict_counts['pudu_count'] = pudu_count

    ####Bihar##############################################################

    print("Checking Bihar UG")
    try:
        bihar_count = 0

        url = 'https://bceceboard.bihar.gov.in/UGMACIndex.php'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'SubDiv'})

        for each_div in table.find_all('li'):
            bihar_count += 1

    except Exception as e:
        print("Exception for Bihar UG:- " + str(e))
        bihar_count = -1

    dict_counts['bihar_count'] = bihar_count

    ####Odisha##############################################################

    print("Checking Odisha")
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
        print("Exception for Odisha:- " + str(e))
        odisha_count = -1

    dict_counts['odisha_count'] = odisha_count

    ####Manipur##############################################################

    print("Checking Manipur")
    try:
        manipur_count = 0
        url = 'https://manipurhealthdirectorate.mn.gov.in/notifications'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'col-md-8'})

        for each_row in table.find_all('li'):
            manipur_count += 1

    except Exception as e:
        print("Exception for Manipur:- " + str(e))
        manipur_count = -1

    dict_counts['manipur_count'] = manipur_count

    ####Meghalaya##############################################################

    print("Checking Meghalaya")
    try:
        meghalaya_count = 0
        url = 'https://meghealth.gov.in/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'col-lg-3 col-md-3 col-sm-6'})

        for each_row in table.find_all('li'):
            meghalaya_count += 1

    except Exception as e:
        print("Exception for Meghalaya:- " + str(e))
        meghalaya_count = -1

    dict_counts['meghalaya_count'] = meghalaya_count

    ####Nagaland##############################################################

    print("Checking Nagaland")
    try:
        nagaland_count = 0
        url = 'https://dte.nagaland.gov.in/index.php/dept-2/'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find('div', attrs={'class': 'entry themeform'})

        for each_row in table.find_all('tr'):
            nagaland_count += 1

    except Exception as e:
        print("Exception for Nagaland:- " + str(e))
        nagaland_count = -1

    dict_counts['nagaland_count'] = nagaland_count

    ####IPU 1 ##############################################################

    print("Checking IPU News")
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
        print("Exception for IPU News:- " + str(e))
        ipu_1_count = -1

    dict_counts['ipu_1_count'] = ipu_1_count

    ####IPU 2 ##############################################################

    print("Checking IPU Current Events")
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
        print("Exception for IPU Current Events:- " + str(e))
        ipu_2_count = -1

    dict_counts['ipu_2_count'] = ipu_2_count

    ####Tripura ##############################################################

    print("Checking Tripura")
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
        print("Exception for Tripura:- " + str(e))
        tripura_count = -1

    dict_counts['tripura_count'] = tripura_count

    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################

    print("Checking MCC PG Current Events ")

    mcc_pg_1_count = web_crawler(paging=True,
                                 paging_count=10,
                                 url_link='https://mcc.nic.in/current-events-pg/page/{0}/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='wpb_column vc_column_container vc_col-sm-12',
                                 sub_attr='tr',
                                 caption='MCC PG Current Events'
                                 )

    dict_counts['mcc_pg_1_count'] = mcc_pg_1_count

    print("Checking MCC eService Schedule")

    mcc_pg_2_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://mcc.nic.in/eservices-schedule-pg/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='vc_row wpb_row vc_row-fluid',
                                 sub_attr='tr',
                                 caption='MCC PG eService Schedule'
                                 )

    dict_counts['mcc_pg_2_count'] = mcc_pg_2_count

    print("Checking MCC PG News Events")

    mcc_pg_3_count = web_crawler(paging=True,
                                 paging_count=10,
                                 url_link='https://mcc.nic.in/news-events-pg/page/{0}/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='wpb_column vc_column_container vc_col-sm-12',
                                 sub_attr='tr',
                                 caption='MCC PG News Events'
                                 )

    dict_counts['mcc_pg_3_count'] = mcc_pg_3_count

    print("Checking MCC PG Candidate Board")

    mcc_pg_4_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://mcc.nic.in/pg-medical-counselling/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='vc_column-inner vc_custom_1647862263119',
                                 sub_attr='li',
                                 caption='MCC PG Candidate Board'
                                 )

    dict_counts['mcc_pg_4_count'] = mcc_pg_4_count

    print("Checking MCC PG Important Link")

    mcc_pg_5_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://mcc.nic.in/pg-medical-counselling/',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='vc_column-inner vc_custom_1647861778410',
                                 sub_attr='li',
                                 caption='MCC PG Important Link'
                                 )

    dict_counts['mcc_pg_5_count'] = mcc_pg_5_count

    ####Punjab PG##############################################################
    print("Checking Punjab PG")

    pb_pg_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://bfuhs.ac.in/MDMS/MDMS.asp',
                                 element_to_find='table',
                                 attr='class',
                                 attr_value='table table-bordered border-success',
                                 sub_attr='a',
                                 caption='Punjab PG'
                                 )

    dict_counts['pb_pg_count'] = pb_pg_count

    ####Rajasthan PG##############################################################

    print("Checking Rajasthan PG")

    rj_pg_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://www.rajpgneet2024.org/',
                                 element_to_find='td',
                                 attr='style',
                                 attr_value='width: 543px; text-align: left;',
                                 sub_attr='tr',
                                 caption='Rajasthan PG'
                                 )

    dict_counts['rj_pg_count'] = rj_pg_count

    ####Karnataka PG##############################################################
    print("Checking Karnataka PG")

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


    dict_counts['karnataka_pg_count'] = karnataka_pg_count

    ####Uttarakhand PG##############################################################
    print("Checking Uttarakhand PG")

    uk_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://meta-secure.com/HNBUMU_NEETPG',
                              element_to_find='div',
                              attr='style',
                              attr_value='height: 300px; overflow-y: scroll;',
                              sub_attr='li',
                              caption='Uttarakhand PG')

    dict_counts['uk_pg_count'] = uk_pg_count


    ####MP PG##############################################################

    print("Checking MP PG")

    mp_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://dme.mponline.gov.in/portal/services/dmemp/DMEPG/Profile/Instructions.aspx?tab=tab1',
                              element_to_find='div',
                              attr='id',
                              attr_value='tab1',
                              sub_attr='li',
                              caption='MP PG')


    dict_counts['mp_pg_count'] = mp_pg_count

    ####West Bengal PG##############################################################

    print("Checking West Bengal PG Notices")

    wb_1_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://wbmcc.nic.in/PGMed/PGMedNotices.aspx',
                              element_to_find='div',
                              attr='class',
                              attr_value='boxdesignCurrentEvents',
                              sub_attr='li',
                              caption='West Bengal PG Notices')

    dict_counts['wb_1_pg_count'] = wb_1_pg_count

    print("Checking West Bengal PG Downloads")

    wb_2_pg_count = web_crawler(paging=False,
                              paging_count=0,
                              url_link='https://wbmcc.nic.in/PGMed/pgmedland.aspx',
                              element_to_find='div',
                              attr='class',
                              attr_value='boxdesignImpLinks',
                              sub_attr='li',
                              caption='West Bengal PG Download')

    dict_counts['wb_2_pg_count'] = wb_2_pg_count

    print("Checking West Bengal PG News & Events")

    wb_3_pg_count = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://wbmcc.nic.in/PGMed/pgmedland.aspx',
                                element_to_find='div',
                                attr='class',
                                attr_value='boxdesignNews',
                                sub_attr='li',
                                caption='West Bengal PG News & Events')


    dict_counts['wb_3_pg_count'] = wb_3_pg_count

    ####Gujarat PG##############################################################

    print("Checking Gujarat PG")

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


    dict_counts['gujju_pg_count'] = gujju_pg_count

    ####Maharashtra PG##############################################################

    print("Checking Maharashtra PG")

    try:
        mh_pg_count = 0

        url = 'https://medical2024.mahacet.org/NEET-PGM-2024/login'
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        table = soup.find_all('div', attrs={'class': 'd-lg-flex pos-relative col-lg-4 card pb-20 m-4px'})

        for each_div in table[1].find_all_next('li'):
            mh_pg_count += 1

    except Exception as e:
        print("Exception for Maharashtra PG:- " + str(e))
        mh_pg_count = -1

    dict_counts['mh_pg_count'] = mh_pg_count

    ####GMCH PG #############################################################

    print("Checking GMCH PG")

    gmch_pg_count = web_crawler(paging=False,
                                paging_count=0,
                                url_link='https://gmch.gov.in/admission-mdms-2024',
                                element_to_find='div',
                                attr='class',
                                attr_value='node node--type-page node--view-mode-full clearfix',
                                sub_attr='tr',
                                caption='MCH PG')

    dict_counts['gmch_pg_count'] = gmch_pg_count

    ##Kerala#########################################################################
    try:
        print("Checking Kerala PG")

    kerala_pg_count = web_crawler(paging=False,
                                  paging_count=0,
                                  url_link='https://cee.kerala.gov.in/pgmonline2024/notification',
                                  element_to_find='div',
                                  attr='class',
                                  attr_value='container',
                                  sub_attr='div',
                                  caption='Kerala PG',
                                  sub_attr_attr='class',
                                  sub_attr_attr_value='row')


    dict_counts['kerala_pg_count'] = kerala_pg_count

    ####Bihar PG##############################################################

    print("Checking Bihar PG")


    bihar_pg_count = web_crawler(paging=False,
                                  paging_count=0,
                                  url_link='https://bceceboard.bihar.gov.in/PGMACindex.php#',
                                  element_to_find='div',
                                  attr='class',
                                  attr_value='SubDiv',
                                  sub_attr='li',
                                  caption='Bihar PG')


    dict_counts['bihar_pg_count'] = bihar_pg_count

    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################

    ####West Bengal Ayush##############################################################

    print("Checking West Bengal Ayush Notices")

    wb_1_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://wbmcc.nic.in/UGAyushW/UGAYUSHNotices.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='boxdesignCurrentEvents',
                                   sub_attr='li',
                                   caption='West Bengal Ayush Notices')

    dict_counts['wb_1_ayush_count'] = wb_1_ayush_count

    print("Checking West Bengal Ayush Downloads")

    wb_2_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://wbmcc.nic.in/UGAyushW/ugayushland.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='boxdesignImpLinks',
                                   sub_attr='li',
                                   caption='West Bengal Ayush Download')

    dict_counts['wb_2_ayush_count'] = wb_2_ayush_count

    print("Checking West Bengal Ayush News & Events")

    wb_3_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://wbmcc.nic.in/UGAyushW/ugayushland.aspx',
                                   element_to_find='div',
                                   attr='class',
                                   attr_value='boxdesignNews',
                                   sub_attr='li',
                                   caption='West Bengal Ayush News & Events')

    dict_counts['wb_3_ayush_count'] = wb_3_ayush_count

    ####UP PG##############################################################

    print("Checking UP Ayush Notices")

    up_ayush_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://upayushcounseling.upsdc.gov.in/Newsandevent1.aspx#',
                                 element_to_find='form',
                                 attr='name',
                                 attr_value='form1',
                                 sub_attr='tr',
                                 caption='UP AYUSH Notices')

    dict_counts['up_ayush_count'] = up_ayush_count

    ####Rajasthan AYUSH##############################################################

    rj_ayush_count = web_crawler(paging=False,
                                 paging_count=0,
                                 url_link='https://rajayushcounselling.com/Notice.aspx',
                                 element_to_find='div',
                                 attr='class',
                                 attr_value='container',
                                 sub_attr='a',
                                 caption='Rajasthan AYUSH Notices')

    dict_counts['rj_ayush_count'] = rj_ayush_count
    ####Haryana AYUSH##############################################################
    skau_ayush_count = web_crawler(paging=False,
                                   paging_count=0,
                                   url_link='https://skau.ac.in/U.G_Admission_2025',
                                   element_to_find='section',
                                   attr='class',
                                   attr_value='bg_color_box1',
                                   sub_attr='tr',
                                   caption='Sri Krishna Kurukshetra AYUSH')

    dict_counts['skau_ayush_count'] = skau_ayush_count
    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################
    ##################################################################



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

    new_df = pd.DataFrame(dict_counts.items(), columns=['State', 'Counts'])
    new_df.to_csv("neet_notifications_count.csv", index=False)

    kerala_new_count = new_df[new_df.State.isin(['kerala_count'])]['Counts'][0]
    tamil_nadu_new_count = new_df[new_df.State.isin(['tamil_nadu_count'])]['Counts'][1]
    haryana_1_new_count = new_df[new_df.State.isin(['haryana_1_count'])]['Counts'][2]
    haryana_2_new_count = new_df[new_df.State.isin(['haryana_2_count'])]['Counts'][3]
    karnataka_new_count = new_df[new_df.State.isin(['karnataka_count'])]['Counts'][4]
    hp_new_count = new_df[new_df.State.isin(['hp_count'])]['Counts'][5]
    uk_new_count = new_df[new_df.State.isin(['uk_count'])]['Counts'][6]
    pb_new_count = new_df[new_df.State.isin(['pb_count'])]['Counts'][7]
    up_new_count = new_df[new_df.State.isin(['up_count'])]['Counts'][8]
    jk_new_count = new_df[new_df.State.isin(['jk_count'])]['Counts'][9]
    rajasthan_new_count = new_df[new_df.State.isin(['rajasthan_count'])]['Counts'][10]
    mp_new_count = new_df[new_df.State.isin(['mp_count'])]['Counts'][11]
    cg_new_count = new_df[new_df.State.isin(['cg_count'])]['Counts'][12]
    jh_new_count = new_df[new_df.State.isin(['jh_count'])]['Counts'][13]
    wb1_new_count = new_df[new_df.State.isin(['wb_count1'])]['Counts'][14]
    wb2_new_count = new_df[new_df.State.isin(['wb_count2'])]['Counts'][15]
    wb3_new_count = new_df[new_df.State.isin(['wb_count3'])]['Counts'][16]
    mcc1_new_count = new_df[new_df.State.isin(['mcc1_count'])]['Counts'][17]
    mcc2_new_count = new_df[new_df.State.isin(['mcc2_count'])]['Counts'][18]
    mcc3_new_count = new_df[new_df.State.isin(['mcc3_count'])]['Counts'][19]
    mcc4_new_count = new_df[new_df.State.isin(['mcc4_count'])]['Counts'][20]
    mcc5_new_count = new_df[new_df.State.isin(['mcc5_count'])]['Counts'][21]
    gujju_new_count = new_df[new_df.State.isin(['gujju_count'])]['Counts'][22]
    mh_new_count = new_df[new_df.State.isin(['mh_count'])]['Counts'][23]
    assam_new_count = new_df[new_df.State.isin(['assam_count'])]['Counts'][24]
    telangana_new_count = new_df[new_df.State.isin(['telangana_count'])]['Counts'][25]
    ap_new_count = new_df[new_df.State.isin(['ap_count'])]['Counts'][26]
    gmch_new_count = new_df[new_df.State.isin(['gmch_count'])]['Counts'][27]
    pudu_new_count = new_df[new_df.State.isin(['pudu_count'])]['Counts'][28]
    bihar_new_count = new_df[new_df.State.isin(['bihar_count'])]['Counts'][29]
    odisha_new_count = new_df[new_df.State.isin(['odisha_count'])]['Counts'][30]
    manipur_new_count = new_df[new_df.State.isin(['manipur_count'])]['Counts'][31]
    meghalaya_new_count = new_df[new_df.State.isin(['meghalaya_count'])]['Counts'][32]
    nagaland_new_count = new_df[new_df.State.isin(['nagaland_count'])]['Counts'][33]
    ipu_1_new_count = new_df[new_df.State.isin(['ipu_1_count'])]['Counts'][34]
    ipu_2_new_count = new_df[new_df.State.isin(['ipu_2_count'])]['Counts'][35]
    tripura_new_count = new_df[new_df.State.isin(['tripura_count'])]['Counts'][36]


    ##############################################################################

    mcc_pg_1_new_count = new_df[new_df.State.isin(['mcc_pg_1_count'])]['Counts'][37]
    mcc_pg_2_new_count = new_df[new_df.State.isin(['mcc_pg_2_count'])]['Counts'][38]
    mcc_pg_3_new_count = new_df[new_df.State.isin(['mcc_pg_3_count'])]['Counts'][39]
    mcc_pg_4_new_count = new_df[new_df.State.isin(['mcc_pg_4_count'])]['Counts'][40]
    mcc_pg_5_new_count = new_df[new_df.State.isin(['mcc_pg_5_count'])]['Counts'][41]
    pb_pg_new_count = new_df[new_df.State.isin(['pb_pg_count'])]['Counts'][42]
    rj_pg_new_count = new_df[new_df.State.isin(['rj_pg_count'])]['Counts'][43]
    karnataka_pg_new_count = new_df[new_df.State.isin(['karnataka_pg_count'])]['Counts'][44]
    uk_pg_new_count = new_df[new_df.State.isin(['uk_pg_count'])]['Counts'][45]
    mp_pg_new_count = new_df[new_df.State.isin(['mp_pg_count'])]['Counts'][46]
    wb_1_pg_new_count = new_df[new_df.State.isin(['wb_1_pg_count'])]['Counts'][47]
    wb_2_pg_new_count = new_df[new_df.State.isin(['wb_2_pg_count'])]['Counts'][48]
    wb_3_pg_new_count = new_df[new_df.State.isin(['wb_3_pg_count'])]['Counts'][49]
    gujju_pg_new_count = new_df[new_df.State.isin(['gujju_pg_count'])]['Counts'][50]
    mh_pg_new_count = new_df[new_df.State.isin(['mh_pg_count'])]['Counts'][51]
    gmch_pg_new_count = new_df[new_df.State.isin(['gmch_pg_count'])]['Counts'][52]
    kerala_pg_new_count = new_df[new_df.State.isin(['kerala_pg_count'])]['Counts'][53]
    bihar_pg_new_count = new_df[new_df.State.isin(['bihar_pg_count'])]['Counts'][54]
    wb_1_ayush_new_count = new_df[new_df.State.isin(['wb_1_ayush_count'])]['Counts'][55]
    wb_2_ayush_new_count = new_df[new_df.State.isin(['wb_2_ayush_count'])]['Counts'][56]
    wb_3_ayush_new_count = new_df[new_df.State.isin(['wb_3_ayush_count'])]['Counts'][57]
    up_ayush_new_count = new_df[new_df.State.isin(['up_ayush_count'])]['Counts'][58]
    rj_ayush_new_count = new_df[new_df.State.isin(['rj_ayush_count'])]['Counts'][59]
    skau_ayush_new_count = new_df[new_df.State.isin(['skau_ayush_count'])]['Counts'][60]

    ##############################################################################


    # caption_msg = ''

    check_new_notification(old_count = kerala_old_count,
                           new_count = kerala_new_count,
                           state = 'Kerala',
                           url = 'https://cee.kerala.gov.in/keam2024/notification')

    check_new_notification(old_count = tamil_nadu_old_count,
                           new_count = tamil_nadu_new_count,
                           state = 'Tamil Nadu',
                           url = 'https://tnmedicalselection.net/Notification.aspx')


    check_new_notification(old_count = haryana_1_old_count,
                           new_count = haryana_1_new_count,
                           state = 'Haryana 1',
                           url = 'https://uhsrugcounselling.com/Notice.aspx')


    check_new_notification(old_count = haryana_2_old_count,
                           new_count = haryana_2_new_count,
                           state = 'Haryana 2',
                           url = 'https://uhsr.ac.in/detail.aspx?artid=79&menuid=12')


    check_new_notification(old_count = karnataka_old_count,
                           new_count = karnataka_new_count,
                           state = 'Karnataka UG',
                           url = 'https://cetonline.karnataka.gov.in/kea/ugneet24')

    check_new_notification(old_count = hp_old_count,
                           new_count = hp_new_count,
                           state = 'Himachal Pradesh',
                           url = 'https://amruhp.ac.in/notices/')

    check_new_notification(old_count = uk_old_count,
                           new_count = uk_new_count,
                           state = 'Uttarakhand UG',
                           url = 'https://meta-secure.com/HNBUMU_NEETUG')

    check_new_notification(old_count = pb_old_count,
                           new_count = pb_new_count,
                           state = 'Punjab UG',
                           url = 'https://bfuhs.ac.in/MBBS_BDS/MBBSBDS.asp')

    check_new_notification(old_count = up_old_count,
                           new_count = up_new_count,
                           state = 'Uttar Pradesh',
                           url = 'http://dgme.up.gov.in/Welcome/linkfiles?catid=news')

    check_new_notification(old_count = jk_old_count,
                           new_count = jk_new_count,
                           state = 'J & K',
                           url = 'https://www.jkbopee.gov.in/')

    check_new_notification(old_count = rajasthan_old_count,
                           new_count = rajasthan_new_count,
                           state = 'Rajasthan UG',
                           url = 'https://www.rajugneet2024.org/')

    check_new_notification(old_count = mp_old_count,
                           new_count = mp_new_count,
                           state = 'Madhya Pradesh UG',
                           url = 'https://dme.mponline.gov.in/Portal/Services/DMEMP/DMEUG/Profile/Instructions.aspx?tab=tab1')

    check_new_notification(old_count = cg_old_count,
                           new_count = cg_new_count,
                           state = 'Chhattisgarh',
                           url = 'https://cgdme.in/Notice_24.php')

    check_new_notification(old_count = jh_old_count,
                           new_count = jh_new_count,
                           state = 'Jharkhand',
                           url = 'https://jceceb.jharkhand.gov.in/Links/counselling.aspx')

    check_new_notification(old_count = wb1_old_count,
                           new_count = wb1_new_count,
                           state = 'West Bengal 1',
                           url = 'https://wbmcc.nic.in/UGMedDen/UGMedDenNotices.aspx')

    check_new_notification(old_count = wb2_old_count,
                           new_count = wb2_new_count,
                           state = 'West Bengal 2',
                           url = 'https://wbmcc.nic.in/UGMedDen/ugmeddenland.aspx')

    check_new_notification(old_count = wb3_old_count,
                           new_count = wb3_new_count,
                           state = 'West Bengal 3',
                           url = 'https://wbmcc.nic.in/UGMedDen/UGMedDenNewsEvents.aspx')

    check_new_notification(old_count = mcc1_old_count,
                           new_count = mcc1_new_count,
                           state = 'MCC 1 UG',
                           url = 'https://mcc.nic.in/current-events-ug')

    check_new_notification(old_count = mcc2_old_count,
                           new_count = mcc2_new_count,
                           state = 'MCC 2 UG',
                           url = 'https://mcc.nic.in/eservices-schedule-ug/')


    check_new_notification(old_count = mcc3_old_count,
                           new_count = mcc3_new_count,
                           state = 'MCC 3 UG',
                           url = 'https://mcc.nic.in/news-events-ug-medical/')

    check_new_notification(old_count = mcc4_old_count,
                           new_count = mcc4_new_count,
                           state = 'MCC 4 UG',
                           url = 'https://mcc.nic.in/ug-medical-counselling/')

    check_new_notification(old_count = mcc5_old_count,
                           new_count = mcc5_new_count,
                           state = 'MCC 5 UG',
                           url = 'https://mcc.nic.in/ug-medical-counselling/')

    check_new_notification(old_count = gujju_old_count,
                           new_count = gujju_new_count,
                           state = 'Gujarat',
                           url = 'https://www.medadmgujarat.org/ug/home.aspx')

    check_new_notification(old_count = mh_old_count,
                           new_count = mh_new_count,
                           state = 'Maharashtra',
                           url = 'https://medical2024.mahacet.org/NEET-UG-2024/login')

    check_new_notification(old_count = assam_old_count,
                           new_count = assam_new_count,
                           state = 'Assam',
                           url = 'https://dme.assam.gov.in/latest/admission-notice-ugpg-and-others')

    check_new_notification(old_count = telangana_old_count,
                           new_count = telangana_new_count,
                           state = 'Telangana',
                           url = 'https://www.knruhs.telangana.gov.in/all-notifications/')

    check_new_notification(old_count = ap_old_count,
                           new_count = ap_new_count,
                           state = 'Andhra Pradesh',
                           url = 'https://drntr.uhsap.in/index/index.html')

    check_new_notification(old_count = gmch_old_count,
                           new_count = gmch_new_count,
                           state = 'GMCH',
                           url = 'https://gmch.gov.in/centralized-admission-prospectus-mbbsbdsbhms-courses-session-2024')

    check_new_notification(old_count = pudu_old_count,
                           new_count = pudu_new_count,
                           state = 'Puducherry',
                           url = 'https://www.centacpuducherry.in/')

    check_new_notification(old_count = bihar_old_count,
                           new_count = bihar_new_count,
                           state = 'Bihar UG',
                           url = 'https://bceceboard.bihar.gov.in/UGMACIndex.php')

    check_new_notification(old_count = odisha_old_count,
                           new_count = odisha_new_count,
                           state = 'Odisha',
                           url = 'https://ojee.nic.in/medical-notice/')

    check_new_notification(old_count = manipur_old_count,
                           new_count = manipur_new_count,
                           state = 'Manipur',
                           url = 'https://manipurhealthdirectorate.mn.gov.in/notifications')

    check_new_notification(old_count = meghalaya_old_count,
                           new_count = meghalaya_new_count,
                           state = 'Meghalaya',
                           url = 'https://meghealth.gov.in/')

    check_new_notification(old_count = nagaland_old_count,
                           new_count = nagaland_new_count,
                           state = 'Nagaland',
                           url = 'https://dte.nagaland.gov.in/index.php/dept-2/')

    check_new_notification(old_count = ipu_1_old_count,
                           new_count = ipu_1_new_count,
                           state = 'IPU News & Events',
                           url = 'https://ipu.admissions.nic.in/news-events/')

    check_new_notification(old_count = ipu_2_old_count,
                           new_count = ipu_2_new_count,
                           state = 'IPU Current Events',
                           url = 'https://ipu.admissions.nic.in/current-events/')

    check_new_notification(old_count = tripura_old_count,
                           new_count = tripura_new_count,
                           state = 'Tripura',
                           url = 'https://dme.tripura.gov.in/notification')

    check_new_notification(old_count = mcc_pg_1_old_count,
                           new_count = mcc_pg_1_new_count,
                           state = 'MCC PG Current Events',
                           url = 'https://mcc.nic.in/current-events-pg')

    check_new_notification(old_count = mcc_pg_2_old_count,
                           new_count = mcc_pg_2_new_count,
                           state = 'MCC PG eService Schedule',
                           url = 'https://mcc.nic.in/eservices-schedule-pg/')

    check_new_notification(old_count = mcc_pg_3_old_count,
                           new_count = mcc_pg_3_new_count,
                           state = 'MCC PG News Events',
                           url = 'https://mcc.nic.in/news-events-pg/')

    check_new_notification(old_count = mcc_pg_4_old_count,
                           new_count = mcc_pg_4_new_count,
                           state = 'MCC PG Candidate Board',
                           url = 'https://mcc.nic.in/pg-medical-counselling/')

    check_new_notification(old_count = mcc_pg_5_old_count,
                           new_count = mcc_pg_5_new_count,
                           state = 'MCC PG Important Link',
                           url = 'https://mcc.nic.in/ug-medical-counselling/')

    check_new_notification(old_count = pb_pg_old_count,
                           new_count = pb_pg_new_count,
                           state = 'Punjab PG',
                           url = 'https://bfuhs.ac.in/MDMS/MDMS.asp')

    check_new_notification(old_count = rj_pg_old_count,
                           new_count = rj_pg_new_count,
                           state = 'Rajasthan PG',
                           url = 'https://www.rajpgneet2024.org/')

    check_new_notification(old_count = karnataka_pg_old_count,
                           new_count = karnataka_pg_new_count,
                           state = 'Karnataka PG',
                           url = 'https://cetonline.karnataka.gov.in/kea/pget2024')

    check_new_notification(old_count = uk_pg_old_count,
                           new_count = uk_pg_new_count,
                           state = 'Uttarakhand PG',
                           url = 'https://meta-secure.com/HNBUMU_NEETPG')

    check_new_notification(old_count = mp_pg_old_count,
                           new_count = mp_pg_new_count,
                           state = 'Madhya Pradesh PG',
                           url = 'https://dme.mponline.gov.in/portal/services/dmemp/DMEPG/Profile/Instructions.aspx?tab=tab1')

    check_new_notification(old_count = wb_1_pg_old_count,
                           new_count = wb_1_pg_new_count,
                           state = 'West Bengal PG Notices',
                           url = 'https://wbmcc.nic.in/PGMed/PGMedNotices.aspx')

    check_new_notification(old_count = wb_2_pg_old_count,
                           new_count = wb_2_pg_new_count,
                           state = 'West Bengal PG Download',
                           url = 'https://wbmcc.nic.in/PGMed/pgmedland.aspx')

    check_new_notification(old_count = wb_3_pg_old_count,
                           new_count = wb_3_pg_new_count,
                           state = 'West Bengal PG News & Events',
                           url = 'https://wbmcc.nic.in/PGMed/pgmedland.aspx')

    check_new_notification(old_count = gujju_pg_old_count,
                           new_count = gujju_pg_new_count,
                           state = 'Gujarat PG',
                           url = 'https://www.medadmgujarat.org/pg/home.aspx')

    check_new_notification(old_count = mh_pg_old_count,
                           new_count = mh_pg_new_count,
                           state = 'Maharashtra PG',
                           url = 'https://medical2024.mahacet.org/NEET-PGM-2024/login')

    check_new_notification(old_count = gmch_pg_old_count,
                           new_count = gmch_pg_new_count,
                           state = 'GMCH PG',
                           url = 'https://gmch.gov.in/admission-mdms-2024')

    check_new_notification(old_count = kerala_pg_old_count,
                           new_count = kerala_pg_new_count,
                           state = 'Kerala PG',
                           url = 'https://cee.kerala.gov.in/pgmonline2024/notification')

    check_new_notification(old_count = bihar_pg_old_count,
                           new_count = bihar_pg_new_count,
                           state = 'Bihar PG',
                           url = 'https://bceceboard.bihar.gov.in/PGMACindex.php#')

    check_new_notification(old_count = wb_1_ayush_old_count,
                           new_count = wb_1_ayush_new_count,
                           state = 'West Bengal AYUSH Notices',
                           url = 'https://wbmcc.nic.in/UGAyushW/UGAYUSHNotices.aspx')

    check_new_notification(old_count = wb_2_ayush_old_count,
                           new_count = wb_2_ayush_new_count,
                           state = 'West Bengal AYUSH Download',
                           url = 'https://wbmcc.nic.in/UGAyushW/ugayushland.aspx')

    check_new_notification(old_count = wb_3_ayush_old_count,
                           new_count = wb_3_ayush_new_count,
                           state = 'West Bengal AYUSH News & Events',
                           url = 'https://wbmcc.nic.in/UGAyushW/ugayushland.aspx')

    check_new_notification(old_count = up_ayush_old_count,
                           new_count = up_ayush_new_count,
                           state = 'UP AYUSH Notices',
                           url = 'https://upayushcounseling.upsdc.gov.in/Newsandevent1.aspx#')

    check_new_notification(old_count = rj_ayush_old_count,
                           new_count = rj_ayush_new_count,
                           state = 'Rajasthan AYUSH Notices',
                           url = 'https://rajayushcounselling.com/Notice.aspx')

    check_new_notification(old_count = skau_ayush_old_count,
                           new_count = skau_ayush_new_count,
                           state = 'Sri Krishna KURUKSHETRA AYUSH Notices',
                           url = 'https://skau.ac.in/U.G_Admission_2025')


# Remaining UG
# Arunachal Pradesh
# Sikkim
# NMC
# Odisha UG  - extra 4

# Remaining PG -
# odisha PG

# Ayush

    