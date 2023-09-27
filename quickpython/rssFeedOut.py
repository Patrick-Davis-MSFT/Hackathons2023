# to run this file, type in the command line:
# pip install -r ./requirements.txt
# then run
# python rssFeedOut.py

import feedparser
import argparse

def readRSS( url ):
    
    feed = feedparser.parse(url)

    # feed_title = feed['feed']['title']  # NOT VALID
    feed_entries = feed.entries

    for entry in feed.entries:

        article_title = entry.title
        article_link = entry.link
        article_published_at = entry.published # Unicode string
        article_published_at_parsed = entry.published_parsed # Time object
        # article_author = entry.author  DOES NOT EXIST
        content = entry.summary
        # article_tags = entry.tags  DOES NOT EXIST


        print ("{}[{}]".format(article_title, article_link))
        print ("Published at {}".format(article_published_at))
        # print ("Published by {}".format(article_author)) 
        print("Content {}".format(content))
        # print("catagory{}".format(article_tags))

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert PDF to text. Output appends to existing file, so if you want to start fresh, delete the output file')
    parser.add_argument('-f', '--rssfeed', help='RSS Feed Xml URI for Reading', required=False)
    args = parser.parse_args()
    
    feedURI = args.rssfeed or "https://www.cisa.gov/cybersecurity-advisories/ics-advisories.xml"

    readRSS(feedURI)
