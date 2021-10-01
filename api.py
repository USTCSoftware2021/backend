from io import BytesIO
from flask import Flask, send_file, request
import json
import os
from os import path
from random import choice
from hashlib import md5
import logging

app = Flask(__name__)

@app.route("/api", methods=["POST"])
def api():
    req = request.get_json()
    return json.dumps([md5(req["sequence"].encode()).hexdigest()])

@app.route("/api/")

# @app.route("/random")
# def random():
#     root = "/root/JSApiSample/statics"
#     with open(path.join(root, choice(os.listdir(root))), 'rb') as f:
#         content = f.read()
#     return send_file(BytesIO(content), mimetype="image/png", as_attachment=False, attachment_filename="random.png")


@app.after_request
def after_request(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = '*'

    return res


if __name__ == "__main__":
    app.run("0.0.0.0", 6002)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)