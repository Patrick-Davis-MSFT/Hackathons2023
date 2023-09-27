# to run this file, type in the command line:
# pip install -r ./requirements.txt
# then run
# python rssFeedOut.py

import feedparser
import argparse
from lxml import html
import requests

def strip_html(s):
  return str(html.fromstring(s).text_content().replace('\n', ' ').replace('\r', '').replace('\t', ' ').replace('    ', ' ').replace('    ', ' ').replace('    ', ' '))

def getFeedArticle(url):
    response = requests.get(url)
    content = response.text
    return content


def readRSS( url ):
    
    feed = feedparser.parse(url)

    # feed_title = feed['feed']['title']  # NOT VALID
    feed_entries = feed.entries

    for entry in feed.entries:

        article_title = entry.title
        article_link = entry.link
        article_published_at = entry.published # Unicode string
        article_published_at_parsed = entry.published_parsed # Time object
        content = entry.summary


        print ("{}[{}]".format(article_title, article_link))
        print ("Published at {}".format(article_published_at))

        return entry.link

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert PDF to text. Output appends to existing file, so if you want to start fresh, delete the output file')
    parser.add_argument('-f', '--rssfeed', help='RSS Feed Xml URI for Reading', required=False)
    args = parser.parse_args()
    
    feedURI = args.rssfeed or "https://www.cisa.gov/cybersecurity-advisories/ics-advisories.xml"

    contentURI = readRSS(feedURI)
    print(" \n ---------------------------------------------------- \n")
    print(str(contentURI))

    content = getFeedArticle(contentURI)

    print(" \n ---------------------------------------------------- \n")
    print(strip_html(content))
        
