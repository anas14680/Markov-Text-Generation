import string
import numpy as np

# create an n-gram dictionary
def na_dict(n,lst):                                                    ## Creates a dictonary where the key is a tuple of each n-1 subsequent words in the corpus
    keys = []                                                          ## the values of the dictionary are a list of all the words that occur after that tuple 
    values=[]                                                          ## through out the corpus
    dic = {}
    
    for i in range(n-1,len(lst)):
        values.append(lst[i])
        temp_lst = []
        for j in range(1,n):
            temp_lst.append(lst[i - j])
            
        keys.append(tuple(temp_lst))

    for i in range(len(keys)):
        if keys[i] not in dic.keys():
            dic[keys[i]] = []
        if keys[i] in dic.keys():
            dic[keys[i]].append(values[i])
            
    return dic


def frequent(lst):
    occurence = []
    x = np.array(lst)                                                 ## returns the most probable element of the list and if two or more words are equally probable 
    y = np.unique(x, return_counts=True)                              ## it will return the word that occurs first in the corpus
    y_dict = dict(zip(y[0],y[1]))
    max_number = max(y_dict.values())
    for i in y_dict.keys():
        if y_dict[i] == max_number:
            occurence.append(i)
    for i in lst:
        if i in occurence:
            return i




def n_gram_sentence(n,lst):                                          ## takes a tokenized list and creates an n-1 words tuple of the last two elements of that list
    previous_words = []
    for i in range(1,n):
        previous_words.append(lst[-i])
    
    return tuple(previous_words)


def add_word(sentence, n, corpus):

    corpus_dict = na_dict(n, corpus)                                   ## based on a choice of n creates an n gram model; uses that ngram model adds the most 
                                                                        ## probable word to the dictionary
    last_n_1words = n_gram_sentence(n,sentence)
    if last_n_1words in list(corpus_dict.keys()):
        next_word = frequent(corpus_dict[last_n_1words])
        sentence.append(next_word)                 

        return sentence
    else:
        if n-1 > 0:
            return add_word(sentence,n-1,corpus)                          ## uses a recursive function to apply stupid mark off smoothing technique


def finish_sentence(sentence, n, corpus, deterministic=False):
    while (len(sentence) < 15) and (sentence[-1] not in ['.','!','?']):
        if deterministic == True:
            sentence = add_word(sentence,n,corpus)                          ## keeps on adding a word until the sentence finishes or or the length of sentence is 15
        elif deterministic == False:
            sentence.append(corpus[np.random.randint(0,len(corpus))])
    return sentence