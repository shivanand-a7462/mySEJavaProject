from __future__ import print_function
from flask import Flask
from flask import jsonify

import sys

app = Flask(__name__)

from database import DBConnection

@app.route('/')
def hello_world():
   db_con = DBConnection().create_connection()
   cursor = db_con.cursor()
   sql = "select place, visit_date from visit_info"
   cursor.execute(sql)
   rs_tuple_list = cursor.fetchall()
   
   #return jsonify(rs_tuple_list)
   value_dict = {}
   for rs_tuple in rs_tuple_list:
       (place, date_of_visit) = rs_tuple
       value_dict[place] = date_of_visit
   #return 'Hello World'
   return jsonify(value_dict)


if __name__ == '__main__':
   app.run()
