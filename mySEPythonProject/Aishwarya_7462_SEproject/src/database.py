import psycopg2

class DBConnection:
    def __init__(self):
        self.db_con = None
    
    def create_connection(self):
        host = 'localhost'
        db_name = 'toi2'
        db_user = 'admin'
        db_password = 'admin'

        if not self.db_con:
             self.db_con = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password)

        return  self.db_con