import cloudscraper
from models import Update, Novel
from bs4 import BeautifulSoup

class LightNovelWorld:

    def __init__(self):
        self.url = 'https://lightnovelworld.com/'

        self.name = 'LightNovelWorld'


    def get_updates(self):
        scraper = cloudscraper.create_scraper()

        url = self.url + 'updates'

        updates_raw = BeautifulSoup(scraper.get(url).content, 'lxml')
        updates_html = updates_raw.select('li.novel-item > a')

        updates = []

        for item in updates_html:
            title = item.find('h4').text.strip()
            latest = item.find('h5').text.strip()
            last_update = item.select('div.novel-stats > span')[0].text.strip()
            rank = item.select('div.novel-stats > span')[1].text.strip()

            updates.append(Update(title, latest, last_update, rank).get_info())

        
        return updates

    def get_novel(self, novel_id):
        scraper = cloudscraper.create_scraper()

        url = self.url + f'novel/{novel_id}'

        novel_raw = BeautifulSoup(scraper.get(url).content, 'lxml')
        novel_info = novel_raw.select('div.novel-info')[0]

        novel_head = novel_info.select('div.main-head')[0]
        novel_stats = novel_info.select('div.header-stats')[0]
        novel_categories = novel_info.select('div.categories')[0]

        title = novel_head.find('h1').text.strip()
        author = novel_head.select('div.author > a > span')[0].text.strip()
        
        rank = novel_head.select('div.rating > div.rank > strong')[0].text.strip()
        # normally it looks like "RANK ###" but I wanted to remove the rank part to just have the numbner
        rank = [str(s) for s in rank.split() if s.isdigit()][0]

        rating = novel_head.select('div.rating > div.rating-star > p > strong')[0].text.strip()
        chapters = novel_stats.select('span > strong')[0].text.strip()
        views = novel_stats.select('span > strong')[1].text.strip()
        bookmarked = novel_stats.select('span > strong')[2].text.strip()
        status = novel_stats.select('span > strong')[3].text.strip()
        last_update = novel_info.select('div.updinfo > strong')[0].text.strip()
        categories = []

        for item in novel_categories.select('ul > li > a'):
            categories.append(item.text.strip())
        
        return Novel(title, author, rank, rating, chapters, views, bookmarked, status, categories, last_update)
