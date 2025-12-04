# AIQ

import fpdf, os
from fpdf import FPDF


def print_pdf(state, rank):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', '', 11)

    f = open(state + '.txt', "r")
    count = 1
    for x in f:
        # print(x)
        x = x.replace("\n", "")
        if ('Colleges - Round' in x) or (('- Round -' in x) and (state == 'delhi' or 'haryana')):
            if count != 1:
                pdf.add_page()
                pdf.set_xy(0, 0)
            pdf.set_font('arial', 'B', 15)
            pdf.cell(ln=2, h=10.0, align='C', w=0, txt=x, border=1)
            pdf.cell(ln=1, h=5.0, align='C', w=0, txt="\n", border=0)

            count += 1
        else:
            pdf.set_font('arial', '', 6)
            pdf.cell(ln=1, h=8.0, align='L', w=1, txt=x, border=0)

    pdf.output(os.getcwd() + '\\' + str(name + '_' + category_AIQ + "_" + category_haryana + "_" + category_hp + "_" + str(rank)) + '\\' + state + '.pdf')

name = input("Name? :- ")
rank = int(input("Rank? :- "))
category_AIQ = input("category_AIQ? Options - G, EWS, OBC, SC, ST(H) :- ")
category_haryana = input("category_haryana? Options - G, EWS, OBC(BC-A), OBC(BC-B), SC, ST :- ")
category_hp = input("category_himachal? Options - General,OBC, SC,ST :- ")

# rank=23949
# category_AIQ='G' # G, EWS, OBC, SC, ST(H)
# category_haryana='G' ## G, EWS, OBC(BC-A), OBC(BC-B), SC, ST, SC
# category_hp= 'General' #General,OBC, SC,ST

try:
    os.mkdir(os.getcwd() + '\\' + str(name + '_' + category_AIQ + "_" + category_haryana + "_" + category_hp + "_" + str(rank)))
except:
    pass


final_str=''
import pandas as pd
###################################################################
###################################################################

#Read data
score_vs_rank_df = pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS AIQ.xlsx", sheet_name = "Score Vs Rank")

#Column Rename
score_vs_rank_df=score_vs_rank_df.rename(columns={'Score':'2023_Score', 'Rank':'AIR_Rank'})

score_vs_rank_df['2023_Score'] = score_vs_rank_df['2023_Score'].astype(str).astype(int)
score_vs_rank_df['AIR_Rank'] = score_vs_rank_df['AIR_Rank'].astype(str).astype(int)

# score_vs_rank_df = score_vs_rank_df.applymap(lambda x:(str(x).strip()))

mbbs_aiq_govt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS AIQ.xlsx", sheet_name = "MBBS AIQ Cut Off - General")

mbbs_aiq_deemed_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS AIQ.xlsx", sheet_name = "MBBS DEEMED COLLEGES CUT OFF")

# final_str = 'Score - {0}\n'.format(score)




#AIQ Govt Colleges

for rounds in ['1','2','3']:

    mbbs_aiq_govt_results_df=mbbs_aiq_govt_df[mbbs_aiq_govt_df['Round ' + rounds] >= rank][['Colleges','State']]
    final_str = final_str + '\n' + "AIQ Govt. Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_aiq_govt_results_df.iterrows():
        final_str = final_str + str(ind) + '. ' + str(row['Colleges']).replace("\n"," ") + ',' + row['State'] + '\n'
        ind+=1


# AIQ Deemed Colleges

for rounds in ['1','2','3']:
    mbbs_aiq_deemed_results_df=mbbs_aiq_deemed_df[mbbs_aiq_deemed_df['Round ' + rounds] >= rank][['Deemed College Name','State','Year of Estbl.','Tution Fee  Structure (Per Year)','Fees payable for','Yearly Hostel Fee']]
    final_str = final_str + '\n' + "AIQ Deemed. Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_aiq_deemed_results_df.iterrows():
        final_str = final_str + str(ind) + '. ' + str(row['Deemed College Name']).replace("\n"," ") + ',' + row['State'] + '\n'
        ind+=1

aiq_final_str=final_str
final_str=''

with open("aiq.txt", "w") as text_file:
    text_file.write(aiq_final_str)


#################################################################################################
#################################################################################################
#DELHI


# G, EWS, OBC, SC, ST(H)

