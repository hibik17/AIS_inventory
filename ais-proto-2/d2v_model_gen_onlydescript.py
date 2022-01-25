#!/usr/bin/python
# coding: UTF-8

import os
import random
import pandas as pd
import glob
import json
import gensim
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import sys
import codecs

# Main procedure
def main_proc(options, argv):
  random.seed(options.random_seed)
  training_dir = options.train_dir

  # 訓練用のデータの生成
  print("Input training dataset")
  # x＿train＝本タイトルとか本の記述を単語分割してリストにまとめたもの　訓練データ
  # y＿train =ysbmその本に関連した情報今のところは著者のみ→位置情報も追加が必要　教師データ
  # get_dfでは訓練データと教師データをそれぞれリストで作成した。
  (x_train, y_train) = get_df(options, training_dir)
  print("Generated")
 
  training_code = []
  # 語彙素とISBNコードを紐付けた
  for (x, y) in zip(x_train, y_train):
    training_code.append(TaggedDocument(words=x, tags=y))

  # モデルの生成、保存
  # DMmodel
  print("Generating Model dm=1")
  # epochs=繰り返しの回数、vector_sizze = 本の内容を表す浮動小数点の数→リストの要素数ー＞単語ごとの200個の浮動小数点で一つのベクトルを作る。作ったベクトルでコサイン類似度をとる。
  # じゃガード係数→類似度を図る方法ー＞浮動小数点はコサイン類似度に見るのがやりやすい→なぜコサイン類似度がいいのか
  # sample平均一回以上出てくる1e-3のものは働く
  # min_countは３以下に修正
  # プロトコルによって窓サイズを変える必要がある。
  model = Doc2Vec(documents=training_code, epochs=20, vector_size=200 , dbow_words=1, sample=1e-3, window=20, min_count=6, dm=1)
  model.save(options.model_file_1)
  print("Model saved to file (" + options.model_file_1 + ")")
  
  # Dbowmodel
  print("Generating Model dm=0")
  model = Doc2Vec(documents=training_code, epochs=20, vector_size=200 , dbow_words=1, sample=1e-3, window=20, min_count=6, dm=0)
  model.save(options.model_file_0)
  print("Model saved to file (" + options.model_file_0 + ")")

# 訓練/テスト用のデータを指定されたディレクトリから読みこみ
def get_df(options, root_dir):
  x_data = []
  y_data = []
  file_count = 0
  skip_count = 0
  for filename in ( glob.glob(root_dir + "/*.json")):
    # 正規化したjsonの形のものを読み込んでいる
    if convert_json(options, root_dir, filename, x_data, y_data):
      if file_count == options.max_files:
        break
      file_count += 1
    else:
      skip_count += 1
  print("Processed: %d, skipped: %d" % (file_count, skip_count))
  return x_data, y_data

# JSON形式のデータの読み込み
def convert_json(options, root_dir, filename, x_data, y_data):
  json_f = codecs.open(filename, 'r', 'utf-8')
  json_dict = json.load(json_f)
  json_f.close()
  
  dummy_file = root_dir + "/0_dummy.json"
  # print(filename)
  # if filename == dummy_file or ("description" in json_dict and json_dict["description"] and len(json_dict["lexemes"]) > 50):
  if filename == dummy_file or len(json_dict["lexemes"]) >= 20:
    if len(json_dict["lexemes"]) > 30:
      lexemes = json_dict["lexemes"][0:30]
    else:
      lexemes = json_dict["lexemes"]
    x_data.append(lexemes)
    tags = []
    identifier = json_dict["identifier"].split(":")[-1]
    tags.append("ID:" + identifier)
    # グループごとにキーワードごとにベクトルができる。
    # 個別の本の場合はキーワドは不要
    set_tags(tags, json_dict["keywords"])
    # print(tags)
    y_data.append(tags)
    return True
  else:
    return False
  #  print("NO DESCRIPTION")

def set_tags(tags, keywords):
  for keyword in keywords:
    if isinstance(keyword, list):
      set_tags(tags, keyword)
    elif keyword != None:
      tags.append(keyword.replace(" ", ""))

from optparse import OptionParser
def parse_args():
  parser = OptionParser()
  parser.add_option("--randomseed", dest="random_seed",
                    default=0, type="int",
                    help="seed for randomizing")
  parser.add_option("--traindir", dest="train_dir",
                    default="./json",
                    help="read training data from DIR", metavar="DIR")
  parser.add_option("--hiddenlayers", dest="hidden_layers",
                    default=250, type="int",
                    help="number of hidden layers")
  parser.add_option("--activation", dest="activation",
                    default="linear",
                    help="activation function")
  parser.add_option("--loss", dest="loss",
                    default="mean_squared_error",
                    help="loss function")
  parser.add_option("--optimizer", dest="optimizer",
                    default="rmsprop",
                    help="algorithm for optimizing")
  parser.add_option("--batchsize", dest="batch_size",
                    default=100, type="int",
                    help="batch size")
  parser.add_option("--epochnum", dest="nb_epoch",
                    default=16, type="int",
                    help="number of epochs")
  parser.add_option("--model_1", dest="model_file_1",
                    default="d2v_ipsj_desc_1.model",
                    help="model file(dm=1) name to be stored")
  parser.add_option("--model_0", dest="model_file_0",
                    default="d2v_ipsj_desc_0.model",
                    help="model file(dm=0) name to be stored")
  parser.add_option("--maxfiles", dest="max_files",
                    default=99999999, type="int",
                    help="max number of files")
  parser.add_option("--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

  return parser.parse_args()  

# Call main procedure
if __name__ == '__main__':
    (options, args) = parse_args()
    main_proc(options, args)

 
