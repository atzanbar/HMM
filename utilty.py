def words(stringIterable):
    #upcast the argument to an iterator, if it's an iterator already, it stays the same
    lineStream = iter(stringIterable)
    for line in lineStream: #enumerate the lines
        for word in line.split(): #further break them down
            yield word


def run_profiler(a):
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()
    a()
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print s.getvalue()



def validate_row_loss(orig_row,tagged_row):
    words = 0
    match = 0
    for i in range(len(orig_row)):
        if orig_row[i][0]== tagged_row[i][0]:
            words +=1
            if orig_row[i][1]== tagged_row[i][1]:
                 match +=1
    return  match,words
