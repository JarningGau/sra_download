# sra_download
This is a python script (draft) for download sequencing data from SRA database

---



### Features

- Parallel processing download or fastq-dump

### Usage

```txt
usage: sra_download.py [-h] [--download] [--fastq_dump] [-t TARGET_PATH]
                       [--sra_file SRA_FILE] [--threads THREADS] [--version]

optional arguments:
  -h, --help            show this help message and exit
  --download            download sra file
  --fastq_dump          tranverse sra to fastq.gz
  -t TARGET_PATH, --target TARGET_PATH
                        target path
  --sra_file SRA_FILE   The txt file contains SRR id for download
  --threads THREADS     threads for tasks
  --version             show program's version number and exit
```

```shell
#for example
# step1. Download SRA file
python sra_download.py --download -t $target_path --sra_file sra_list.txt --threads 5
# step2. Tranverse SRA file to FASTQ file
python sra_download.py --fastq_dump -t $target_path --threads 5
```

`sra_list.txt` contains a series of SRR ID. Each ID takes up one line.

`run.pbs` is a pbs script running on Nebula cluster.

Please add `sratoolkit` directory to you $PATH first.

### Requirements

- [sratoolkit](<https://www.ncbi.nlm.nih.gov/sra/docs/toolkitsoft/>)