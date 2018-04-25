import flask
import pytesseract
import time

from PIL import Image
import requests
conn = requests.Session()
app = flask.Flask(__name__)

@app.route('/index/')
@app.route('/')
def index():

	codstr = conn.get('http://678v.cc/verifycode.do?timestamp='+str(int(time.time()))).content
	with open('code.png','wb') as f:
		f.write(codstr)
		f.close()
	image = Image.open('code.png')
	pytesseract.pytesseract.tesseract_cmd = 'F:\\Tesseract-OCR\\tesseract.exe'
	tessdata_dir_config = '--tessdata-dir "F:\\Tesseract-OCR\\tessdata"'
	vcode = pytesseract.image_to_string(image, config=tessdata_dir_config)
	return vcode


if __name__ == '__main__':
	app.run(host="0.0.0.0",debug=True,port=8081)