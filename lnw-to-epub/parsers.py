import cloudscraper
import time
from models import Update, Novel, Chapter
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

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

            updates.append(Update(title, latest, last_update, rank))

        
        return updates

    def get_chapters(self, novel_id):
        scraper = cloudscraper.create_scraper()

        page_num = 1
        
        chapters = []

        def get_chapter_contnent(page_url):
                chapter_content_raw = BeautifulSoup(scraper.get(page_url).content, 'lxml')
                chapter_content = chapter_content_raw.select('div.chapter-content')

                if len(chapter_content) > 0:
                    curr_chapter = chapter_content[0]
                    return curr_chapter.get_text('\n')
                else:
                    print(Style.RESET_ALL + Style.BRIGHT + Fore.WHITE + Back.RED + "RATE LIMITED WAITING 5 SECONDS" + Style.RESET_ALL)
                    time.sleep(5)
                    return get_chapter_contnent(page_url)

        def scrape_chapters(page):
            url = self.url + f'/novel/{novel_id}?tab=chapters&page={page}&chorder=asc'

            chapters_raw = BeautifulSoup(scraper.get(url).content, 'lxml')
            chapters_html = chapters_raw.select('ul.chapter-list > li')

            has_more_pages = len(chapters_raw.select('div.pagination-container > ul.pagination > li.PagedList-skipToNext')) > 0
            
            for item in chapters_html:
                title = item.select('a')[0].get('title')
                link = self.url + item.select('a')[0].get('href')
                chapter_number = item.get('data-chapterno')
                text = get_chapter_contnent(link)

                print(Style.RESET_ALL + Style.BRIGHT + Fore.GREEN + title + Style.RESET_ALL)

                chapters.append(Chapter(title, link, chapter_number, text))
                time.sleep(3)

            if has_more_pages:
                scrape_chapters(page + 1)
        
        scrape_chapters(page_num)

        for index, chapter in enumerate(chapters):
            print(f'#{index}: {chapter.title}')

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