category=category_AIQ

import pandas as pd

#Read data
score_vs_rank_df = pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS Delhi.xlsx", sheet_name = "Score Vs Rank")

#Column Rename
score_vs_rank_df=score_vs_rank_df.rename(columns={'NEET 2023 Score (Marks)':'2023_Score', 'NEET 2023 All India Rank (AIR)':'AIR_Rank'})

score_vs_rank_df['2023_Score'] = score_vs_rank_df['2023_Score'].astype(str).astype(int)
score_vs_rank_df['AIR_Rank'] = score_vs_rank_df['AIR_Rank'].astype(str).astype(int)

# score_vs_rank_df = score_vs_rank_df.applymap(lambda x:(str(x).strip()))

mbbs_delhi_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS Delhi.xlsx", sheet_name = "MBBS New Delhi GOVT. and Pvt.")


for rounds in ['-R1','-R2','-R3','-SR']:
    mbbs_delhi_results_df=mbbs_delhi_df[mbbs_delhi_df[category + rounds] >= rank][['College Name','Quota']]
    final_str = final_str + '\n' + "Delhi Colleges - Category {0} - Round {1}\n".format(category,rounds)

    ind=1
    for index, row in mbbs_delhi_results_df.iterrows():
        final_str = final_str + str(ind) + '. ' + str(row['College Name']).replace("\n"," ") + ',' + row['Quota'] + '\n'
        ind+=1

delhi_final_str=final_str
final_str=''

with open("delhi.txt", "w") as text_file:
    text_file.write(delhi_final_str)

#################################################################################################
#################################################################################################
#HARYANA

category=category_haryana
import pandas as pd

#Read data
score_vs_rank_df = pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS Haryana.xlsx", sheet_name = "Score Vs Rank")

#Column Rename
score_vs_rank_df=score_vs_rank_df.rename(columns={'NEET 2023 Score (Marks)':'2023_Score', 'NEET 2023 All India Rank (AIR)':'AIR_Rank'})

score_vs_rank_df['2023_Score'] = score_vs_rank_df['2023_Score'].astype(str).astype(int)
score_vs_rank_df['AIR_Rank'] = score_vs_rank_df['AIR_Rank'].astype(str).astype(int)

# score_vs_rank_df = score_vs_rank_df.applymap(lambda x:(str(x).strip()))

mbbs_haryana_govt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS Haryana.xlsx", sheet_name = "MBBS Haryana Govt Cut Off")

mbbs_haryana_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS Haryana.xlsx", sheet_name = "MBBS HARYANA STATE PVT. CUT OF")

#Haryana Govt. Colleges

for rounds in ['-R1','-R2','-R3','-SR']:
    mbbs_haryana_govt_results_df=mbbs_haryana_govt_df[mbbs_haryana_govt_df[category + rounds] >= rank]['College Name']
    final_str = final_str + '\n' + "Haryana Govt. Colleges - Category {0} - Round {1}\n".format(category,rounds)

    ind=1
    for college in mbbs_haryana_govt_results_df:
        final_str = final_str + str(ind) + '. ' + college.replace("\n",' ') + '\n'
        ind+=1

# Haryana Private Colleges

for rounds in ['-R1','-R2','-R3','-SR']:
    mbbs_haryana_pvt_results_df=mbbs_haryana_pvt_df[mbbs_haryana_pvt_df[category + rounds] >= rank]['College Name']
    final_str = final_str + '\n' + ("Haryana Private Colleges - Category {0} - Round {1}\n".format(category,rounds))

    ind=1
    for college in mbbs_haryana_pvt_results_df:
        final_str = final_str + str(ind) + '. ' + college.replace("\n",' ') + '\n'
        ind+=1


haryana_final_str=final_str
final_str=''

with open("haryana.txt", "w") as text_file:
    text_file.write(haryana_final_str)

#################################################################################################
#################################################################################################
#Rajasthan

import pandas as pd

#Read data
score_vs_rank_df = pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS RAJASTHAN OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Score Vs Rank")

#Column Rename
score_vs_rank_df=score_vs_rank_df.rename(columns={'NEET 2023 Score (Marks)':'2023_Score', 'NEET 2023 All India Rank (AIR)':'AIR_Rank'})

