#!/usr/bin/python3

from .ipc2_lib.svr_functions import get_pI_features
import pickle
import json
from pkgutil import get_data


PEPT_MODEL_FILE = "peptide.pickle"
PROT_MODEL_FILE = "protein.pickle"


class IPC2:
    def __init__(self) -> None:
        self.pept_est = pickle.loads(get_data(__package__, PEPT_MODEL_FILE))
        self.prot_est = pickle.loads(get_data(__package__, PROT_MODEL_FILE))


    def get_result(self, fasta_str, pred_type):
        X_val, _ = get_pI_features([[fasta_str, '_']])
        if pred_type == "peptide":
            return self.pept_est.predict(X_val)[0]
        elif pred_type == "protein":
            return self.prot_est.predict(X_val)[0]

    def get_result_json(self, fasta_str, pred_type):
        return {pred_type: self.get_result(fasta_str, pred_type)}