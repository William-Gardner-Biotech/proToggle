import jsonpickle

if __name__ == "__main__":
    print("Running in library")

### CR = computer readable, HR = human_readable
### This function can handle a list
def JSONs_outfmt(object_list):
    export_list_HR = []
    export_list_CR = []
    for mutant_obj in object_list:
        mutant_obj_HR = jsonpickle.encode(mutant_obj, indent=4)
        mutant_obj_CR = jsonpickle.encode(mutant_obj)
        export_list_HR.append(mutant_obj_HR)
        export_list_CR.append(mutant_obj_CR)

    # creates Human readable file
    with open("mutant_objects_HR.json", 'a') as HR:
        last_sep_removal = 0
        for i in export_list_HR:
            HR.write(f"{i},\n")
            if last_sep_removal == len(export_list_HR) - 1:
                continue
            else:
                HR.write(",")
                last_sep_removal += 1

    HR.close()

    # We need to add a special character onto this to find the seperators for individual objects
    with open("mutant_objects_CR.json", 'a') as CR:
        last_seperator_removal = 0
        for i in export_list_CR:
            CR.write(i)
            # seperator
            if last_seperator_removal == len(export_list_CR) - 1:
                continue
            else:
                CR.write("~")
                last_seperator_removal += 1
    CR.close()
    return print("JSON outfile created! [HR = Human Readable | CR = Computer Readable]")

def JSONs_open():
    object_list = []
    jsons_raw = open("mutant_objects_CR.json", 'r')
    jsons_raw = jsons_raw.read()
    jsons_list = jsons_raw.split("~")
    for indv_json in jsons_list:
        mutant_obj = jsonpickle.decode(indv_json)
        object_list.append(mutant_obj)
    return object_list
