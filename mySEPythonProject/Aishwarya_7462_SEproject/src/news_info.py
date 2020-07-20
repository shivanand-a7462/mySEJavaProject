

import re

import requests
from bs4 import BeautifulSoup
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.tree import Tree
from database import DBConnection
import psycopg2
from constants import COUNTRY


def get_continuous_chunks(text):    
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        #print(i)
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            
            continue

    return continuous_chunk






bag_of_words = ['tavel', 'tour', 'visit', 'trip', 'flying', 'visiting', 'modi', 'prime minister', 'narenda']
month_stemer = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'july', 'aug', 'sep', 'nov', 'dec']
regex_list = ['']

country_capital_list = []

with open('/home/aish/Desktop/capital.txt', 'r') as f:
    lines = f.readlines()
    for capital_name in lines:
        country_capital_list.append(capital_name)

country_capital_list.extend(COUNTRY)
regex = "|".join(str(item.lower()) for item in country_capital_list)


sql = "UPDATE classified_article SET counter = %s WHERE id = %s"
dbcon = DBConnection().create_connection()
cursor = dbcon.cursor()
cursor.execute("SELECT id,article,counter FROM classified_article WHERE id > 0 AND counter >3 ORDER BY id asc")
result_set = cursor.fetchall()

frequency_dict = {}
for result in result_set:
    (id, content, filter_count) = result
    #print (id)
    content = content.lower()
    content = re.sub("<.*?\>", " ", content)
    content = re.sub('[,.]', '', content)
    '''
    #Stage 1
    if re.search('visit|visiting|travel|trip', content):
        filter_count = filter_count + 1
        cursor.execute(sql, (filter_count, id))
       
    '''

    '''
    #Stage 2
    #remove this we do not need visit to india
    if re.search('visit to india', content):
        filter_count = 0
        cursor.execute(sql, (filter_count, id))
        print (">>>>>>>>>>>>>>>>>",id)
    '''
    '''
    #Stage 3
    #check for foreign country and thier capital names
    if re.search(regex, content):
        filter_count = filter_count + 1
        cursor.execute(sql, (filter_count, id))
        print (">>>>>>>>>>>>>>>>>",id)
    '''
    '''
    #Stage 4
    # keyword specific seach
    if re.search("arrives|attend|embarks|reaches", content,re.DOTALL):
        filter_count = filter_count + 1
        cursor.execute(sql, (filter_count, id))
        print (">>>>>>>>>>>>>>>>>",id)
    '''
#dbcon.commit()
requests
sql_news_title = "SELECT n.title, n.id, n.url FROM news_url n INNER JOIN classified_article c ON c.news_url_id = n.id WHERE c.counter > 3 "
sql_insert = "INSERT INTO visit_info(place, visit_date) values(%s, %s) ON CONFLICT (place, visit_date) DO NOTHING"
cursor.execute(sql_news_title)
rs_tuple_list = cursor.fetchall()
for rs_tuple in rs_tuple_list:
    (title, id, url) = rs_tuple
    lst_ner = get_continuous_chunks(title)
    country_list = []
    for item in lst_ner:
        if re.search(regex, item.strip().lower()):
            country_list.append(item)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    if country_list:
        for country in country_list:
            date = soup.find('span', {'class':"time_cptn"}).text
            date_reg =  re.search(r'(.*\|)(.*2015)(.*)',date)
            date_str = date_reg.group(2)
            cursor.execute(sql_insert, (country, date_str))
            dbcon.commit()
  
