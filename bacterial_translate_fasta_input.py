#!/usr/bin/python

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

###### for bacterial genomes only, working version 1.0  ###########


filepath = sys.argv[1]


name = filepath.split('.')[0]


count = 0

trans_out = open('%s_protein.fasta' %(name),'w')



for seq_record in SeqIO.parse(filepath, "fasta"):
    count += 1

    prot_id = ("%s_orf" %(name[:-3]) + str(count) )


    seq = seq_record.seq


    if len(seq) < 25:

        print len(seq)

        continue

    
    protein = seq.translate(table="Bacterial")


    trans_out.write(">" + prot_id + "\n" + str(protein) + "\n")
    
    
