import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

url = 'https://www.barcodelookup.com/885909918164'
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

product_name = soup.find('h1', class_='product-name').text.strip()
barcode_formats = [item.text.strip() for item in soup.select('.formats-list .format-name')]
category = soup.find('td', text='Category').find_next('td').text.strip()
manufacturer = soup.find('td', text='Manufacturer').find_next('td').text.strip()
description = soup.find('div', class_='description').text.strip()
features = soup.find('div', class_='features').text.strip()

attributes_dict = {}
attributes_table = soup.find('table', class_='attributes-table')
if attributes_table:
    rows = attributes_table.find_all('tr')
    for row in rows:
        label = row.find('td', class_='attr-label').text.strip()
        value = row.find('td', class_='attr-value').text.strip()
        attributes_dict[label] = value

print("Nombre del producto:", product_name)
print("Formatos de códigos de barras:", barcode_formats)
print("Categoría:", category)
print("Fabricante:", manufacturer)
print("Descripción:", description)
print("Características:", features)
print("Atributos:", attributes_dict)
