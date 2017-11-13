
def get_score(word,tag,prev_tag,prev_prev_tag,ngram_counts,emission_counts,emission_counts_len):
    pos_score = 0.8*( ngram_counts[tuple([prev_prev_tag,prev_tag,tag])] / (ngram_counts[tuple([prev_prev_tag,prev_tag])]+1)) \
    * 0.15*( ngram_counts[tuple([prev_tag,tag])] / (ngram_counts[tuple(prev_tag)]+1)) \
    * 0.05*(ngram_counts[tuple(tag)]/emission_counts_len)
    escore = emission_counts[word]+1/emission_counts_len +1
    return  pos_score + escore

