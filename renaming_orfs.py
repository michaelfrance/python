#!/usr/bin/python

import sys
import os

#looping through text file with 1 genome filename per line

for org_name in open(sys.argv[1],"r"):
    org_name = org_name.replace("\n","")
    genus_species = ''.join(org_name.split("_")[0:2]).replace("\n","")
    orf_filename = org_name + ".PATRIC.ffn"
    
    strain_name = org_name.split("_")[2]
    print strain_name

    if genus_species == "Pseudomonasaeruginosa":
        renamed_file = open('%s_renamed.fasta' %(strain_name), "w")
    	for rec in SeqIO.parse(open(orf_filename,"r"), "fasta"):
    		old_name = str(rec.id)
    		new_name = strain_name
    		rename_file.write('>' + new_name +'\n'+str(rec.seq)+'\n')
    	renamed_file.close()

    	   



