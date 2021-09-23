from io import BytesIO
from flask import Flask, send_file
import json
import os
from os import path
from random import choice
# from CellPLoc2 import CellPloc
# from DeepTMHMM import DeepTMHMM
# from JPred import JPred

app = Flask(__name__)


@app.route("/")
def hello_world():
    return json.dumps({"msg": "hello, world."})


@app.route("/random")
def random():
    root = "/root/JSApiSample/statics"
    with open(path.join(root, choice(os.listdir(root))), 'rb') as f:
        content = f.read()
    return send_file(BytesIO(content), mimetype="image/png", as_attachment=False, attachment_filename="random.png")


@app.after_request
def after_request(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


app.run("0.0.0.0", 6002)
