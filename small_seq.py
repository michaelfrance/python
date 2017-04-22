#!/usr/bin/python
from Bio.Seq import Seq
from Bio import SeqIO
import sys
greater500 = 0
short_seq = 0
totalseq = 0
long_seqlength = 0.0
short_seqlength = 0.0

for rec in SeqIO.parse(open(sys.argv[1],"r"), "fasta"):
	
    totalseq += 1


    if len(rec.seq) > 500:
        greater500 += 1
        long_seqlength = long_seqlength + len(rec.seq)
    if len(rec.seq) < 500:
        short_seqlength = short_seqlength + len(rec.seq)
        short_seq += 1
    

average_length = (short_seqlength+long_seqlength)/float(totalseq)
ave_long = long_seqlength/float(greater500)
ave_short = short_seqlength/float(short_seq)

print(str(totalseq))
print(str(int(average_length)))
print(str(greater500))
print(str(int(ave_long)))
print(str(short_seq))
print(str(int(ave_short)))
