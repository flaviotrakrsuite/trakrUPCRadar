import requests
from bs4 import BeautifulSoup
import sys
import json

upc = sys.argv[1]  

if len(upc) < 12:
    upc = upc.zfill(12) 

url = "https://upcitemdb.com/upc/"+upc

img_key = "IMG"
img_value = ""
status_key = "Status"
status_value = "OK"
description_error_key = "Description Error"
description_error_value = ""

data = {}

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    info_table = soup.find('table', class_='detail-list')
    img_tag = soup.find('img', class_='product')

    if img_tag:
        img_value = img_tag['src']

    if info_table:

        for row in info_table.find_all('tr'):
            cells = row.find_all('td')
            
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                
                data[key] = value

        data[img_key] = img_value
        data[status_key] = status_value

        json_response = json.dumps(data)

        print(json_response)
    else:
        status_value = "ERROR"
        data[status_key] = status_value
        description_error_value = "Information table not found."
        data[description_error_key] = description_error_value
        
        json_response = json.dumps(data)

        print(json_response)
else:
    status_value = "ERROR"
    data[status_key] = status_value
    description_error_value = ("The page could not be accessed:", url)
    data[description_error_key] = description_error_value
    
    json_response = json.dumps(data)

    print(json_response)
