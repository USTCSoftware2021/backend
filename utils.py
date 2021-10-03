from pool import tasks, hash_redis
import CellPLoc
import DeepTMHMM
import JPred
import IPC2

class TaskInvalidError(Exception):
    pass


def task_submit(task: str, *args):
    if task == "CellPLoc":
        tasks.get_CellPLoc.apply_async([task])
    elif task == "DeepTMHMM":
        tasks.get_DeepTMHMM.apply_async([task])
    elif task == "JPred":
        tasks.get_IPC2.apply_async([task])
    elif task == "IPC2":
        tasks.get_JPred.apply_async([task])
    else:
        raise TaskInvalidError

def get_db_from_task(task: str):
    if task == "CellPLoc":
        return CellPLoc.redis
    elif task == "DeepTMHMM":
        return DeepTMHMM.redis
    elif task == "JPred":
        return JPred.redis
    elif task == "IPC2":
        return IPC2.redis
    else:
        raise TaskInvalidError