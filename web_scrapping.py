import requests
import time
import urllib.request
from bs4 import BeautifulSoup
import re


def get_product_id(soup):
    product_id = int(soup.find('p', {'class' : 'pdp-main-block__product-code'}).find('span').text)
    return product_id


def get_name(soup):
    name = soup.find('h1', {'class' : 'pdp-main-block__product-name'}).text
    return name.strip()


# Download Photos and keep directory reference
def get_photo_links(soup):
    links = []
    images = soup.find_all('div', {'class' : 'pdp-main-slider__content-inner'})
    for image in images:
        image_link = image.find('img')

        link = image_link['src']

        links.append(link)
    return links


def get_photo(link):
    link_split = link.split('/')
    name = link_split[-2] + link_split[-1]
    print(name)
    urllib.request.urlretrieve(link, name)


# Get Summary
def get_summary(soup):
    if soup.find('p', {'class': 'pdp-product-features__detail-summary'}):
        summary = soup.find('p', {'class': 'pdp-product-features__detail-summary'}).text
    else:
        summary = ''
    return summary.strip()


# Get specifications
def get_spec(soup):
    spec_list = []
    specs = soup.find('div', {'id': 'details-specification'}).find_all('tr')
    for spec in specs:
        if spec.find('th'):
            key = spec.find('th').text
            value = spec.find('td').text
            spec_list.append([key, value])
    return spec_list


# Get Warranty
def get_warranty(soup):
    warrantys = soup.find('div', {'id': 'details-warranty'}).find_all('tr')
    for warranty in warrantys:
        key = warranty.find('th').text
        value = warranty.find('td').text
        print(key + ' : ' + value)


# Get Product Links

def get_number_of_pages(arr):
    marker = 0
    for string in arr:
        if marker == 1:
            return int(string)
        elif string == "of":
            marker = 1
    return 0


def get_product_links(page_url):

    page = requests.get(page_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find('select', {'class': 'product-listing__pagination-control--page'}).find('option').text
    results = results.split(" ")
    pages = get_number_of_pages(results)

    start = 0
    url_query_start = '/?pageNumber='
    url_query_end = '&pageSize=15'
    links = []

    for x in range(pages):
        time.sleep(1)
        new_url = page_url + url_query_start + str(x) + url_query_end
        new_page = requests.get(new_url)

        new_soup = BeautifulSoup(new_page.content, 'html.parser')

        products = new_soup.find_all('div', {'class': 'product-tile'})

        for product in products:
            a = product.find('a')
            link = a['href']
            links.append(link)

    return links




