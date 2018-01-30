import os
import json
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
from nltk.tokenize import RegexpTokenizer



captions2filename={}

curdir=os.getcwd()

what_dir_to_look_in='9gag_small'

eng_stemmer = SnowballStemmer('english')
reg_tokenizer = RegexpTokenizer(r'\w+')
default_stopwords = set(stopwords.words('english'))



for root, dirs, files in os.walk(what_dir_to_look_in):
	for file in files:
		if file.endswith(".json"):
			 data = json.load(open(os.path.join(curdir,what_dir_to_look_in,file)))
			 print (data['caption'])
			 label=file            
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

				if term in captions2filename:
					
					captions2filename[term].append(label)
				else:
					captions2filename[term]=[]
					captions2filename[term].append(label)


print (captions2filename)

					

			
				



			 