score_vs_rank_df['2023_Score'] = score_vs_rank_df['2023_Score'].astype(str).astype(int)
score_vs_rank_df['AIR_Rank'] = score_vs_rank_df['AIR_Rank'].astype(str).astype(int)


mbb_rajasthan_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS RAJASTHAN OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "MBBS Rajasthan MQ")


# Rajasthan Private Colleges

for rounds in ['1','2','3']:

    mbbs_rajasthan_pvt_mq_results_df=mbb_rajasthan_pvt_df[mbb_rajasthan_pvt_df['Round ' + rounds] >= rank][['College','ESTD']]
    final_str = final_str + '\n' + "Rajasthan Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_rajasthan_pvt_mq_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['College']).replace("\n"," ") + ',' + str(row['ESTD'])  + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['College']).replace("\n", " ") + '\n'
        ind+=1

rajasthan_final_str=final_str
final_str=''

with open("rajasthan.txt", "w") as text_file:
    text_file.write(rajasthan_final_str)

#################################################################################################
#################################################################################################
#UP

import pandas as pd

#Read data
score_vs_rank_df = pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS u.p. OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Score Vs Rank")

#Column Rename
score_vs_rank_df=score_vs_rank_df.rename(columns={'NEET 2023 Score (Marks)':'2023_Score', 'NEET 2023 All India Rank (AIR)':'AIR_Rank'})

score_vs_rank_df['2023_Score'] = score_vs_rank_df['2023_Score'].astype(str).astype(int)
score_vs_rank_df['AIR_Rank'] = score_vs_rank_df['AIR_Rank'].astype(str).astype(int)


mbbs_up_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS u.p. OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "MBBS UP")



# UP Private Colleges

for rounds in ['1','2','3']:

    mbbs_up_pvt_results_df=mbbs_up_pvt_df[mbbs_up_pvt_df['Round ' + rounds] >= rank][['Name of Colleges','TUITION FEE PER YEAR']]
    final_str = final_str + '\n' + "UP Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_up_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['Name of Colleges']).replace("\n"," ") + ',' + str(row['TUITION FEE PER YEAR'])  + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['Name of Colleges']).replace("\n", " ") + '\n'
        ind+=1

up_final_str=final_str
final_str=''

with open("up.txt", "w") as text_file:
    text_file.write(up_final_str)


#################################################################################################
#################################################################################################
#Uttarakhand

import pandas as pd

#Read data
score_vs_rank_df = pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS Uttranchal.xlsx", sheet_name = "Score Vs Rank")

#Column Rename
score_vs_rank_df=score_vs_rank_df.rename(columns={'Score':'2023_Score', 'Rank':'AIR_Rank'})

score_vs_rank_df['2023_Score'] = score_vs_rank_df['2023_Score'].astype(str).astype(int)
score_vs_rank_df['AIR_Rank'] = score_vs_rank_df['AIR_Rank'].astype(str).astype(int)


mbbs_uttranchal_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS Uttranchal.xlsx", sheet_name = "MBBS Uttranchal")



# Uttaranchal Private Colleges

for rounds in ['1','2','3']:

    mbbs_uttranchal_pvt_results_df=mbbs_uttranchal_pvt_df[mbbs_uttranchal_pvt_df['Round ' + rounds] >= rank][['COLLEGE NAME','Tuition Fees for Other State Students per year','ESTD']]
    final_str = final_str + '\n' + "Uttranchal Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_uttranchal_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['Tuition Fees for Other State Students per year']) + ',' + str(row['ESTD']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ") + '\n'
        ind+=1

uttaranchal_final_str=final_str
final_str=''

with open("uttarakhand.txt", "w") as text_file:
    text_file.write(uttaranchal_final_str)


#################################################################################################
#################################################################################################
#Kerala

mbbs_kerala_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS KERALA OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Table 1")



# Kerala Private Colleges

for rounds in ['1','2','3']:

    mbbs_kerala_pvt_results_df=mbbs_kerala_pvt_df[mbbs_kerala_pvt_df['Round ' + rounds] > rank][['Name of College','Year of Establish','Tuition Fee Per Year']]
    final_str = final_str + '\n' + "Kerala Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_kerala_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['Name of College']).replace("\n"," ") + ',' + str(row['Year of Establish']) + ',' + str(row['Tuition Fee Per Year']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['Name of College']).replace("\n", " ") + '\n'
        ind+=1

