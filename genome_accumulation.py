#!/usr/bin/python
import numpy as np
import sys
import random

#defining a fuction that allows loadtxt to skip the first column, taken from user mgilson stackoverflow http://stackoverflow.com/questions/20624137/numpy-loadtxt-skip-first-column
def read_wo_first_column(fname, delimiter=None):
    with open(fname, "r") as fin:
        for line in fin:
            try:
                yield line.split(delimiter,1)[1]
            except IndexError:
                continue

#reading in the initial data
all_input = np.loadtxt(read_wo_first_column(sys.argv[1]),skiprows=1,delimiter="   ")

#trimming down the dataset to only include certain rows, 
select = [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]
print select

all_input = all_input[select,]
for line in all_input:
    print line
#creating the output file
core_out = open("jensenii_accumulations.csv","w")
#writing the column headings to the output file
core_out.write("N,pan,pan_stderr,pan_lower,pan_upper,core,core_std.err,core_lower,core_upper,accessory,acc_stderr,acc_lower,acc_upper")

#looping through the options for the genome accumulation curve
for n in range(1,16):
    print n
    core_all_reps = list()
    accessory_all_reps = list()
    pan_all_reps = list()
    #looping through the number of replicates
    for rep in range(0,1000):

        #creating the randomly selected genomes to include
        genome_select = random.sample(range(0,15),n)
        #subsetting the original array to contain only the selected columns
        
        subset_genomes = all_input[genome_select]

        #summing the columns to determine if core or accessory, creates a list
        col_sums = np.sum(subset_genomes,axis=0)

        #setting the counting variables for each type of gene
        core_gene_count = 0
        accessory_gene_count = 0
        pan_gene_count = 0

        #correcting core check to include things htat are in (n-1) for values of n > 1
        if n == 1:
            core_check = int(n)
        else:
            core_check = int(n) - 1

        #counting up core an accessory from list the column sums
        for entry in col_sums:
            if int(entry) >= int(core_check):
                core_gene_count += 1
            elif entry > 0:
                accessory_gene_count += 1

        #pan genome is the core genome + accessory genome
        pan_gene_count = core_gene_count + accessory_gene_count
        
        #appending values list for all the replicates
        core_all_reps.append(core_gene_count)
        accessory_all_reps.append(accessory_gene_count)
        pan_all_reps.append(pan_gene_count)

    #analysing core genome data
    #incorporating the mean and calculating standard error and such
    core_all_reps_ave = np.mean(core_all_reps)
    core_all_reps_std_er = np.std(core_all_reps)/10
    core_all_reps_li = core_all_reps_ave - 1.96*core_all_reps_std_er
    core_all_reps_ui = core_all_reps_ave + 1.96*core_all_reps_std_er

    #analysing accessory genome data, same
    accessory_all_reps_ave = np.mean(accessory_all_reps)
    accessory_all_reps_std_er = np.std(accessory_all_reps)/10
    accessory_all_reps_li = accessory_all_reps_ave - 1.96*accessory_all_reps_std_er
    accessory_all_reps_ui = accessory_all_reps_ave + 1.96*accessory_all_reps_std_er

    #analysing pan genome data, same
    pan_all_reps_ave = np.mean(pan_all_reps)
    pan_all_reps_std_er = np.std(pan_all_reps)/10
    pan_all_reps_li = pan_all_reps_ave - 1.96*pan_all_reps_std_er
    pan_all_reps_ui = pan_all_reps_ave + 1.96*pan_all_reps_std_er

    #writing reults out to file
    core_out.write("\n" + str(n) + "," + str(pan_all_reps_ave) + "," + str(pan_all_reps_std_er) + "," + str(pan_all_reps_li) + "," + str(pan_all_reps_ui) + "," + str(core_all_reps_ave) + "," + str(core_all_reps_std_er) + "," + str(core_all_reps_li) + "," + str(core_all_reps_ui)+ "," + str(accessory_all_reps_ave) + "," + str(accessory_all_reps_std_er) + "," + str(accessory_all_reps_li) + "," + str(accessory_all_reps_ui))

#closing output file
core_out.close()
