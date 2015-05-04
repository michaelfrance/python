#!/usr/bin/python

from Bio.Seq import Seq
from Bio import SeqIO
import sys
import os


file_list = os.listdir(".")

fasta_out = open("ci_outgroups_DNA.fasta","w")

for filename in file_list:
    for rec in SeqIO.parse(open(filename,"r"), "fasta"):
    	fasta_out.write(">" + str(rec.id) + "\n" + str(rec.seq) + "\n")
    	

