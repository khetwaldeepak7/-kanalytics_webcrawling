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
site = 'en_asaninst_org_publication'
c = Crawl()  # creating object

# create directories to store logs.
log_path = c.create_directories(project_path, client_id, site)

# create image directories
image_directory = c.create_image_directories(project_path)

# logger
logger = log_func(log_path, created_on, current_time)
logger.info("Process Started ...\n")

# creating pdf directories
pdf_directory = c.create_pdf_directories(project_path, site)

# initialize variables
skipped_due_to_headline = 0
skipped_due_to_content = 0
skipped_due_to_date = 0
missing_overall_tonality = 0
no_of_data = 0
duplicate_data = 0  
unable_to_fetch_article_url = 0
unable_to_fetch_cat_url = 0
unable_to_download_pdf = 0
publish_source = 'en.asaninst.org'
country = 'South Korea'
language = 'English'
images_path = []

cat_pages = c.download_page('http://en.asaninst.org/')
cat_pages = c.scrap('class="menu-gnb-container">(.*?)<div\s*class="menu-one">',cat_pages)
for _ in cat_pages.split('<li id="menu-item-')[1:]:
    
    cat_url = c.scrap('<a\s*href="(.*?)"', _)
    if cat_url.endswith('issues/'):
        continue
    print("cat_url : ",cat_url)
    
    logger.info(f'Fetching cat url {cat_url}\n')
    cat_page = c.download_page(cat_url)
    
    if cat_page.startswith('Unable to fetch'):
        logger.info(cat_page) # writes error message with error code
        unable_to_fetch_cat_url += 1
        continue

    for i in cat_page.split('class="post_key">')[1:]:

        # source_link
        source_link = c.scrap('<a\s*href="(.*?)"', i)
        if not source_link:
            continue

        # handle duplicates
        source_link_query = {'source_link':source_link}
        dic = cl_data.find_one(source_link_query,{'source_link': 1}) 
        if dic:
            duplicate_data += 1
            continue

        time.sleep(random.randint(3,7))

        page = c.download_page(source_link)
        if page.startswith('Unable to fetch'):
                logger.info(page) # writes error message with error code
                unable_to_fetch_article_url += 1
                continue    
                
        # source_headline
        source_headline = c.scrap('<title>(.*?)\|', page)
        
        # skip if headline not found
        if not source_headline:
            logger.info(f'Skipping due to headline {source_link}\n')
            skipped_due_to_headline += 1
            continue
            
         # Date and time
        pub_date, publish_time = '', ''

        try:
            date_time_str = c.scrap('class="post_date_big">(.*?)</span></div>', page) + '000000'        
            date_time_str = c.strip_html(date_time_str)
            date_time_obj = datetime.strptime(date_time_str, '%Y%b%d%H%M%S')
            ist_date_time = date_time_obj - timedelta(hours = 0,minutes = 0)  # utc+8 to ist
            ist_date_time = ist_date_time.strftime('%Y-%m-%d %H:%M:%S')
            pub_date = ist_date_time[:10]
            publish_time = ist_date_time[11:]
        except:
            pass
        
        # skip null date
        if not pub_date:
            logger.info(f'Skipping due to date {source_link}\n')
            skipped_due_to_date += 1
            continue

        # break if date is not today's date
#         if pub_date != created_on:
#             break    

        logger.info(f'Fetching {source_link}\n')

        # source_content          
        source_content = c.scrap('class="top_content".*?>(.*?)<div\s*addthis:url=', page)
        if not source_content:
            source_content = c.scrap('class="entry-content">(.*?)<div\s*class="foot_social">',page)
        source_content = re.sub('Advertisement' , '', source_content, flags=re.S)
        source_content = c.strip_html(source_content)
       
        # skip if content not found
        if not source_content:
            logger.info(f'Skipping due to content {source_link}\n')
            skipped_due_to_content += 1
            continue

        # journalist
        journalist =  c.scrap('content="Author(.*?)"',page)
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
        
        pdf_path, pdf_name = '', ''

        pdf_url = c.scrap('class="post_download">.*?href="(.*?)"', page)

        if (pdf_url) and ('wp-content' in pdf_url) :         
            # pdf_name
            pdf_name = c.scrap('class="post_download">.*?title="(.*?)"', page)

            # pdf_path
            pdf_path = f'{pdf_directory}/{pdf_name}'        

            # download pdf
            pdf = c.download_pdf(pdf_url, pdf_path)
            if pdf.startswith('Unable to fetch'):
                logger.info(pdf) # writes error message with error code
                unable_to_download_pdf += 1
                continue   


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
                        "html_content":html_content,
                        "pdf_url": pdf_url,
                        "pdf_name": pdf_name,
                        "pdf_path":pdf_path
                    } 

        cl_data.insert_one(clientdata)  
        no_of_data += 1


logger.info('Iteration complete\n')   

logger.info(f'Number of data: {no_of_data}\n')
logger.info(f'Duplicate data: {duplicate_data}\n')
logger.info(f'Unable to fetch cat url: {unable_to_fetch_cat_url}\n')
logger.info(f'Unable to fetch article url: {unable_to_fetch_article_url}\n')
logger.info(f'Skipped due to headline: {skipped_due_to_headline}\n')
logger.info(f'Skipped due to content: {skipped_due_to_content}\n')
logger.info(f'Skipped due to date: {skipped_due_to_date}\n')
logger.info(f'Unable to download image: {unable_to_download_pdf}\n')
logger.info(f'country : {country}\n')
logger.info(f'language : {language}\n')
logger.info(f'Processing finished in {time.time() - start_time} seconds.\n')