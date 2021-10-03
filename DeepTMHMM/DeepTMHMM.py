#! /usr/bin/python3

from .BioLibPatch import BioLibPatch
from redis import Redis

redis = Redis("localhost", port=6379, db=5)


def get_result(sequence_str: str):
    sequence_str = ">sample\n" + sequence_str
    model = BioLibPatch("DTU/DeepTMHMM")
    return model(sequence_str)


def get_result_dict(sequence_str: str):
    return get_result(sequence_str)


if __name__ == '__main__':
    test_sequence = """MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEV\
QQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    print(get_result(test_sequence))
