import requests
from bs4 import BeautifulSoup
import sys

upc = sys.argv[1]  

if len(upc) < 12:
    upc = upc.zfill(12) 

url = "https://upcitemdb.com/upc/"+upc

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    info_table = soup.find('table', class_='detail-list')

    if info_table:
        data = {}

        for row in info_table.find_all('tr'):
            cells = row.find_all('td')
            
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                
                data[key] = value

        print(data)
    else:
        print("Information table not found.")
else:
    print("The page could not be accessed:", url)
