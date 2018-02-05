import os
import json
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
from nltk.tokenize import RegexpTokenizer
import json

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

print(captions_to_indexes)
print(int_to_filename)

print("Enter Query: ", end='')
q = input()
query = reg_tokenizer.tokenize(q)
# print(query)

for i in query:
	if (i in default_stopwords):
		query.remove(i)

# print(query)

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

ans = set()
count1 = 0

for i in range(len(query) - 1):
	x = query[i]
	y = query[i+1]
	x.lower()
	y.lower()

	x_root=eng_stemmer.stem(x)
	y_root=eng_stemmer.stem(y)
	# print(x_root)
	# print(y_root)

	valx = []
	valy = []
	if (x in captions_to_indexes):
		valx = list(captions_to_indexes[x])
	if (y in captions_to_indexes):
		valy = list(captions_to_indexes[y])
	res = xANDy(valx, valy, 1)
	
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
