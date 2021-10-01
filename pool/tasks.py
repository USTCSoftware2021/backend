from pool import app
from CellPLoc import CellPloc
from DeepTMHMM import DeepTMHMM
from JPred import JPred
from IPC2 import IPC2


cellPloc = CellPloc()
deepTMHMM = DeepTMHMM()
jPred = JPred()
iPC2 = IPC2()

@app.task
def get_CellPloc(sequence_str, ploc_type):
    return cellPloc.get_result_dict(sequence_str, ploc_type)

@app.task
def get_DeepTMHMM(sequence_str):
    return deepTMHMM.get_result_dict(sequence_str)

@app.task
def get_JPred(sequence_str):
    return jPred.get_result_dict(sequence_str)

@app.task
def get_IPC2(sequence_str, ipc2_type):
    return iPC2.get_result_dict(sequence_str, ipc2_type)

def task_process