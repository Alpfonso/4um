from nltk import tokenize
from operator import itemgetter
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

stop_words = set(stopwords.words('english'))

doc = "Recall that we need to finally vectorize the document, when we are planning to vectorize the documents, we cannot just consider the words that are present in that particular document. If we do that, then the vector length will be different for both the documents, and it will not be feasible to compute the similarity. So, what we do is that we vectorize the documents on the vocab. vocab is the list of all possible words in the corpus."

new_text = ""
for word in doc:
    if word not in stop_words:
        new_text = new_text + " " + word

for word in doc:
    if len(word) > 1:
       new_text = new_text + " " + word


num_of_words = len(doc.split())
words = doc.split()


print(words)