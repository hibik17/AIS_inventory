#!/usr/bin/python
# coding: UTF-8

import random
import gensim
from gensim.models.doc2vec import Doc2Vec
import sys
import os
import re
import shlex
import MeCab
import json
import numpy as np
import copy
import traceback

# IPSJ papers DB model (generated by Doc2Vec)
class IpsjModel:
  def __init__(self, model_name):
    self.models = {
      "model_dm":   "./" + model_name + "_1.model",
      "model_dbow": "./" + model_name + "_0.model"
    };
    self.current_model = "model_dm"  # DM model (not DBOW model)
    self.model = self.load_model(self.models[self.current_model])
    self.output_types = {
      'author': 'P',
      'org': 'O',
      'sig': 'SIG',
      'sig_year': 'SIG',
      'year': 'Y',
      'year_month': 'M',
      'article': 'ID',
      'filename': 'FILE'
    };

  def load_model(self, model_file):
    print("### load model from %s" % model_file)
    model = Doc2Vec.load(model_file)
    return model

  def vectorize(self, results, words, outline_area = ""):
    wordvecs = self.model.wv
    docvecs = self.model.docvecs
    vectors = []
    for word in words:
      if word in docvecs:
        vector = docvecs[word]
        results["input"].append(self.set_input_item(word, vector))
        vectors.append(vector)
      else:
        new_word = self.search_docvec(docvecs, word)
        if not isinstance(new_word, bool):
          results["input"].append(self.set_input_item(word, docvecs[new_word]))
          vectors.append(docvecs[new_word])
        else:
          lexemes = self.parse_text2(word)
          for lexeme in lexemes:
            if lexeme in wordvecs:
              results["input"].append(self.set_input_item(lexeme, wordvecs[lexeme]))
              vectors.append(wordvecs[lexeme])
            else:
              error_message = "Not found word %s in docvecs / wordvecs" % lexeme
              results["message"].append(error_message)
              print(error_message)

    print("OUTLINE: " + outline_area)
    if len(outline_area) > 0:
      lexemes = self.parse_text2(outline_area)
      outlne_vector =  self.model.infer_vector(lexemes, alpha=0.1, min_alpha=0.0001, steps=5)
      results["input"].append(self.set_input_item("[outline]", outlne_vector))
      vectors.append(outlne_vector)
    return(vectors)

  # search vector
  def search_docvec(self, docvecs, word):
    prefixes = self.output_types.values();
    for prefix in prefixes:
      new_word = prefix + ":" + word
      if new_word in docvecs:
        return new_word
    return False

  # merge (word/document) vectors
  def merge_vecs(self, positive, negative):
    mean = copy.copy(positive)
    for neg_vec in negative:
      weighted_vec = [-1.0 * elem for elem in neg_vec]
      mean.append(weighted_vec)
    normalized_mean = gensim.matutils.unitvec(np.array(mean).mean(axis=0)).astype(np.float32)
    return normalized_mean

  def construct_message(self, result_num, positive_words, negative_words, outline_area):
    positive_string = " ".join(positive_words)
    negative_string = " ".join(negative_words)
    if len(outline_area) > 0:
      positive_string += " [Outline]"
    message = ""
    if(result_num == 0):
      message += "No results. "
    else:
      message += "Most similar"
    if(len(negative_words) == 0):
      message += str(result_num) + " items of " + positive_string
    else:
      message += str(result_num) + " items of positive(" + positive_string + "), negative(" + negative_string + ")"
    return message

  # Search similar words
  def select_model(self, model_type):
    if model_type and len(model_type) > 0:
      if not self.current_model == model_type:
        self.current_model = model_type
        self.model = self.load_model(self.models["model_" + model_type])
    return(self.model)

  # Search similar words
  def search(self, positive_words, negative_words, outline_area, output_types, model_type):
    max_count = 100
    min_count = 20
    model = self.select_model(model_type)

    current_output = [self.output_types[type] for type in output_types]
    positive_words = shlex.split(positive_words.replace("　", " "))
    negative_words = shlex.split(negative_words.replace("　", " "))
    # results = {"message": [], "data": [], "label": [], "title": [], "description": [], "similarity": [], "vector": []}
    results = {"message": [], "data": None, "input": []}
    try:
      positive_vecs = self.vectorize(results, positive_words, outline_area)
      negative_vecs = self.vectorize(results, negative_words)
      #print(results["input"])
      #vecs = self.merge_vecs(positive_vecs, negative_vecs)
      #nominates = self.model.docvecs.similar_by_vector(vecs, topn=max_count)
      #print(positive_words)
      #print(negative_words)
      if len(positive_vecs) > 0 or len(negative_vecs) > 0:
        results["data"] = self.get_result_items(current_output, positive_vecs, negative_vecs, max_count)
        result_num = len(results["data"])
        if result_num < min_count:
          extended_results = self.get_result_items_2(current_output, positive_vecs, negative_vecs, max_count)
          results["data"].extend(extended_results)
          results["data"] = self.unique_result(results["data"])
          result_num = len(results["data"])
        results["message"].insert(0, self.construct_message(result_num, positive_words, negative_words, outline_area))
        results["rc"] = True
      else:
        results["message"].insert(0, "No word available")
        results["rc"] = False
    except (KeyError, TypeError):
      ex, ms, tb = sys.exc_info()
      print("".join(traceback.format_tb(tb)))
      print("%s: %s" % (ex, ms))
      results["message"].append("Server error: %s" % ms)
      results["rc"] = False
    # print(results)
    return results

  # 通常の方法で見つからなかった場合の処理
  def get_result_items_2(self, current_output, positive_vecs, negative_vecs, max_count):
    # print(current_output)
    result_items = []
    output_type_tags = {
      "Y":   ["Y:1973", "Y:2017"],
      "SIG": ["SIG", "SIG-end"]
    }
    for output_tag in current_output:
      if output_tag in output_type_tags:
        doctags =  self.model.docvecs.doctags
        if not output_type_tags[output_tag][1] in doctags:
          print("NG!!")
        c_start = doctags[output_type_tags[output_tag][0]].offset
        c_end = doctags[output_type_tags[output_tag][1]].offset
        nominates =  self.model.docvecs.most_similar(positive=positive_vecs, negative=negative_vecs, topn=max_count, clip_start=c_start, clip_end=c_end)

        for nominate in nominates:
          similarity = nominate[1]
          if similarity > 0.9999 and nominate[0][0:3] != "ID:":  # skip if the same vector
              continue
          result_item = self.set_result_item(nominate)
          result_items.append(result_item)

    return result_items

  def unique_result(self, result_items):
    # 重複の削除
    result_uniq = []
    for result_item in result_items:
      if not result_item["label"] in [ item["label"] for item in result_uniq]:
        result_uniq.append(result_item)
        if not "similarity" in result_item:
          print("ERROR: No similarity in result_item")
          print(result_item)
          quit()
    return sorted(result_uniq, key=lambda item: -item["similarity"])

  def get_result_items(self, current_output, positive_vecs, negative_vecs, max_count):
    nominates = self.model.docvecs.most_similar(positive=positive_vecs, negative=negative_vecs, topn=max_count)
    # nominates = self.model.docvecs.most_similar(positive=positive_words, negative=negative_words, topn=max_count)
    # print(len(nominates))

    result_items = []
    for nominate in nominates:
      similarity = nominate[1]
      if similarity > 0.9999 and nominate[0][0:3] != "ID:":  # skip if the same vector
        continue
      current_elems = nominate[0].split(":")
      item_type = current_elems[0]
      if(item_type in current_output and len(current_elems) == 2):
        result_item = self.set_result_item(nominate)
        result_items.append(result_item)
    return result_items

  def set_result_item(self, nominate):
      result_item = {}
      result_item["label"] = nominate[0]
      doctags =  self.model.docvecs.doctags
      result_item["count"] = doctags[nominate[0]].doc_count
      explanation = self.get_explanation(nominate)
      result_item["title"] = explanation[0]
      result_item["similarity"] = explanation[1]
      result_item["description"] = explanation[2]
      result_item["data"] = nominate[1]
      vec = list(self.model.docvecs[nominate[0]])
      vec = [float(x) for x in vec]
      result_item["vector"] = vec
      return result_item

  def set_input_item(self, word, vector):
      input_item = {}
      input_item["label"] = word
      vec = list(vector)
      vec = [float(x) for x in vec]
      input_item["vector"] = vec
      return input_item

  # Search similar words
  def search_words(self, word_string):
    count = 10
    max_count = 100
    words = shlex.split(word_string)
    positive_words = [ x for x in words if x[0] != '^']
    negative_words = [ x[1:] for x in words if x[0] == '^']
    results = {"message": [], "data": [], "label": []}
    try:
      nominates = self.model.most_similar(positive=positive_words, negative=negative_words, topn=max_count)
      if len(nominates) > count:
        nominates = nominates[0:count]
      for (i, item) in enumerate(nominates):
        if(i == 0):
          if(len(negative_words) == 0):
            message = "Most similar " + str(len(nominates)) + " words of " + " ".join(positive_words)
          else:
            message = str(len(nominates)) + " words of positive(" + " ".join(positive_words) + "), negative(" + " ".join(negative_words) + ")"
        results["label"].append(item[0])
        results["data"].append(item[1])
      results["message"].append(message)
    except KeyError as ev:
      results["message"].append("Error, no valid word")
    print(results)
    return results

  # Search similar papers or categories
  def search_docs(self, doc_string):
    docs = shlex.split(doc_string)
    count = 10
    max_count = 1000
    doc = docs[0]
    results = {"message": "", "data": [], "label": [], "title": [], "description": []}
    try:
      print([doc])
      nominates = self.model.docvecs.most_similar(positive=[doc], topn=max_count)
      words = doc.split(":")
      nominates = [x for x in nominates if(str(x[0]).find(words[0]) == 0)]
      print(len(nominates))
      if len(nominates) > count:
        nominates = nominates[0:count]
      for (i, item) in enumerate(nominates):
        if(i == 0):
          results["message"] = "Most similar " + str(len(nominates)) + " categories of " + doc
        results["label"].append(item[0])
        explanation = self.get_explanation(item)
        results["title"].append(explanation[0])
        results["description"].append(explanation[2])
        results["data"].append(item[1])
      results["message"] = "OK"
    except KeyError as ev:
      results["message"] = "Key Error"
    except TypeError as ev:
      results["message"] = "Type Error"
    print(results)
    return results

  # Get explanation from JSON text (out of Doc2Vec model)
  def get_explanation(self, item):
    word = item[0]
    similarity = item[1]
    explanation = [word, similarity, ""]
    print(item)
    if(word[0:3] == "ID:"):
      json_file = "./json/id_" + word[3:] + ".json"
      #json_file = word[3:]
      with open(json_file, "r") as json_f:
        json_dict = json.load(json_f)
      authors = [x[2:] for x in json_dict["keywords"] if(str(x).find("P:") == 0)]
      authors_str = ", ".join(authors)
      if not "dateofissued" in json_dict:
        json_dict["dateofissued"] = "出版日不明"
      if not "index" in json_dict:
        json_dict["index"] = "インデクス無し"
      title = authors_str + ", " + '"' + json_dict["title"] + '"' + ", " + json_dict["index"] + ", " + json_dict["dateofissued"]
      if not "description" in json_dict:
        json_dict["description"] = "内容無し"
      description = json_dict["description"]
      if isinstance(description, list):
        description = description[0]
      explanation = [title, similarity, description]
      print(explanation)
    return explanation

  # Search similar studies of specified paper absstruct
  def search_paper(self, description):
    lexemes = self.parse_text2(description)
    vector =  self.model.infer_vector(lexemes, alpha=0.1, min_alpha=0.0001, steps=5)
    doctags =  self.model.docvecs.doctags
    #print(doctags["SIG"])
    #print(doctags["SIG-end"])
    #c_start = doctags["SIG"].offset
    #c_end = doctags["SIG-end"].offset
    # nominates =  self.model.docvecs.most_similar(positive=[vector], topn=20, clip_start=c_start, clip_end=c_end)
    nominates =  self.model.docvecs.most_similar(positive=[vector], topn=20, clip_start=0, clip_end=None)
    results = {"message": "", "data": [], "label": [], "title": [], "description": []}
    for (i, item) in enumerate(nominates):
      if(i == 0):
        results["message"] = "Most similar 20 tags"
      results["label"].append(item[0])
      explanation = self.get_explanation(item)
      results["title"].append(explanation[0])
      results["description"].append(explanation[2])
      results["data"].append(item[1])
    return(results)

  # concatinate text
  def concat_text(self, item):
    if isinstance(item, list):
      return " ".join(item)
    else:
      return item

  # Parse text using MeCab
  def parse_text2(self, text):
    if not text:
      return [];
    text = self.concat_text(text)
    mt = MeCab.Tagger('mecab-ipadic-neologd')
    # print(text)
    lines = mt.parse(text).split("\n")
    # print(lines)
    lexemes = []
    for line in lines:
      print(line)
      if line == "EOS" or line == "":
        continue
      words = re.split(r"[,\t]", line)
      if words[7][0:5] == "代表表記：":
        lexemes.append(words[7][6:])
      elif words[5] != "*":
        lexemes.append(words[5])
      else:
        lexemes.append(words[0])
    return lexemes

