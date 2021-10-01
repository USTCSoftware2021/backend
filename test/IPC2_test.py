#!python
import sys
sys.path.append("..")

import IPC2

test_sequence = """MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPAD\
RCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""

print(IPC2.get_result_dict(test_sequence, "peptide"))
print(IPC2.get_result_dict(test_sequence, "protein"))
