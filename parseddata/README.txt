Put the "jsonl" folder in the parseddata folder i.e. parseddata/jsonl should be the path.  Or just modify path to point to the jsonl folder.

modify INDIVIDUAL_FILE_PATH to point to where you want the data to be made, by default it will be made in parseddata/jsonl.

requirements:
os
sys
json
tensorflow

Run create_individual_java_files.py
Then run test_individual_java_files_creation.py.  If all dirs are printed true with no other output, create ran successfully.


Copy the preprocess.sh of this folder into code2seq.  
run preprocess.sh of code2seq pointing to the (created) train test valid folders in CodeSearchNet/parseddata.
Make sure the number of threads is limited to 4.

Extracting paths from validation set...
Finished extracting paths from validation set
Extracting paths from test set...
Finished extracting paths from test set
Extracting paths from training set...
Finished extracting paths from training set
Creating histograms from the training data
subtoken vocab size:  78
node vocab size:  49
target vocab size:  18
File: parseddata_valid.test.raw.txt
Average total contexts: 151.1
Average final (after sampling) contexts: 130.1
Total examples: 10
Max number of contexts per word: 392
File: parseddata_valid.val.raw.txt
Average total contexts: 232.93829531812725
Average final (after sampling) contexts: 118.36818727490997
Total examples: 16660
Max number of contexts per word: 11643
File: parseddata_valid.train.raw.txt
Average total contexts: 110.18181818181819
Average final (after sampling) contexts: 110.18181818181819
Total examples: 11
Max number of contexts per word: 442
Dictionaries saved to: data/parseddata_valid/parseddata_valid.dict.c2s

Command: bash preprocess.sh

run: mind the paths. Must have model (52 iterations) downlaoded.  its predictions.
python3 code2seq/code2seq.py --load code2seq_data/models/java-large-model/model_iter52.release --test code2seq/data/parseddata_valid/preproc_val_codesearch.val.c2s

finally, run this command after opening elastic search.

To open elastic search:  go to the folder and run ./bin/elasticsearch
The command must be run inside "parseddata" folder, i.e. where the requests_valid.txt file is
the command: 
curl -X DELETE "localhost:9200/valid?pretty"
above makes sure that the is no valid index
curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary "@requests_valid.txt"; echo
this pushes all of them into the index.  There should be one error case at the end, ignore that

curl -XGET 'localhost:9200/test/_count?pretty' gives the count should be around 15k.
To search:

curl -X GET "localhost:9200/valid/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "simple_query_string" : {
        "query": "foo bar",
        "fields": ["full_doc"],
        "default_operator": "and"
    }
  }
}
'

The output is 10 functions by default, and it returns the entire document.
the query field is the one that we insert the query string into.  By default the string is tokenized and then its searched for the tokens.  In the above case it searches for documents that have foo and bar in their full_doc json field.




