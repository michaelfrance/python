#!/usr/bin/python
from Bio.Seq import Seq
from Bio import SeqIO
import sys

#asks the user for the genome file name

filepath = sys.argv[1]

name = filepath.split('.')[-2]
Genome = ''

#opens the give file
for rec in SeqIO.parse(open(filepath,"r"), "fasta") :
    Genome += rec + ("N" * 50) 

Genome.id = "mergedseq"
Genome.description = "merged seq"
SeqIO.write(Genome, "%s_combined.fasta" %(name), "fasta")




