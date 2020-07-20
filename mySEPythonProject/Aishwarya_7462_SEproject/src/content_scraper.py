from bs4 import BeautifulSoup
import requests
from database import DBConnection
class ContentScraper:
    def __init__(self):
        self.db_con = DBConnection().create_connection()
        self.cursor = self.db_con.cursor()
    def scrape_content(self):
        sql_url = "SELECT id, url FROM news_url WHERE is_valid = true;"
        sql_scrape = "INSERT INTO classified_article (news_url_id, article) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
        self.cursor.execute(sql_url)
        rs_tuple = self.cursor.fetchall()
        print(rs_tuple)

        for each_row in rs_tuple:
            news_url_id = each_row[0]
            content_url = each_row[1]
            
            r=requests.get(content_url)
            content_page=r.text
            soup=BeautifulSoup(content_page,"lxml")
            div = soup.find("div",{"class":"Normal"})
            if div:
                content = str(div)
                self.cursor.execute(sql_scrape, (news_url_id, content))
                self.db_con.commit()
if __name__ == "__main__":
    ContentScraper().scrape_content()