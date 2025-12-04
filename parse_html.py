from bs4 import BeautifulSoup
import requests
import pandas as pd

college_info_master_dict = {}
college_info_master_df = pd.DataFrame()
student_admission_details_master_df = pd.DataFrame()
hospital_details_master_df = pd.DataFrame()
clinical_load_details_master_df = pd.DataFrame()
death_birth_details_master_df = pd.DataFrame()
faculty_details_master_df = pd.DataFrame()
ot_details_master_df = pd.DataFrame()
community_medicine_master_df = pd.DataFrame()

######################################################################
def college_name_details(url_college, class_college, college_name):

    url=url_college
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    table = soup.find('table', attrs={'class':class_college})
    table_rows = table.find_all('tr')
    rows = []

    for tr in table.find_all('tr'):
        rows.append([td.text for td in tr.find_all(['th', 'td'])])
    count = 1
    data = {}
    for each in rows:
        if count == 1:
            count +=1
            continue
        else:
            data[each[0]] = each[1]

    # return(data)
    df = pd.DataFrame({'name': data.keys(), 'value': data.values()})

    college_details = {}
    # print(df)
    for index, row in df.iterrows():
        college_details[row['name']] = row['value']

    # print(college_details.keys())
    # print(college_details.values())
    college_info_master_dict[college_name] = college_details
    return df

#############################################################################
def student_admission_details(url_college, class_college):
    url = url_college
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    table = soup.find('table', attrs={'class': class_college})

    rows = []

    for tr in table.find_all('tr'):
        rows.append([td.text for td in tr.find_all(['th', 'td'])])
    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])

    return df

#############################################################################

url='https://msmer.nmc.org.in/public/performaAdminDetails'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
table = soup.find('table', attrs={'class':'table table-bordered table-striped'})

table_rows = table.find_all('tr')
count = 1
master_college = {}
for td in table_rows:
    if count == 1:
        count += 1
        continue
    else:
        tds= td.find_all('td')
        td_texts = [td.text for td in tds if 'Completed' not in td.text]
        # print(type(td_texts))

        links= td.find_all('a')
        rows = ['https://msmer.nmc.org.in' + link.get('href') for link in links]

        college_item = td_texts + rows
        college_name = college_item[1]
        master_college[college_name] = college_name_details(college_item[3],
                                                            'table table-vertical table-bordered', college_name)
        # print(college_info_master_dict.keys())
        for value in college_info_master_dict.values():
            college_info_master_df1 = pd.DataFrame(list(value.items()), columns = ['Name','Value'])
            college_info_master_df1['College_Name'] = college_name
        # college_info_master_df1 = college_info_master_df1.rename(columns={'0': 'Name', '1': 'Value'})
        # print(college_info_master_df1)
        college_info_master_df = college_info_master_df.append(college_info_master_df1, ignore_index=True)
        # print(college_info_master_df)
        # print(college_info_master_df.columns)

        ##########################################################################

        master_college['student_admission_details'] = student_admission_details(college_item[4],
                                                                              'table table-bordered table-striped')
        master_college['student_admission_details']['College_Name'] = college_name

        student_admission_details_master_df = student_admission_details_master_df.append(master_college['student_admission_details'] )

        ##########################################################################

        master_college['hospital_details'] = student_admission_details(college_item[5],
                                                                     'table table-bordered table-striped')

        master_college['hospital_details']['College_Name'] = college_name

        hospital_details_master_df = hospital_details_master_df.append(
            master_college['hospital_details'])


        ##########################################################################
        master_college['clinical_load_details'] = student_admission_details(college_item[6],
                                                                     'table table-bordered table-striped')

        master_college['clinical_load_details']['College_Name'] = college_name

        clinical_load_details_master_df = clinical_load_details_master_df.append(
            master_college['clinical_load_details'])

        ##########################################################################
        master_college['death_birth_details'] = student_admission_details(college_item[7],
                                                                     'table table-bordered table-striped')

        master_college['death_birth_details']['College_Name'] = college_name

        death_birth_details_master_df = death_birth_details_master_df.append(
            master_college['death_birth_details'])
        ##########################################################################
        master_college['faculty_details'] = student_admission_details(college_item[8],
                                                                     'table table-bordered table-striped')

        master_college['faculty_details']['College_Name'] = college_name

        faculty_details_master_df = faculty_details_master_df.append(
            master_college['faculty_details'])
        ##########################################################################
        master_college['ot_details'] = student_admission_details(college_item[9],
                                                                     'table table-bordered table-striped')

        master_college['ot_details']['College_Name'] = college_name

        ot_details_master_df = ot_details_master_df.append(
            master_college['ot_details'])
        ##########################################################################
        master_college['community_medicine'] = student_admission_details(college_item[10],
                                                                     'table table-bordered table-striped')

        master_college['community_medicine']['College_Name'] = college_name

        community_medicine_master_df = community_medicine_master_df.append(
            master_college['community_medicine'])
       ##########################################################################

college_info_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "college_info_master_df.xlsx", index=False)
student_admission_details_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "student_admission_details_master_df.xlsx", index=False)
hospital_details_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "hospital_details_master_df.xlsx", index=False)
clinical_load_details_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "clinical_load_details_master_df.xlsx", index=False)
death_birth_details_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "death_birth_details_master_df.xlsx", index=False)
faculty_details_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "faculty_details_master_df.xlsx", index=False)
ot_details_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "ot_details_master_df.xlsx", index=False)
community_medicine_master_df.to_excel('./nmc_annual_declaration_college_info_2024/' + "community_medicine_master_df.xlsx", index=False)


        # writer = pd.ExcelWriter('./nmc_annual_declaration_college_info_2024/' + college_name + ".xlsx", engine='xlsxwriter')
        # # print(master_college[college_name],master_college[student_admission_details])
        #
        # names = ["College_Information", "Student_Admission_details", "Hospital_Details",'clinical_load_details', 'death_birth_details', 'faculty_details', 'ot_details', 'community_medicine']
        # dataframes = [master_college['college_name'],
        #               master_college['student_admission_details'],
        #               master_college['hospital_details'],
        #               master_college['clinical_load_details'],
        #               master_college['death_birth_details'],
        #               master_college['faculty_details'],
        #               master_college['ot_details'],
        #               master_college['community_medicine']
        #               ]
        #
        # for i, frame in enumerate(dataframes):
        #     frame.to_excel(writer, sheet_name=names[i], index=False)
        #
        # writer.save()
        # # writer.close()


        # print(master_college[student_admission_details])
        # break


    # df.to_excel(college_name + ".xlsx", sheet_name='College_Information', index=False)
    # df.to_excel(college_name + ".xlsx", sheet_name='Student_Admission_details', index=False)


