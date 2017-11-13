import itertools
import numpy as np
from numpy.core.defchararray import rsplit
from collections import deque
from utilty import words
from collections import defaultdict

input_file = 'ass1-tagger-train'
test_file1 = 'ass1-tagger-test'
test_file2 = 'ass1-tagger-rest-input'
output_e_file = 'e.mle'
output_q_file = 'q.mle'

emission_counts = defaultdict(int)
ngram_counts = defaultdict(int)
emission_counts_len = 0
qeue = deque('s')
qeue.append('s')
qeue.append('s')

def load_corpus():
    with open(input_file, 'r') as myself:
        global  emission_counts_len
        for pair in words(myself):
            word, pos = pair.rsplit('/',1)
            emission_counts[(word,pos)] += 1
            ngram_counts[tuple(pos)] +=1
            qeue.append(pos)
            qeue.popleft()
            bigram = tuple(qeue)[1:]
            ngram_counts[bigram] +=1
            trigram = tuple(qeue)
            ngram_counts[trigram] +=1
            emission_counts_len = len(emission_counts)


def save_words():
    with open(output_q_file, 'w') as outfile:
        for key, value in emission_counts.items():
            outfile.write('%s\t%s\n' % (key,value))
    return

def HMM_stats_e():

    return

def HMM_stats():
    load_corpus()
    save_words()

    print(dict(itertools.islice(ngram_counts.items(),0,100)))
   # HMM_stats_e()



HMM_stats()

def get_score(word,tag,prev_tag,prev_prev_tag):
    pos_score = ngram_counts[tuple(prev_prev_tag,prev_tag,tag)]+1 / ngram_counts[tuple(prev_prev_tag,prev_tag)]+1
    escore = emission_counts[word]+1/emission_counts_len +1
    return  pos_score + escore






