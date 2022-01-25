#!/usr/bin/python
# coding: UTF-8

import random
import gensim
from gensim.models.doc2vec import Doc2Vec
import sys
import atexit
import os
import readline
import re
import shlex
from optparse import OptionParser
import numpy as np
import copy

# Main procedure
def main_proc(options, argv):
  random.seed(options.random_seed)
  model = Doc2Vec.load(options.model_file)
  read_commands(model)
  
  # atexit.register(readline.write_history_file, histfile)

# get similarity of two (word/document) vectors
def similarity(vec1, vec2):
  norm_vec1 = vec1 / np.linalg.norm(vec1)
  norm_vec2 = vec2 / np.linalg.norm(vec2)
  return(np.dot(norm_vec1, norm_vec2))

# merge (word/document) vectors
def merge_vecs(positive, negative):
  mean = copy.copy(positive)
  for neg_vec in negative:
    weighted_vec = [-1.0 * elem for elem in neg_vec]
    mean.append(weighted_vec)
  normalized_mean = gensim.matutils.unitvec(np.array(mean).mean(axis=0)).astype(np.float32)
  return normalized_mean

def read_commands(model):
  prompt = D2vPrompt(model)
  prompt.prompt = '\n> '
  start_msg = 'Enter "word if" or "doc MaxNesting#7"... or quit'
  prompt.cmdloop(start_msg)
        