# Main procedure
def main_proc(options, argv):
  random.seed(options.random_seed)
  model = Doc2Vec.load(options.model_file)
  read_commands(model)

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

  def do_word(self, args):
    argv = shlex.split(args)
    (options, argv) = self.parser.parse_args(argv)
    count = options.count
    max_count = options.max_count
    positive_words = [ x for x in argv if x[0] != '^']
    negative_words = [ x[1:] for x in argv if x[0] == '^']
    try:
      nominates = self.model.most_similar(positive=positive_words, negative=negative_words, topn=max_count)
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
    except KeyError as ev:
      print("Error: {0}".format(ev.message))

  def do_document(self, args):
    argv = shlex.split(args)
    (options, argv) = self.parser.parse_args(argv)
    count = options.count
    max_count = options.max_count
    doc = argv[0]
    try:
      print(doc)
      print(type(count))
      nominates = self.model.docvecs.most_similar(positive=doc, topn=max_count)
      if(options.display_metrics):
        nominates = [x for x in nominates if(str(x).find("#") > 0)]
      elif(not options.display_all):
        nominates = [x for x in nominates if(str(x).find("@") < 0)]
        match_data = re.match(r"^.+?#" , doc)
        if match_data:
          doc_type = match_data.group()
          nominates = [x for x in nominates if(str(x).find(doc_type) > 0)]

        match_data = re.match(r'^.+?\.' , doc)
        if match_data:
          doc_type = match_data.group()
          nominates = [x for x in nominates if(str(x).find('.') > 0)]

      if len(nominates) > count:
        nominates = nominates[0:count]
      for (i, item) in enumerate(nominates):
        if(i == 0):
          print("Most similar " + str(len(nominates)) + " categories of " + doc)
        print("  " + str(item[0]) + "\t" + str(item[1]))
    except KeyError as ev:
      print("Error: {0}".format(ev.message))

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
                    default="d2v_ipsj_desc_1.model",
                    help="model file name to be stored")
  parser.add_option("--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

  return parser.parse_args()

# Call main procedure
if __name__ == '__main__':
    (options, args) = parse_args()
    main_proc(options, args)
