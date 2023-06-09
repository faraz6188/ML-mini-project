from flask import Flask
from flask import request,redirect,render_template,url_for
from werkzeug.utils import secure_filename
import os
import pytesseract
import sys
from functools import update_wrapper
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.views.decorators.cache import never_cache
from importlib import reload
from PIL import ImageFilter
from PIL import Image

import sys
reload(sys)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './media'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitImage/',methods=['POST',])
def submitImage():
    image = request.files['ocrImage']
    text = ''
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    text = pytesseract.image_to_string(img)
    f = open(os.path.join(app.config['UPLOAD_FOLDER'], filename)+'.txt','w')
    f.write(text)
    f.close()
    return render_template('textFile.html',text=text,filename=f)


if __name__ == '__main__':
    app.run('0.0.0.0',8000)
