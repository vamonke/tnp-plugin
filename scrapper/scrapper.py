# import libraries
import csv
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

def scrap_article(url):
  article_page = urlopen(url)
  soup = BeautifulSoup(article_page, 'html.parser')

  headline = soup.find('h1', attrs={'class': 'story-headline'}).get_text()
  published_date = soup.find('div', attrs={'class': 'story--published-date'}).get_text()
  keywords = soup.find('div', attrs={'class': 'story--keyword'}).get_text()
  tag = soup.find('div', attrs={'class': 'story--web-category'}).get_text()
  
  img = soup.select('.group-media-frame > img')
  img_src = ''
  if img and img[0]:
    img_src = img[0]['src']

  body_copy = ''
  lead = ''
  paragraphs = soup.select('.body-copy > p')
  for p in paragraphs:
    p_class = p.get('class')
    if p_class and p_class[0] == 'lead':
      lead = p.get_text()
    else:
      body_copy += p.get_text()

  return [url, headline, published_date, keywords, tag, lead, body_copy, img_src]

start_time = time.time()

tnp = 'https://tnp.sg'
homepage = urlopen(tnp)
soup = BeautifulSoup(homepage, 'html.parser')
links = soup.select('.card-title > a')

with open('tnp_stories.csv', 'a', newline='') as csv_file:
  for link in links:
    print(link['href'])
    story = scrap_article(link['href'])
    # append to csv file
    writer = csv.writer(csv_file)
    writer.writerow(story)

# idk = scrap_article('https://www.tnp.sg/news/singapore/taxi-passenger-who-alighted-ecp-cabby-appeared-dazed')
# print(idk)

elapsed_time = time.time() - start_time
print('\r\nElapsed time: ' + str(round(elapsed_time, 2)) + 's')