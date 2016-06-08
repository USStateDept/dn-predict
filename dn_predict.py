#! /usr/bin/env python3

import re
import sys
import json
import csv
import codecs
from datetime import datetime
from nltk import PorterStemmer
from fileIO import FileIO

##
## CONSTANTS and REGEX
##

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again",
             "against", "all", "almost", "alone", "along", "already", "also","although",
             "always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another",
             "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",
             "at", "back","be","became", "because","become","becomes", "becoming", "been",
             "before", "beforehand", "behind", "being", "below", "beside", "besides",
             "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can",
             "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe",
             "detail", "do", "done", "down", "due", "during", "each", "eg", "eight",
             "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even",
             "ever", "every", "everyone", "everything", "everywhere", "except", "few",
             "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former",
             "formerly", "forty", "found", "four", "from", "front", "full", "further",
             "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her",
             "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself",
             "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc",
             "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last",
             "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me",
             "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
             "move", "much", "must", "my", "myself", "name", "namely", "neither", "never",
             "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not",
             "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only",
             "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out",
             "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same",
             "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she",
             "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
             "somehow", "someone", "something", "sometime", "sometimes", "somewhere",
             "still", "such", "system", "take", "ten", "than", "that", "the", "their",
             "them", "themselves", "then", "thence", "there", "thereafter", "thereby",
             "therefore", "therein", "thereupon", "these", "they", "thickv", "thin",
             "third", "this", "those", "though", "three", "through", "throughout", "thru",
             "thus", "to", "together", "too", "top", "toward", "towards", "twelve",
             "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via",
             "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever",
             "where", "whereafter", "whereas", "whereby", "wherein", "whereupon",
             "wherever", "whether", "which", "while", "whither", "who", "whoever",
             "whole", "whom", "whose", "why", "will", "with", "within", "without",
             "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

##
## FUNCTIONS
##

def main():
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--in", metavar="FILE", dest="in_file", default=None,
                    help="Specify the input FILE.", required=True)
  parser.add_argument("-m", "--model", metavar="FILE", dest="model_out", default=None,
                    help="Specify the output model FILE.", required=True)
  parser.add_argument("-r", "--ranges", metavar="FILE", dest="ranges_out", default=None,
                    help="Specify the output ranges FILE.", required=True)
  args = parser.parse_args()
  
  in_file = args.in_file
  model_out = args.out_file
  ranges_out = args.ranges_out

##
## CLASSES
##

class Model(FileIO):
  def __init__(self, *args, **kwargs):
    FileIO.__init__(self, *args, **kwargs)
    self.data_list = []
    self.stemmer = PorterStemmer() # correct syntax?
    self.score_map = 
    self.ranges = 

  def isInt(self, val):
    try:
      val = int(val)
      return True
    except ValueError:
      return False

  def cleanString(self, word):
    if (word not in stopwords) and (word is not " ") and (self.isInt(word) is False):
      word = word.lower()
      return self.stemmer.stem(word)
    else:
      return None

  def makeScoreList(self):
    '''Initialize a new array of 0s for each range'''
    s_list = [0] * len(self.ranges))


##
## IFMAIN 
##

if __name__ == '__main__':
  main()