#! /usr/bin/python3

import json
import os
import biolib
import re
import random
# from settings import BASE_DIR

BASE_DIR = '/Users/haoyuanwang/Desktop/iGEM_program/'


def parse(fasta_str: str):
    query_protein = re.search(">(.*?)\n", fasta_str).groups()[0]
    amino_acid_str = fasta_str.split('\n')[1]
    return (query_protein, amino_acid_str)


def str2json(qurey_protein: str, job_id: str):
    result_path = BASE_DIR + 'DeepTMHMM/deeptmhmm_results/' + job_id + '/'
    data = [{"qurey_protein": qurey_protein, "result_path": result_path}]
    return json.dumps(data)


def generate_job_id(length=7):
    BASE_STR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    BASE_LEN = len(BASE_STR)
    job_id = ''
    for i in range(length):
        job_id += BASE_STR[random.randint(0, BASE_LEN-1)]
    return job_id


def deeptmhmm(fasta_str: str):
    deeptmhmm_tool = biolib.load('DTU/DeepTMHMM')
    # update input.fasta file
    os.system('touch input.fasta')
    f = open('input.fasta', 'w')
    f.write(fasta_str)
    f.close()

    # produce a job id randomly (string)
    job_id = generate_job_id()
    qurey_protein, amino_acide_str = parse(fasta_str)
    result = deeptmhmm_tool(args='--fasta input.fasta')
    # print(result)

    # change the result directory name
    os.system('mv biolib_results deeptmhmm_results/%s' % job_id)
    # os.rename("biolib_results", job_id)
    json_data = str2json(qurey_protein, job_id)
    return json_data


if __name__ == '__main__':
    test_str = """>test1
MKMRFFSSPCGKAAVDPADRCKEDQHPMKMRFFSSPCGKAAVDPADRCKEVQQIRDQHPMKMRFFSSPCGKAAVDPADRCKEVQQKMRFFSSPCGKAADRCKEVQQIRDQHPEDQHPMKMRFFSSP"""
    print(deeptmhmm(test_str))
