import json
import os

valid_json_loc = 'jsonl/valid/java_valid_0.jsonl' #path to the json file of CodeSearchnet valid dataset
valid_log_location = "../../" + "code2seq_data/models/java-large-model/log.txt" #path to the log file (output of code2seq on CodeSearchNet valid dataset)
valid_json_modified = 'jsonl/valid/java_valid_0_modified.jsonl'  #should be same path as valid_json_loc other than the "modified"
f = open(valid_log_location, 'r')
method_to_c2sprediction = dict()
c2sprediction_to_method = dict()
method_to_method_tokens = dict()
predictions = f.readlines()
print("no of lines in valid log file" + str(len(predictions)))  #should be 16660
firstflag = False
no_pred_count = 0
fail_count = 0
line_count = 0
for line in predictions:
    line_count = line_count + 1
    words = line.split()
    flag = True
    if len(words) != 6:
        #print("reason 1 " + line)
        if len(words) == 5:
            no_pred_count = no_pred_count + 1
        flag = False
    elif (words[0]!= "Original:"):
        print("reason 2 " + line + str(line_count))
        flag = False
    if flag == True:
        method = words[1]
        method = method.replace('|', '')
        c2sprediction = words[5] #we dont replace the prediction words | because if we do, then we loose the tokens!
        c2sprediction = c2sprediction.replace('|', ' ')
        if method in method_to_c2sprediction.keys(): #build method_to_c2sprediction dict, with value being list of keys, since there are multiple methods with the same name
            if c2sprediction not in method_to_c2sprediction[method]: #we add only unique predictions i.e. same method name, different function body, and now how do we map them?
                method_to_c2sprediction[method].append(c2sprediction)
        else:
            method_to_c2sprediction[method] = []
            method_to_c2sprediction[method].append(c2sprediction)
        if c2sprediction in c2sprediction_to_method.keys(): #same logic as the method_to_c2sprediction dictionary
            if method not in c2sprediction_to_method[c2sprediction]:
                c2sprediction_to_method[c2sprediction].append(method)
        else:
            c2sprediction_to_method[c2sprediction] = []
            c2sprediction_to_method[c2sprediction].append(method)
        method1 = words[1]
        method_to_method_tokens[method] = method1.replace('|', ' ')
dup_method_count = 0
emp_method_count = 0
for key in method_to_c2sprediction:
    # print(key)
    # print(method_to_c2sprediction[key])
    key_count = len(method_to_c2sprediction[key])
    if (key_count > 1):
        dup_method_count = dup_method_count + key_count
    elif (key_count == 0):
        emp_method_count = emp_method_count + 1
print(no_pred_count)
print(emp_method_count)
print(dup_method_count) #this is a problem... 
#to generate index methodname mapping

bad_chars = ['|']
with open(valid_json_loc, 'r') as f:
    write_file = open(valid_json_modified, 'w')
    lines = f.readlines()
    for i in range(0,len(lines)):
        code_dict = json.loads(lines[i])
        func_name = code_dict["func_name"]
        func_name_split = func_name.split('.')
        #full_func_name_split = re.split("([.]|[A-Z]|[_])", func_name)
        #print(full_func_name_split)
        method_name = func_name_split[-1]
        method_name = method_name.lower()
        c2sprediction = ""
        if (method_name in method_to_c2sprediction.keys()): #there are no empty keys so thats good
            c2sprediction = method_to_c2sprediction[method_name][0] #this line is fine because of no empty keys
        #print("orig_method: " + method_name+', ' + " c2sprediction: " + c2sprediction)
        code_dict["func_name_prediction"] = c2sprediction
        #the full doc will be made from the code tokens, of course you can clean up here
        code_string = ""
        for elem in code_dict["code_tokens"]:
            code_string = code_string + elem + ' '
        doc_string = ""
        for elem in code_dict["docstring_tokens"]:
            doc_string = doc_string + elem + ' '
        if method_name in method_to_method_tokens.keys():
            method_string = method_to_method_tokens[method_name]
#         for elem in method_to_method_tokens[method_name]:
#             method_string = method_string + elem + ' '
        code_dict["full_doc"] = code_dict["func_name_prediction"] + " " + method_string + " " + doc_string +" " + code_string
        #print(code_dict["full_doc"])
        json.dump(code_dict, write_file)
        write_file.write('\n')
#         print()
#         if i == 5:
#             break
# print(count)

#official code!
path_to_modified_valid = valid_json_modified
with open(valid_json_modified, 'r') as f:
    sample_file = f.readlines()  #guarentees that they are read in order, so there is no problem here
print(sample_file[15327])
request_file = "requests_valid.txt"
with open(request_file, 'w') as f:
    count = 0
    for l in sample_file:
        command_str = '{ "index" : { "_index" : "valid", "_id" : "' + str(count) + '" } }' +'\n'
        f.write(command_str)
        f.write(l)
        if (count == 15327):
            print(l)
        count = count + 1