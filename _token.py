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
import json
 
adata = {
    "id":"1111",
    "name": "Parinya Apaipak",
    "nickname": "Boom",
    "Role": "4",
}

payload_data = {
    # "id":"1111",
    # "name": "Parinya Apaipak",
    # "nickname": "Boom",
    # "Role": "4",
    "sub" : adata,
    "iss": "PARINYADEV",
    "aud": "PARINYADEV",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
}

my_secret = 'PARINYADEV'

def generateToken():
    token = jwt.encode(
        payload=payload_data,
        key=my_secret
    )
    return token

def decodeToken(token):
    detoken = jwt.decode(token, key='PARINYADEV', issuer="PARINYADEV" ,audience="PARINYADEV", algorithms=['HS256', ])
    return detoken