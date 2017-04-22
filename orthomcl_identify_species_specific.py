#!/usr/bin/python
from Bio import SeqIO                                                               
import sys                                                                          
import fileinput
import time

crisp_core = open("crisp_unique_core.fasta","w")
iners_core = open("iners_unique_core.fasta","w")
crisp_iners_core = open("crisp_iners_corep.fasta","w")

num_shared_core = 0
num_crisp_core = 0
num_iners_core = 0

crisp_ids = ["lac102","lac103","lac104","lac105","lac106","lac107","lac108","lac109","lac110","lac111","lac112","lac113","lac114","lac115","lac116"]
iners_ids = ["lac120","lac121","lac122","lac123","lac124","lac125","lac126","lac127","lac128","lac129","lac130","lac131","lac132","lac133","lac134"]
lacto_ids = ["lac100","lac101","lac117","lac119","lac135","lac136","lac138"]


crisp_iners_ids = crisp_ids + iners_ids
print crisp_iners_ids

for line in fileinput.input(sys.argv[1]):
    line = line.strip()
    orf = line.split(" ")[0]
    orf = orf.replace(':','')
    print orf
    
    protein_ids_init = line.split(" ")
    protein_ids_init.pop(0)
    protein_org_set = list()
    protein_ids = list()

    lacto_count = 0

    for protein_id in protein_ids_init:
        protein_org = protein_id.split("|")[0]       
        if protein_org in crisp_iners_ids:
            protein_org_set.append(protein_org)
            protein_ids.append(protein_id)
        elif protein_org in lacto_ids:
            lacto_count += 1


    #print protein_org_set    
    protein_org_set = list(set(protein_org_set))
    #print(str(len(protein_org_set)) + "\t"  +  str(len(protein_ids)))
    
    
    if len(protein_ids) > len(protein_org_set):
        print "Paralog detected"
    
    if len(protein_org_set) > 26:

        iners_count = 0
        crisp_count = 0

        for iners_id in iners_ids:
            if iners_id in protein_org_set: 
                iners_count += 1
        for crisp_id in crisp_ids:
            if crisp_id in protein_org_set:
                crisp_count += 1
        
        print iners_count
        print crisp_count

        if int(iners_count) > 13 and int(crisp_count) > 13:
            num_shared_core += 1

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
                    crisp_iners_core.write('>' + orf + '_' + rec.id + '_' + str(lacto_count) +'\n'+str(rec.seq)+'\n')
                    count_single += 1
            continue
                    

    
    if len(protein_org_set) > 13:
        
        count = 0

        for iners_id in iners_ids:
            if iners_id in protein_org_set: 
                count += 1
        if count > 13:

            num_iners_core += 1

            orf_seq = open('%s.fasta' % (orf),'w')
            seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
            SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
            orf_seq.close()
            filename = orf + '.fasta'
            count_single = 0
            for rec in SeqIO.parse(open(filename,"r"), "fasta"):
                if count_single == 0:
                    check = rec.id.split("|")[0]            
                    if check in iners_id:
                    
                        rec.id = rec.id.split("|")[1]
                        rec.id = rec.id.split("_")[0]
                        rec.id = rec.id.replace("-","")
                        iners_core.write('>' + orf + '_' + rec.id + '_' + str(lacto_count) +'\n'+str(rec.seq)+'\n')
                        count_single += 1

    if len(protein_org_set) > 13:
        
        count = 0

        for crisp_id in crisp_ids:
        
            if crisp_id in protein_org_set: 
                count += 1
        
        if count > 13:
            num_crisp_core += 1

            orf_seq = open('%s.fasta' % (orf),'w')
            seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
            SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
            orf_seq.close()
            filename = orf + '.fasta'

            count_single = 0
            for rec in SeqIO.parse(open(filename,"r"), "fasta"):
                if count_single == 0:
                    check = rec.id.split("|")[0]
                    if check in crisp_ids:
                        rec.id = rec.id.split("|")[1]
                        rec.id = rec.id.split("_")[0]
                        rec.id = rec.id.replace("-","")
                        crisp_core.write('>' + orf + '_' + rec.id + '_' + str(lacto_count) + '\n'+str(rec.seq)+'\n')
                        count_single += 1


print("Number shared core " + str(num_shared_core) + "\n" + "Number crisp core" + str(num_crisp_core) + "\n" + "Number iners core" + str(num_iners_core))

crisp_core.close()
iners_core.close()
crisp_iners_core.close()
