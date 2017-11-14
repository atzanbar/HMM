import numpy as np
import re

word_patterns = [
    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
    (r'.*ould$', 'MD'),
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*ness$', 'NN'),
    (r'.*ment$', 'NN'),
    (r'.*ful$', 'JJ'),
    (r'.*ious$', 'JJ'),
    (r'.*ble$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*ive$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*est$', 'JJ'),
    (r'^a$', 'PREP'),
]

reg_ex_dic = dict((l[1].lower(),l[0]) for l in word_patterns)

class RegExScorer:

     def __init__(self):
        a=1


     def get_score(self,word,tag):
        if (tag in reg_ex_dic) and re.search(reg_ex_dic[tag],word):
                return 1
        else:
                return 0




class Scorer:


    def __init__(self, ngram_counts,emission_counts,emission_len,wordcount):
        self.ngram_counts  = ngram_counts
        self.emission_counts = emission_counts
        self.emission_len = emission_len
        self.wordCount = wordcount




    def get_score(self,word,tag,prev_tag,prev_prev_tag):
        unk_score =0
        word_count = (self.wordCount[word]*1.0)
        if (word_count)<3:
            unk_score=RegExScorer().get_score(word,tag)
            if unk_score<1:
                word='unk'
                word_count = (self.wordCount[word]*1.0)

        pos_count = self.ngram_counts.get(tuple([tag]),1)
        emission_count = self.emission_counts.get(tuple([word, tag]), 1)
        escore = 0.7*(emission_count/((pos_count*1.0)+1)) + 0.2* unk_score  +0.1* (1.0/self.emission_len)

        if escore > 0.55:
            return 1

        trigram_count = self.ngram_counts.get(tuple([prev_prev_tag,prev_tag,tag]),0)
        bigram_prev_count = self.ngram_counts.get(tuple([prev_prev_tag,prev_tag]),0)
        bigram_count = self.ngram_counts.get(tuple([prev_tag,tag]),0)
        pos_prev_count = self.ngram_counts.get(tuple([prev_tag]), 1)
        pos_count = self.ngram_counts.get(tuple([tag]),1)
        a = (0.8*(trigram_count/((bigram_prev_count*1.0)+1)))
        b = (0.15*(bigram_count/((pos_prev_count*1.0)+1)))
        c = (0.05*(pos_count/(word_count + 1)))
        pos_score = a + b + c
    
    
    
        return  (np.log(pos_score) +np.log(escore))

