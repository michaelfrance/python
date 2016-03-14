#!/usr/bin/python
from Bio import SeqIO                                                               
import sys                                                                          
import fileinput


crisp_core = open("crisp_unique_core.fasta","w")
iners_core = open("iners_unique_core.fasta","w")
crisp_iners_core = open("crisp_iners_corep.fasta","w")

num_shared_core = 0
num_crisp_core = 0
num_iners_core = 0

crisp_ids = ["lic1","lic2","lic3","lic4","lic5","lic6","lic7","lic8","lic9","lic10","lic11","lic12"]
iners_ids = ["lic13","lic14","lic15","lic16","lic17","lic18","lic19","lic20","lic21","lic22","lic23","lic24","lic25","lic26","lic27"]

for line in fileinput.input(sys.argv[1]):
    line = line.strip()
    orf = line.split(" ")[0]
    orf = orf.replace(':','')
    print orf
    
    protein_ids = line.split(" ")
    protein_ids.pop(0)
    protein_org_set = list()

    for protein_id in protein_ids:
       protein_org = protein_id.split("|")[0]       
       protein_org_set.append(protein_org)

    protein_org_set = list(set(protein_org_set))
    print protein_org_set

    print(str(len(protein_org_set)))
    
    
    if len(protein_org_set) > 24:

        num_shared_core += 1

        orf_seq = open('%s.fasta' % (orf),'w')
        seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
        SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
        orf_seq.close()
        filename = orf + '.fasta'

        for rec in SeqIO.parse(open(filename,"r"), "fasta"):            
            rec.id = rec.id.split("|")[1]
            rec.id = rec.id.split("_")[0]
            rec.id = rec.id.replace("-","")

            crisp_iners_core.write('>' + orf + '_' + rec.id +'\n'+str(rec.seq)+'\n')

        continue
    
    if len(protein_ids) > len(protein_org_set):
        print "Paralog detected"
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
            for rec in SeqIO.parse(open(filename,"r"), "fasta"):            
                rec.id = rec.id.split("|")[1]
                rec.id = rec.id.split("_")[0]
                rec.id = rec.id.replace("-","")
                iners_core.write('>' + orf + '_' + rec.id +'\n'+str(rec.seq)+'\n')

    if len(protein_org_set) > 10:
        
        count = 0

        for crisp_id in crisp_ids:
        
            if crisp_id in protein_org_set: 
                count += 1
        
        if count > 10:
            num_crisp_core += 1

            orf_seq = open('%s.fasta' % (orf),'w')
            seqiter = SeqIO.parse(open(sys.argv[2]), 'fasta')                                    
            SeqIO.write((seq for seq in seqiter if seq.id in protein_ids), orf_seq, "fasta")
            orf_seq.close()
            filename = orf + '.fasta'

            for rec in SeqIO.parse(open(filename,"r"), "fasta"):            
                rec.id = rec.id.split("|")[1]
                rec.id = rec.id.split("_")[0]
                rec.id = rec.id.replace("-","")
                crisp_core.write('>' + orf + '_' + rec.id +'\n'+str(rec.seq)+'\n')


print("Number shared core " + str(num_shared_core) + "\n" + "Number crisp unique core" + str(num_crisp_core) + "\n" + "Number iners unique core" + str(num_iners_core))

crisp_core.close()
iners_core.close()
crisp_iners_core.close()
