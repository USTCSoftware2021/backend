#!python
import sys
sys.path.append("..")

import CellPLoc
from CellPLoc.CellPLoc import ploc_urls

test_sequence = """MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPAD\
RCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""

for i in ploc_urls.keys():
    print(CellPLoc.get_result_dict(test_sequence, i))
