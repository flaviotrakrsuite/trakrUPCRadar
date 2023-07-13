import requests
from bs4 import BeautifulSoup
import json
import random

proxies = [
    '117.69.232.171:8089',
    '183.164.243.213:8089',
    '36.6.145.119:8089',
    '47.96.143.117:80',
    '39.175.92.35:30001',
    '111.20.217.178:9091',
    '200.110.169.203:999',
    '167.250.29.235:3128',
    '45.133.168.157:8080',
    '103.167.134.31:80',
    '72.52.91.126:3128',
    '138.91.159.185:80',
    '177.10.201.171:9812',
    '103.178.12.166:3030',
    '103.155.54.26:83',
    '5.189.144.84:3128',
    '45.180.16.210:9292',
    '41.203.83.66:8080',
    '45.5.92.94:8137',
    '45.167.90.69:999',
    '146.83.128.23:80',
    '64.225.8.191:9999',
    '112.111.1.217:4430',
    '201.71.2.115:999',
    '81.169.204.107:8080',
    '43.255.113.232:84',
    '75.89.101.63:80',
    '103.127.38.46:7070',
    '177.12.220.252:8080',
    '187.141.184.235:8080',
    '138.121.161.82:8290',
    '124.131.219.94:9091',
    '186.167.67.36:8080',
    '24.152.40.49:8080',
    '116.68.170.115:8019'
]

ean_key = "EAN"
ean_value = ""
upc_key = "UPC"
upc_value = ""
category_key = "Category"
category_value = ""
description_key = "Description"
description_value = ""
additional_attributes_key = "Additional Attributes"
additional_attributes_value = ""
name_key = "Name"
name_value = ""
img_key = "IMG"
img_value = ""

proxy = random.choice(proxies)

proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
}

url = 'https://go-upc.com/search?q=05530011001'
#url = 'https://go-upc.com/search?q=052000014778'

response = requests.get(url, proxies=proxies)
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
    #print(label + ':', value)    

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
