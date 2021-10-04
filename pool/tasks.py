import re
from pool import app, hash_redis
import CellPLoc
import DeepTMHMM
import JPred
import IPC2


@app.task
def get_CellPLoc(md5_hash):
    try:
        result = dict()
        for ploc_type in CellPLoc.ploc_urls.keys():
            result[ploc_type] = CellPLoc.get_result(hash_redis.get(md5_hash).decode(), ploc_type)
        result["status"] = "Success"
        CellPLoc.redis.set(md5_hash, str(result))
        return True
    except:
        CellPLoc.redis.set(md5_hash, str({"status": "Failed"}))
        return False

@app.task
def get_DeepTMHMM(md5_hash):
    try:
        result = DeepTMHMM.get_result_dict(hash_redis.get(md5_hash).decode())
        result["status"] = "Success"
        DeepTMHMM.redis.set(md5_hash, str(result))
        return True
    except:
        DeepTMHMM.redis.set(md5_hash, str({"status": "Failed"}))
        return False

@app.task
def get_JPred(md5_hash):
    try:
        result = JPred.get_result_dict(hash_redis.get(md5_hash).decode())
        result["status"] = "Success"
        JPred.redis.set(md5_hash, str(result))
        return True
    except Exception as e:
        JPred.redis.set(md5_hash, str({"status": "Failed"}))
        return False

@app.task
def get_IPC2(md5_hash):
    try:
        result = dict()
        for ipc2_type in ["peptide", "protein"]:
            result[ipc2_type] = IPC2.get_result_dict(hash_redis.get(md5_hash).decode(), ipc2_type)
        result["status"] = "Success"
        IPC2.redis.set(md5_hash, str(result))
        return True
    except Exception as e:
        IPC2.redis.set(md5_hash, str({"status": "Failed"}))
        return False
