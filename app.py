from flask import Flask
from flask import request
import redis

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route("/")
def hello():
    page = "<h1>Hello Flask</h1>"
    keys = r.keys()
    for key in keys:
        page += "<p style='color:red'>" + key + "-" + r.get(key) + "</p>"
    return page

@app.route("/add/<text>/<value>")
def add(text, value):
    r.set(text, value)
    return text+' has been received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080')