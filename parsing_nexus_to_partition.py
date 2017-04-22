#!/usr/bin/python
import sys




with open (sys.argv[1], "r") as nexus_header:
    unsplit =str(nexus_header.readlines())

partition_out = open('lac_partition.txt','w')

unsplit.replace('[','')
unsplit.replace(']','')
unsplit.replace('\n','')

split_list = unsplit.split(" ")

gene_count = 0
count = 0

for entry in split_list:
    if count == 0:
        gene_count += 1
        count += 1

    elif count == 1:
        count = 0
        start = int(entry.split("-")[0])
        end = int(entry.split("-")[1])
        start2 = start + 1
        start3 = start + 2
        partition_out.write('gene' + str(gene_count) + '_pos1'  + ' = ' + str(entry) + "\\3;\ngene" + str(gene_count) + '_pos2' + ' = ' + str(start2) + '-' + str(end) + '\\3;\ngene' + str(gene_count) + '_pos3' + ' = ' + str(start3) + '-' + str(end) + '\\3;\n')


partition_out.close()



