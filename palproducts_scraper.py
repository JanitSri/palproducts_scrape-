''' 
NAME: Janit Sriganeshaelankovan 
CREATED: November 19, 2017 - 02:40 (EDT)
GOAL: Web Scrape all the Products of Princess Auto 
ENVIRONMENT: Base 
LAST UPDATE: January 17, 2019 - 11:58 (EDT)
'''




import os
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
import datetime 

from chromedriverpath import CHROMEDRIVER_PATH


os.chdir(r'C:\Users\janit\Documents\GIT\pal_scraper')


# add chrome driver path 
chrome_driver = CHROMEDRIVER_PATH


pa_products = set()
len(pa_products)
loop_times = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
main_url = r'https://www.princessauto.com/en/search' 
urls = []
for x in range (0, 25400, 100):
    urls.append(main_url + '?Nrpp=100&No={}'.format(str(x)))

print(len(urls))

options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_driver, chrome_options=options)
driver.maximize_window()
    
for idx, u in enumerate(urls):
    start = time.time()
    print('On URL {0}: {1}'.format(str(idx), u))
    
    driver.get(u)
    source = driver.page_source 

    page_soup = soup(source, 'lxml')
    body = page_soup.body
    
    products = page_soup.find_all('a', {"class":'cta-magnify quickview-modal'})
    
    if products:
        print(len(products))
        for product in products:
            product_name = product['data-product-name']
            product_SKU = product['data-product-id']
            product_category = product['data-category-trail']
            pa_products.add((product_SKU, product_name, product_category))
    print('The length of the Product List is {}'.format(len(pa_products)))
    loop_times.append(time.time() - start)
    print('This loop took {}'.format(str(time.time() - start)))



with open('PA_PRODUCTS_ALL_{}.txt'.format(datetime.datetime.now().strftime('%d_%m_%Y')), 'a') as f:
    for x in pa_products:
        xx = ','.join(x)
        f.write(xx +'\n')


with open('PA_PRODUCTS_ALL_12_22_2018.csv', 'w', newline='') as f:
    header = ['SKU', 'PRODUCT NAME', 'PRODUCT CATEGORY']
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    for p in pa_products:
        writer.writerow({'SKU':p[0], 'PRODUCT NAME':p[1], 'PRODUCT CATEGORY':p[2]})