from cmd import Cmd
class D2vPrompt(Cmd):
  def __init__(self, model):
    Cmd.__init__(self)
    self.model = model
    self.parser = self.set_parse()
    self.years = self.generate_year_data(1980, 2030)
    
  def generate_year_data(self, begin_year, end_year):
    year_hash = {}
    for year in range(begin_year, end_year + 1):
      year_str = "Y:" + str(year)
      if year_str in self.model.docvecs:
        year_hash[year_str] = self.model.docvecs[year_str]
      elif "Y:" + str(year - 1) in year_hash and "Y:" + str(year - 2) in year_hash:
        last_year_vec = year_hash["Y:" + str(year - 1)]
        two_year_vec  = year_hash["Y:" + str(year - 2)]
        est_vec = merge_vecs(positive=[last_year_vec, last_year_vec], negative=[two_year_vec])
        year_hash[year_str] = est_vec
      else:
        print("Cannot generate year data of (%s)." % year)
    return year_hash
    
  def do_word(self, args):
    argv = shlex.split(args)
    (options, argv) = self.parser.parse_args(argv)
    count = options.count
    max_count = options.max_count
    positive_words = [ x for x in argv if x[0] != '^']
    negative_words = [ x[1:] for x in argv if x[0] == '^']
    try:
      nominates = self.model.wv.most_similar(positive=positive_words, negative=negative_words, topn=max_count)
      if(not options.display_all):
        nominates = [x for x in nominates if(str(x).find("@") < 0)]
      if len(nominates) > count:
        nominates = nominates[0:count]
      for (i, item) in enumerate(nominates):
        if(i == 0):
          if(len(negative_words) == 0):
            print("Most similar " + str(len(nominates)) + " words of " + " ".join(positive_words))
          else:
            print(str(len(nominates)) + " words of positive(" + " ".join(positive_words) + "), negative(" + " ".join(negative_words) + ")")
        print("  " + item[0] + "\t" + str(item[1]))

      positive_vecs = [self.model[word] for word in positive_words]
      negative_vecs = [self.model[word] for word in negative_words]
      word_vec = merge_vecs(positive_vecs, negative_vecs)
      #for year in range(1990, 2018):
      #  year_word = "Y:" + str(year)
      #  year_vec = self.years[year_word]
      #  print("  %d:\t%f" % (year, similarity(year_vec, word_vec)))
    except KeyError:
      ex, ms, tb = sys.exc_info()
      print("%s: %s" % (ex, ms))

  def do_document(self, args):
    argv = shlex.split(args)
    (options, argv) = self.parser.parse_args(argv)
    count = options.count
    max_count = options.max_count
    positive_words = [ x for x in argv if x[0] != '^']
    negative_words = [ x[1:] for x in argv if x[0] == '^']
    try:
      nominates = self.model.docvecs.most_similar(positive=positive_words, negative=negative_words, topn=max_count)

      if len(nominates) > count:
        nominates = nominates[0:count]
      for (i, item) in enumerate(nominates):
        if(i == 0):
          if(len(negative_words) == 0):
            print("Most similar " + str(len(nominates)) + " documents of " + " ".join(positive_words))
          else:
            print(str(len(nominates)) + " words of positive(" + " ".join(positive_words) + "), negative(" + " ".join(negative_words) + ")")
        print("  " + str(item[0]) + "\t" + str(item[1]))

      positive_vecs = [self.model.docvecs[word] for word in positive_words]
      negative_vecs = [self.model.docvecs[word] for word in negative_words]
      word_vec = merge_vecs(positive_vecs, negative_vecs)
      for year in range(1990, 2018):
        year_word = "Y:" + str(year)
        year_vec = self.years[year_word]
        print("  %d:\t%f" % (year, similarity(year_vec, word_vec)))

    except (KeyError, TypeError):
      ex, ms, tb = sys.exc_info()
      print("%s: %s" % (ex, ms))

  def do_dw(self, args):
    argv = shlex.split(args)
    (options, argv) = self.parser.parse_args(argv)
    count = options.count
    max_count = options.max_count
    positive_words = [ x     for x in argv if x[0] != '^']
    negative_words = [ x[1:] for x in argv if x[0] == '^']
    doc_model = self.model.docvecs
    try:
      positive_vecs = [ doc_model[x] for x in positive_words]
      negative_vecs = [ doc_model[x] for x in negative_words]
      #print(doc)
      #docvec = merge_vecs(positive_vecs, negative_vecs)
      #nominates = self.model.wv.similar_by_vector(docvec, topn=max_count)
      nominates = self.model.wv.most_similar(positive=positive_vecs, negative=negative_vecs, topn=max_count)

      if len(nominates) > count:
        nominates = nominates[0:count]
      for (i, item) in enumerate(nominates):
        if(i == 0):
          if(len(negative_words) == 0):
            print("Most similar " + str(len(nominates)) + " words of " + " ".join(positive_words))
          else:
            print(str(len(nominates)) + " words of positive(" + " ".join(positive_words) + "), negative(" + " ".join(negative_words) + ")")
        print("  " + str(item[0]) + "\t" + str(item[1]))
    except KeyError:
      ex, ms, tb = sys.exc_info()
      print("%s: %s" % (ex, ms))



  def do_quit(self, args):
    print("Bye!")
    return True

  def do_w(self, args):
    self.do_word(args)

  def do_d(self, args):
    self.do_document(args)

  def do_doc(self, args):
    self.do_document(args)

  def do_q(self, args):
    return self.do_quit(args)
  
  def do_EOF(self, args):
    return self.do_quit(args)
  
  def set_parse(self):
    parser = OptionParser()
    parser.add_option("--count", dest="count",
                      default=10, type="int",
                      help="count of results")
    parser.add_option("--max_count", dest="max_count",
                      default=100, type="int",
                      help="max count of results")
    parser.add_option("--metrics",
                      action="store_true", dest="display_metrics", default=False,
                      help="display metrics data")
    parser.add_option("--all",
                      action="store_true", dest="display_all", default=False,
                      help="display all data")
    return parser


def parse_args():
  parser = OptionParser()
  parser.add_option("--randomseed", dest="random_seed",
                    default=0, type="int",
                    help="seed for randomizing")
  parser.add_option("--model", dest="model_file",
                    default="d2v_ipsj_desc_0.model",
                    help="model file name to be stored")
  parser.add_option("--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

  return parser.parse_args()  

# Call main procedure
if __name__ == '__main__':
    (options, args) = parse_args()
    main_proc(options, args)

 
