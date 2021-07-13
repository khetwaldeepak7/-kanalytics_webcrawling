from scrawl import *
import random
import json
import os 
import requests
import time
from datetime import datetime,timedelta
from datetime import date
import re
import sys
import urllib, urllib.request, urllib.parse


c = Crawl() # Creating object

# Creating list of proxies
proxy_col = dashboard['proxies']
proxy = proxy_col.find({'country':'China'})
proxy_list = list(map(lambda x:x['ip'],list(proxy)))


def get_proxy():
    
    return {'http': random.choice(proxy_list)}


def download_image(image_url,image_path):

    time.sleep(random.randint(1,3))
    try:
        r = requests.get('https://s.weibo.com/top/summary?cate=realtimehot',proxies=get_proxy(),timeout=120)
        response_code = r.status_code
        if response_code != 200:
            return f'Unable to fetch image {image_url} Error code: {r.status_code}\n'
            # print(f'Unable to fetch image {image_url} Error code: {r.status_code}')
        else:
            r = r.content
            with open(image_path, 'wb') as f:
                f.write(r)
    except:
        return f'Unable to fetch image {image_url} Unknown error\n'
        # print(f'Unable to fetch image {image_url} Unknown error\n')

    
# Date and time
start_time = time.time()
current_time = datetime.now().strftime("%H-%M-%S")
created_on = date.today().strftime("%Y-%m-%d")

# client_id = sys.argv[1]
client_id = '5eb16c2db378671cf746ebb8'  # China
site = 's_weibo_com_hot'
cl_data = dashboard['core_weibo']

# create directories to store logs.
log_path = c.create_directories(project_path, client_id, site)

# create image directories
image_directory = c.create_image_directories(project_path)

# logger
logger = log_func(log_path, created_on, current_time)
logger.info("Process Started ...\n")

# initialize variables
skipped_due_to_username = 0
skipped_due_to_headline = 0
skipped_due_to_content = 0
skipped_due_to_date = 0
missing_overall_tonality = 0
no_of_data = 0
duplicate_data = 0  
unable_to_fetch_url = 0
unable_to_download_image = 0
publish_source = 's.weibo.com'
country = 'China'
language = 'Chinese'
cnt = 0
publish_time = '00:00:00'
pub_date = created_on  # no pattern to find date
# Hence we will concate date(which is in a sentence) in the source content.
no_of_not_working_queries = 0


