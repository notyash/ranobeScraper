import time
from difflib import get_close_matches

from scripts.novels import NovelScraper
from scripts.utils import undetected_request, save_data


class DataScraper(NovelScraper):
    def __init__(self):
        super().__init__()

    def take_input(self, title):
        name = title
        all_novels = list(self.data.keys())
        try:
            novel = get_close_matches(name, all_novels)[0]
        except IndexError:
            print('Invalid name.')
            return False, False

        return self.data[novel]['link'], novel

    @staticmethod
    def get_title(soup):
        title = soup.select_one('h1.title span').get_text().encode("ascii", "ignore").decode()
        return title

    @staticmethod
    def get_description(soup):
        description = \
            soup.select_one('div[class="moreless cont-text showcont-h"]').get_text(strip=True).encode(
                "ascii", "ignore").decode().split('Read more')[1].replace('Collapse', '').replace('\u2019', '')

        return description

    @staticmethod
    def get_rating(soup):
        rating = soup.select_one('div[class="rate-stat-num"] span[class="bold"]').get_text(strip=True).encode(
            "ascii", "ignore").decode()

        return rating

    @staticmethod
    def get_image_link(soup):
        image_link = soup.select_one('div[class="poster"] a')['href']

        return image_link

    @staticmethod
    def get_genres(soup):
        genres = list()
        for genre in soup.select('div#mc-fs-genre a'):
            genres.append(genre.get_text(strip=True).encode("ascii", "ignore").decode())

        return genres

    @staticmethod
    def get_details(soup):

        details = dict()
        for detail in soup.select('div.r-fullstory-spec ul li'):
            keyValue = detail.get_text(strip=True).encode("ascii", "ignore").decode().split(':')
            details[keyValue[0].replace(' ', '_')] = keyValue[1]

        return details

    def find_data(self, title):
        link, novel = self.take_input(title)
        if not novel:
            return False
        start_time = time.time()
        print(f'\nGetting Data For {novel}..')
        if self.data[novel].get('Title') is not None:
            print("Data already available.")
            print(f"\nTotal Time Taken For Data: {time.time() - start_time}\n")
            return novel
        soup = undetected_request(link)
        self.data[novel]['Title'] = self.get_title(soup)
        self.data[novel]['Description'] = self.get_description(soup)
        self.data[novel]['Rating'] = self.get_rating(soup)
        self.data[novel]['ImageLink'] = self.get_image_link(soup)
        self.data[novel]['Genres'] = self.get_genres(soup)
        self.data[novel]['Details'] = self.get_details(soup)

        save_data(self)
        print('Data Scraped.')
        print(f"\nTotal Time Taken For Data: {time.time() - start_time}\n")

        return novel


def run_data_scraper(title):
    scraper = DataScraper()
    novel = scraper.find_data(title)
    return novel
