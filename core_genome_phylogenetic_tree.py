#!/usr/bin/python

import shutil
import os
import sys
from Bio import AlignIO
from Bio.Alphabet import generic_dna
from Bio.Nexus import Nexus
from Bio.Align.Applications import ClustalwCommandline

if not os.path.exists('./core_genes'):
    os.makedirs('./core_genes')



#looping through a text file (sysarv1) and converting the contents to file name format, then converting to nexus format and adding to tar file
for name in open(sys.argv[1],"r") :
    filename = 'Gene' + name[:-1] + '-DNA.fasta'
    print filename
    shutil.copy2(filename,'./core_genes/%s' %(filename))
    os.chdir('./core_genes/')
    cline = ClustalwCommandline("clustalw", infile=filename, output="PHYLIP")
    cline()
    #AlignIO.convert(filename[:-6] + '.aln', "clustal", filename[:-6] + '.nexus', "nexus",alphabet=generic_dna)
 
    #nexus_name = filename[:-6] + '.nexus' 
    
    #mrbayes_instruct = open('mrbayes_batch.txt','w')
    #mrbayes_instruct.write('set autoclose=yes nowarn=yes\n')
    #mrbayes_instruct.write(' execute %s\n' %(nexus_name))
    #mrbayes_instruct.write('lset nst=6 rates=invgamma\n')
    #mrbayes_instruct.write('mcmc ngen=10000 samplefreq=10 Nruns=1\n')
    #mrbayes_instruct.write('quit')

    #mrbayes_instruct.close()
    #os.system('mb  < mrbayes_batch.txt > mrbayes_log.txt &')
    #print "%s.t" %(nexus_name)
    #print nexus_name
    
    os.chdir('./../')




