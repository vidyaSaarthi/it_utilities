import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests

url = 'https://www.quora.com/Kasturba-Medical-College'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
df = pd.DataFrame({'question': [],'answers':[]})

# question = soup.find('span', {'class': 'ui_qtext_rendered_qtext'})
answers = soup.find_all('div', attrs={'id': 'page_wrapper'})

for answer in answers:
     df = df.append({'question': question.text,
        'answers': answer.text
          }, ignore_index=True)
df.to_csv(‘One_URLs.csv’)

