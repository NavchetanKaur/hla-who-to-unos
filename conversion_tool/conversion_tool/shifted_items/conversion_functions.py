#! usr/bin/python 

import os
import re
import requests   
import operator
import glob
from . import hla
#from hla import allele_truncate, locus_string_geno_list, expand_ac, single_locus_allele_codes_genotype

allele_to_ag_dict = {}
population_allele_frequencies = {}
allele_frequencies = {}

### Dictionary with alleles and equivalent antigens

UNOS_conversion_table_filename = "conversion_table.csv"
UNOS_conversion_table_file = open(UNOS_conversion_table_filename, 'r')
for row in UNOS_conversion_table_file:
	expression_character = ""
	if row.startswith("Allele"):
		continue 
	else:
		allele = row.split(',')[0]
		allele_4d = hla.allele_truncate(allele)
		antigen = row.split(',')[1]
		rule = row.split(',') [2]
		bw4_6 = row.split(',')[3]
		
	allele_to_ag_dict[allele] = antigen, rule, bw4_6 
	allele_to_ag_dict[allele_4d] = antigen, rule, bw4_6

for file in glob.glob('*.freqs'):
	#print(file)
	pop = file.split(".")[0]
	# print(pop)
	population_allele_frequencies[pop] = {}
	freq_file = open(file, 'r')
	for line in freq_file:
		if line.startswith("Haplo"):
			continue
		else:
			
			line_split = line.split(",")
			allele_list = line_split[0]
			count = line_split[1]
			haplotype_frequency = line_split[2]
			allele_split = allele_list.split("~")
			for allele in allele_split:
				allele = allele.rstrip("g")
				if allele in population_allele_frequencies[pop]:
					population_allele_frequencies[pop][allele] += float(haplotype_frequency)
				else:
					population_allele_frequencies[pop][allele] = float(haplotype_frequency)	



def convert_allele_to_ag(allele):

	"""This function should be called when antigen conversion has to be done for a single allele. Enter an IMGT/HLA allele as a  string 
	input and the get the coressponding antigen as per UNOS rules. Also if the antigen is Bw4/6 is also indicated. 
	The rule applied for the conversion is printed out with every input"""
	
	if allele in allele_to_ag_dict:	
		ag = allele_to_ag_dict[allele][0]
		rule = allele_to_ag_dict[allele][1]
		bw4_6 = allele_to_ag_dict[allele][2]
		print("UNOS Antigen is:" + ag)
		print("Rule followed:" + rule)
		if bw4_6 != "NA":
			print("It's a " + bw4_6)
		else:
			print("It's neither Bw4 nor Bw6")	
	else:
			print(allele + ": is not a IMGT/HLA allele")

	
### convert a list of alleles to corresponding ags


def convert_allele_list_to_ags(hla_allele_list):
	
	"""This function can be called if a list of alleles has to be converted to antigens. Input format is a list and 
	the corresponding antigens and rules will be printed out"""
	
	for allele in hla_allele_list:
		if allele in allele_to_ag_dict:
			ag = ""
			rule = ""
			ag = allele_to_ag_dict[allele][0]
			#print(ag)
			rule = allele_to_ag_dict[allele][1]
			bw4_6 = allele_to_ag_dict[allele][2]

			print("Allele:" + allele)
			print("Antigen:" + ag)
			print("rule:" + rule)
			print("Bw4/6:" + bw4_6)


		else:
			print(allele + " :is not a IMGT/HLA allele")	


