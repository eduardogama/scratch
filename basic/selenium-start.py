from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


import sys

user = sys.argv[1] if len(sys.argv) > 1 else "anonymous"

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


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-application-cache')
options.add_argument('--media-cache-size=1')
options.add_argument('--disk-cache-dir=/dev/null')
options.add_argument('--disable-gpu')
options.add_argument('--incognito')
options.add_argument('--new-window')

display = Display(visible=0, size=(1024, 768))
display.start()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("http://143.106.73.50:30002/samples/ericsson/vod-client.html?userid={}".format(user))

WebDriverWait(driver, 634).until(WaitLoad())
            

driver.quit()
display.stop()

