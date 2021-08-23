import json
import requests
from requests_toolbelt import MultipartEncoder
import re

urls = {
    "Euk-mPLoc2.0": "http://www.csbio.sjtu.edu.cn/cgi-bin/EukmPLoc2.cgi",
    "Hum-mPLoc2.0": "http://www.csbio.sjtu.edu.cn/cgi-bin/HummPLoc2.cgi",
    "Plant-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/PlantmPLoc.cgi",
    "Gpos-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/GposmPLoc.cgi",
    "Gneg-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/GnegmPLoc.cgi",
    "Virus-mPLoc": "http://www.csbio.sjtu.edu.cn/cgi-bin/VirusmPLoc.cgi",
}


class QueryError(Exception):
    pass


def sjtu_job(url: str, fasta_str: str):
    # url = "http://www.csbio.sjtu.edu.cn/cgi-bin/EukmPLoc2.cgi"
    msg = MultipartEncoder({
        "mode": "string",
        "S1": fasta_str,
        "B1": "Submit"
    })
    res = requests.post(url, data=msg, headers={
                        'Content-Type': msg.content_type})
    if res.status_code != 200:
        raise QueryError
    return re.search("<font size=4pt color='#5712A3'>(.*?)</font>", res.content.decode()).groups()[0]


def str2json(method: str, protein: str, location: str):
    data = [{"method": method, "Query Protein": protein,
             "Predicted Location(s)": location}]
    return json.dumps(data)


def sjtu(fasta_str: str):
    query_protein = re.search(">(.*?)\n", fasta_str).groups()[0]
    result = []
    for url in urls:
        # TODO: select a few specific urls
        location = sjtu_job(urls[url], fasta_str)
        result.append(str2json(url, query_protein, location))
    return result


if __name__ == '__main__':
    test_str = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    # query_protein = re.search(">(.*?)\n", test_str).groups()[0]
    # for url in urls:
    #     json_data = str2json(
    #         query_protein, sjtu_job(urls[url], test_str))
    #     print(json_data)
    print(sjtu(test_str))
