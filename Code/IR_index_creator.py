#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import nltk
from nltk.tokenize import RegexpTokenizer,word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
import operator
import json
import numpy as np

prtrstmr = PorterStemmer()
stpwrds=set(stopwords.words('english'))

# tf-idf for captions
term_to_tf={}
term_to_idf={}
wt_dic_captions = {}
ind_to_paths={}

ctr=0
for dname,subdnames,fnames in os.walk("Test_Set"):
	sorted(fnames)
	for f in fnames:
		# tokenize,remove punctuation,remove stopwords then stem
		# do normal "english" stopword removal then do some more task specific stopword removal
		# using tfidf techniques
		if f.endswith('.json'):
			ctr+=1

			name = f.split('.')

			# print ctr
			ind_to_paths[name[0]]=(dname+'/'+f)
			data = json.load(open(dname+'/'+f))

			try:
				
				file_token_to_count={}
				line_spl=data['caption'].split(' ')
				print ("Caption",data['caption'],"\n\n")
				line_new=''

				for term in line_spl:
					print(term)
					try:
						# term=term.decode('utf-8').lower()
						term = term.lower()
						# print(term)
						line_new+=(' '+term)
					except Exception as e:
						print(e)			
				# print line_new
				words=word_tokenize(line_new)
				print (words)
				for word in words:
					if word not in stpwrds:
						if word not in file_token_to_count:
							file_token_to_count[word]=1
						else:
							file_token_to_count[word]+=1


				for word in file_token_to_count:
					if word not in term_to_tf:
						term_to_tf[word]=[(name[0],file_token_to_count[word])]
					else:
						term_to_tf[word].append((name[0],file_token_to_count[word]))

					if word not in term_to_idf:
						term_to_idf[word]=1
					else:
						term_to_idf[word]+=1
			except Exception as e:
				print(e)


for word in term_to_idf:
	term_to_idf[word]=np.log10(1.0*(ctr)/term_to_idf[word])

for word in term_to_tf:
	for i in range(len(term_to_tf[word])):
		if term_to_tf[word][i][1]>0:
				
			tf=np.log10(1+term_to_tf[word][i][1])
		else:
			tf=0

		term_to_tf[word][i]=(term_to_tf[word][i][0],tf)

		if word in term_to_idf:
			tfidf = tf*term_to_idf[word]
			term_to_tf[word][i] = (term_to_tf[word][i][0], tfidf)

# tf-idf for images
term_to_tf_img = {}
term_to_idf_img = {}
ind_to_paths_img = {}
wt_dic_img = {}

ctr=0

for dname,subdnames,fnames in os.walk("Test_Set"):
	sorted(fnames)
	for f in fnames:
		# tokenize,remove punctuation,remove stopwords then stem
		# do normal "english" stopword removal then do some more task specific stopword removal
		# using tfidf techniques
		if f.endswith('_img.json'):


			ctr+=1
			name = f.split('.')[0].strip("_img")
			# print(name)
			# exit(0)

			# print ctr
			ind_to_paths_img[name]=(dname+'/'+f)
			data = json.load(open(dname+'/'+f))

			try:
				
				file_token_to_count={}
				line_spl=data['img_text'].split(' ')
				print ("Caption",data['img_text'],"\n\n")
				line_new=''

				for term in line_spl:
					try:
						# term=term.decode('utf-8').lower()
						term = term.lower()
						line_new+=(' '+term)
					except Exception as e:
						print(e)		
				# print line_new
				words=word_tokenize(line_new)
				# print words
				for word in words:
					if word not in stpwrds:
						if word not in file_token_to_count:
							file_token_to_count[word]=1
						else:
							file_token_to_count[word]+=1


				for word in file_token_to_count:
					if word not in term_to_tf_img:
						term_to_tf_img[word]=[(name,file_token_to_count[word])]
					else:
						term_to_tf_img[word].append((name,file_token_to_count[word]))

					if word not in term_to_idf_img:
						term_to_idf_img[word]=1
					else:
						term_to_idf_img[word]+=1
							
					# for word in term_to_tf_img:
					# 	print word,term_to_tf_img[word]

			except Exception as e:
				print(e)
			
for word in term_to_idf_img:
	term_to_idf_img[word]=np.log10(1.0*(ctr)/term_to_idf_img[word])

		
for word in term_to_tf_img:
	for i in range(len(term_to_tf_img[word])):
		if term_to_tf_img[word][i][1]>0:
				
			tf=np.log10(1+term_to_tf_img[word][i][1])
		else:
			tf=0

		term_to_tf_img[word][i]=(term_to_tf_img[word][i][0],tf)
		if word in term_to_idf_img:
			tfidf = tf*term_to_idf_img[word]
			term_to_tf_img[word][i] = (term_to_tf_img[word][i][0], tfidf)

wt_dic_captions = term_to_tf;
wt_dic_img = term_to_tf_img

with open('ind_to_paths.json', 'w') as fp:
	json.dump(ind_to_paths, fp, indent=4)

with open('ind_to_paths_img.json', 'w') as fp:
	json.dump(ind_to_paths_img, fp, indent=4)

with open('wt_dic_captions.json', 'w') as fp:
	json.dump(term_to_tf, fp, indent=4)

with open('wt_dic_img.json', 'w') as fp:
	json.dump(term_to_tf_img, fp, indent=4)

lambd = 0.2

wt_dic = {}

for word in wt_dic_captions:
	if word not in wt_dic:
		wt_dic[word] = []

	if word in wt_dic_img:
		postings_captions=wt_dic_captions[word]
		postings_img=wt_dic_img[word]

		postings_final=[]

		for pair in postings_captions:
			doc_id,tfidf=pair

			for some_pair in postings_img:
				doc_id_img,tfidf_img=some_pair
				if doc_id==doc_id_img:
					postings_final.append((doc_id,lambd*tfidf+(1-lambd)*tfidf_img))

			for i in postings_final:
				wt_dic[word].append(i)

			flag = 0
			for i in postings_final:
				if pair[0] == i[0]:
					flag = 1
			if flag == 0:
				wt_dic[word].append(pair)

	else:
		wt_dic[word] = wt_dic_captions[word]



for word in wt_dic_img:
	if word not in wt_dic:
		wt_dic[word] = []

	if word in wt_dic_captions:
		postings_captions = wt_dic_captions[word]
		postings_img = wt_dic_img[word]

		postings_final = []

		for pair in postings_img:
			docid_img, tfidf_img = pair

			for some_pair in postings_captions:
				doc_id, tfidf = some_pair

				if doc_id == docid_img:
					postings_final.append((doc_id, lambd*tfidf + (1-lambd)*tfidf_img))

			for i in postings_final:
				wt_dic[word].append(i)
				
			flag = 0
			for i in postings_final:
				if pair[0] == i[0]:
					flag = 1
			if flag == 0:
				wt_dic[word].append(pair)

	else:
		wt_dic[word] = wt_dic_img[word]


with open('wt_dic.json','w') as fp:
	json.dump(wt_dic, fp, indent=4)