import os
import json

cwd = os.getcwd()
file = open(os.path.join(cwd, 'gold_set.txt'))

# lines = file.read()

for line in file:
	phrases = line.split('%%%')
	
	for i in range(len(phrases)):
		phrases[i] = phrases[i].strip()
		
	words = phrases[1].split('.')
	file_name = words[0] + '.json';

	word_dic = {}
	word_dic['caption'] = phrases[0]

	f = open(cwd + os.path.join('/Test_Set/', file_name), 'w')
	json.dump(word_dic, f, indent=4)
