import re
import jpredapi
import requests
from retrying import retry
from redis import Redis


class UnfinishedError(Exception):
    pass


JOB_URL = "http://www.compbio.dundee.ac.uk/jpred4/cgi-bin/rest/job/id/%s"
SVG_URL = "http://www.compbio.dundee.ac.uk/jpred4/results/%s/%s.svg.html"
redis = Redis("localhost", port=6379, db=2)


def get_result(sequence_str: str):
    sequence_str = ">sample\n" + sequence_str
    res = jpredapi.submit(
        mode="msa", user_format="fasta", seq=sequence_str, silent=True)
    jobid = re.search(
        r'"http://www.compbio.dundee.ac.uk/jpred4/cgi-bin/chklog\?(.*?)"', res.text).groups()[0]
    wait_result(jobid)
    return requests.get(SVG_URL % (jobid, jobid)).text


@retry(wait_fixed=5000, stop_max_attempt_number=5)
def wait_result(jobid):
    res = requests.get(JOB_URL % (jobid))
    if "finished" not in res.text:
        raise UnfinishedError
    return res


def get_result_dict(sequence_str: str):
    return {"svg": get_result(sequence_str)}


if __name__ == '__main__':
    test_str = """MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPM\n
KMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    print(get_result_dict(test_str))
