import re
import jpredapi
import requests
from retrying import retry


class UnfinishedError(Exception):
    pass


class JPred:
    def __init__(self):
        self.JOB_URL = "http://www.compbio.dundee.ac.uk/jpred4/cgi-bin/rest/job/id/%s"
        self.SVG_URL = "http://www.compbio.dundee.ac.uk/jpred4/results/%s/%s.svg.html"

    def get_result(self, fasta_str: str):
        res = jpredapi.submit(
            mode="msa", user_format="fasta", seq=fasta_str, silent=True)
        jobid = re.search(
            r'"http://www.compbio.dundee.ac.uk/jpred4/cgi-bin/chklog\?(.*?)"', res.text).groups()[0]
        self.wait_result(jobid)
        return requests.get(self.SVG_URL % (jobid, jobid)).text

    @retry(wait_fixed=5000, stop_max_attempt_number=5)
    def wait_result(self, jobid):
        res = requests.get(self.JOB_URL % (jobid))
        if "finished" not in res.text:
            raise UnfinishedError
        return res

    def get_result_dict(self, fasta_str: str):
        return {"svg": self.get_result(fasta_str)}


if __name__ == '__main__':
    test_str = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    jpred = JPred()
    print(jpred.get_result_dict(test_str))
