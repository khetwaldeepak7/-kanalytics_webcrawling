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
client_id = '5eb16c2db378671cf746ebb8'  # China
site = 's_weibo_com'
c = Crawl()  # creating object
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
queries = ['国家航天局', '中国航天总公司', '特种部队', '特种部队', '军舰', '监视', '飞机', '侦察飞机', '东部战区司令部', '东部战区司令部', '西部战区司令部', '西部战区司令部', '北部战区司令部', '北部战区司令部', '南部战区司令部', '南部战区司令部', '中央战区司令部', '解放军', '陆军', '空军', '解放军', '解放军', '解放军海军', '解放军海军', '西藏自治区', '西藏', '达赖喇嘛', '拉达克', '塔旺', '春比', '列伊', '加尔万', '多克拉姆', '锡金', '阿鲁纳恰尔邦', '布拉马普特拉', '雅鲁藏布江', '三角高地', '实际控制线', '中文应用程序', '中印', '印中', '莫迪', '印度人民党', '阿米特·莎', '印度西藏边防警察', '班公湖', '新德里', '印度', '吉尔吉特', '巴尔的斯坦', '中印边界', '中国对印度的网络攻击', '印度太平洋', '四方', '四方加', '修正主义力量', '巴布·曼达卜', '马六甲海峡', 'da他海峡', '阿拉伯海', '霍尔木兹海峡', '扼流点', '政治派别', '习近平', '中共中央政治局常委', '全国人大', '政协', '全国人民代表大会', '中国人民政治协商会议', '李克强', '政治局', '王毅', '赵立坚', '中央网络安全和信息化委员会', '中央军民融合发展委员会', '中央国家安全委员会', '中央统一战线工作领导小组', '国家安全部', '公安部', '台湾自由分子', '机密中央文件', '中国人权分子', '外来侵略', '韩国', '日本', '朝鲜', '东京', '平壤', '首尔', '金正恩', '钓鱼岛', '东海', '朝鲜', '金正恩', '金二成', '朝鲜劳动党', '中央政治局主席', '巴西', '哥伦比亚', '阿根廷', '秘鲁', '委内瑞拉', '智利', '厄瓜多尔', '玻利维亚', '巴拉圭', '乌拉圭', '圭亚那', '苏里南', '法属圭亚那', '福克兰群岛', '墨西哥', '加拿大', '危地马拉', '古巴', '海地', '多米尼加共和国', '洪都拉斯', '萨尔瓦多', '尼加拉瓜', '中国应用程序', '巴布-埃尔-曼德', '台独分子', '中央机密文件'
'暴恐势力','边境自卫反击战','传统安全','大校','霸权主义','单边主义','弹道导弹','单极','第二炮兵','帝国主义','地缘政治','电磁空间安全','东突','独联体','多级','反海盗','非传统安全','非对称作战','非战争军事行动','共同安全','国际秩序','国家主权','海湾战争','航空母舰','和平发展','核心利益','轰炸机','缉毒','积极防御','军备竞赛','军民融合','军事外交','军事战略','军种战略','恐怖主义','空地一体战','空海一体战','联合作战','民族分裂势力','潜水艇','抢险救灾','区域拒止','驱逐舰','上将','少将','双极','孙子兵法','台独势力','突击步枪','网络安全','威慑','武警','西藏农奴制','新干涉主义','信息化局部战争','新型大国关系','巡洋舰','亚太再平衡战略','颜色革命','一带一路战略',
'一国两制','意识形态','隐形战机','藏独','战斗机','战略机遇期','战略空间','战略判断','战略评估','战略武器系统','战略指导','战区战略','政委','殖民主义','中将','中央军委','洲际导弹','主要战略方向','主战坦克','总参谋部','综合国力','总后勤部','宗教极端势力','总政治部','总装备部']


logger.info(f'Iterating through {len(queries)} queries.\n')

for query in queries:
    
    cnt += 1
    logger.info(f'Firing query no. {cnt}\n')
    
    modified_query = query.replace(' ', '%20').strip()
    try:
        search_page = requests.get(f'https://s.weibo.com/weibo?q={modified_query}', timeout=60).text
    except:
        logger.info(f'Unable to fire query no. {cnt}\n')
        no_of_not_working_queries += 1
        continue
    
    for i in search_page.split('class="card-feed">')[1:]:

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
        
        for img_url in img_urls:
            img_name = c.scrap('.*/(.*)', img_url)
            img_path = f'{image_directory}/{img_name}'
            img_url = 'https://ww4.sinaimg.cn/bmiddle/' + img_name
            
            # if image is not downloaded return an error message
            download_message = c.download_image(img_url, img_path)  
            images_path.append(img_path)
            
            if download_message:
                logger.info(download_message)  # writes error message with error code
                unable_to_download_image += 1
                continue    
            
        # storing the above data in a dictionary
        clientdata = {
                        "client_master": client_id,
                        "articleid": client_id,
                        "medium": "Weibo",
                        "searchkeyword": [query], 
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
logger.info(f'Total number of queries: {len(queries)}\n')
logger.info(f'No. of not working queries: {no_of_not_working_queries}\n')
logger.info(f'Duplicate data: {duplicate_data}\n')
logger.info(f'Skipped due to username: {skipped_due_to_username}\n')
logger.info(f'Skipped due to content: {skipped_due_to_content}\n')
logger.info(f'Unable to download image: {unable_to_download_image}\n')
logger.info(f'Processing finished in {time.time() - start_time} seconds.\n')
