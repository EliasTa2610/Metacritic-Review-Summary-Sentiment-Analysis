# Metacritic Review Summary Sentiment Analysis

# Introduction

As part of its review aggregation process, Metacritic.com tries to give an idea of the contents of a critic review by quoting parts of it. The goal of this project is to assess the effectiveness of Metacritic's review summarization methods in conveying the overall sentiment of a review.

Review summaries are scraped for each video game listed on the webpage https://www.metacritic.com/browse/games/score/metascore/all/all/filtered and analyzed for sentiment using neural networks.

# Technical
* Dataset scraped with Scrapy and stored with SQLite. Spiders in 'games.py' and 'analyze.py' adapted from https://github.com/Markel/metacritic-crawler (credit to @Markel). Please visit page for more details on usage.
* To run spider in 'reviews.py', simply run
```console
scrapy runspider games.py
```
* Jupyter notebook metacritic_sent_analy.ipynb was run on Google Colab Pro
* To view progress bars shown at training step properly, install pywidgets. You can do so at the beginning of the notebook by executing
```console
!pip install ipywidgets
```
* Written for Python 3
* Uses Scrapy, SQLite, PyTorch, NLTK, TextBlob, Pandas along with standard libraries
* Uses the 50d GloVe embedding provided by the Stanford NLP group. If you wish to run the notebook you must have the corresponding file in your working directory. To obtain it, run the following commands from a terminal:
```console
wget http://nlp.stanford.edu/data/glove.6B.zip
unzip -j glove.6B.zip '*50d*'
rm glove.6B.zip
```
Alternatively, you can run these commands from the notebook by preprending each with an exclamation mark.

# Other
* Scraped data is not included as it is protected by copyright
* Trained PyTorch model can be downloaded here: https://drive.google.com/file/d/1bvuXoIZTcbkxD52zDc1dB-I0Nq6o84Fm/view?usp=sharing
