import requests
from bs4 import BeautifulSoup
import json
import random
import sys

with open("proxies.txt") as file:
    proxies = [line.strip() for line in file.readlines()]

upc = sys.argv[1]  
useProxy = sys.argv[2]

if len(upc) < 12:
    upc = upc.zfill(12) 

ean_key = "EAN"
ean_value = ""
upc_key = "UPC"
upc_value = ""
category_key = "Category"
category_value = ""
description_key = "Description"
description_error_key = "Description"
description_value = ""
additional_attributes_key = "Additional Attributes"
additional_attributes_value = ""
name_key = "Name"
name_value = ""
img_key = "IMG"
img_value = ""
status_key = "Status"
status_value = "OK"
msg = ""

proxy = random.choice(proxies)

proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
}

url = 'https://go-upc.com/search?q='+upc

try:
    if useProxy == 1:
        response = requests.get(url, proxies=proxies)
    else:
        response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.Timeout:
    msg = "Error: Waiting time exhausted when making the request."
except requests.exceptions.SSLError as e:
    msg = ("Error de SSL:", e)
except requests.exceptions.RequestException as e:
    msg = ("Failed to make the request:", e)
   
if msg != "":
    status_value="ERROR"
    data = {
        status_key: status_value,
        description_error_key: msg
    }
    json_response = json.dumps(data, default=str)
    print(json_response)
    exit()

content = response.text

soup = BeautifulSoup(content, 'html.parser')

table = soup.find('table', class_='table table-striped')
rows = table.find_all('tr')

data = {}
for row in rows:
    cells = row.find_all('td')
    if len(cells) == 2:
        label = cells[0].text.strip()
        value = cells[1].text.strip()
        data[label] = value

for label, value in data.items():
    if label == ean_key:
        ean_value = value

    if label == upc_key:
        upc_value = value

    if label == category_key:
        category_value = value  

product_container_left = soup.find('div', class_='left-column')
product_container_right = soup.find('div', class_='right-column')

name_value = product_container_left.find('h1', class_='product-name').text.strip()
image_element = product_container_right.find('img')
img_value = image_element['src']
description_section = product_container_left.find_all('div')

counter = 0
attributes_dict = {}
for div in description_section:
    counter +=1
    if counter == 2:
        description_value = div.find('span').text.strip()
    if counter == 3:
        additional_attributes_value = div.find('ul')
        if additional_attributes_value:
            li_elements = additional_attributes_value.find_all('li')
            for li in li_elements:
                span_text = li.find('span', class_='metadata-label').text.strip(':')
                other_text = li.text.split(':', 1)[1].strip()
                attributes_dict[span_text] = other_text

data = {
    status_key: status_value,
    name_key: name_value,
    ean_key: ean_value,
    upc_key: upc_value,
    category_key: category_value,
    img_key: img_value,
    description_key: description_value,
    additional_attributes_key: attributes_dict
}

json_response = json.dumps(data)

print(json_response)
