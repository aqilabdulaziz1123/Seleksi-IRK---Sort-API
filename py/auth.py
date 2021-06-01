import jwt
import os
from flask import Flask, request

app = Flask(__name__)

user = os.environ.get("user")
pswd = os.environ.get("pass")

secret = os.environ.get("secret")

memoryauth = set()

def getloggedin():
    return memoryauth

def login(us, ps):
    if us == user:
        if ps == pswd:
            key = encode(user)
            memoryauth.add(user)
            return key
    return None

def encode(user):
    return jwt.encode({'user': user}, secret, algorithm='HS256')

def decode(encoded):
    return jwt.decode(encoded, secret, algorithms=['HS256'])

def auth(next):
    def wrapper(*args, **kwargs):
        if not ("AUTH" in request.headers):
            return {"error": "auth header is required"}, 401
        
        key = request.headers["AUTH"]
        try:
            decoded = decode(key)
        except:
            decoded = None

        if decoded is None or not("user" in decoded) or not (decoded["user"] in memoryauth):
            return {"error": "bad key"}, 401

        return next(*args, **kwargs)
    wrapper.__name__ = next.__name__
    return wrapper
