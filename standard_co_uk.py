import json
import os 
import requests
import time
from datetime import datetime,timedelta
from datetime import date
import re
import sys
import urllib, urllib.request, urllib.parse
import random
from scrawl import *
    
# Date and time
start_time = time.time()
current_time = datetime.now().strftime("%H-%M-%S")
created_on = date.today().strftime("%Y-%m-%d")

# client_id = sys.argv[1]
client_id = '5f69d22ef472d6646f577fa6'  # Europe
site = 'standard_co_uk'
c = Crawl()  # creating object
# cl_data = dashboard['core_web_india']
# create directories to store logs.
log_path = c.create_directories(project_path, client_id, site)

# create image directories
image_directory = c.create_image_directories(project_path)

# logger
logger = log_func(log_path, created_on, current_time)
logger.info("Process Started ...\n")

# initialize variables
skipped_due_to_headline = 0
skipped_due_to_content = 0
skipped_due_to_date = 0
missing_overall_tonality = 0
no_of_data = 0
duplicate_data = 0  
unable_to_fetch_article_url = 0
publish_source = 'standard.co.uk'
country = 'United Kingdom'
language = 'English'
images_path = []

year = date.today().strftime("%Y-%m-%d")
archive_pages = c.download_page(f'https://www.standard.co.uk/archive/{year}')
home_page = c.scrap('</a><a rel="noopener" class="link">(.*?)lass="sc-pANHa la-dINt">',archive_pages)

for i in home_page.split('</p><a href=')[1:2]:
    source_link = c.scrap('"(.*?)"', i)
    if 'http' not in source_link:
        source_link = ('https://www.standard.co.uk'+ source_link)
    # re.seacrh()
    source_link_query = {'source_link':source_link}
    dic = cl_data.find_one(source_link_query,{'source_link': 1}) 
  
    if dic:
        duplicate_data += 1
        continue    
        
    logger.info(f'Fetching {source_link}\n')
    time.sleep(random.randint(1,3))

    page = c.download_page(source_link)

    if page.startswith('Unable to fetch'):
        logger.info(page) # writes error message with error code
        unable_to_fetch_article_url += 1
        continue
    
    
    source_headline = c.scrap('article_title":"(.*?)",',page)
    source_headline = re.sub('&.*?;','',source_headline)
    if not source_headline:
        logger.info(f'Skipping due to headline {source_link}\n')
        skipped_due_to_headline += 1
        continue
   
    pub_date, publish_time = created_on, current_time            
            
#     try: 
#         date_time_str = c.scrap('<pubDate>(.*?)\+', page)
#         date_time_str = re.sub('[^\w+]','',date_time_str)#Tue27Apr2021063724
#         date_time_obj = datetime.strptime(date_time_str, '%a%d%b%Y%H%M%S')
#         ist_date_time = date_time_obj + timedelta(hours = 0,minutes = 0)  
#         ist_date_time = ist_date_time.strftime('%Y-%m-%d %H:%M:%S')  
#         pub_date = ist_date_time[:10]
#         publish_time = ist_date_time[11:]
    
#     except:
#         pass
  
    if not pub_date:
        logger.info(f'Skipping due to date {source_link}\n')
        skipped_due_to_date += 1
        continue
    
    if pub_date != created_on:
        break 

    
    source_content = c.scrap('</amp-social-share></div>(.*?)<interaction\s*class="', page)
    if not source_content:
        source_content = c.scrap('</amp-social-share></div>(.*?)<aside\s*id="articleTopic"',page) 
    source_content = source_content.replace("<![CDATA[","").replace("]]>","")
    source_content = re.sub('&.*?;','',source_content)
    source_content = c.strip_html(source_content)
 
    if not source_content:
        logger.info(f'Skipping due to content {source_link}\n')
        skipped_due_to_content += 1
        continue
    
    journalist =  ''
    if not journalist: journalist = 'NA'
        
        
  # current date and time 
    harvest_time = datetime.now().strftime("%H:%M:%S")

    # temp link
    temp_link = source_link

    # headline and content 
    headline = source_headline
    content = source_content

    # overall_tonality
    overall_tonality = ''

    # word count
    word_count = len((source_headline + ' ' + source_content).split())

    html_content = ''

    # image_urls
    image_urls = []

   # storing the above data in a dictionary
    clientdata ={
                    "client_master" : client_id, 
                    "articleid":client_id,
                    "medium":'Web' ,
                    "searchkeyword":[],
                    "entityname" : [] ,
                    "process_flage":"1",
                    "na_flage":"0",
                    "na_reason":"",
                    "qc_by":"",
                    "qc_on":"",
                    "location":"",
                    "spokeperson":"",
                    "quota":"",
                    "overall_topics":"",
                    "person":"",
                    "overall_entites":"",
                    "overall_tonality": overall_tonality,
                    "overall_wordcount":word_count,
                    "article_subjectivity":"",
                    "article_summary":"",
                    "pub_date":pub_date,
                    "publish_time":publish_time,
                    "harvest_time":harvest_time,
                    "temp_link":temp_link,
                    "publish_source": publish_source,
                    "programme":'null',
                    "feed_class":"News",
                    "publishing_platform":"",
                    "klout_score":"",
                    "journalist":journalist,
                    "headline":headline,
                    "content":content,
                    "source_headline":source_headline,
                    "source_content":source_content,
                    "language":language,
                    "presence":'null',
                    "clip_type":'null',
                    "prog_slot":'null',
                    "op_ed":'0',
                    "location_mention":'',
                    "source_link":source_link,
                    "author_contact":'',
                    "author_emailid":'',
                    "author_url":'',
                    "city":'',
                    "state":'',
                    "country":country,
                    "source":publish_source,
                    "foot_fall":'',
                    "created_on":created_on,
                    "active":'1',
                    'crawl_flag':2,
                    "images_path":images_path,
                    "html_content":html_content
                } 

#     cl_data.insert_one(clientdata)  
    no_of_data += 1


logger.info('Iteration complete\n')   
logger.info(f'Number of data: {no_of_data}\n')
logger.info(f'Duplicate data: {duplicate_data}\n')
logger.info(f'Unable to fetch article url: {unable_to_fetch_article_url}\n')
logger.info(f'Skipped due to headline: {skipped_due_to_headline}\n')
logger.info(f'Skipped due to content: {skipped_due_to_content}\n')
logger.info(f'Skipped due to date: {skipped_due_to_date}\n')
logger.info(f'Processing finished in {time.time() - start_time} seconds.\n')





