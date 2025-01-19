from os import listdir
from selenium.webdriver.common.by import By
from random import choice
from time import sleep
from typing import Final
from webdriver_manager.core.os_manager import OperationSystemManager,ChromeType
import undetected_chromedriver as UC
import logging

download_dir = '/Users/andreimorais/Desktop'
chrome_version = OperationSystemManager().get_browser_version_from_os(ChromeType.GOOGLE)
version_main=int(chrome_version.split('.')[0])
user_agents: Final = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            ]
options = UC.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument(f'--user-agent={choice(user_agents)}')
options.add_experimental_option(
    'prefs', {
        'download.default_directory': '/Users/andreimorais/Desktop',
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True,
    })
options.headless = True
driver = UC.Chrome(options=options, version_main=version_main)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

try:
    driver.get('https://ssstik.io/')
    sleep(2)
    text_input_element = driver.find_element(By.XPATH, "//div[@class='relative u-fw']//input[@id='main_page_text']")
    download_button = driver.find_element(By.XPATH,"//button[@id='submit']")
    text_input_element.send_keys('https://www.tiktok.com/@ofelipedabarbearia/video/7455798338642857221')
    download_button.click()
    sleep(2)

    hd_button = driver.find_element(By.XPATH, "//a[@id='hd_download']")
    hd_button.click()
    sleep(3)
    while any([f.endswith('.crdownload') for f in listdir('/Users/andreimorais/Desktop')]):
        print('aguardando download')
        sleep(1)
    print('finalizando o download')
except Exception  as e:
    print(e)
finally:
    driver.quit()