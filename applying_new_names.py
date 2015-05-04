#!/usr/bin/python

from Bio.Seq import Seq
from Bio import SeqIO
import sys


old_rec_ids = list()

filename = str(sys.argv[2]).split(".")[0]


fasta_out = open("%s_prot_names.fasta" %(filename),"w")

for rec in SeqIO.parse(open(sys.argv[1],"r"), "fasta"):
    old_rec_ids.append(rec.id)

counter = 0
for rec in SeqIO.parse(open(sys.argv[2],"r"),"fasta"):
    rec.id = old_rec_ids[counter]
    fasta_out.write(">" + str(rec.id) + "\n" + str(rec.seq) + "\n")
    counter += 1
