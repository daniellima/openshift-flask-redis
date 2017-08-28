import redis
import os
from flask import Flask
from flask import request

app = Flask(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
USE_REDIS = REDIS_HOST is not None
REDIS_ERROR_MESSAGE = "Redis not available. Please provide a REDIS_HOST and REDIS_PORT env variables."

if USE_REDIS:
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

@app.route("/")
def hello():
    if not USE_REDIS:
        return REDIS_ERROR_MESSAGE
    page = "<h1>Hello Flask</h1>"
    keys = r.keys()
    for key in keys:
        page += "<p style='color:red'>" + key + "-" + r.get(key) + "</p>"
    return page

@app.route("/add/<text>/<value>")
def add(text, value):
    if not USE_REDIS:
        return REDIS_ERROR_MESSAGE
    r.set(text, value)
    return text+' has been received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')