kerala_final_str=final_str
final_str=''

with open("kerala.txt", "w") as text_file:
    text_file.write(kerala_final_str)


#################################################################################################
#################################################################################################
#Puducherry

mbbs_puducherry_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS puducherry OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Table 1")

# Puducherry Private Colleges

for rounds in ['1']:

    mbbs_puducherry_pvt_results_df=mbbs_puducherry_pvt_df[mbbs_puducherry_pvt_df['Round ' + rounds] > rank][['COLLEGE NAME','ESTD','TUITION FEE PER YEAR']]
    final_str = final_str + '\n' + "Puducherry Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_puducherry_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['ESTD']) + ',' + str(row['TUITION FEE PER YEAR']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ") + '\n'
        ind+=1

puducherry_final_str=final_str

final_str=''

with open("puducherry.txt", "w") as text_file:
    text_file.write(puducherry_final_str)

#################################################################################################
#################################################################################################
#punjab

mbbs_punjab_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS PUNJAB OPEN STATE CUT OFF 2023.xlsx", sheet_name = "Table 1")

# punjab Private Colleges

for rounds in ['1', '2', '3']:

    mbbs_punjab_pvt_results_df=mbbs_punjab_pvt_df[mbbs_punjab_pvt_df['Round ' + rounds] > rank][['COLLEGE NAME']]
    final_str = final_str + '\n' + "Punjab Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_punjab_pvt_results_df.iterrows():
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ")  + '\n'
        ind+=1

punjab_final_str=final_str

final_str=''

with open("punjab.txt", "w") as text_file:
    text_file.write(punjab_final_str)


#################################################################################################
#################################################################################################
#Telangana

# MBBS Telangana OPEN STATE  CUT OFF 2023.xlsx


#################################################################################################
#################################################################################################
#Tamil Nadu



mbbs_tamil_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\private colleges 2023 - Tamilnadu.xlsx", sheet_name = "Table 1")

# Tamil Nadu Private Colleges

for rounds in ['1','2']:

    mbbs_tamil_pvt_results_df=mbbs_tamil_pvt_df[mbbs_tamil_pvt_df['Round ' + rounds] > rank][['COLLEGE NAME','ESTD','Tuition fee per year']]
    final_str = final_str + '\n' + "Tamil Nadu Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_tamil_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['ESTD']) + ',' + str(row['Tuition fee per year']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ") + '\n'
        ind+=1

tamil_final_str=final_str

final_str=''

with open("tamil_nadu.txt", "w") as text_file:
    text_file.write(tamil_final_str)



#################################################################################################
#################################################################################################
#west bengal

mbbs_westbengal_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS west bengal OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Table 1")

# westbengal Private Colleges

for rounds in ['1','2', '3']:

    mbbs_westbengal_pvt_results_df=mbbs_westbengal_pvt_df[mbbs_westbengal_pvt_df['Round ' + rounds] > rank][['COLLEGE NAME','ESTD','Tuition fee per year']]
    final_str = final_str + '\n' + "West bengal Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_westbengal_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['ESTD']) + ',' + str(row['Tuition fee per year']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ")+ '\n'
        ind+=1

westbengal_final_str=final_str

final_str=''

with open("westbengal.txt", "w") as text_file:
    text_file.write(westbengal_final_str)


#################################################################################################
#################################################################################################
#A.P



mbbs_ap_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS A.P. OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Table 1")

# AP Private Colleges

for rounds in ['1','2', '3']:

    mbbs_ap_pvt_results_df=mbbs_ap_pvt_df[mbbs_ap_pvt_df['Round ' + rounds] > rank][['COLLEGE NAME','ESTD','MANAGEMENT FEE', 'NRI FEE']]
    final_str = final_str + '\n' + "Andhra Pradesh Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_ap_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['ESTD']) + ',' + str(row['MANAGEMENT FEE']) + ',' + str(row['NRI FEE'])+ '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ")  + '\n'
        ind+=1

ap_final_str=final_str

final_str=''

with open("andhra_pradesh.txt", "w") as text_file:
    text_file.write(ap_final_str)

#################################################################################################
#################################################################################################
#Bihar

mbbs_bihar_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS bihar OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Table 1")

# bihar Private Colleges

