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
from utils import get_text_from_img
import autocorrect as ac

cwd = os.getcwd()

for dname,subdnames,fnames in os.walk("Test_Set"):

	for f in fnames:
	
		# try:
		if f.endswith('.jpg'):
			print (os.path.join(os.getcwd(),dname+'/'+f))
			text=get_text_from_img(os.path.join(os.getcwd(),dname+'/'+f))


			fname_spl = f.split('.')
			file_name = fname_spl[0] + '_img.json';

			word_dic = {}
			word_dic['img_text'] = text

			# print (text)
			f = open(cwd + os.path.join('/Test_Set/', file_name), 'w')
			json.dump(word_dic, f, indent=4)
			# breakcwd = os.getcwd()


		# except Exception as e:

			# print e	
						
