#!/usr/bin/python3

from .ipc2_lib.svr_functions import get_pI_features
import pickle
from pkgutil import get_data
from redis import Redis

PEPT_MODEL_FILE = "peptide.pickle"
PROT_MODEL_FILE = "protein.pickle"

pept_est = pickle.loads(get_data(__package__, PEPT_MODEL_FILE))
prot_est = pickle.loads(get_data(__package__, PROT_MODEL_FILE))

redis = Redis("localhost", port=6379, db=4)


def get_result(sequence_str, pred_type):
    X_val, _ = get_pI_features([[sequence_str, '_']])
    if pred_type == "peptide":
        return pept_est.predict(X_val)[0]
    elif pred_type == "protein":
        return prot_est.predict(X_val)[0]


def get_result_dict(sequence_str, pred_type):
    return {pred_type: get_result(sequence_str, pred_type)}