for rounds in ['1','2','3']:

    mbbs_bihar_pvt_results_df=mbbs_bihar_pvt_df[mbbs_bihar_pvt_df['Round ' + rounds] > rank][['COLLEGE NAME','ESTD','Tuition fee per year']]
    final_str = final_str + '\n' + "Bihar Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_bihar_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['ESTD']) + ',' + str(row['Tuition fee per year']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ") + '\n'
        ind+=1

bihar_final_str=final_str

final_str=''

with open("bihar.txt", "w") as text_file:
    text_file.write(bihar_final_str)


#################################################################################################
#################################################################################################
#CHHATISGARH


mbbs_chattisgarh_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS CHHATISGARH OPEN STATE  CUT OFF 2023 (1).xlsx", sheet_name = "Table 1")

# CHHATISGARH Private Colleges

for rounds in ['1','2','3']:

    mbbs_chattisgarh_pvt_results_df=mbbs_chattisgarh_pvt_df[mbbs_chattisgarh_pvt_df['Round ' + rounds] > rank][['COLLEGE NAME','Total Annual Fees Included Hostel and All (Per Year)','Tuition fee per year']]
    final_str = final_str + '\n' + "Chhatisgarh Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_chattisgarh_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['Total Annual Fees Included Hostel and All (Per Year)']) + ',' + str(row['Tuition fee per year']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ") + '\n'
        ind+=1

chattisgarh_final_str=final_str

final_str=''

with open("chattisgarh.txt", "w") as text_file:
    text_file.write(chattisgarh_final_str)


#################################################################################################
#################################################################################################
#HP

#General,OBC, SC,ST
quota_student = category_hp
mbbs_hp_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS h.p. OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Table 1")

# HP Private Colleges

for rounds in ['1','2','3']:

    mbbs_hp_pvt_results_df=mbbs_hp_pvt_df[(mbbs_hp_pvt_df['Round ' + rounds] > rank) & (mbbs_hp_pvt_df['Quota'] == quota_student)][['COLLEGE NAME','Tuition fee per year']]
    final_str = final_str + '\n' + "HP Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_hp_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n"," ") + ',' + str(row['Tuition fee per year']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['COLLEGE NAME']).replace("\n", " ") + '\n'

        ind+=1

hp_final_str=final_str

final_str=''

with open("himachal_pradesh.txt", "w") as text_file:
    text_file.write(hp_final_str)

#################################################################################################
#################################################################################################
#karnataka


mbbs_karnataka_pvt_df= pd.read_excel(r"H:\My Drive\Business\Vidya Saarthi\Counselling\Customers\MBBS karnataka OPEN STATE  CUT OFF 2023.xlsx", sheet_name = "Table 1")

# karnataka Private Colleges

for rounds in ['1','2','3']:

    mbbs_karnataka_pvt_results_df=mbbs_karnataka_pvt_df[mbbs_karnataka_pvt_df['Round ' + rounds] > rank][['College Name','ESTD','Tuition Fee per year']]
    final_str = final_str + '\n' + "Karnataka Private Colleges - Round {0}\n".format(rounds)

    ind=1
    for index, row in mbbs_karnataka_pvt_results_df.iterrows():
        # final_str = final_str + str(ind) + '. ' + str(row['College Name']).replace("\n"," ") + ',' + str(row['ESTD']) + ',' + str(row['Tuition Fee per year']) + '\n'
        final_str = final_str + str(ind) + '. ' + str(row['College Name']).replace("\n", " ")  + '\n'
        ind+=1

karnataka_final_str=final_str
final_str=''

with open("karnataka.txt", "w") as text_file:
    text_file.write(karnataka_final_str)

print_pdf('aiq', rank)
print_pdf('delhi', rank)
print_pdf('haryana', rank)
print_pdf('uttaranchal', rank)
print_pdf('himachal_pradesh', rank)
print_pdf('up', rank)
print_pdf('rajasthan', rank)
print_pdf('punjab', rank)
print_pdf('chattisgarh', rank)
print_pdf('bihar', rank)
print_pdf('karnataka', rank)
print_pdf('kerala', rank)
print_pdf('andhra_pradesh', rank)
print_pdf('puducherry', rank)
print_pdf('tamil_nadu', rank)
print_pdf('westbengal', rank)
