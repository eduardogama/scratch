from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER="geckodriver"
service = Service(executable_path=DRIVER)
driver = webdriver.Firefox(service=service)
