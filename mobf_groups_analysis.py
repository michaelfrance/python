#!/usr/bin/python
from Bio import SeqIO                                                               
import sys                                                                          
import fileinput
import time
import os

num_high = 0
num_inter = 0
num_low = 0

if not os.path.exists("high_freq_genes"):
    os.makedirs("high_freq_genes")
if not os.path.exists("inter_freq_genes"):
    os.makedirs("inter_freq_genes")
if not os.path.exists("low_freq_genes"):
    os.makedirs("low_freq_genes")

os.chdir("./high_freq_genes")
high_freq_genes = open("mobf_high_freq.fasta","w")
os.chdir("../inter_freq_genes")
inter_freq_genes = open("mobf_inter_freq.fasta","w")
os.chdir("../low_freq_genes")
low_freq_genes = open("mobf_low_feq.fasta","w")
os.chdir("../")


mobf_ids = list()
for strain in open(sys.argv[3],'r'):
    strain = strain.replace("\n","")
    mobf_ids.append(strain.split(",")[1])

print str(mobf_ids)


for line in fileinput.input(sys.argv[1]):
    line = line.strip()
    orf = line.split(" ")[0]
    orf = orf.replace(':','')
    print orf
    
    protein_ids_init = line.split(" ")
    protein_ids_init.pop(0)
    protein_org_set = list()
    protein_ids = list()

    for protein_id in protein_ids_init:
       protein_org = protein_id.split("|")[0]       
       if protein_org in mobf_ids:
           protein_org_set.append(protein_org)
           protein_ids.append(protein_id)

    #print protein_org_set    
    protein_org_set = list(set(protein_org_set))
    print(str(len(protein_org_set)) + "\t"  +  str(len(protein_ids)))
        
    if len(protein_org_set) > 222:

        os.chdir("./high_freq_genes")

        num_high += 1

        orf_seq = open('%s.fasta' % (orf),'w')
        seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
        SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
        orf_seq.close()
        filename = orf + '.fasta'

        count_single = 0
        for rec in SeqIO.parse(open(filename,"r"), "fasta"):            
            if count_single == 0:
                    
                rec.id = rec.id.split("|")[1]
                rec.id = rec.id.split("_")[0]
                rec.id = rec.id.replace("-","")
                high_freq_genes.write('>' + orf + '_' + rec.id +'\n'+str(rec.seq)+'\n')
                count_single += 1

        os.chdir("../")

    
    if len(protein_org_set) > 74:

        os.chdir("./inter_freq_genes")    

        num_inter += 1

        orf_seq = open('%s.fasta' % (orf),'w')
        seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
        SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
        orf_seq.close()
        filename = orf + '.fasta'

        count_single = 0
        for rec in SeqIO.parse(open(filename,"r"), "fasta"):            
            if count_single == 0:
                    
                rec.id = rec.id.split("|")[1]
                rec.id = rec.id.split("_")[0]
                rec.id = rec.id.replace("-","")
                inter_freq_genes.write('>' + orf + '_' + rec.id +'\n'+str(rec.seq)+'\n')
                count_single += 1
         
        os.chdir("../")

    if len(protein_org_set) > 1:

        os.chdir("./low_freq_genes")
        
        num_low += 1

        orf_seq = open('%s.fasta' % (orf),'w')
        seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
        SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
        orf_seq.close()
        filename = orf + '.fasta'

        count_single = 0
        for rec in SeqIO.parse(open(filename,"r"), "fasta"):            
            if count_single == 0:
                    
                rec.id = rec.id.split("|")[1]
                rec.id = rec.id.split("_")[0]
                rec.id = rec.id.replace("-","")
                low_freq_genes.write('>' + orf + '_' + rec.id +'\n'+str(rec.seq)+'\n')
                count_single += 1

        os.chdir("../")

print("Number high freq:  " + str(num_high) + "\n" + "Number inter freq:  " + str(num_inter) + "\n" + "Number low freq  " + str(num_low))

high_freq_genes.close()
inter_freq_genes.close()
low_freq_genes.close()
