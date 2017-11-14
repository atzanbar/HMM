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
ngram_counts = [defaultdict(int) for i in range(3)]
emission_counts_len = 0
qeue = deque(['start'])
qeue.append('start')
qeue.append('start')

def load_corpus():
    for line in file(input_file):
        for pair in line.strip().lower().split(" "):
            global  emission_counts_len
            emission_counts_len+=1
            word, pos = pair.rsplit('/',1)
            emission_counts[(word,pos)] += 1
            ngram_counts[0][tuple([pos])] +=1
            qeue.append(pos)
            qeue.popleft()
            bigram = tuple(qeue)[1:]
            ngram_counts[1][bigram] +=1
            trigram = tuple(qeue)
            ngram_counts[2][trigram] +=1



def save_words():
    with open(output_q_file, 'w') as outfile:
        for i in range(3):
            for key, value in ngram_counts[i].items():
                 outfile.write('\t'.join(str(s) for s in key)+'\t' + str(value) +"\n")
    with open(output_e_file, 'w') as outfile:
        for key, value in emission_counts.items():
            outfile.write('\t'.join(str(s) for s in key)+'\t' + str(value) +"\n")
    return

def HMM_stats_e():

    return

def HMM_stats():
    load_corpus()
    save_words()

    from  hmmscore import get_score

    #print (get_score('chief','JJ','CC','NN',ngram_counts,emission_counts,emission_counts_len))
    #print(dict(itertools.islice(ngram_counts.items(),0,100)))
   # HMM_stats_e()



HMM_stats()







