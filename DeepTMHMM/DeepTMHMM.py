#! /usr/bin/python3

import json
from BioLibPatch import BioLibPatch

class DeepTMHMM:
    def get_result(self, fasta_str: str):
        model = BioLibPatch("DTU/DeepTMHMM")
        return model(fasta_str)

    def get_result_json(self, fasta_str: str):
        return json.dumps(self.get_result(fasta_str))


if __name__ == '__main__':
    test_str = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    deeptmhmm = DeepTMHMM()
    print(deeptmhmm.get_result(test_str))
