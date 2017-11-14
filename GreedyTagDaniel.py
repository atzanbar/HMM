import hotshot
import sys
import os.path
from collections import defaultdict
from itertools import chain
from math import log

import time

from hmmscore import Scorer

qFile = 'q.mle'
eFile = 'e.mle'
inputFile = 'ass1-tagger-test-input'
inputFileTaged = 'ass1-tagger-test'
unk_score=0.1
unk_det=3

class GreedyDecode:
    def __init__(self, inputFile, qFile, eFile, outputFile,tfile,tfileinput):
        self.qdict = dict()
        self.qFile = qFile
        self.eFile = eFile
        self.tfile = tfile
        self.tfileinput = tfileinput
        self.totalWords = 0
        self.taglist = set()
        self.edict = dict()
        self.wordCount = defaultdict(int)
        #turn the q data to q dictionary
        with open(qFile, "r") as qFileOpened:
            self.q = qFileOpened.readlines()
            for line in self.q:
                linelist = line.split()
                self.taglist |= set(linelist[:-1])
                self.qdict[tuple(linelist[:-1])] = int(linelist[-1])
        # turn the e data to e dictionary
        with open(eFile, "r") as eFileOpened:
            self.e = eFileOpened.readlines()
            for line in self.e:
                linelist = line.split()
                self.wordCount[linelist[0]] += int(linelist[-1])
                self.edict[tuple(linelist[:-1])] = int(linelist[-1])
                self.totalWords += 1
        unk_count = int(unk_score * self.totalWords)
        self.edict[('unk','nn')] = unk_count
        self.qdict[('nn'),]+=unk_count
        self.totalWords += unk_count
        self.wordCount['unk'] += unk_count




    def tagger(self, line):
        scorer = Scorer(self.qdict, self.edict,self.totalWords,self.wordCount)
        inputSentence = line.strip('.').lower().split(" ")
        retdic = {}
        previous2 = "start"
        previous1 = "start"
        for inputWord in inputSentence:
            scoreNow = None
            wordTag = None
            for tag in self.taglist:
                testScore = scorer.get_score(inputWord, tag, previous1, previous2)
                #print (testScore)
                if testScore==1:
                    wordTag = tag
                    break
                if (scoreNow is None) or testScore > scoreNow:
                    scoreNow = testScore
                    wordTag = tag
                    previous2 = previous1
                    previous1 = wordTag
            retdic[inputWord] = wordTag
        #print(retdic)
        return retdic


    def multiTagger(self):
        start_time = time.time()
        linelistTagged = []
        linelistAnswer = []
        match = 0
        words = 0
        for line in file(self.tfile):
            items = [item for item in line.lower().split(" ")]
            linelistTagged.append({d.split("/")[0]:d.split("/")[1] for d in items})

        linecounter = 0
        for line in file(self.tfileinput):
            linelistAnswer.append(self.tagger(line))
        for i in range(len(linelistAnswer)):
                matchcount=0
                for key in linelistAnswer[i].keys():
                    answer_value = linelistTagged[i].get(key,1)
                    if answer_value !=1:
                        words +=1
                        est_value=linelistAnswer[i][key]
                        if answer_value == est_value:
                            match +=1
                        else:
                            print("word : '" + key + "'  train : '" +  est_value + "' , actual : '" + answer_value +"'")

        print match/(words*1.0)
        print("--- %s seconds ---" % (time.time() - start_time))









if __name__ == '__main__':
    def usage():
          print("Run this program as follow:\n"
                "python GreedyTag.py input_file_name q_mle_filename e_mle_filename output_file_name extra_file_name")


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

    def processingInput(inputParameters):
        """
        checks if there right numbers of parameters, and if they exsist.
        :param inputParameters:
        :return:
        """
        if len(inputParameters) == 5:
            for parameter in inputParameters:
                if os.path.isfile(parameter) == False:
                    print(parameter + " does not exists!")
                    usage()
                    exit()
            return inputParameters
        else:
            print("Wrong number of parameters.")
            exit()

    greedy_decoder = GreedyDecode(inputFile, qFile, eFile, 'out.txt','ass1-tagger-test','ass1-tagger-test-input')
    greedy_decoder.multiTagger()
    #run_profiler(greedy_decoder.multiTagger)