def gl_string_ags(gl_string, pop):

	gl_string = gl_string.replace("HLA-", "")
	locus_split = gl_string.split("^")

	ag_freq_1 = 0.0
	ag_freq_2 = 0.0
	geno_antigen_freq = {}

	ag_list = ""

	Three_locus_typing = 0
	Four_locus_typing = 0
	Five_locus_typing = 0
	Six_locus_typing = 0

	if len(locus_split) == 3:
		Three_locus_typing = 1
		print("Three locus typing")
		geno_antigen_freq = {}
		a_locus = locus_split[0]
		a_genotype_list = locus_string_geno_list(a_locus)
		a_ags = genotype_ags(a_genotype_list,pop)
		geno_antigen_freq = {}
		b_locus = locus_split[1]
		b_genotype_list = locus_string_geno_list(b_locus)
		b_ags = genotype_ags(b_genotype_list,pop)
		geno_antigen_freq = {}
		c_locus = locus_split[2]
		c_genotype_list = locus_string_geno_list(c_locus)
		c_ags = genotype_ags(c_genotype_list,pop)
		ag_list = a_ags + "," + b_ags + "," + c_ags
	
	
	if len(locus_split) == 4:
		Four_locus_typing = 1
		print("Four locus typing")
		geno_antigen_freq = {}
		a_locus = locus_split[0]
		a_genotype_list = locus_string_geno_list(a_locus)
		a_ags = genotype_ags(a_genotype_list,pop)
		geno_antigen_freq = {}
		b_locus = locus_split[1]
		b_genotype_list = locus_string_geno_list(b_locus)
		b_ags = genotype_ags(b_genotype_list,pop)
		geno_antigen_freq = {}
		c_locus = locus_split[2]
		c_genotype_list = locus_string_geno_list(c_locus)
		c_ags = genotype_ags(c_genotype_list,pop)
		geno_antigen_freq = {}
		dr_locus = locus_split[3]
		dr_genotype_list = locus_string_geno_list(dr_locus)
		dr_ags = genotype_ags(dr_genotype_list,pop)
		ag_list = a_ags + "," + b_ags + "," + c_ags + "," + dr_ags

	if len(locus_split) == 5:
		Five_locus_typing = 1
		print("Five locus typing")
		geno_antigen_freq = {}
		a_locus = locus_split[0]
		a_genotype_list = locus_string_geno_list(a_locus)
		a_ags = genotype_ags(a_genotype_list,pop)
		geno_antigen_freq = {}
		b_locus = locus_split[1]
		b_genotype_list = locus_string_geno_list(b_locus)
		b_ags = genotype_ags(b_genotype_list,pop)
		geno_antigen_freq = {}
		c_locus = locus_split[2]
		c_genotype_list = locus_string_geno_list(c_locus)
		c_ags = genotype_ags(c_genotype_list,pop)
		geno_antigen_freq = {}
		dr_locus = locus_split[3]
		dr_genotype_list = locus_string_geno_list(dr_locus)
		dr_ags = genotype_ags(dr_genotype_list,pop)
		geno_antigen_freq = {}
		dq_locus = locus_split[4]
		dq_genotype_list = locus_string_geno_list(dq_locus)
		dq_ags = genotype_ags(dq_genotype_list,pop)
		ag_list = a_ags + "," + b_ags + "," + c_ags  + "," + dr_ags + "," + dq_ags

	if len(locus_split) == 6:
		Six_locus_typing = 1
		print("Six locus typing")
		geno_antigen_freq = {}
		a_locus = locus_split[0]
		a_genotype_list = locus_string_geno_list(a_locus)
		a_ags = genotype_ags(a_genotype_list,pop)
		geno_antigen_freq = {}
		b_locus = locus_split[1]
		b_genotype_list = locus_string_geno_list(b_locus)
		b_ags = genotype_ags(b_genotype_list,pop)
		geno_antigen_freq = {}
		c_locus = locus_split[2]
		c_genotype_list = locus_string_geno_list(c_locus)
		c_ags = genotype_ags(c_genotype_list,pop)
		geno_antigen_freq = {}
		dr_locus = locus_split[3]
		dr_genotype_list = locus_string_geno_list(dr_locus)
		dr_ags = genotype_ags(dr_genotype_list,pop)
		geno_antigen_freq = {}
		dq_locus = locus_split[4]
		dq_genotype_list = locus_string_geno_list(dq_locus)
		dq_ags = genotype_ags(dq_genotype_list,pop)
		geno_antigen_freq = {}
		dr345_locus = locus_split[5]
		dr345_genotype_list = locus_string_geno_list(dr345_locus)
		dr345_ags = genotype_ags(dr345_genotype_list,pop)
		ag_list = a_ags + "," + b_ags + "," + c_ags  + "," + dr_ags + "," + dq_ags + "," + dr345_ags

	return ag_list
	
