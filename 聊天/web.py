import flask
import json
from flask import request
from flask import session
# from PIL import Image,ImageDraw,ImageFont
import sqlite3
import random
import base64
import re
import time
import os
import sys
import math
app = flask.Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
path = os.path.dirname(sys.argv[0])
db = path+'/monitoring.db'



@app.route('/index/')
@app.route('/',methods=['GET'])
def index():

	return flask.render_template('index.html')

if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8008)