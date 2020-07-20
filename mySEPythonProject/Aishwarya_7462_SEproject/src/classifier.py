import re
import time
from database import DBConnection

class Classifier:
    
    def __init__(self):
        self.bag_of_words = ['modi', 'pm', 'visit', 'narendra', 'prime minister']
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

            for key_word in self.bag_of_words:
                if re.search(key_word, title.strip(), re.I):
                    self.cursor.execute(sql_update, (news_url_id, ))
                    self.db_con.commit()
            counter += 1
            if counter % 1000 == 0:
                print('Sleeping for 5 seconds')
                time.sleep(5)

            self.update_last_news_url_id(news_url_id)

    
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


if __name__ == "__main__":
    Classifier().classify_title()
