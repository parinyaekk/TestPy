import mysql.connector
import datetime
from model import Book,ListBook, BaseModel

def connect_database():
  global mydb
  global mycursor
  try:
    if mydb.is_connected():
      pass
  except:
    try:
      print("\nCreating new db connection...")
      # mydb = mysql.connector.connect(host="XXX.XXX.XXX.XXX",user="XXXXXX",password="XXXXXXXXXX",database="XXXXXX", ssl_ca='ssl-client/ca.pem', ssl_cert='ssl-client/client-cert.pem', ssl_key='ssl-client/client-key.pem')
      # 'buffered=True' is used to prevent unread result error
      mydb = mysql.connector.connect(
        host="92.249.44.52",
        user="u979780448_dbadmin",
        password="*C28kc4mTZtw",
        database="u979780448_SaveMe"
      )
      mycursor = mydb.cursor(dictionary=True)
    except mysql.connector.Error as q:
      print("["+datetime.datetime.now().strftime("%a %b %d, %Y %I:%M:%S %p")+"] Database Error: "+str(q)+"\n")

def disconnect_database():
  global mydb
  global mycursor
  try:
    if mydb.is_connected():
      mycursor.close()
      mydb.close()
      mydb = None
  except:
    pass

def GetBook():
  try:       
      connect_database()    
      query = "select * from book where is_active != 0" 
      val = None 
      global mycursor
      mycursor.execute(query,val)
      myresult = mycursor.fetchall()
      return myresult
  except mysql.connector.Error as error:
      print("Failed to get record from MySQL table: {}".format(error))
      return None
  finally:
    disconnect_database()
    
def PostBook(author,price,title):
  try:       
      connect_database()
      query = "INSERT INTO book (author, price, title, create_date, create_by) VALUES (%s, %s,%s, %s, %s)"
      val = (author, price, title, datetime.datetime.utcnow(), 'INSERTBYAPI')    
      global mycursor
      mycursor.execute(query,val)
      mydb.commit()
      return mycursor.lastrowid
  except mysql.connector.Error as error:
      print("Failed to get record from MySQL table: {}".format(error))
      return None
  finally:
    disconnect_database()
    
def PutBook(request):
  try:       
      connect_database()
      classrequest = Book(**request)
      query = "UPDATE book SET create_by = %s WHERE id = %s"
      val = ('UPDATEAPI',classrequest.id)    
      global mycursor
      mycursor.execute(query,val)
      mydb.commit()
      return mycursor.lastrowid
  except mysql.connector.Error as error:
      print("Failed to get record from MySQL table: {}".format(error))
      return None
  finally:
    disconnect_database()
    
def DeleteBook(id):
  try:       
      connect_database()
      query = "UPDATE book SET is_active = %s WHERE id = %s"
      val = (0,id)    
      global mycursor
      mycursor.execute(query,val)
      mydb.commit()
      return mycursor.lastrowid
  except mysql.connector.Error as error:
      print("Failed to get record from MySQL table: {}".format(error))
      return None
  finally:
    disconnect_database()
    
# mycursor = mydb.cursor()
# print(mydb)