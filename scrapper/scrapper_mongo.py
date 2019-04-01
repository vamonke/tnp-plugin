# import libraries
import csv
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tnf"]
table = mydb["articles"]

browser = webdriver.PhantomJS()

def scrap_article(url):
  # article_page = urlopen(url)
  # soup = BeautifulSoup(article_page, 'html.parser')
  browser.get(url)
  html = browser.page_source
  soup = BeautifulSoup(html, 'lxml')

  headline = soup.find('h1', attrs={'class': 'story-headline'}).get_text()
  published_date = soup.find('div', attrs={'class': 'story--published-date'}).get_text()
  published_date = datetime.strptime(published_date, '%b %d, %Y %I:%M %p') # Mar 11, 2019 06:00 am
  # print(published_date)
  category = soup.find('div', attrs={'class': 'story--web-category'}).get_text()
  tag = soup.find('div', attrs={'class': 'story--keyword'}).get_text().upper()

  # Standfirst
  standfirst = ''
  standfirst_tag = soup.find('h3', attrs={'class': 'standfirst'})
  if (standfirst_tag):
    standfirst = standfirst_tag.get_text()

  # Lead
  lead = ''
  lead_tag = soup.find('p', attrs={'class': 'lead'})
  if lead_tag:
    lead = lead_tag.get_text()
  
  # Image URL source
  img = soup.select('.group-media-frame > img')
  img_src = ''
  if img and img[0]:
    img_src = img[0]['src']
    if img_src[0] == '/':
      img_src = 'https://www.tnp.sg' + img_src

  # Engagements: Shares, Comments, Reactions
  engagements_tag = soup.find('li', attrs={'class': 'share-count'})
  engagement_count = engagements_tag.find('span', attrs={'class': 'share-count-figure'}).get_text()

  engagements_arr = engagements_tag['title'].split(' ')
  if (len(engagements_arr) > 7):
    shares = engagements_arr[0]
    comments = engagements_arr[3]
    reactions = engagements_arr[6]
  else:
    shares = 0
    comments = 0
    reactions = 0

  story = {
    'url': url,
    'headline': headline,
    'breaking': False,
    'published_date': published_date,
    'standfirst': standfirst,
    'category': category,
    'tag': tag,
    'fb_engagements': int(engagement_count),
    'fb_shares': int(shares),
    'fb_comments': int(comments),
    'fb_reactions': int(reactions),
    'lead': lead,
    'img_src': img_src,
  }

  return story

start_time = time.time()

urls = [
  'https://www.tnp.sg', # tnp
  'https://www.tnp.sg/lifestyle/hed-chef', # hedchef
  'https://www.tnp.sg/news/singapore', # singapore
  'https://www.tnp.sg/tag/food-drink', # fooddrink
  'https://www.tnp.sg/entertainment' # entertainment
]

for url in urls:
  homepage = urlopen(url)

  soup = BeautifulSoup(homepage, 'html.parser')
  links = soup.select('.card-title > a')

  for index, link in enumerate(links):
    print(link['href'])
    # story = scrap_article(link['href'])
    try:
      story = scrap_article(link['href'])
      if url == 'https://www.tnp.sg' and index < 5:
        story['breaking'] = True
      # insert to mongo db
      # print(story)
      # table.insert_one(story)
      table.update_one({ 'headline': story['headline'] }, { '$set': story }, True)
    except:
      print('failed')
    # break

# urls = [
#   "https://www.tnp.sg/news/singapore/ex-gm-town-council-contractor-plead-guilty-bribery",
# ]

# for url in urls:
#   story = scrap_article(url)
#   print(story['img_src'])
#   table.update_one({ 'headline': story['headline'] }, { '$set': story }, True)

elapsed_time = time.time() - start_time
print('\r\nElapsed time: ' + str(round(elapsed_time, 2)) + 's')