def genotype_ags(genotype_list, pop):
	geno_antigen_freq = {}
	for genotype in genotype_list:
		allele_1 = genotype.split("+")[0]
		allele_1 = allele_1.rstrip("g")
		allele_1 = allele_truncate(allele_1)

		allele_2 = genotype.split("+")[1]
		allele_2 = allele_2.rstrip("g")
		allele_2 = allele_truncate(allele_2)

		ag_1 = allele_to_ag_dict[allele_1][0]
		ag_2 = allele_to_ag_dict[allele_2][0]

		if allele_1 in population_allele_frequencies[pop]:
			ag_freq_1 = population_allele_frequencies[pop][allele_1]
			if allele_2 in population_allele_frequencies[pop]:
				ag_freq_2 = population_allele_frequencies[pop][allele_2]

				gf = 0
				if (ag_1 == ag_2):
					gf = float(ag_freq_1) * float(ag_freq_2)
				else:
					gf = 2 * float(ag_freq_1) * float(ag_freq_2)	

					geno_antigen = ag_1 + "+" + ag_2

					if geno_antigen in geno_antigen_freq.keys():
						geno_antigen_freq[geno_antigen] += float(gf)
					else:
						geno_antigen_freq[geno_antigen] = float(gf)
						sorted_gf = sorted(geno_antigen_freq.items(), key = operator.itemgetter(1), reverse = True)
	#print(sorted_gf)
	top_ag_geno = sorted_gf[0][0]
	top_gf = sorted_gf[0][1]
	#print(top_ag_geno)	
	ag_1 = top_ag_geno.split("+")[0]
	ag_2 = top_ag_geno.split("+")[1]	
	#print(ag_1)
	#print(ag_2)
	ag_list = ag_1 + "," + ag_2	
	return ag_list