home_page = requests.get('https://s.weibo.com/top/summary?cate=realtimehot',proxies=get_proxy(),timeout=60).text
for _ in home_page.split('<tr class="">')[1:]: 
    
    cat_url =c.scrap('<a\s*href="(.*?)"',_)
    
    if 'http' not in cat_url:
        cat_url = 'https://s.weibo.com' + cat_url
    logger.info(f'Fetching cat url  {cat_url}\n') 
    
    cat_page = requests.get(cat_url,proxies=get_proxy()).text
    if cat_page.startswith('Unable to fetch'):
        logger.info(cat_page) # writes error message with error code
        no_of_not_working_queries += 1
        continue   
    
    for i in cat_page.split('class="card-feed">')[1:]:
        # source_link
        source_link = 'https:' + c.scrap('href="(.*?)"', i)

        # handle duplicates
        source_link_query = {'source_link':source_link}
        dic = cl_data.find_one(source_link_query,{'source_link': 1}) 
        if dic:
            duplicate_data += 1
            continue

        # time.sleep(random.randint(1,3))

        # source_headline
        source_headline = ''

        username = c.scrap('nick-name="(.*?)"', i)

        # skip if username not found
        if not username:
            logger.info(f'Skipping due to username {source_link}\n')
            skipped_due_to_username += 1
            continue
        
        # Date and time
        date_time = c.scrap('wb_time">(.*?)<', i)
        date_time = c.strip_html(date_time)  

        # source_content          
        source_content = c.scrap('feed_list_content".*?>(.*?)<p\s*class="from"\s*>', i) + '\n' + date_time
        source_content = c.strip_html(source_content)

        # skip if content not found
        if not source_content:
            logger.info(f'Skipping due to content {source_link}\n')
            skipped_due_to_content += 1
            continue

        # journalist
        journalist = ''
        if not journalist: journalist = 'NA'

        # current date and time 
        harvest_time = datetime.now().strftime("%H:%M:%S")

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
        images_path = []
        
        favourites = c.scrap('click:fav">.*?>(.*?)<', i)
        favourites = c.scrap('(\d+)', favourites)
        
        forward = c.scrap('click:repost.*?>(.*?)<', i)
        forward = c.scrap('(\d+)', forward)
        
        comments = c.scrap('click:comment.*?>(.*?)<', i)
        comments = c.scrap('(\d+)', comments)        
        
        likes = c.scrap('click:like.*?<em>(.*?)</em>', i)
        likes = c.scrap('(\d+)', likes)
        
        # Image
        img_urls = re.findall('<li>\s*<img\s*src="(.*?)"', i, flags=re.S)
        # print('source_link', source_link)
        for img_url in img_urls:
            img_name = c.scrap('.*/(.*)', img_url)
            img_path = f'{image_directory}/{img_name}'
            img_url = 'https://ww4.sinaimg.cn/bmiddle/' + img_name
            print('img_url', img_url)
            
            # if image is not downloaded return an error message
            download_message = c.download_image(img_url, img_path)  
            images_path.append(img_path)
            
            if download_message:
                print('unable to download image', img_url)
                logger.info(download_message)  # writes error message with error code
                unable_to_download_image += 1
                continue    
            
        # storing the above data in a dictionary
        clientdata = {
                        "client_master": client_id,
                        "articleid": client_id,
                        "medium": "Weibo",
#                         "searchkeyword": [query], 
                        "entityname": [], 
                        "process_flage": "1",
                        "na_flage": "0",
                        "na_reason": "",
                        "qc_by": "",
                        "qc_on": "",
                        "location": "",
                        "spokeperson": "",
                        "quota": "",
                        "overall_topics": "",
                        "person": "",
                        "overall_entites": "",
                        "overall_tonality": "",
                        "overall_wordcount": word_count,
                        "article_subjectivity": "",
                        "article_summary": "",
                        "pub_date": pub_date,
                        "publish_time": publish_time,
                        "harvest_time": harvest_time,  
                        "temp_link": source_link,
                        "publish_source": username,  
                        "programme": "null",
                        "feed_class": "",
                        "publishing_platform": "Weibo",
                        "klout_score": "0",
                        "journalist": "", 
                        "headline": source_content,  
                        "content": source_content,  
                        "language": language,
                        "location_mention": "",
                        "source_link": source_link,
                        "author_contact": "",
                        "author_emailid": "",
                        "author_url": "",
                        "city": "",
                        "state": "",
                        "country": country,
                        "source": username,
                        "foot_fall": "",
                        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "active": "1",
                        "circulation": "0",
                        'favourites':favourites,
                        'forward': forward,
                        'comments':comments,
                        'likes': likes,
                        'images_path': images_path
        }

        cl_data.insert_one(clientdata)  
        no_of_data += 1
        

logger.info('Iteration complete\n')   
logger.info(f'Number of data: {no_of_data}\n')
# logger.info(f'Total number of queries: {len(queries)}\n')
logger.info(f'No. of not working queries: {no_of_not_working_queries}\n')
logger.info(f'Duplicate data: {duplicate_data}\n')
logger.info(f'Skipped due to username: {skipped_due_to_username}\n')
logger.info(f'Skipped due to content: {skipped_due_to_content}\n')
logger.info(f'Unable to download image: {unable_to_download_image}\n')
logger.info(f'country: {country}\n')
logger.info(f'language: {language}\n')
logger.info(f'Processing finished in {time.time() - start_time} seconds.\n')