from io import BytesIO
from flask import Flask, send_file, request
import json
from hashlib import md5
import logging
from utils import hash_redis, get_db_from_task, task_submit
import re

app = Flask(__name__)

sequence_checker = re.compile("^[ACDEFGHIKLMNPQRSTUVWY\s]+$")

def check(seq):
    return sequence_checker.match(seq)

@app.route("/api", methods=["POST"])
def api():
    try:
        req = request.get_json()
        if check(req["sequence"]):
            md5_hash = md5(req["sequence"].encode()).hexdigest()
            hash_redis.set(md5_hash, req["sequence"])
            
            for task in req["tasks"]:
                db = get_db_from_task(task)
                if not db.get(md5_hash) or eval(db.get(md5_hash))["status"] == "Failed":
                    if type(req["tasks"][task]) == dict:
                        task_submit(task, md5_hash, **req["tasks"][task])
                    elif req["tasks"][task] == True:
                        task_submit(task, md5_hash)
                    db.set(md5_hash, json.dumps({"status": "Running"}))

            return json.dumps({"hash": md5_hash})
    except Exception as e:
        raise e
        # return json.dumps({"status": str(e)})


@app.route("/api/<md5_hash>/<task>/", methods=["get"])
def get_task_info(md5_hash, task):
    if hash_redis.get(md5_hash):
        result = get_db_from_task(task).get(md5_hash)
        result = eval(result)
        if task == "DeepTMHMM" and result["status"] == "Success":
            del result["/plot.png"]
            result["/TMRs.gff3"] = result["/TMRs.gff3"].decode()
            result["/predicted_topologies.3line"] = result["/predicted_topologies.3line"].decode()
            return json.dumps(result)
        if result != None:
            return json.dumps(result)
        else:
            return json.dumps({"status": "NotRequested"})
    else:
        return json.dumps({"status": "NoSuchSequence"}) 

@app.route("/api/<md5_hash>/DeepTMHMM/plot.png", methods=["get"])
def get_plot(md5_hash):
    if hash_redis.get(md5_hash):
        result = eval(get_db_from_task("DeepTMHMM").get(md5_hash))
        if (result["status"] == "Success"):
            return send_file(BytesIO(result["/plot.png"]), mimetype="image/png", as_attachment=False, attachment_filename="plot.png")
        else:
            return json.dumps({"status": result["status"]})
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