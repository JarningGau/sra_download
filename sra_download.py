import os
import threading
import argparse


## Parameters
parser = argparse.ArgumentParser()

parser.add_argument('--download', action='store_const', dest='mode',
        const='download',
        help='download sra file')
parser.add_argument('--fastq_dump', action='store_const', dest='mode',
        const='fastq_dump',
        help='tranverse sra to fastq.gz')
parser.add_argument('-t','--target', action='store', dest='target_path',
        help='target path')
parser.add_argument('--sra_file', action='store', dest='sra_file',
        help='The txt file contains SRR id for download')
parser.add_argument('--threads', action='store', dest='threads', type=int,
        help='threads for tasks')
parser.add_argument('--version', action='version', version='sra_download 0.1')

paras = parser.parse_args()


class runParallel(threading.Thread):
    def __init__(self, cmds):
        super(runParallel, self).__init__()
        self.cmds = cmds

    def run(self):
        for cmd in self.cmds:
            os.system(cmd)

def make_parallel(cmds, threads):
    '''
    Divide tasks into blocks for parallel running.
    Put the cmd in parallel into the same bundle.
    The bundle size equals the threads.
    '''
    cmd_list = []
    i,j = 0,0
    for cmd in cmds:
        if j == 0:
            cmd_list.append(list())
            i += 1
        cmd_list[i-1].append(cmd)
        j = (j+1) % threads
    return cmd_list

def exe_parallel(cmds, threads):
    cmd_list = make_parallel(cmds, threads)
        for cmd_batch in cmd_list:
            for cmd in cmd_batch:
                t = runParallel(cmd)
                t.start()
            t.join()

def check_config():
    pass

def load_task(taskfile):
    '''
    The taskfile is a txt file with sra ids. Each id in one line. 
    For Example:
    srr_list.txt
    ---------
    SRR5440939
    SRR5440940
    ---------
    '''
    return [l.rstrip() for l in open(taskfile, 'r').readlines()]

def load_sra_file(path):
    return [os.path.join(path, sra) for sra in os.listdir(path) if sra.endswith("sra")]

def wget(srr_id):
    '''
    wget is considered in priority to download sra file
    '''
    target_path = paras.target_path.rstrip("/")
    if not os.path.exists(target_path): os.makedirs(target_path)
    cmd = ['wget --timeout=30 -nc -c -O %s/%s.sra ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/%s/%s/%s/%s.sra' %(
        target_path, srr_id, srr_id[0:3], srr_id[0:6], srr_id, srr_id)]
    return cmd

def prefetch(srr_id):
    pass

def fastq_dump(sra_file):
    target_path = paras.target_path if paras.target_path.endswith("/") else paras.target_path+"/"
    cmd = ['fastq-dump -O %s --split-3 --gzip %s' %(target_path, sra_file)]
    return cmd


if __name__ == '__main__':
    check_config()
    if paras.mode == "download":
        tasks = load_task(paras.sra_file)
        cmds = [wget(srr_id) for srr_id in tasks]
    if paras.mode == "fastq_dump":
        sra_files = load_sra_file(paras.target_path)
        cmds = [fastq_dump(sra_f) for sra_f in sra_files]
    try:
        cmds
    except NameError:
        print("Please select one mode [--download|--fastq_dump]")
    else:
        exe_parallel(cmds, paras.threads)