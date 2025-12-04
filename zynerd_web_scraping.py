import requests
from bs4 import BeautifulSoup

try:
    aiq_pg_count = 0
    url = 'https://portal.zynerd.com/dashboard/allotments?counselling_id=1'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    table = soup.find('table', attrs={'class': 'styles_tableSticky__nJclw m-0 styles_tableContentHeader__DqEUl'})

    for each_row in table.find_all('div', attrs={'class': 'row'}):
        haryana_1_count += 1

except Exception as e:
    print("Exception for Haryana 1:- " + str(e))
    haryana_1_count = -1


import pandas as pd

# html_string = '''
# <table id="customTable" role="table" class="styles_tableContClass__NcBf7 styles_tableContentHeader__DqEUl styles_tableResponsive__ILm+b">
#     <thead class="styles_thheadClass__fOTug undefined">
#         <tr role="row" class="undefined undefined border-b !border-[#D9D9D9]">
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43"></div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderContainer__h0xLa">
#                         <p class="styles_thHeaderText__mkC43">Round </p>
#                         <div class="styles_iconMain__sBqfW">
#                             <div class="styles_iconNorm__OxmzI styles_headerIconFilter__O4W8f"><img src="/static/media/sort_arrow.8a73cfe5185eb667465d.svg" alt="" class="cursor-pointer"><img src="/static/media/sort_arrow.8a73cfe5185eb667465d.svg" alt="" class="cursor-pointer"></div>
#                         </div>
#                     </div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderContainer__h0xLa">
#                         <p class="styles_thHeaderText__mkC43">AI Rank </p>
#                         <div class="styles_iconMain__sBqfW">
#                             <div class="styles_iconNorm__OxmzI styles_headerIconFilter__O4W8f"><img src="/static/media/sort_arrow.8a73cfe5185eb667465d.svg" alt="" class="cursor-pointer"><img src="/static/media/sort_arrow.8a73cfe5185eb667465d.svg" alt="" class="cursor-pointer"></div>
#                         </div>
#                     </div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">State</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Institute</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Course</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Quota</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Category</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Fee</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Stipend Year 1</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Bond Years</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Bond Penalty</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43">Beds</div>
#                 </div>
#             </th>
#             <th colspan="1" role="columnheader" class=" px-[6px] py-[12px] font-black uppercase" style="position: relative;">
#                 <div>
#                     <div class="styles_thHeaderText__mkC43"></div>
#                 </div>
#             </th>
#         </tr>
#     </thead>
#
#     <tbody role="rowgroup" class="styles_tbClass__z9uxv undefined">
#         <tr role="row" class="styles_trSubClass__NUvQG undefined   cursor-pointer  hover:bg-[#F0F0F0]">
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index"></td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1">1</div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1">
#                     <div class="px-2">1</div>
#                 </div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1">Delhi</div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index" style="color: rgb(1, 87, 155); font-weight: 700;">
#                 <div class="institute-clickable-div-class" style="cursor: pointer; width: fit-content; color: rgb(1, 49, 143);"><span>VMMC, Delhi</span></div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1"><span>RADIO DIAGNOSIS</span></div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1">AIQ</div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1">GEN</div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1"><span>₹41,000*</span></div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1"><span>₹1,20,965*</span></div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1"><span>0*</span></div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1"><span>₹0*</span></div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="p-1">-</div>
#             </td>
#             <td role="cell" class="styles_tdSubClass__wq-43 undefined !px-[6px] !py-[12px] text-[14px] td-index">
#                 <div class="cursor-pointer">
#                     <svg class="fill-[#FFFFFF]" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
#                         <path d="M21 8.25C21 5.765 18.901 3.75 16.312 3.75C14.377 3.75 12.715 4.876 12 6.483C11.285 4.876 9.623 3.75 7.687 3.75C5.1 3.75 3 5.765 3 8.25C3 15.47 12 20.25 12 20.25C12 20.25 21 15.47 21 8.25Z" stroke="black" stroke-width="2" stroke-linecap="round"
#                         stroke-linejoin="round"></path>
#                     </svg>
#                 </div>
#             </td>
#         </tr>
#         </tbody>
# </table>
# '''
lis = pd.read_html('./zynerd/sample.html', encoding = 'utf-8')
df = pd.DataFrame(lis)
del df['Unnamed: 0']

df.to_csv("./zynerd/sample.csv", encoding='utf-8', index=False)

import pyperclip as pc

text_1= ''
text_2 = ''
while 1:
    text_2 = pc.paste()
    if text_1 != text_2:
        file1 = open("./zynerd/Fee, Stipend and Bonds - Latest.txt", "a", encoding='utf-8')
        file1.write(text_2)
        file1.write("\n\n-------------------------------------------------------------------------------------------------")
        file1.write("-------------------------------------------------------------------------------------------------\n\n")
        file1.close()
        # print(text_2)
        text_1 = text_2

file1.close()

import pyperclip as pc

import pyperclip as pc

import pyautogui
print()

import glob

# list all csv files only
csv_files = glob.glob(""'*.{}'.format('csv'))
csv_files
