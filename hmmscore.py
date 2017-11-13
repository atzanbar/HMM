
def get_score(word,tag,prev_tag,prev_prev_tag,ngram_counts,emission_counts,emission_counts_len):

    trigram_count = ngram_counts.get(tuple([prev_prev_tag,prev_tag,tag]),0)
    bigram_count = ngram_counts.get(tuple([prev_prev_tag,prev_tag]),0)
    pos_count = ngram_counts[tuple(prev_tag)]
    pos_score = 0.8*( trigram_count / bigram_count+1) * 0.15*( bigram_count / (pos_count+1) ) * 0.05*(ngram_counts[tuple(tag)]/emission_counts_len)
    escore = emission_counts[word]+1/emission_counts_len +1
    return  pos_score + escore

