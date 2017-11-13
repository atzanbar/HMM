import sys
import os.path
from collections import defaultdict
from itertools import chain
from math import log

from hmmscore import get_score

class GreedyDecode:
    def __init__(self, inputFile, qFile, eFile, outputFile, extraFile):
        self.numWords = 0
        self.taglist = set()
        self.edict = dict()
        self.qdict = dict()
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
                self.edict[tuple(linelist[:-1])] = int(linelist[-1])
                self.numWords += 1
        with open(inputFile, "r") as inputFileOpened:
            self.inputText = inputFileOpened.readlines()
            self.tagger(self.inputText, outputFile)

    def score(self, word, tag, previoustag1, previoustag2):
        numWords = self.calNumWords()
        countABC = 0
        countAB = 0
        countBC = 0
        countB = 0
        countC = 0
        lamdaq1 = 0.8
        lamdaq2 = 0.15
        lamdaq3 = 0.05
        lamdae1 = 0.95
        lamdae2 = 0.05
        countWPOS = 0
        countPOS = 0
        for pair in self.qdict:
            if len(pair) == 4:
                if (pair[0], pair[1], pair[2]) == (previoustag2, previoustag1, tag):
                    countABC = int(pair[3])
                if (pair[0], pair[1]) == (previoustag2, previoustag1):
                    countAB += int(pair[3])
            elif len(pair) == 3:
                if (pair[0], pair[1]) == (previoustag1, tag):
                    countBC = int(pair[2])
                if (pair[0]) == previoustag1:
                    countB += int(pair[2])
            elif len(pair) == 2:
                if (pair[0]) == tag:
                    countC = int(pair[1])
        if countABC == 0:
            if countBC == 0:
                qResult = (lamdaq3 * countC * 1.0 / (numWords * 1.0))
            else:
                qResult = (lamdaq2 * countBC * 1.0 / (countB * 1.0)) + (lamdaq3 * countC * 1.0 / (numWords * 1.0))
        else:
            qResult = (lamdaq1*countABC*1.0/(countAB*1.0)) + (lamdaq2*countBC*1.0/(countB*1.0)) + (lamdaq3*countC*1.0/(numWords*1.0))
        for pair in self.edict:
            if pair[1] == tag:
                countPOS += int(pair[2])
                if pair[0] == word:
                    countWPOS = int(pair[2])
        eResult = (lamdae1*countWPOS/(countPOS*1.0)) + (lamdae2/countPOS)
        return log(qResult, 10) + log(eResult, 10)

    def get_score(self, word, tag, prev_tag, prev_prev_tag, ngram_counts, emission_counts, emission_counts_len):
        pos_score = 0.8 * (
        ngram_counts[tuple([prev_prev_tag, prev_tag, tag])] / (ngram_counts[tuple([prev_prev_tag, prev_tag])] + 1)) \
                    * 0.15 * (ngram_counts[tuple([prev_tag, tag])] / (ngram_counts[tuple(prev_tag)] + 1)) \
                    * 0.05 * (ngram_counts[tuple(tag)] / emission_counts_len)
        escore = emission_counts[word] + 1 / emission_counts_len + 1
        return pos_score + escore

    def tagger(self, inputText, outputFile):
        lenOfInput = len(inputText)
        with open(outputFile, "w") as output:
            for inputLine in inputText:
                inputLine = inputText[1]
                inputSentence = inputLine.split(" ")[:-1]
                previous2 = "start"
                previous1 = "start"
                for inputWord in inputSentence:
                    scoreNow = None
                    wordTag = None
                    for tag in self.taglist:
                        testScore = get_score(inputWord, tag, previous1, previous2, self.qdict, self.edict, self.numWords)
                        if testScore > scoreNow:
                            scoreNow = testScore
                            wordTag = tag
                            previous2 = previous1
                            previous1 = wordTag
                    toWrite = inputWord + "/" + wordTag + " "
                    output.writelines(toWrite)
                output.writelines("\n")
                print (str(inputText.index(inputLine)) + " of " + str(lenOfInput))
                print







if __name__ == '__main__':
    def usage():
          print("Run this program as follow:\n"
                "python GreedyTag.py input_file_name q_mle_filename e_mle_filename output_file_name extra_file_name")

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
            usage()
            exit()

    inputParameters = sys.argv[1:]
    (inputFile, qFile, eFile, outputFile, extraFile) = processingInput(inputParameters)
    GreedyDecode(inputFile, qFile, eFile, outputFile, extraFile)
