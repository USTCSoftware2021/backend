#! /usr/bin/python3

from .BioLibPatch import BioLibPatch

class DeepTMHMM:
    def get_result(self, fasta_str: str):
        model = BioLibPatch("DTU/DeepTMHMM")
        return model(fasta_str)

    def get_result_dict(self, fasta_str: str):
        return self.get_result(fasta_str)


if __name__ == '__main__':
    test_str = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    deeptmhmm = DeepTMHMM()
    print(deeptmhmm.get_result(test_str))
