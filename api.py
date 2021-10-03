from io import BytesIO
from flask import Flask, send_file, request
import json
from hashlib import md5
import logging
from utils import hash_redis, get_db_from_task, task_submit

app = Flask(__name__)

def check(seq):
    return True

@app.route("/api", methods=["POST"])
def api():
    try:
        req = request.get_json()
        if check(req["sequence"]):
            md5_hex = md5(req["sequence"].encode()).hexdigest()
            hash_redis.set(md5_hex, req["sequence"])
            
            for task in req["tasks"]:
                if type(req["tasks"][task]) == dict:
                    task_submit(task, **req["tasks"][task])
                elif req["tasks"][task] == True:
                    task_submit(task)
                get_db_from_task(task).set(md5_hex, json.dumps({"status": "Running"}))

            return json.dumps({"hash": md5_hex})
    except Exception as e:
        raise e
        # return json.dumps({"status": str(e)})


@app.route("/api/<md5_hash>/<task>/", methods=["get"])
def get_task_info(md5_hash, task):
    if hash_redis.get(md5_hash):
        result = get_db_from_task(task).get(md5_hash)
        if task == "DeepTMHMM":
            result = eval(result)
            del result["/plot.png"]
            return json.dumps(result)
        if result != None:
            return json.dumps(eval(result))
        else:
            return json.dumps({"status": "NotRequested"})
    else:
        return json.dumps({"status": "NoSuchSequence"}) 

@app.route("/api/<md5_hash>/DeepTMHMM/plot.png", methods=["get"])
def get_plot(md5_hash):
    if hash_redis.get(md5_hash):
        result = get_db_from_task("DeepTMHMM").get(md5_hash)
        return send_file(BytesIO(result["/plot.png"]), mimetype="image/png", as_attachment=False, attachment_filename="plot.png")
    else:
        return json.dumps({"status": "NoSuchSequence"}) 

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