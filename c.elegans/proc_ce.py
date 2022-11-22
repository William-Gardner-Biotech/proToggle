import argparse
import gzip
import json
import re
import sys


parser = argparse.ArgumentParser(
	description='cadaframe processing for C. elegans')
parser.add_argument('cgc', type=str, metavar='<cgc>',
	help='path to cgc strain list file')
parser.add_argument('vcf', type=str, metavar='<vcf>',
	help='path to vcf file')
arg = parser.parse_args()

# process cgc strain list

db = {}

with gzip.open(arg.cgc, 'rt') as fp:
	species = None
	gene = None
	allele = None
	phenotype = None
	for line in fp.readlines():
		m1 = re.search('(\S+): (.+)', line)
		if m1:
			if m1.group(1) == 'Species':
				species = m1.group(2)
			if m1.group(1) == 'Genotype':
				m2 = re.search('^(\S+)\((\S+)\)', m1.group(2))
				if m2:
					gene = m2.group(1)
					allele = m2.group(2)
			if m1.group(1) == 'Description':
				phenotype = m1.group(2)
				m3 = re.search('temperature', phenotype, re.IGNORECASE)
				m4 = re.search('sensitive', phenotype, re.IGNORECASE)
				if m3 and m4:
					if 'elegans' not in species: continue
					if allele in db: continue
					db[allele] = {
						'species': 'Caenorhabditis elegans',
						'gene': gene,
						'phenotype': phenotype
					}

# process vcf file

with gzip.open(arg.vcf, 'rt') as fp:
	for line in fp.readlines():
		if line.startswith('#'): continue
		chrom, pos, wbvar, ref, alt, qual, filt, info = line.split()
		allele = None
		for thing in info.split(';'):
			if thing.startswith('PN='):
				tok, name = thing.split('=')
				allele = name
				break
		if allele is not None and allele in db:
			db[allele]['chrom'] = chrom
			db[allele]['pos'] = pos
			db[allele]['ref'] = ref
			db[allele]['alt'] = alt

kill = []
for key in db:
	if 'ref' not in db[key]:
		kill.append(key)
		continue
	
	if len(db[key]['ref']) > 1 or len(db[key]['alt']) > 1: kill.append(key)
for key in kill: del db[key]


#for aid in db:
#	if 'ref' in db[aid]: del db[aid] #  dbe.pop(aid)

print(json.dumps(db, indent=4))

"""
Notes:

Caenorhabditis elegans is listed under several names

+ Caenorhabditis elegans (19406)
+ C. elegans (3580)
+ <em>Caenorhabditis elegans</em> (347)
+ C elegans (90)
+ C.elegans (73)
+ C. elegans N2 (2)
+ C. eleagns (1)


Haven't done anything with cold sensitive or other conditionals

"""