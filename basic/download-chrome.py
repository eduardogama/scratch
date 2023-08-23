import os
import sys
import randomname

from selenium import webdriver

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


"""
A simple selenium test example written by python
"""


"""Start web driver"""
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

service = Service() # Service(ChromeDriverManager().install())

driver = webdriver.Chrome(
    options=chrome_options,
    service=service,
)

driver.quit()
