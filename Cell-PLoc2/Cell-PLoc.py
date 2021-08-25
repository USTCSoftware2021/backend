# ToDo: 异步化方法
import json
import requests
from requests_toolbelt import MultipartEncoder
import re


class QueryError(Exception):
    pass


class CellPloc:
    def __init__(self):
        self.ploc_urls = {
            "Euk-mPLoc2.0": "http://www.csbio.sjtu.edu.cn/cgi-bin/EukmPLoc2.cgi",
            "Hum-mPLoc2.0": "http://www.csbio.sjtu.edu.cn/cgi-bin/HummPLoc2.cgi",
            "Plant-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/PlantmPLoc.cgi",
            "Gpos-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/GposmPLoc.cgi",
            "Gneg-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/GnegmPLoc.cgi",
            "Virus-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/VirusmPLoc.cgi",
        }

    def get_result(self, ploc_type: str, fasta_str: str):
        form = MultipartEncoder({
            "mode": "string",
            "S1": fasta_str,
            "B1": "Submit"
        })
        res = requests.post(self.ploc_urls[ploc_type], data=form, headers={
                            'Content-Type': form.content_type})
        if res.status_code != 200:
            raise QueryError
        return re.search("<font size=4pt color='#5712A3'>(.*?)</font>", res.content.decode()).groups()[0]

    def get_result_json(self, ploc_type: str, fasta_str: str):
        return json.dumps([{"Predicted Location(s)": self.get_result(ploc_type, fasta_str)}])


if __name__ == '__main__':
    test_fasta = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    cell_ploc = CellPloc()
    for i in cell_ploc.ploc_urls.keys():
        print(cell_ploc.get_result_json(i, test_fasta))
