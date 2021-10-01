from pool import app
from CellPLoc2 import CellPloc
from DeepTMHMM import DeepTMHMM
from JPred import JPred
from IPC2 import IPC2


cellPloc = CellPloc()
deepTMHMM = DeepTMHMM()
jPred = JPred()
iPC2 = IPC2()

@app.task
def get_CellPloc(fasta_str, ploc_type):
    return cellPloc.get_result_dict(fasta_str, ploc_type)

@app.task
def get_DeepTMHMM(fasta_str):
    return deepTMHMM.get_result_dict(fasta_str)

@app.task
def get_JPred(fasta_str):
    return jPred.get_result_dict(fasta_str)

@app.task
def get_IPC2(fasta_str, ipc2_type):
    return iPC2.get_result_json(fasta_str, ipc2_type)
