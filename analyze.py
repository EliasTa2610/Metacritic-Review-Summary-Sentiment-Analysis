# This file gets the information of the games you have collected
# previously on games.py
# The program runs using 'scrapy runspider analyze.py'
# This file should take around 2 hours to completed
# This file is NOT a final build, expect MANY bugs, especially skipping games
# crawl.
# You bear all responsibility about the use of this program

import scrapy
import sqlite3
import re
from tqdm import tqdm

# --------------------------OPEN GAME LINKS FILE-----------------------------


def parse_url(route):
    return 'https://www.metacritic.com' + re.findall(r'\"(.+?)\"', route)[1]


with open("gm.jl", "r") as myfile:
    games_list = [parse_url(line) for line in myfile]
    # Detect how many lines are for the loading bar
    num_lines = 0
    for line in games_list:
        if line.strip():
            num_lines += 1

# ------------------------------SQLITE STUFF---------------------------------

# Special thanks to hypertaboo for his code:
# https://gist.github.com/hypertaboo/4464096
# It creates a SQLite database (take care that it doesn't already exist)
cnn = sqlite3.connect('games.db')
cnn.execute('PRAGMA foreign_keys=ON')
mycursor = cnn.cursor()

# Create the games table
sql_new_table = '''create table games(
title text,
platform text,
company text,
release text,
description text,
metascore integer,
critics_desc text,
critics_count integer,
rating text,
reviews_link text,
PRIMARY KEY(title, platform))'''
mycursor.execute(sql_new_table)
cnn.commit()


# ---------------------------DEFINING THE SPIDER-----------------------------
def extract_value(res, text_path):
    value = res.css(text_path).get()
    return value if value is None else value.strip()


pbar = tqdm(total=num_lines, desc="Scrapping", ascii=True, mininterval=0.3,
            unit="games")


class DetailsSpider(scrapy.Spider):
    name = "Details"
    start_urls = games_list
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'RETRY_TIMES': 500,
    }

# ---------------------------------CRAWL------------------------------------
    def parse(self, response):
        # Title
        ti = extract_value(response,
                           '''.product_title a.hover_none h1 ::text''')
        # Platform
        pl = extract_value(response, '''.product_title span.platform::text''')
        if pl == '':
            pl = extract_value(
                response, '''.product_title span.platform a::text''')
        # Company
        c = extract_value(
            response,
            '''div.product_data ul.summary_details li.publisher span.data
            a::text''')
        # Release Date
        r = extract_value(response, '''div.product_data ul.summary_details
                          li.release_data span.data::text''')
        # Game description
        d = extract_value(response, '''div.product_details
                          div.main_details ul.summary_details
                          li.summary_detail span.data span.inline_collapsed
                          span.blurb_expanded::text''')
        # Metascore
        cs = extract_value(response, '''.metascore_w span::text''')
        # Critics Description
        cd = extract_value(response, '''div.summary p span.desc::text''')
        # Critics Count
        cn = extract_value(response, '''div.summary p span.count a span
                           ::text''')
        # Rating (ESRB)
        rt = extract_value(response, '''div.product_details
                           div.side_details ul.summary_details
                           li.product_rating span.data::text''')
        # Link to reviews
        rl = extract_value(response, '''div.summary p span.count
                           a::attr(href)''')

# -------------------------INSERT DATA INTO THE SQL---------------------------

        # Establishing all the variable in one single variable
        game_d = [(ti, pl, c, r, d, cs, cd, cn, rt, rl)]

        # Inserting the data on the SQL database
        mycursor.executemany('''insert into games values (?, ?, ?, ?, ?,
                             ?, ?, ?, ?, ?)''', game_d)
        cnn.commit()
        # Update the progress bar
        pbar.update(1)
