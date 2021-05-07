# This file contains a Scrapy spider to extract review summaries from
# Metacritic.com

import sqlite3
import scrapy
from tqdm import tqdm

# get links to critics reviews
cnn = sqlite3.connect('games.db')
cnn.execute('PRAGMA foreign_keys = ON')
cur = cnn.cursor()
cur.execute('SELECT reviews_link from games')
links = cur.fetchall()
links_ls = ['https://www.metacritic.com' + link[0] for link in links]

# Create table to contain critics reviews
cur.execute('DROP TABLE critics_reviews')
cur.execute('''create table critics_reviews(
            title text,
            platform text,
            body text,
            reviewer text,
            score integer,
            link text,
            FOREIGN KEY(title, platform) REFERENCES games(title, platform))''')
cnn.commit()

# post-process extracted strings
def extract_value(value):
    return value if value is None else value.strip()

# progress bar
num_lines = len(links_ls)
pbar = tqdm(total=num_lines, desc="Scrapping",
            ascii=True, mininterval=0.3, unit="games")

# spider
class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    start_urls = links_ls
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'RETRY_TIMES': 500,
    }

    def parse(self, response):
        ga = extract_value(response.css('div.product_title a h1::text').get())
        pl = extract_value(response.css('span.platform::text').get())
        if pl == '':
            pl = extract_value(response.css('span.platform a::text').get())

        num_reviews = len(response.css('div.source').getall())
        for x in range(0, num_reviews):
            review = response.css("div[class='review_section']")[x]
            bo = extract_value(review.css('div.review_body::text').get())
            re = extract_value(review.css('div.source::text').get())
            sco = extract_value(review.css(
                'div.review_grade div::text').get())
            lk = extract_value(review.css('div.source a.external::attr(href)'
                                          ).get())
            if lk != None:
                re = extract_value(
                    review.css('div.source a.external::text').get())
            d = [(ga, pl, bo, re, sco, lk)]
            cur.executemany(
                'insert into critics_reviews values (?, ?, ?, ?, ?, ?)', d)
            cnn.commit()
        pbar.update(1)
