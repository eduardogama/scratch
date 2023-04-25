import os
import sys
import unittest

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

"""
A simple selenium test example written by python
"""


urlBase = "http://143.106.73.50:30002/samples/ericsson/vod-client.html"


class WaitLoad:
    def __call__(self, driver):
        response = driver.execute_script(
        """
            try {
                return window.player.time() >= 600;
            } catch (e) {
                return e.message;
            }
        """
        )

        return response if type(response) == bool else False

class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
    
        self.user = sys.argv[1] if len(sys.argv) > 1 else "anonymous"
        
        os.makedirs('browser/' + self.user, exist_ok = True)
        
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--user-data-dir=browser/' + self.user)
        chrome_options.add_argument('--verbose')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'browser': 'INFO'}

        self.driver = webdriver.Chrome(
            options=chrome_options,
            desired_capabilities=caps,
            service=Service(ChromeDriverManager().install()),
        )
        
    def tearDown(self):
        """Stop web driver"""
        self.driver.get_screenshot_as_file(
            "screenshot/example-{}.png".format(self.user)
        )
        self.driver.quit()
        
    def test_case_1(self):
        """Watching BBB Video Streaming"""
        
        try:
            print("Starting", urlBase, "...")
            
            self.driver.get(urlBase)

            print("Starting BBB Video Streaming ...")
            self.driver.execute_script(
                "init('{}')".format(self.user)
            )

            print("Sending QoE Player from BBB Video Streaming ...")            
            self.driver.execute_script(
                "sendQoE(player, '{}')".format(self.user)
            )
            
            WebDriverWait(self.driver, 634).until(WaitLoad())
            
        except Exception as e:
            print(e)


if __name__ == '__main__':    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplate)
    unittest.TextTestRunner(verbosity=2).run(suite)
