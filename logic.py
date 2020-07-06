#program to generate json file with 4 letter english words
#for word dictionary -https://github.com/dwyl/english-words

from nltk.corpus import wordnet as word_net
from nltk.tokenize import word_tokenize
import os
import json
words_list=list()
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
dictionary_file = os.path.join(THIS_FOLDER, 'word_dictionary.txt')


file_obj=open(dictionary_file,"r")
content=file_obj.read()
words=word_tokenize(str(content))
#to extract 4 letter words
for word in words:
    if len(word)==4 and word in word_net.all_lemma_names():
        words_list.append(word)

json_object = json.dumps(words_list)

# Writing to word_dictionary.json 
with open("word_dictionary.json", "w") as outfile: 
    outfile.write(json_object)