def allele_code_ags(allele_codes_list, pop):

	ag_freq_1 = 0.0
	ag_freq_2 = 0.0
	geno_antigen_freq = {}
 	

	if len(allele_codes_list) == 6:
		print("Three locus typing")
		Three_locus_typing = 1
		A_1_code = allele_codes_list[0]
		A_2_code = allele_codes_list[1]
		A_codes_pair = [A_1_code, A_2_code]
		geno_antigen_freq = {}
		acodes_genotype = single_locus_allele_codes_genotype(A_codes_pair)
		a_ags = genotype_ags(acodes_genotype, pop)

		C_1_code = allele_codes_list[2]
		C_2_code = allele_codes_list[3]
		C_codes_pair = [C_1_code, C_2_code]
		geno_antigen_freq = {}
		ccodes_genotype = single_locus_allele_codes_genotype(C_codes_pair)
		c_ags = genotype_ags(ccodes_genotype, pop)

		B_1_code = allele_codes_list[4]
		B_2_code = allele_codes_list[5]
		B_codes_pair = [B_1_code, B_2_code]
		geno_antigen_freq = {}
		bcodes_genotype = single_locus_allele_codes_genotype(B_codes_pair)
		b_ags = genotype_ags(bcodes_genotype, pop)
		
		ag_list = a_ags + "," + b_ags + "," + c_ags

	if len(allele_codes_list) == 8:
		print("Four locus typing")
		Four_locus_typing = 1
		A_1_code = allele_codes_list[0]
		A_2_code = allele_codes_list[1]
		A_codes_pair = [A_1_code, A_2_code]
		geno_antigen_freq = {}
		acodes_genotype = single_locus_allele_codes_genotype(A_codes_pair)
		a_ags = genotype_ags(acodes_genotype, pop)

		C_1_code = allele_codes_list[2]
		C_2_code = allele_codes_list[3]
		C_codes_pair = [C_1_code, C_2_code]
		geno_antigen_freq = {}
		ccodes_genotype = single_locus_allele_codes_genotype(C_codes_pair)
		b_ags = genotype_ags(ccodes_genotype, pop)

		B_1_code = allele_codes_list[4]
		B_2_code = allele_codes_list[5]
		B_codes_pair = [B_1_code, B_2_code]
		geno_antigen_freq = {}
		bcodes_genotype = single_locus_allele_codes_genotype(B_codes_pair)
		c_ags = genotype_ags(bcodes_genotype, pop)
			
		dr_1_code = allele_codes_list[6]
		dr_2_code = allele_codes_list[7]
		dr_codes_pair = [dr_1_code, dr_2_code]
		geno_antigen_freq = {}
		drcodes_genotype = single_locus_allele_codes_genotype(dr_codes_pair)
		dr_ags = genotype_ags(drcodes_genotype, pop)

		ag_list = a_ags + "," + b_ags + "," + c_ags + "," + dr_ags
	
	if len(allele_codes_list) == 10:
		print("Five locus typing")
		Five_locus_typing = 1
		A_1_code = allele_codes_list[0]
		A_2_code = allele_codes_list[1]
		A_codes_pair = [A_1_code, A_2_code]
		geno_antigen_freq = {}
		acodes_genotype = single_locus_allele_codes_genotype(A_codes_pair)
		a_ags = genotype_ags(acodes_genotype, pop)

		C_1_code = allele_codes_list[2]
		C_2_code = allele_codes_list[3]
		C_codes_pair = [C_1_code, C_2_code]
		geno_antigen_freq = {}
		ccodes_genotype = single_locus_allele_codes_genotype(C_codes_pair)
		c_ags = genotype_ags(ccodes_genotype, pop)

		B_1_code = allele_codes_list[4]
		B_2_code = allele_codes_list[5]
		B_codes_pair = [B_1_code, B_2_code]
		geno_antigen_freq = {}
		bcodes_genotype = single_locus_allele_codes_genotype(B_codes_pair)
		b_ags = genotype_ags(bcodes_genotype, pop)
			
		dr_1_code = allele_codes_list[6]
		dr_2_code = allele_codes_list[7]
		dr_codes_pair = [dr_1_code, dr_2_code]
		geno_antigen_freq = {}
		drcodes_genotype = single_locus_allele_codes_genotype(dr_codes_pair)
		dr_ags = genotype_ags(drcodes_genotype, pop)	
		
		dq_1_code = allele_codes_list[8]
		dq_2_code = allele_codes_list[9]
		dq_codes_pair = [dq_1_code, dq_2_code]
		geno_antigen_freq = {}
		dqcodes_genotype = single_locus_allele_codes_genotype(dq_codes_pair)
		dq_ags = genotype_ags(dqcodes_genotype, pop)

		ag_list = a_ags + "," + b_ags + "," + c_ags + "," + dr_ags + "," + dq_ags
				
	if len(allele_codes_list) == 12:
		print("Six locus typing")
		Six_locus_typing = 1
		A_1_code = allele_codes_list[0]
		A_2_code = allele_codes_list[1]
		A_codes_pair = [A_1_code, A_2_code]
		geno_antigen_freq = {}
		acodes_genotype = single_locus_allele_codes_genotype(A_codes_pair)
		a_ags = genotype_ags(acodes_genotype, pop)

		C_1_code = allele_codes_list[2]
		C_2_code = allele_codes_list[3]
		C_codes_pair = [C_1_code, C_2_code]
		geno_antigen_freq = {}
		ccodes_genotype = single_locus_allele_codes_genotype(C_codes_pair)
		c_ags = genotype_ags(ccodes_genotype, pop)

		B_1_code = allele_codes_list[4]
		B_2_code = allele_codes_list[5]
		B_codes_pair = [B_1_code, B_2_code]
		geno_antigen_freq = {}
		bcodes_genotype = single_locus_allele_codes_genotype(B_codes_pair)
		b_ags = genotype_ags(bcodes_genotype, pop)
			
		dr_1_code = allele_codes_list[6]
		dr_2_code = allele_codes_list[7]
		dr_codes_pair = [dr_1_code, dr_2_code]
		geno_antigen_freq = {}
		drcodes_genotype = single_locus_allele_codes_genotype(dr_codes_pair)
		dr_ags = genotype_ags(drcodes_genotype, pop)	
		
		dq_1_code = allele_codes_list[8]
		dq_2_code = allele_codes_list[9]
		dq_codes_pair = [dq_1_code, dq_2_code]
		geno_antigen_freq = {}
		dqcodes_genotype = single_locus_allele_codes_genotype(dq_codes_pair)
		dq_ags = genotype_ags(dqcodes_genotype, pop)
							

		dr345_1_code = allele_codes_list[10]
		dr345_2_code = allele_codes_list[11]
		dr345_codes_pair = [dr345_1_code, dr345_2_code]
		geno_antigen_freq = {}
		dr345codes_genotype = single_locus_allele_codes_genotype(dr345_codes_pair)
		dr345_ags = genotype_ags(dr345codes_genotype, pop)			


		ag_list = a_ags + "," + b_ags + "," + c_ags + "," + dr_ags + "," + dq_ags + "," + dr345_ags
	return ag_list	
	

