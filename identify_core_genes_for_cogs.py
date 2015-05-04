#!/usr/bin/python

#this script expects the orthomcl groups.txt file as arg1 and the goodproteins.fasta file as arg2



from Bio import SeqIO                                                               
import sys                                                                          
import fileinput
import shutil
import os
import sys
from Bio import AlignIO
from Bio.Alphabet import generic_protein
from Bio.Nexus import Nexus
from Bio.Align.Applications import ClustalwCommandline


core = 0
paralog = 0


cog_fixed = open('crisp_iners_core_for_cog.fasta','w')




for line in fileinput.input(sys.argv[1]):
    
    
    line = line.strip()
    
    
    orf = line.split(" ")[0]
    
    
    orf = orf.replace(':','')
    
    
    protein_ids = line.split(" ")
    
    
    protein_ids.pop(0)
    

    count=0
    
    
    protein_org_set = list()
    

    for i in protein_ids:

    
       protein_org = i.split("|")[1]       

    
       protein_org = protein_org.split("_")[0]

    
       protein_org_set.append(protein_org)
    

    
       count +=1

    
    size1=len(protein_org_set)
    
    
    protein_org_set = list(set(protein_org_set))
    

    
    size2=len(protein_org_set)

    
    print(str(size1) + "   " + str(size2))

    if size1 > size2:
        
        print "PARALOG"
        paralog += 1    

    
    elif size2 ==12 or size2 ==11:
        

        core += 1
        

        orf_seq = open('%s.fasta' % (orf),'w')
        
        seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
        SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")

        
        orf_seq.close()

        
        filename = orf + '.fasta'
        
        
        for rec in SeqIO.parse(open(filename,"r"), "fasta"):            

            rec.id = rec.id.split("|")[1]
        
            rec.id = rec.id.split("_")[0]
        
            rec.id = rec.id.replace("-","")

            cog_fixed.write('>' + orf + '_' + rec.id +'\n'+str(rec.seq)+'\n')

print("paralog\t" + str(paralog))
print("core\t" + str(core))


cog_fixed.close()


