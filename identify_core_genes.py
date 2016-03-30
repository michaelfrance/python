#!/usr/bin/python
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
import time



core = 0
paralog = 0

running_length = 1
partition = open("crisp_iners_outgroups_partition.txt","w")

for line in fileinput.input(sys.argv[1]):
    line = line.strip()
    orf = line.split(" ")[0]
    orf = orf.replace(':','')
    #print orf

    protein_ids = line.split(" ")

    protein_ids.pop(0)
 

    remove_list = list()
    for i in protein_ids:
       if i.split("|")[0] == "lic17":
           remove_list.append(i)
    for removal in remove_list:
        protein_ids.remove(removal)

    count=0
    protein_org_set = list()
    size1=len(protein_ids)

    for i in protein_ids:
       protein_org = i.split("|")[1]       
       protein_org = protein_org.split("_")[0]
       protein_org_set.append(protein_org)
       count +=1
    protein_org_set = list(set(protein_org_set))
    
    #print protein_org_set
    #time.sleep(1)    
    size2=len(protein_org_set)
    
    if size1 > size2:
        print "HERE"
        paralog = paralog + 1 
    elif size2 == 40:
        print "HERE2"
        core = core + 1
        orf_seq = open('%s.fasta' % (orf),'w')
        seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
        SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
        orf_seq.close()
        filename = orf + '.fasta'
 
        orf_seq_fixed = open('%s_fixed.fasta' % (orf),'w')

        for rec in SeqIO.parse(open(filename,"r"), "fasta"):            
            rec.id = rec.id.split("|")[1]
            rec.id = rec.id.split("_")[0]
            rec.id = rec.id.replace("-","")

            orf_seq_fixed.write('>'+rec.id+'\n'+str(rec.seq)+'\n')
        orf_seq_fixed.close()

        new_filename = orf + '_fixed.fasta'
        alignment_name = orf + '_alignment.fasta'

        cline = ClustalwCommandline("clustalw2", infile=new_filename, output="fasta", outfile=alignment_name)
        cline()

        alignment = AlignIO.read(open(alignment_name), "fasta")
        for record in alignment :
            aligned_length = len(record.seq)
        
        running_length2 = running_length + aligned_length

        partition.write('DNA, ' + orf + '=' + str(running_length) + '-' + str(running_length2) + '\n')
        
        running_length = running_length2

        running_length += 1

        #block of code for running mrbayes separately on each gene and then mbsum
        #AlignIO.convert(new_filename[:-6] + '.aln', "clustal", new_filename[:-6] + '.nexus', "nexus",alphabet=generic_protein)
 
        #nexus_name = new_filename[:-6] + '.nexus' 
    
        #mrbayes_instruct = open('mrbayes_batch.txt','w')
        #mrbayes_instruct.write('set autoclose=yes nowarn=yes\n')
        #mrbayes_instruct.write(' execute %s\n' %(nexus_name))
        #mrbayes_instruct.write('lset nst=6 rates=invgamma\n')
        #mrbayes_instruct.write('mcmc ngen=2000 samplefreq=100 Nruns=1\n')
        #mrbayes_instruct.write('quit')

        #mrbayes_instruct.close()

        #os.system('mb  < mrbayes_batch.txt > mrbayes_log.txt')
        #print "%s.t" %(nexus_name)
        #print nexus_name
        print core
        #os.system('mbsum -n 4 -o %s.in %s.t' %(nexus_name,nexus_name))


partition.close()
print("paralog\t" + str(paralog))
print("core\t" + str(core))



