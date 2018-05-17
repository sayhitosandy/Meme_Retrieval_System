import pytesseract
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np
from nltk.corpus import wordnet


def get_text_from_img(img_path):
	

#USE python3.5

#plot histogram and get the maximum histogram peak

	img = cv2.imread(img_path)
	img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
	img_mod = cv2.medianBlur(img,3)

	# print(img_mod)
	xy=np.unique(img_mod,return_counts=True)
	img_mod[img_mod<=200]=0

	# plt.plot(xy[0],np.gradient(xy[1])
	# plt.plot(xy[0],xy[1])
	# plt.show()

	# plt.subplot(121),plt.imshow(img)
	# plt.subplot(122),plt.imshow(img_mod)

	# plt.show()

	return (pytesseract.image_to_string(img_mod).lower())  # print ocr text from image
	# or

def get_synonyms(word):
	
	synonyms = []
	for syn in wordnet.synsets(word):
	    for l in syn.lemmas():
	        synonyms.append(l.name())

	return synonyms

