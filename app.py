from flask import Flask, render_template, flash, request
import shutil

import requests

from base64 import b64encode

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route('/')
def index():
    url = 'https://tracuunnt.gdt.gov.vn/tcnnt/captcha.png?uid=d436b815-5ad2-497c-adb9-33fffddc2f19'
    response = requests.get(url, stream=True, verify=False)
    encode = b64encode(response.content)
    iur = "data:%s;base64,%s" % ("image/png",encode)
    return render_template('index.html',imag_data = iur)


if __name__ == "__main__":
    app.run()