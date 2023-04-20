import json
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import os


os.environ['PATH'] += "/usr/local/bin/chromedriver"



options = Options()

options.add_argument('lang=en') 
options.add_argument('--headless') 
options.add_argument('--no-sandbox')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')




options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})


chrome_driver_path = '/snap/bin/chromium.chromedriver'

ser = Service(chrome_driver_path)


#driver = webdriver.Chrome(ChromeDriverManager().install())
driver = webdriver.Chrome(service=ser, chrome_options=options)
# driver = webdriver.Chrome(executable_path=chrome_driver_path)


driver.get("http://143.106.73.50:30002/samples/dash-if-reference-player/demo.html")
print(driver.title)
search_bar = driver.find_element_by_name("q")
search_bar.clear()
search_bar.send_keys("getting started with python")
search_bar.send_keys(Keys.RETURN)
print(driver.current_url)
driver.close()
