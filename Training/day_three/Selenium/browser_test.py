from time import sleep

from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    # options = Options()
    # options.arguments.extend(["--no-sandbox", "--disable-dev-shm-usage", "--remote-allow-origins=*"])

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    # chrome_options.add_argument('ignore-certificate-errors')
    # chrome_options.add_argument("test-type")
    # chrome_options.add_argument("disable-gpu")
    # chrome_options.add_argument("disable-infobars")
    # chrome_options.add_argument("disable-extensions")
    # chrome_options.add_argument("no-sandbox")
    # chrome_options.add_argument("disable-dev-shm-usage")
    # chrome_options.add_argument("remote-allow-origins=*")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # chrome_options.experimental_options['useAutomationExtension'] = False

    # service = service.Service('/usr/local/bin/chromedriver')
    # service.start()
    # driver = webdriver.Chrome(service=service, options=chrome_options)

    with webdriver.Chrome(options=chrome_options) as browser:
        browser.get('http://www.google.com/')
        # browser.get("https://www.lambdatest.com")

        '''
        browser.find_element(By.NAME, 'li1').click()
        browser.find_element(By.NAME, 'li2').click()

        title: str = 'Sample page - lambdatest.com'

        text_field = browser.find_element(By.ID, 'sampletodotext')
        text_field.send_keys('Checking my source code')

        sleep(5)

        browser.find_element(By.ID, 'addbutton').click()
        '''

        sleep(2)

        browser.quit()
