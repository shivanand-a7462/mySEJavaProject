from flask import Flask,render_template
app = Flask(__name__)


from database import DBConnection

@app.route('/')
def display_vist_details():
   db_con = DBConnection().create_connection()
   cursor = db_con.cursor()
   sql = "select place, visit_date from visit_info"
   cursor.execute(sql)
   rs_tuple_list = cursor.fetchall()
   value_dict = {}

   for rs_tuple in rs_tuple_list:
       (place, date_of_visit) = rs_tuple
       value_dict[place] = date_of_visit
       
   return render_template('index.html', vist_details=value_dict)
if __name__ == '__main__':
   app.run()