#!/usr/bin/python
# coding: UTF-8

import random
import gensim
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import sys
import atexit
import os
import readline
import re
import shlex
from optparse import OptionParser
import MeCab
import json

# Main procedure
def main_proc(options, argv):

  # random.seed(options.random_seed)
  model = Doc2Vec.load(options.model_file)
  
  mt = MeCab.Tagger('mecab-ipadic-neologd')
  text = "ダークネットでは，DDoS 攻撃，DNS アンプ攻撃などの大規模な攻撃を行うための事前活動や新しいマルウェアの出現によるスキャン活動などのトラフィックが観測される事例が数多く報告されている．また，近年，官公庁・政府機関・企業などを狙った標的型攻撃や新たな攻撃手法である水飲み場型攻撃などのサイバー攻撃は，今まで以上に高度化・巧妙化している．本論文においては，日本における NICTER と世界規模の NORSE，二つのダークネット観測網のトラフィックデータの相関分析を行い，両者のダークネットトラフィックに相関関係があることがわかった．"
  text = "米ファイザーが、開発中の新型コロナウイルスの飲み薬について言及した重症化リスクを9割低減させたとする最終試験結果を公表また、「オミクロン株に対しても有効性が維持できる可能性がある」とした"
  text = ""
  text = "自民党の総裁は誰でしょう。"
  text = "ファッション、美容、エステは、いつ誕生したか?ルネッサンス期から現代までの「美人」と「化粧法・美容法」をめぐる歴史。当初、普遍的で絶対的なものとしてあった「美」は、「自分を美しくする」技術や努力が重要視されるなかで、個性的なもの、誰もが手にしうるものとして徐々に“民主化”され、現代の化粧品、ファッション、エステ、ダイエットが示すごとく、“美の追求”は万人にとっての強迫観念にまでなった。"
  text = "自民党の総裁は誰でしょう。"
  text = "米ファイザーが、開発中の新型コロナウイルスの飲み薬について言及した重症化リスクを9割低減させたとする最終試験結果を公表また、「オミクロン株に対しても有効性が維持できる可能性がある」とした"
  text = "韓国の「国民の党」から出馬したアン・チョルス（安哲秀）大統領候補が、日本のメルカリに近い中古取引プラットホーム「ニンジンマーケット」に売り物として出現した。"
  text = "イギリス王室に使える身として大陸に単身赴任し、もう何カ月も家族の顔も見ることが"
  text = "消される天安門事件の記憶。香港の大学、親中派が圧力。香港の大学で、民主化を求める学生らが北京で武力弾圧された1989年の天安門事件"
 
  lexemes = parse_text(text, mt)
  print(lexemes)
 
  # モデルを使うときではなく、新しい文章のベクトルを図るもの
  # 単語なら不要、今まで出てきた単語の範囲で新しい文章のベクトルを予測する
  vector = model.infer_vector(lexemes, alpha=0.1, min_alpha=0.0001, steps=10)  # 

  # doctags = model.docvecs.doctags
  #print(doctags["SIG"])
  #print(doctags["SIG-end"])
  #c_start = doctags["SIG"].offset
  #c_end = doctags["SIG-end"].offset
  #nominates = model.docvecs.most_similar(positive=[vector], topn=1000, clip_start=c_start, clip_end=c_end)
  # positiveはニュースのコサイン類似度が高い16個出して、そのコサイン類似度の高い本を出力する
  nominates = model.docvecs.most_similar(positive=[vector], topn=16)

  print(text)
  for nominate in nominates:
    explanation = get_explanation(nominate)
    print(explanation)
  quit()
  read_commands(model)
  
  # atexit.register(readline.write_history_file, histfile)

def parse_text(text, mecab_tag):
    lexemes = []
    text = text.replace("　", " ")
    for line in mecab_tag.parse(text).split("\n"):
        # print(line)
        if line == "EOS" or line == "":
            continue
        words = re.split(r"[,\t]", line)
        #print(words)
        # 助詞が重要ではない
        if words[2] == "サ変接続" and words[7] == "*":
            pass # print("zz " + line)
        elif words[2] == "記号" or words[1] == "記号":
            pass
        elif words[1] == "助詞":
            pass
        else:
            lexemes.append(words[0])
    return lexemes

# Get explanation from JSON text (out of Doc2Vec model)
def get_explanation(nominate):
  print(nominate)
  word = nominate[0]
  similarity = nominate[1]
  explanation = ""
  if(word[0:3] == "ID:"):
    json_file = "./json/id_" + word[3:] + ".json"
    #json_file = word[3:]
    with open(json_file, "r") as json_f:
      json_dict = json.load(json_f)
    authors_str = json_dict["biblio_authors"]
    title = json_dict["title"]
    description = json_dict["description"][0:50]
    explanation = "%f, %s, %s, %s" % (similarity, authors_str, title, description)
  return explanation

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
                    default="d2v_ipsj_1.model",
                    help="model file name to be stored")
  parser.add_option("--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

  return parser.parse_args()  

# Call main procedure
if __name__ == '__main__':
    (options, args) = parse_args()
    main_proc(options, args)

 
