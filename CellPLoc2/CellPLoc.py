# ToDo: 异步化方法
import requests
from requests_toolbelt import MultipartEncoder
import re


class QueryError(Exception):
    pass


class CellPloc:
    def __init__(self):
        self.ploc_urls = {
            "euk": "http://www.csbio.sjtu.edu.cn/cgi-bin/EukmPLoc2.cgi",
            "hum": "http://www.csbio.sjtu.edu.cn/cgi-bin/HummPLoc2.cgi",
            "plant": "http://www.csbio.sjtu.edu.cn/cgi-bin/PlantmPLoc.cgi",
            "gpos": "http://www.csbio.sjtu.edu.cn/cgi-bin/GposmPLoc.cgi",
            "gneg": "http://www.csbio.sjtu.edu.cn/cgi-bin/GnegmPLoc.cgi",
            "virus": "http://www.csbio.sjtu.edu.cn/cgi-bin/VirusmPLoc.cgi",
        }

    def get_result(self, fasta_str: str, ploc_type: str):
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

    def get_result_dict(self, fasta_str: str, ploc_type: str):
        return {ploc_type: self.get_result(fasta_str, ploc_type)}


if __name__ == '__main__':
    test_fasta = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    cell_ploc = CellPloc()
    for i in cell_ploc.ploc_urls.keys():
        print(cell_ploc.get_result_dict(test_fasta, i))
