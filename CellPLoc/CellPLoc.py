import requests
from requests_toolbelt import MultipartEncoder
import re
from redis import Redis


class QueryError(Exception):
    pass

redis = Redis("localhost", port=6379, db=3)

ploc_urls = {
    "euk": "http://www.csbio.sjtu.edu.cn/cgi-bin/EukmPLoc2.cgi",
    "hum": "http://www.csbio.sjtu.edu.cn/cgi-bin/HummPLoc2.cgi",
    "plant": "http://www.csbio.sjtu.edu.cn/cgi-bin/PlantmPLoc.cgi",
    "gpos": "http://www.csbio.sjtu.edu.cn/cgi-bin/GposmPLoc.cgi",
    "gneg": "http://www.csbio.sjtu.edu.cn/cgi-bin/GnegmPLoc.cgi",
    "virus": "http://www.csbio.sjtu.edu.cn/cgi-bin/VirusmPLoc.cgi",
}


def get_result(sequence_str: str, ploc_type: str):
    sequence_str = ">sample\n" + sequence_str
    form = MultipartEncoder({
        "mode": "string",
        "S1": sequence_str,
        "B1": "Submit"
    })
    res = requests.post(ploc_urls[ploc_type], data=form, headers={
                        'Content-Type': form.content_type})
    if res.status_code != 200:
        raise QueryError
    return re.search("<font size=4pt color='#5712A3'>(.*?)</font>", res.content.decode()).groups()[0]


def get_result_dict(sequence_str: str, ploc_type: str):
    return {ploc_type: get_result(sequence_str, ploc_type)}


if __name__ == '__main__':
    test_sequence = """MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQ\n
QIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    for i in ploc_urls.keys():
        print(get_result_dict(test_sequence, i))
