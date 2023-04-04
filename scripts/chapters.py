import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from scripts.data import DataScraper
from scripts.utils import make_request, get_total_pages, save_data


class ChapterScraper(DataScraper):
    def __init__(self):
        super().__init__()

    @staticmethod
    def generateChapterLinks(start_url):
        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)
        driver.get(start_url)

        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div[style="cursor: pointer;"]'))).click()
        time.sleep(2.5)

        totalPages = get_total_pages(False, driver)
        chapters = dict()
        currentPage = 0
        while currentPage < totalPages:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            scripts = soup.find_all('script')
            script_index = 3  # changes to 3 from 7 due to ranobes.net changed to ranobes.top
            dictionary_text = str(scripts[script_index]).replace('<script>window.__DATA__ = ', '').replace('</script>',
                                                                                                           '')
            data = json.loads(dictionary_text)
            for i in range(len(data['chapters'])):
                chapters[data['chapters'][i]['title']] = data['chapters'][i]['link']

            try:
                WebDriverWait(driver, 2).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'span.page_next'))).click()
                currentPage += 1
                print(f"Page {currentPage} done.")
            except TimeoutException:
                break
        driver.quit()
        return chapters, len(chapters)

    def newChaptersFound(self, name, start_url):
        links, new_total_chapters = self.generateChapterLinks(start_url)

        if self.data[name].get('Total Chapters') is not None:
            old_total_chapters = self.data[name]['Total Chapters']
            if old_total_chapters >= new_total_chapters:
                print('No New Chapters Found.')
                return False, None
            else:
                print('New Chapters Found.')
                self.data[name]['Total Chapters'] = new_total_chapters
                newChapters = new_total_chapters - old_total_chapters
                return True, newChapters
        else:
            self.data[name]['Chapter Links'] = links
            self.data[name]['Total Chapters'] = new_total_chapters
            return True, None

    def save_chapters(self, soup, chapter, name):
        body = ''
        for p in soup.select('div#arrticle p'):
            body += p.text + '\n\n'
        try:
            chapterNumber = re.findall(r'[\d+\.\d+|\d]+', chapter)
            if not chapterNumber:
                self.data[name]['Chapters'].append({'title': chapter, chapter: body})
            else:
                self.data[name]['Chapters'].append({'title': chapter, f'Chapter{chapterNumber[0]}': body})

        except Exception:
            self.data[name]['Chapters'] = list()
            chapterNumber = re.findall(r'[\d+\.\d+|\d]+', chapter)
            if not chapterNumber:
                self.data[name]['Chapters'].append({'title': chapter, chapter: body})
            else:
                self.data[name]['Chapters'].append({'title': chapter, f'Chapter{chapterNumber[0]}': body})

    def fetch_chapters(self, name, link):
        soup = make_request(link[1])
        chapter = link[0]
        self.save_chapters(soup, chapter, name)

        print('.', end="|", flush=True)

    def find_chapters(self, scraper, name):
        print('Getting Chapters..')
        start_time = time.time()
        start_url = self.data[name]['Chapter Link'].replace('100000', '1')
        true, chaptersFound = scraper.newChaptersFound(name, start_url)
        if not true:
            print(f"\nTotal Time Taken For Chapters:{time.time() - start_time}\n")
            return self.data[name]

        if chaptersFound is not None:
            links = list(self.data[name]['Chapter Links'].items())[:chaptersFound]
            with ThreadPoolExecutor(max_workers=8) as executor:
                executor.map(scraper.fetch_chapters, repeat(name), links)
            save_data(self)
            print('Chapters Scraped.')
            print(f"\nTotal Time Taken For Chapters:{time.time() - start_time}\n")
            return self.data[name]

        links = list(self.data[name]['Chapter Links'].items())
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(scraper.fetch_chapters, repeat(name), links)
        save_data(self)

        print('Chapters Scraped.')
        print(f"\nTotal Time Taken For Chapters:{time.time() - start_time}\n")
        return self.data[name]


def run_chapter_scraper(name):
    scraper = ChapterScraper()
    data = scraper.find_chapters(scraper, name)
    return data
