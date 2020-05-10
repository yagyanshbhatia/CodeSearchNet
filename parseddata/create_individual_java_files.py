import sys
import json
import os
PATH = "jsonl/"
INDIVIDUAL_FOLDER_PATH = ""
# print(os.path.isdir(INDIVIDUAL_FOLDER_PATH))
for val in ["train", "test", "valid"]: #put train, test here for the other data
    cur_path = PATH + val + '/'
    f = open(cur_path + "java_" + val + "_0.jsonl", 'r')
    jsonl = f.readlines()
    if not os.path.isdir(INDIVIDUAL_FOLDER_PATH + val + '/'):
        os.mkdir(INDIVIDUAL_FOLDER_PATH + val + '/')
    print("running for " + val + " set located at " + cur_path)
    if val == "valid":
        for i in range(0,len(jsonl)):
            code_dict = json.loads(jsonl[i])
            code = code_dict["code"]
            outfile_name = val + '_' + str(i) + ".java"
            outfile = open(INDIVIDUAL_FOLDER_PATH + val + '/' + outfile_name, 'w', encoding="utf8")
            outfile.write(code)
            if i%1000 == 0:
                print("finished " + val + "until " + str(i))
    else:
        for i in range(0, 10):
            code_dict = json.loads(jsonl[i])
            code = code_dict["code"]
            outfile_name = val + '_' + str(i) + ".java"
            outfile = open(INDIVIDUAL_FOLDER_PATH + val + '/' + outfile_name, 'w', encoding="utf8")
            outfile.write(code)