#training dataset : 454451 rows, and all are supposed to be full i.e. non-null
#valid dataset: 15328 rows, all columns have same number of non null entries
#testing dataset: 26,909 rows, same condition as above
#total is 496688, the same as solved below
#test to make sure that all the required files are created
#print

import json
import os

INDIVIDUAL_FOLDER_PATH = ""

# INDIVIDUAL_FOLDER_PATH = create_individual_java_files.INDIVIDUAL_FOLDER_PATH

directories = ["train", "valid", "test"]
dir_dict = {"train": 10, "valid": 15328, "test": 10}
# file_count = [451451, 15328, 26909]
# file_count = [10, 15328, 10]
for directory in directories:
    p = INDIVIDUAL_FOLDER_PATH + directory+ '/'
    print(p + " is a directory " + str(os.path.isdir(p)))
    code_header = directory + '_'
    fc = dir_dict[directory] #fc is filecount
    for i in range(0,fc):
        filename = code_header + str(i) + ".java"
        filepath = p + filename
        if not os.path.isfile(filepath): #not() is different from not (of somethign)
            print(filepath)
#Expect all true to be printed out