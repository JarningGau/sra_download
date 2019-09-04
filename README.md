# sra_download
This is a python script (draft) for download sequencing data from SRA database

---



### Features

- Parallel processing download or fastq-dump

### Usage

```txt
usage: sra_download.py [-h] [--wget] [--prefetch] [--fastq-dump] [--sam-dump]
                       [-t TARGET_PATH] [--sra SRA_FILE] [--threads THREADS]
                       [--version]

optional arguments:
  -h, --help            show this help message and exit
  --wget                download sra file through ftp use wget
  --prefetch            download sra file through https use prefetch
  --fastq-dump          tranverse sra to fastq.gz
  --sam-dump            tranverse sra to SAM and then to fastq with CB and UB
                        information, specially for dropseq data
  -t TARGET_PATH, --target TARGET_PATH
                        download path of sra file use --wget. For --fastq-
                        dump, this is the path containing sra file
  --sra SRA_FILE        The txt file contains SRR id for download
  --threads THREADS     threads for tasks
  --version             show program's version number and exit
```

```shell
#for example
# step1. Download SRA file though ftp (wget)
python sra_download.py --wget -t $target_path --sra sra_list.txt --threads 5
# or Download SRA file though https (prefetch)
# Under this mode, user can not define the download path, 
# except define by vdb-config. (vdb-config -i)
# The default download path is /home/${user_name}/ncbi
python sra_download.py --prefetch --sra sra_list.txt --threads 5
# step2. Tranverse SRA file to FASTQ file
python sra_download.py --fastq_dump -t $target_path --threads 5
```

`sra_list.txt` contains a series of SRR ID. Each ID takes up one line.

`run.pbs` is a pbs script running on Nebula cluster.

Please add `sratoolkit` directory to you $PATH first.

For details of `vdb-config`, see this link: <https://github.com/ncbi/sra-tools/wiki/Toolkit-Configuration>

### Requirements

- [sratoolkit](<https://www.ncbi.nlm.nih.gov/sra/docs/toolkitsoft/>)