import re
import time
from constants import COUNTRY
from database import DBConnection
COUNTRY = [country.lower() for country in COUNTRY]
from nltk.stem.porter import *

from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import re

class Classifier:
    
    def __init__(self):
        self.bag_of_words = ['modi', 'pm', 'visit', 'narendra', 'prime minister']
        self.bag_of_words_set = set(self.bag_of_words)
        self.db_con = DBConnection().create_connection()
        self.cursor = self.db_con.cursor()
        
    
    def classify_title(self):
        sql = "SELECT id, title FROM news_url WHERE id > %s ORDER BY id ASC "
        sql_update = "UPDATE news_url SET is_valid = True WHERE id = %s"

        news_url_id = self.get_last_news_url_id()
        counter = 0

        while True:            
            self.cursor.execute(sql, (news_url_id, ))
            rs_tuple = self.cursor.fetchone()
            if not rs_tuple:
                break
            
            (news_url_id, title) = rs_tuple
            print(news_url_id)
            stemmer = PorterStemmer()
            result_set = None
            title = title.lower()
            title_set = set([stemmer.stem(item) for item in title.split()])
            #print (title)
            result_set = (title_set & self.bag_of_words_set)
            print ("result_set", result_set)

            '''if result_set:
                self.cursor.execute(sql_update, (news_url_id, ))
                self.db_con.commit()'''

            
            #for item in title_set:
                
            #    if item.lower() in COUNTRY:
            #       # print(item)    
            #        if result_set:
            #            self.cursor.execute(sql_update, (news_url_id, ))
            #            self.db_con.commit()
            #    else:
            #        if self.get_place(item) and result_set:
            #           self.cursor.execute(sql_update, (news_url_id, ))
            #            self.db_con.commit()
            

            counter += 1
            if counter % 1000 == 0:
                print('Sleeping for 5 seconds')
                time.sleep(5)

            #self.update_last_news_url_id(news_url_id)

    
    def update_last_news_url_id(self, news_url_id):
        sql = "UPDATE scraper_info SET news_url_id = %s WHERE id = 1"
        self.cursor.execute(sql, (news_url_id, ))
        self.db_con.commit()

    
    def get_last_news_url_id(self):
        sql = "SELECT news_url_id FROM scraper_info"
        self.cursor.execute(sql)
        rs_tuple = self.cursor.fetchone()
        (news_url_id, ) = rs_tuple
        return news_url_id

    def get_place(self, text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))

        for i in chunked:
            if type(i) == Tree:
                if i.label()=="GPE":
                    for token, pos in i.leaves():
                        #print("found country %s " %token)
                        return True

        return False


if __name__ == "__main__":
    Classifier().classify_title()
