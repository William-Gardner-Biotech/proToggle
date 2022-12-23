import gzip
import json_object_list_handler


class yeast_mutant(object):
    species = "Saccharomyces cerevisiae"
    molecular_mutation = "N/A"

    def __init__(self, id):
        self.id = id
    pass

def first_use():

    infile = gzip.open("conditional_phenodata.tab.gz", "rt")

    temp_alleles = ["ts allele", "temperature sensitive", "temperature-sensitive", "temperature-inducible degron", "-ts"]

    allels = []

    # If there is an allele_name we use it
    #We have already narrowed down with awk to produce these

    for line in infile:
        line_splits = line.split("\t")
        #print(line)
        # line_splits[5] is the allele name
        if (line_splits[5]) == " ":
            continue
        if any(word in line_splits[5] for word in temp_alleles):
            allels.append(line)

    # Let's create an object that can hold these
    # Let's make the id "Yeast"+allele


    # [0] = Gene name, [1] = feature type. [2] = gene ID [3] = Reference [4] = Not Important [5] = allele [6] = description

    object_list = []
    easy_fstring = f"Entry_id\tGene_name\tSGD_gene_ID\tPubmed_ID\tSGD_Reference\tAllele\tDescription\n"
    for entry in allels:
        entry_splits = entry.split("\t")
        entry_id = "Yeast_"+entry_splits[0]+"_"+entry_splits[5]
        entry_id = entry_id.replace(" ", "")
        #print(entry_id)
        curr_mutant = yeast_mutant(entry_id)
        curr_mutant.Gene = entry_splits[0]
        curr_mutant.Feature_type = entry_splits[1]

        # Potentially add RE here to cut the first part or use .split(":")

        References2 = entry_splits[3]
        PubmedID, SGD_reference = References2.split("|")
        curr_mutant.Pubmed_ID = PubmedID
        curr_mutant.SGD_Ref = SGD_reference

        curr_mutant.SGD_ID = entry_splits[2]
        curr_mutant.allele = entry_splits[5]
        curr_mutant.description = entry_splits[6]
        # Add this at the end
        object_list.append(curr_mutant)
        easy_fstring+=f"{curr_mutant.id}\t{curr_mutant.Gene}\t{curr_mutant.SGD_ID}\t{curr_mutant.Pubmed_ID}\t{curr_mutant.SGD_Ref}\t{curr_mutant.allele}\t{curr_mutant.description}"
        print(PubmedID, SGD_reference)

    with open("TS_alleles.tab", 'w') as tab:
        tab.write(easy_fstring)

    json_object_list_handler.JSONs_outfmt(object_list)

    mutants = json_object_list_handler.JSONs_open()

    return mutants

# Returns a list of all the mutant objects
def subsequent_use():
    return json_object_list_handler.JSONs_open()

mutants = subsequent_use()

#mutants = first_use()
