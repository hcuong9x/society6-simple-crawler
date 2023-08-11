import csv
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By

from core.config import Config
from libs.shopify_csv.shopify_csv import ShopifyCsv
from slugify import slugify
from inc.constant import product_element as element
from selenium.common.exceptions import NoSuchElementException


class Society6(ShopifyCsv):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        store_info = Config('config/store.ini')
        self.brand = store_info.get_config('store', 'brand')

    def crawler(self, url):
        """crawl a society6 product by url to simple product"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options)
        self.driver = driver
        driver.get(url)
        
        # set an implicit wait of 10 seconds
        driver.implicitly_wait(10)

        title = self.get_element_by_xpath(element['title_xpath'], 'text')
        self.click_element(element['next_slider_btn'],5)
        
        images = self.get_element_by_xpath(element['image_xpath'], 'images')

        # close the webdriver instance
        driver.quit()

        self.create_simple_product(title, images) 

    def click_element(self, xpath, times):
        driver = self.driver
        images = driver.find_elements(By.XPATH, element['image_xpath'])

        count = len(images)
        if count > 1:
            btn_next = driver.find_element(By.XPATH, xpath)
            for j in range(1, count+1):
                btn_next.click()
                time.sleep(1)

    def get_element_by_xpath(self, xpath, type):
        driver = self.driver
        value = ''

        if type == 'text':
            ele = driver.find_element(By.XPATH, xpath)  
            value = ele.text
        elif type == 'images':
            eles= driver.find_elements(By.XPATH, xpath) 
            image_urls = [img.get_attribute("src") for img in eles]
            value = image_urls

        return value
    
    def create_simple_product(self, title, gallery_images):
        if title == '' or len(gallery_images) == 0:
            print('Get title or images fail!')
            return
        
        handle = self.generate_handle(title)
        shopify_item = self.create_shopify_item(handle, title)

        with open('spf_products.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for i, item in enumerate(gallery_images):
                index = i + 1
                shopify_item = self.update_shopify_item_image(shopify_item, item, index, title)
                is_row_image = False if i == 0 else True
                rows = self.get_shopify_row(shopify_item, index, is_row_image)
                for row in rows:
                    writer.writerow(row)

    def generate_handle(self, product_title):
        handle = slugify(str(product_title))
        handle += f'-{random.randint(1000, 9999)}'
        return handle

    def create_shopify_item(self, handle, title):
        shopify_item = {}
        shopify_item['handle'] = handle
        shopify_item['title'] = title
        shopify_item['body_html'] = ''
        shopify_item['type'] = ''
        shopify_item['tags'] = ''
        shopify_item['variant_price'] = 0
        return shopify_item

    def update_shopify_item_image(self, shopify_item, image_src, index, product_title):
        shopify_item['image_src'] = image_src
        shopify_item['image_position'] = index
        shopify_item['image_alt_text'] = ""

        return shopify_item