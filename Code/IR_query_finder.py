import os
import json
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
from nltk.tokenize import RegexpTokenizer,word_tokenize
import json
import operator


eng_stemmer = SnowballStemmer('english')
# reg_tokenizer = RegexpTokenizer(r'\w+')
default_stopwords = set(stopwords.words('english'))

ind_to_paths = json.load(open('ind_to_paths.json'))
ind_to_paths_img = json.load(open('ind_to_paths_img.json'))

wt_dic = json.load(open('wt_dic.json'))


def run_query(query):
	q_words=word_tokenize(query.lower())
	relevant_docs_and_scores={}

	for word in q_words:

		try:
			print(word)
			# idf_w=term_to_idf[word]

			for doc_tfidf_pair in wt_dic[word]:
				docid,tfidf=doc_tfidf_pair
				print(docid, tfidf)

				if docid not in relevant_docs_and_scores:
					relevant_docs_and_scores[docid]=tfidf
				else:
					relevant_docs_and_scores[docid]+=tfidf
		except Exception as e:
			print(e)


	sorted_docs = sorted(relevant_docs_and_scores.items(), key=operator.itemgetter(1),reverse=True)
	# sorted_docs=sorted_docs[:10]
	print (sorted_docs)
	for x in sorted_docs:
		fname=ind_to_paths[str(x[0])]
		with open(fname) as f:
			data = json.load(open(fname))
			if 'caption' in data.keys():
				print("Result:", data['caption'])
			else:
				print("Result:", data['img_text'])
	return sorted_docs


# while 1:
# 	# query=raw_input("Enterx` query :")
# 	query=input("Enter query :")
# 	run_query(query)