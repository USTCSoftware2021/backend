#!python
import sys
sys.path.append("..")

import DeepTMHMM

test_sequence = """MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPAD\
RCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""

test_case = """AAAAAAAAAAAAAAAGAGAGAK\nAAAAAASAGSSASSGNQPPQELGLGELLEEFSR\nAAAAASAAGPGGLVAGKEEK"""

# for i in test_case.split():
#     print(DeepTMHMM.get_result_dict(i)["/predicted_topologies.3line"])

print(DeepTMHMM.get_result_dict(test_sequence)["/predicted_topologies.3line"])
