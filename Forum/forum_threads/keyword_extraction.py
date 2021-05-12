from nltk import tokenize
from operator import itemgetter
import math


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem.porter import PorterStemmer

import json

# Summa textrank
from summa import keywords


def initialize(form_doc, update_tf):
    
    doc_idf = form_doc
    f = open("stopwords.txt", "r")
    #f.write(sb)
    file_stopwords = f.read()
    f.close()
    list_set = stopwords.words('english') + file_stopwords.split()
    #print(list_set)
    stop_words = set(list_set) 
    #print(stop_words)

    doc_idf = doc_idf.lower()
    
    if update_tf:
        f_doc = open("full_doc.txt", "a")
        f_doc.write("\n")
        form_encode = form_doc.encode(encoding='ascii', errors='ignore')
        f_doc.write(form_encode.lower().decode('ascii', 'ignore'))
        f_doc.write("\n")
        f_doc.close()

    f_doc = open("full_doc.txt", "r")
    doc_tf = f_doc.read()
    f_doc.close()

    tokens = word_tokenize(doc_tf) #doc_tf.split() NOTE: might need to be changed if word_tokenize doesn't work
    tokens = nltk.pos_tag(tokens)
    tokens = [s for (s, p) in tokens if p == 'NN']  #Grab only nouns
    words = [word for word in tokens if word.isalpha()]
    

    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in words]

    total_words_tf = stemmed
    total_word_length_tf = len(total_words_tf)
    ######################################

    total_words_idf = doc_idf.split()
    #total_word_length_idf = len(total_words_idf)


    

    total_sentences = tokenize.sent_tokenize(doc_idf)
    total_sent_len = len(total_sentences)

    #sb = ""
    tf_score = {}
    for each_word in total_words_tf:
        each_word = each_word.replace('.','')
        each_word = each_word.replace(',','')
        each_word = each_word.replace('(','')
        each_word = each_word.replace(')','')
        each_word = each_word.replace(':','')
        each_word = each_word.replace(';','')
        each_word = each_word.replace('"','')
        each_word = each_word.replace("'",'')
        each_word = each_word.replace('“','')
        each_word = each_word.replace('—','')
        if each_word not in stop_words:
            if each_word.isdigit() == False:
                if each_word in tf_score:
                    tf_score[each_word] += 1
                else:
                    tf_score[each_word] = 1
                #sb += each_word + " "

    #####
    #f = open("demofile2.txt", "a")
    #f.write(sb)
    #f.close()
    #####
    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length_tf)) for x, y in tf_score.items())

    idf_score = {}
    for each_word in total_words_idf:
        each_word = each_word.replace('.','')
        each_word = each_word.replace(',','')
        each_word = each_word.replace('(','')
        each_word = each_word.replace(')','')
        each_word = each_word.replace(':','')
        each_word = each_word.replace(';','')
        each_word = each_word.replace('"','')
        each_word = each_word.replace("'",'')
        each_word = each_word.replace('“','')
        each_word = each_word.replace('—','')
        if each_word not in stop_words:
            if each_word.isdigit() == False:
                if each_word in idf_score:
                    idf_score[each_word] = check_sent(each_word, total_sentences)
                else:
                    idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    
    return get_top_n(tf_idf_score, 5)

def check_sent(word, sentences): 
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n])
    print(result)
    f = open("keyword_comparison.txt", "w")
    f.write("Keyword extraction example\n")
    f.write("TF-IDF algorithm\n")
    f.write(json.dumps(result))
    f.close()

    for key, value in result.items():
        print(key)
        print(" - ")
        print(value)

    return list(result.keys())


# Textrank extraction

def textrank(form_doc):
    result = keywords.keywords(form_doc, words=5)
    f = open("keyword_comparison.txt", "a")
    f.write("\nTextrank algorithm\n")
    f.write(result)
    f.close()
    print(result)

