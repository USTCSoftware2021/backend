import re
from time import sleep, time
import json
import jpredapi
# from settings import BASE_DIR

BASE_DIR = '/Users/haoyuanwang/Desktop/iGEM_program/'


def jpred_job(fasta_seq: str):
    # fasta_seq: only amino acid sequence
    submit_response = jpredapi.submit(
        mode='single', user_format='fasta', seq=fasta_seq, silent=False)
    if submit_response:
        ls = re.findall(
            r'"http://www.compbio.dundee.ac.uk/jpred4/cgi-bin/chklog\?(.*?)"', submit_response.text)
        if ls:
            jobid = ls[0]
            start_time = time()
            while True:
                sleep(10)
                if 'finished' in jpredapi.status(jobid=jobid, results_dir_path='jpred_results', extract=True, silent=False).text:
                    break
                if time() - start_time > 120:
                    return None
            return jobid


def parse(fasta_str: str):
    # fasta: all fasta sequence
    # if fasta[0] == '>':
    query_protein = re.search(">(.*?)\n", fasta_str).groups()[0]
    # amino_acid_str = re.search(">*\n(.*?)", fasta).groups()[0]  # wrong
    amino_acid_str = fasta_str.split('\n')[1]
    # else:
    #     query_protein = "Unnamed"
    #     amino_acid_str = fasta
    return (query_protein, amino_acid_str)


def str2json(query_protein: str, jobid: str):
    svg_path = '%sJPred/jpred_results/%s/%s.svg.html' % (
        BASE_DIR, jobid, jobid)
    data = [{"query_protein": query_protein, "svg_path": svg_path}]
    return json.dumps(data)


def jpred(fasta_str: str):
    query_protein, amino_acid_str = parse(fasta_str)
    jobid = jpred_job(amino_acid_str)
    json_data = str2json(query_protein, jobid)
    return json_data


if __name__ == '__main__':
    test1_str = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    # test2_str = """MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    # query_protein, amino_acid_str = parse(test1_str)
    # jobid = jpred_job(amino_acid_str)
    # # print('jobid:%s query_protein:%s' % (jobid, query_protein))
    # # query_protein, amino_acid_str = parse(test2_str)
    # # jobid = jpred(amino_acid_str)
    # # print('jobid:%s query_protein:%s' % (jobid, query_protein))
    # # print("query_protein:%s amino_acid_str:%s" % (query_protein, amino_acid_str))
    # json_data = str2json(query_protein, jobid)
    print(jpred(test1_str))
