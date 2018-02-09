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

what_dir_to_look_in='9gag'

eng_stemmer = SnowballStemmer('english')
reg_tokenizer = RegexpTokenizer(r'\w+')
default_stopwords = set(stopwords.words('english'))

file_ctr=0

int_to_filename={}


for root, dirs, files in os.walk(what_dir_to_look_in):
	for file in files:
		if file.endswith(".json"):

			file_ctr+=1
			int_to_filename[file_ctr]=file

			data = json.load(open(os.path.join(curdir,what_dir_to_look_in,file)))
			# print (data['caption'])
			# print data
			label=file_ctr    
			# Vishal's code        
			# captions_separated=str(data['caption']).split()
			# print(captions_separated)
			# captions_sep_stemmed=[]
			# for term in captions_separated:
			#   if term[0]=='#':
			#       term=term[1:]
			#   if term not in default_stopwords:
			#       try:
			#           term_stemmed=eng_stemmer.stem(term)
			#       except Exception as e:
			#           term_stemmed=term
			#       captions_sep_stemmed.append(term_stemmed)
			# for term in captions_sep_stemmed:

			#   if term in captions_to_indexes:
					
			#       captions_to_indexes[term].append(label)
			#   else:
			#       captions_to_indexes[term]=[]
			#       captions_to_indexes[term].append(label)

			# Aditya's code: The preprocessing is a little bit too strong as it removes words like can't or don't or doesn't,
			# but I'll think of something a little less strong later
			try:
				words = reg_tokenizer.tokenize(data['caption'])
				print(words)
				# words = [word for word in words if len(word) > 1]
				#convert to lower case
				words = [word.lower() for word in words]
				#remove stopwords
				words = [word for word in words if not word in default_stopwords]
		#         #removing numbers
		#         words = [word for word in words if not word.isnumeric()]
				#stem the words
				words = [eng_stemmer.stem(word) for word in words]
				print(words)
				#X_preprocessed.append(str(words))
				for word in words:
					if word not in captions_to_indexes.keys():
						captions_to_indexes[word] = set()
						captions_to_indexes[word].add(label)
					else:
						captions_to_indexes[word].add(label)
			except Exception as e:
				pass
				
for key in captions_to_indexes.keys():
	captions_to_indexes[key] = sorted(list(captions_to_indexes[key]))
print(captions_to_indexes)
# print (captions_to_indexes)
# print int_to_filename

with open('captions_to_indexes.json', 'w') as fp:
	json.dump(captions_to_indexes, fp, indent=4)

with open('int_to_filename.json', 'w') as fp:
	json.dump(int_to_filename, fp, indent=4)