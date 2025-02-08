import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from random import choice
from time import sleep
from typing import Final
from webdriver_manager.core.os_manager import OperationSystemManager,ChromeType
import undetected_chromedriver as UC
from platformdirs import user_documents_dir
from pathlib import Path
import logging

class Downloader:
    version_main: Final[int]
    driver: Final[UC.Chrome]
    download_dir: Final[str]
    actions: Final[ActionChains]
    executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=3)
    user_agents: Final[list] = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    ]

    def __init__(self):
        _doc_dir: Path = Path(user_documents_dir())
        _downloader_dir = _doc_dir / 'downloader'
        if _downloader_dir.exists():
            self.download_dir = str(_downloader_dir)
        else:
            _downloader_dir.mkdir()
            self.download_dir = str(_downloader_dir)
        _chrome_version: str = OperationSystemManager().get_browser_version_from_os(ChromeType.GOOGLE)
        self.version_main = int(_chrome_version.split('.')[0])
        _options: UC.ChromeOptions = UC.ChromeOptions()
        _options.add_argument('--disable-blink-features=AutomationControlled')
        _options.add_argument('--disable-dev-shm-usage')
        _options.add_argument('--start-maximized')
        _options.add_argument('--disable-gpu')
        _options.add_argument('--no-sandbox')
        _options.add_argument(f'--user-agent={choice(self.user_agents)}')
        _options.add_experimental_option(
            'prefs', {
                'download.default_directory': self.download_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True,
            })
        _options.headless = False
        self.driver: UC.Chrome = UC.Chrome(options=_options, version_main=self.version_main)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.actions = ActionChains(self.driver)


    def await_download(self):
        while any([f.endswith('.crdownload') for f in os.listdir(self.download_dir)]):
            sleep(1)


    def _download_tiktok_video(self, video_link: str):
        try:
            self.driver.get('https://ssstik.io/')
            text_input_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='relative u-fw']//input[@id='main_page_text']")))
            download_button = self.driver.find_element(By.XPATH, "//button[@id='submit']")

            text_input_element.send_keys(video_link)
            download_button.click()
            sleep(2)

            hd_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='hd_download']")))
            self.actions.move_to_element(hd_button).click().perform()
            sleep(3)
            self.await_download()

        except Exception as e:
            print(e)
        finally:
            self.driver.quit()


    def _download_instagram_video(self, video_link: str):
        try:
            self.driver.get('https://sssinstagram.com/pt')
            sleep(2)
            text_input_element = self.driver.find_element(By.XPATH, "//input[@id='input']")
            text_input_element.send_keys(video_link)
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()


            download_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button button--filled button__download']")))
            self.actions.move_to_element(download_button).click().perform()
            sleep(2)
            self.await_download()
        except Exception as e:
            print(e)
        finally:
            self.driver.quit()


    async def download_video_async(self, video_link: str):
        loop = asyncio.get_running_loop()
        if 'instagram' in video_link:
            await loop.run_in_executor(self.executor, self._download_instagram_video, video_link)
        elif 'tiktok' in video_link:
            await loop.run_in_executor(self.executor, self._download_tiktok_video, video_link)
        elif 'facebook' in video_link:
            raise NotImplementedError()
        else:
            raise NotImplementedError()