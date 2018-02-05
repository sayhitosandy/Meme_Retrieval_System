import os
import json
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
from nltk.tokenize import RegexpTokenizer
import json

# creates indices. works on 'what_dir_to_look_in' wala dir inside the current dir.

# creates two jsons : int_to_filename: integers to actual filenames and captions_to_indexes :terms to their posting's list.

captions_to_indexes={}

curdir=os.getcwd()

what_dir_to_look_in='9gag_small'

eng_stemmer = SnowballStemmer('english')
reg_tokenizer = RegexpTokenizer(r'\w+')
default_stopwords = set(stopwords.words('english'))

file_ctr=0

int_to_filename={}


for root, dirs, files in os.walk(what_dir_to_look_in):
	for file in files:
		if file.endswith(".json"):

			 int_to_filename[file_ctr]=file
			 file_ctr+=1

			 data = json.load(open(os.path.join(curdir,what_dir_to_look_in,file)))
			 # print (data['caption'])
			 # print data
			 label=file_ctr            
			 captions_separated=str(data['caption']).split()
			 captions_sep_stemmed=[]
			 for term in captions_separated:
				if term[0]=='#':
					term=term[1:]
				if term not in default_stopwords:
					try:
						term_stemmed=eng_stemmer.stem(term)
					except Exception as e:
						term_stemmed=term
					captions_sep_stemmed.append(term_stemmed)
			 for term in captions_sep_stemmed:

				if term in captions_to_indexes:
					
					captions_to_indexes[term].append(label)
				else:
					captions_to_indexes[term]=[]
					captions_to_indexes[term].append(label)


# print (captions_to_indexes)
# print int_to_filename

with open('captions_to_indexes.json', 'w') as fp:
	json.dump(captions_to_indexes, fp, indent=4)

with open('int_to_filename.json', 'w') as fp:
	json.dump(int_to_filename, fp, indent=4)