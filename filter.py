#!/usr/bin/python
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import sys

singles_out = open('singletons_cleaned.fasta','w')
count = 0
for rec in SeqIO.parse(open(sys.argv[1],"r"), "fasta") :
    num_n = 0
    for i in rec:
        if i == 'X':
            num_n += 1
            print num_n
    if num_n > 5:
        continue
    singles_out.write('>'+rec.id+'\n'+str(rec.seq)+'\n')
    count += 1
print count

singles_out.close()
