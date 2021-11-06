import json
from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
from model import Book,ListBook, BaseModel
from typing import List, Optional
from pydantic import parse_obj_as
import jwt
import time
import datetime
import mysql_connection 
import _token 
import json
 
books = []
app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

@app.route('/')
def hello():
    return {"message": "Successfully", "status" : "0", "data": "Hello World"}, 200

@app.route('/generateToken')
def generateToken_Endpoint():
    token = _token.generateToken()
    return {"message": "Successfully", "status" : "0", "data": token}, 200

@app.route('/decodeToken')
def decodeToken_Endpoint():
    headertoken  = request.environ.get('HTTP_AUTHORIZATION')
    authen = headertoken.split(' ')
    if len(authen) > 1 :
        token = _token.decodeToken(authen[1])
    return {"message": "Successfully", "status" : "0", "data": token}, 200

@app.route('/connectmysql', methods=['POST', 'GET', 'PUT', 'DELETE'])
def mysql():
    headertoken  = request.environ.get('HTTP_AUTHORIZATION')

    if headertoken != None :

        authen = headertoken.split(' ')

        if len(authen) > 1 :
            # authen[0] == "Bearer".lower()
            detoken = jwt.decode(str(authen[1]), key='PARINYADEV', issuer="PARINYADEV" ,audience="PARINYADEV", algorithms=['HS256', ])
            # detoken = jwt.decode(authen[1], key='PARINYADEV', issuer="PARINYADEV" ,audience="PARINYADEV", algorithms=['HS256'])
            if detoken["sub"]["id"] == "1111" :
                try:            
                    if request.method == 'GET': #SELECTMYSQL
                        results = mysql_connection.GetBook()
                        # a = ListBook(**results)
                        books.extend(results)
                        if results is not None:
                            return {"message": "Successfully", "status" : "0", "data": results}, 200
                            
                    elif request.method == 'POST': #INSERTMYSQL
                        body = request.get_json()
                        results = mysql_connection.PostBook(body['author'], body['price'], body['title'])
                        if results is not None:
                            return {"message": "Successfully", "status" : "0", "data": "1 record inserted, ID:" + str(results)}, 201

                    elif request.method == 'PUT': #UPDATEMYSQL
                        body = request.get_json()
                        results = mysql_connection.PutBook(body)
                        if results is not None:
                            return {"message": "Successfully", "status" : "0", "data": None}, 201
                            
                    elif request.method == 'DELETE': #DELETEMYSQL
                        deleteId = request.args.get('id')
                        results = mysql_connection.DeleteBook(deleteId)
                        if results is not None:
                            return {"message": "Successfully", "status" : "0", "data": None}, 201
                except Exception as e:
                    return {"message": "Exception: " + e, "body": None}, 404
            return {"message": "UnAuthorization"}, 403
    return {"message": "Error"}, 404

@app.route('/book', methods=['POST', 'GET', 'PUT', 'DELETE'])
def book():
    try:
        if request.method == 'POST':
            body = request.get_json()
            try:
                if len(books) > 0:
                    for i, book in enumerate(books):
                        if str(book['title']).lower() == str(body['title']).lower():
                            return {"message": "Duplicate Title Book", "body": None}, 400
                books.append(body)
                return {"message": "Book already add to database", "body": body}, 201
            except Exception as e:
                return {"message": "Exception: " + e, "body": None}, 404
        elif request.method == 'GET':
            return {"books": books}, 200
        elif request.method == 'PUT':
            body = request.get_json()
            for i, book in enumerate(books):
                if book['id'] == body['id']:
                    books[i] = body
            return {"message": "Book has been replace", "body": body}, 200
        elif request.method == 'DELETE':
            deleteId = request.args.get('id')
            for i, book in enumerate(books):
                if int(book['id']) == int(deleteId):
                    books.pop(i)
            return {"message": "Book is deleted"}, 200
    except Exception as e:
        print(e)
# app.run()
