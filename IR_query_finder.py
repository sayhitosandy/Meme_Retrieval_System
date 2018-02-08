import os
import json
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
from nltk.tokenize import RegexpTokenizer
import json

def run_query(query):
	curdir=os.getcwd()

	eng_stemmer = SnowballStemmer('english')
	reg_tokenizer = RegexpTokenizer(r'\w+')
	default_stopwords = set(stopwords.words('english'))

	fp = open(os.path.join(curdir,r"captions_to_indexes.json"), 'r')
	captions_to_indexes = json.load(fp)
	fp.close()

	fp = open(os.path.join(curdir,r"int_to_filename.json"), 'r')
	int_to_filename = json.load(fp)
	fp.close()

	# print(captions_to_indexes)
	# print(int_to_filename)

	query = reg_tokenizer.tokenize(query)
	words = [word.lower() for word in query]
	words = [word for word in words if not word in default_stopwords]
	words = [eng_stemmer.stem(word) for word in words]
	query = words
	# print(query)

	ans = set()
	count1 = 0

	if(len(query)==1):
		if (query[0] in captions_to_indexes):
			ans = set(captions_to_indexes[query[0]])
		return ans

	for i in range(len(query) - 1):
		x = query[i]
		y = query[i+1]

		valx = set()
		valy = set()
		if (x in captions_to_indexes):
			valx = set(captions_to_indexes[x])
		if (y in captions_to_indexes):
			valy = set(captions_to_indexes[y])
		# res = xANDy(valx, valy, 1)
		# print(valx)
		# print(valy)
		res = valx.intersection(valy)
		# print(res)
		
		count1 += 1
		if (count1 == 1):
			for v in res:
				ans.add(v)
		
		else:
			r = set(res)
			ans = ans.intersection(r)		
		
		# for item in ans:
		# 	print(int_to_filename[str(item)])
	if (len(ans) > 0):
		print(ans)
	else:
		print("No matching item.")

	return ans


def xANDy(valx, valy, skips=1):
    res = []
    i = 0
    j = 0
    lvalx = len(valx)
    lvaly = len(valy)
    while (i<lvalx and j < lvaly):
        if (valx[i] == valy[j]):
            res.append(valx[i])
            i += 1
            j += 1
        elif (valx[i] < valy[j]):
            if (skips != 1):
                if (i%skips == 0 and i+skips < lvalx and valx[i+skips] < valy[j]):
                    i += skips
                else:
                    i += 1
            else:
                i += 1
        else:
            if (skips != 1): 
                if (j%skips == 0 and j+skips < lvaly and valy[j+skips] < valx[i]):
                    j += skips
                else:
                    j += 1
            else:
                j += 1
    return res

# print("Enter Query: ", end='')
# q = input()
# run_query(query)
