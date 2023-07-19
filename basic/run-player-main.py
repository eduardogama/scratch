import os
import sys
import randomname

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



"""
A simple selenium test example written by python
"""

abrStrategy = sys.argv[1] if len(sys.argv) > 1 else "abrDynamic"
user = sys.argv[2] if len(sys.argv) > 2 else randomname.get_name()


class WaitLoad:
    def __call__(self, driver):
        response = driver.execute_script(
        """
            try {
                return window.player.time() >= 10;
            } catch (e) {
                return e.message;
            }
        """
        )

        return response if type(response) == bool else False


"""Start web driver"""
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--disk-cache-dir=/dev/null')
chrome_options.add_argument("--no-user-gesture-required")
chrome_options.add_argument('--user-data-dir=users/' + user)

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'browser': 'INFO'}

driver = webdriver.Chrome(
    options=chrome_options,
    desired_capabilities=caps,
    service=Service(ChromeDriverManager().install()),
)

"""Watching BBB Video Streaming"""
driver.get(
    "http://143.106.73.50:30002/samples/ericsson/vod-client.html?abrStrategy={}&userid={}".format(abrStrategy, user)
)

#driver.execute_script(
#    "init('{}')".format(user)
#)

#driver.execute_script(
#    "sendQoE(player, '{}')".format(user)
#)

WebDriverWait(driver, 634).until(WaitLoad())


"""Stop web driver"""
driver.get_screenshot_as_file(
    "{}/screenshot.png".format(user)
)

driver.quit()
