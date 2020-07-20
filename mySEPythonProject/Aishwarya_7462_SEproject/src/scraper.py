import requests
import calendar
import traceback
import time
import sys

from bs4 import BeautifulSoup
from xception import NoMoreUrlFoundException
from database import DBConnection


class Xtractor:

    def __init__(self):
        self.year = 2015
        self.base_url = "http://timesofindia.indiatimes.com/%s" 
        self.url_to_scrape = None
        self.db_con = DBConnection().create_connection()
        self.cursor = self.db_con.cursor()
        self.request_headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    


    def save_last_month_date_url(self, month_date_url_id):
        sql_scraper_info = "UPDATE scraper_info SET last_month_date_url_id = %s WHERE id=1"
        self.cursor.execute(sql_scraper_info, (month_date_url_id, ))
        self.db_con.commit()
        
    

    def get_url_to_scrape(self):
        month_date_url_id = 0
        sql_last_month_date_url = "SELECT last_month_date_url_id FROM scraper_info WHERE id=1"
        sql_get_month_date_url = """SELECT month_date_url ,id
                                    FROM month_date_url 
                                    %s """
        self.cursor = self.db_con.cursor()
        self.cursor.execute(sql_last_month_date_url)        
        rs_tuple = self.cursor.fetchone()

        (month_date_url_id, ) = rs_tuple

        if rs_tuple:
            (month_date_url_id, ) =  rs_tuple
            condition = 'WHERE id > %s ORDER BY id asc' %(month_date_url_id)
            self.cursor.execute(sql_get_month_date_url % condition)
            rs_tuple = self.cursor.fetchone()
            
            if not rs_tuple:
                raise NoMoreUrlFoundException("No URL left to scrape...you are done scraping all the urls present in DB")
            (month_date_url, month_date_url_id) =  rs_tuple
        else:
            self.cursor.execute(sql_get_month_date_url % ('ORDER BY id asc'))
            rs_tuple = self.cursor.fetchone()
            (month_date_url, month_date_url_id) =  rs_tuple
        
        return (month_date_url_id, month_date_url)


    def start(self):
        while True:
            try:
                time.sleep(5)
                (month_date_url_id, month_date_url) = self.get_url_to_scrape()   
                print(month_date_url)     
                url_to_open = self.base_url % month_date_url
                print (url_to_open)
                html = requests.get(url_to_open, headers=self.request_headers).text
                self.parse_titles(html, month_date_url_id)
            except NoMoreUrlFoundException:
                print("------------------DONE------------------------")
                sys.exit(0)
        return 


    def save_tile_and_href(self, month_date_url_id, title, href):
        sql = "INSERT INTO news_url (month_date_url_id, title, url) VALUES (%s, %s, %s) ON CONFLICT (title) DO NOTHING"
        self.cursor.execute(sql, (month_date_url_id, title, href))
        self.db_con.commit()
        return

    def parse_titles(self, html, month_date_url_id):
        soup = BeautifulSoup(html, 'lxml')
        div = soup.find('div', {'style': 'font-family:arial ;font-size:12;font-weight:bold; color: #006699'})
        table = div.find('table')
        atag_list = table.find_all('a')
        
        with open("/home/aish/Desktop/toi/toi.html", 'w')as f:
            f.write(str(table))        

        for a in atag_list:            
            title = a.text.strip()
            href = a['href']
            self.save_tile_and_href(month_date_url_id, title, href)
        
        self.save_last_month_date_url(month_date_url_id)
        return 
        
        

    def initiate(self):
        sql_insert_month_date_url = "INSERT INTO month_date_url (url_month, url_date, year, month_date_url) VALUES (%s, %s, %s, %s)"
        toi_starttime = 42005        
        month_counter = 1
        date_counter = 1

        # Add all url of all month date to database
        while True:
            # Get number of days in a month depending on the year 
            num_of_days_in_month = calendar.monthrange(self.year, month_counter)[1]
            
            while True:
                toi_url_month_date = "/%s/1/1/archivelist/year-%s,month-%s,starttime-%s.cms" % (self.year, self.year, month_counter, toi_starttime)
                self.cursor.execute(sql_insert_month_date_url, (month_counter, date_counter, self.year, toi_url_month_date))
                self.db_con.commit()

                toi_starttime += 1
                date_counter += 1
                print(toi_url_month_date)

                
                if date_counter > num_of_days_in_month:
                    # Reset the date counter to 1 before break for each month
                    date_counter = 1  
                    break


            month_counter += 1       
            
            # Break when December is reached              
            if month_counter > 12:
                break
            
            
        


if __name__ == "__main__":
    #Xtractor().initiate()
    Xtractor().start()