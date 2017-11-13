
def get_score(word,tag,prev_tag,prev_prev_tag,ngram_counts,emission_counts,emission_counts_len):
    pos_score = ngram_counts[tuple(prev_prev_tag,prev_tag,tag)]+1 / ngram_counts[tuple(prev_prev_tag,prev_tag)]+1
    escore = emission_counts[word]+1/emission_counts_len +1
    return  pos_score + escore
