import numpy as np
def get_score(word,tag,prev_tag,prev_prev_tag,ngram_counts,emission_counts,emission_counts_len):

    trigram_count = ngram_counts.get(tuple([prev_prev_tag,prev_tag,tag]),0)
    bigram_count = ngram_counts.get(tuple([prev_tag,tag]),0)
    pos_count = ngram_counts.get(tuple([tag]), 0)
    a = (0.8*(trigram_count/((bigram_count*1.0)+1)))
    b = (0.15*(bigram_count/((pos_count*1.0)+1)))
    c = (0.05*(pos_count/((emission_counts_len*1.0) + 1)))
    pos_score = a + b + c
    escore = emission_counts.get(tuple([word, tag]), 0)/(emission_counts_len +1)
    if escore == 0:
        return  np.log(pos_score)
    else:
        np.log(pos_score) + np.log(escore)

