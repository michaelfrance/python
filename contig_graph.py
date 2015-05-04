#!/usr/bin/python

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

filepath = sys.argv[1]


name = filepath.split('.')[0]

contig_graph_out = open('%s_contig.tsv' %(name),'w')

contig_graph_out.write("Contig\tLength\n")
for seq_record in SeqIO.parse(filepath, "fasta"):

    contig_graph_out.write(str(seq_record.id) + "\t" + len(seq_record.seq) + "\n")
 

contig_graph_out.close()