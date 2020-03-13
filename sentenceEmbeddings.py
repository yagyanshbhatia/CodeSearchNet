# This file generates 512 dimensional embeddings for each of the sentences in sentences_list


import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

import tensorflow_hub as hub
import numpy as np
import os, sys
import pickle
# from sklearn.metrics.pairwise import cosine_similarity


module_url = "https://tfhub.dev/google/universal-sentence-encoder/2" #@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

# Import the Universal Sentence Encoder's TF Hub module
embed = hub.Module("USE/")

# Reduce logging output.
# tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# load the sentences
pickle_in = open("/data/CodeSearchNet/notebooks/docstrings_list_train_java.pkl","rb")

sentences_list = pickle.load(pickle_in)
pickle_in.close()

temp = []
for method in sentences_list:
    for comment in method:
        temp.append(comment)
sentences_list = temp

with tf.Session() as session:
  session.run([tf.global_variables_initializer(), tf.tables_initializer()])
  sentences_embeddings = session.run(embed(sentences_list))

for partition in range(0,10):
  # default embedding size in USE is 512
  embeddings = {}
  for i in range(partition*len(sentences_list)/10, (partition+1)*len(sentences_list)/10):
      embeddings[sentences_list[i]] = sentences_embeddings[i]

  # dump the embeddings Finally.
  pickle_out = open("sentence_embeddings_"+str(partition)+".pkl","wb")
  pickle.dump(embeddings, pickle_out)
  pickle_out.close()
