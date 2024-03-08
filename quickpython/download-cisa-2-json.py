# Web Data scraping into JSON format example.
# to run 
# import requirements
# pip install -r ./requirements.txt
# run the command
# python .\download-cisa-2-json.py -a 'https://www.cisa.gov/news-events/cybersecurity-advisories?f%5B0%5D=advisory_type%3A94&page=' -p 1 -b 'https://www.cisa.gov'


import pandas as pd
import argparse
from bs4 import BeautifulSoup
import re
import requests
import json



class DetailSection: 
    section = ''
    content = ''
    def __init__(self, section, content):
        self.section = section
        self.content = content
    
    def __str__(self):
        return self.section + '\n' + self.content

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert First HTML table in file to CSV')
    
    parser.add_argument('-a', '--address', help='base web address', required=True)
    parser.add_argument('-p', '--maxPages', help='The Maximum number of pages', required=True)
    parser.add_argument('-b', '--baseurl', help='The baseurl', required=True)
    args = parser.parse_args()

    for i in range(0, int(args.maxPages)):
      currURI = args.address
      response = requests.get(currURI + str(i))
      if response.status_code != 200:
          print("Error fetching page")
          exit(1)
      else:
          listContent = response.content



      soup = BeautifulSoup(listContent, 'html.parser')
      alerts_items = soup.find_all('h3', class_='c-teaser__title')
      

      for item in alerts_items:
          print('processing ' + args.baseurl + '/' + item.find('a').get('href'))
          uri=args.baseurl + '/' + item.find('a').get('href')

    
          response = requests.get(uri)
          if response.status_code != 200:
              print("Error fetching page")
              exit(1)
          else:
              content = response.content

          soup2 = BeautifulSoup(content, 'html.parser')
          content = soup2.find('main')
          title = re.sub(r'\n\s*\n', r'\n\n', content.find('h1').get_text().strip(), flags=re.M)
          date = re.sub(r'\n\s*\n', r'\n\n', content.find('time')['datetime'], flags=re.M)
          alert_cd = re.sub(r'\n\s*\n', r'\n\n', content.find('div', class_='c-field--name-field-alert-code').find('div', class_='c-field__content').get_text().strip(), flags=re.M)



          print(title)
          print(date)
          print(alert_cd)
          subcontent = content.find('div', class_="l-page-section__content")
          fullbody = re.sub(r'\n\s*\n', r'\n\n', subcontent.get_text().strip(), flags=re.M)
        
          arrayObj = []
          currObj = DetailSection('','')
          for sc in subcontent.contents:
              if sc.find('h3') and sc.get_text().strip() != '':
                  heading=sc.get_text().strip()
                  section = re.sub(r'\n\s*\n', r'\n\n', heading, flags=re.M)
                  if currObj:
                      arrayObj.append(currObj)
                      currObj = DetailSection('','')
                  currObj.section = section.replace(' ','_').strip()
                  currObj.content = ''
              else:
                  currObj.content += ' ' + re.sub(r'\n\s*\n', r'\n\n', sc.get_text().strip(), flags=re.M)
          arrayObj.append(currObj)
          alertObj = {}
          alertObj["uri"] = uri
          alertObj["title"] = title
          alertObj["date"] = date
          alertObj["alert_cd"] = alert_cd
          alertObj["body"] = fullbody

          for obj in arrayObj:
              if (obj.section != ""):
                alertObj[obj.section.replace(' ','_').strip().lower()] = obj.content.strip()
          
          with open ('./output/' + alert_cd + '.json', 'w') as f:
              json.dump(alertObj, f, indent=4)

      
