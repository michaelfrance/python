#!/usr/bin/python
from Bio import SeqIO
from Bio.Blast import NCBIXML
from Bio.Blast import NCBIWWW
from Bio.Align.Applications import ClustalwCommandline
import sys



gene_name = sys.argv[1].split(".")[0]

fasta_out = open('%s.fasta' %(gene_name), "w")

fasta_name = gene_name + '.fasta'

blast_records = NCBIXML.parse(open(sys.argv[1]))

check = list()
for blast_record in blast_records:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
            	 
            	 count = 0

            	 sequence_name = alignment.title.split(" ")[1]

            	 for string in check:
            	     if string == sequence_name:
            	     	count = 1
            	 if count > 0:
            	 	continue
            	 	
            	 fasta_out.write('>' + alignment.title.split(" ")[1] + '\n' + hsp.sbjct + '\n')

            	 check.append(sequence_name)


cline = ClustalwCommandline("clustalw", infile=fasta_name, output="PHYLIP")
cline()