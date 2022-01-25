#!/usr/bin/python
# coding: UTF-8

# PYTHON3 ONLY

import sys
import json
import glob
#import xmltodict
import collections
import pandas as pd
import requests
import MeCab
#import mojimoji
import re
import html
import random
import string
import datetime
import os
import time

# Main procedure
def main(argv):
  root_dir = "./xml"
  get_biblio_data()
  
def get_biblio_data():
  index_hash = {}
  df = pd.read_csv( './相1F300.txt',  delimiter='\t', index_col='ISBN/ISSN', encoding="cp932" )
  #print(df['書名'])
  for key, elems in df.iterrows():
    if not pd.isna(key):
      # print(key, elems["書名"])
      isbn_code = str(key)
      json_file = "google_books/id_" + isbn_code + ".json"
      if not os.path.isfile(json_file):
        rq = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+ isbn_code)
        if rq.status_code == 200:
          json_text = rq.text
          with open(json_file, "w", encoding='utf8') as fh:
            fh.write(json_text)
          time.sleep(0.2)
        else:
          print("Error: %d" % rq.status_code)
    else:
      print("ISBN not found, %s" % elems['書名'])

def puts_dummy_file(index_hash):
  dummy_file = "json/0_dummy.json"
  info = {
    "dateofissued": "2999-12-31",
    "description": None,
    "identifier": "dummy",
    "index": "Dummy",
    "keywords": [],
    "lexemes": generate_random_string(),
    "set": "00000:00000:00000",
    "title": None
  }
  prev = None
  for index in index_hash["StringIndex"]:
    elems = index.split(":")
    if prev and elems[0] != prev:
      info["keywords"].append(prev + "-end")
    prev = elems[0]
    info["keywords"].append(index)
  for year in range(1973, datetime.datetime.now().year + 1):
    info["keywords"].append("Y:" + str(year))
  json_text = json.dumps(info, sort_keys=True, ensure_ascii=False, indent=2, separators=(',', ': '))
  with open(dummy_file, "w", encoding='utf8') as fh:
    fh.write(json_text)

def get_text(dict, elem):
  if elem in dict:
    return get_text2(dict[elem])
  else:
    return None

def get_text2(tag):
  if isinstance(tag, collections.OrderedDict):
    return get_text2(tag["#text"])
  elif isinstance(tag, list):
    return list(map(lambda x: get_text2(x), tag))
  else:
    return html.unescape(tag)

def generate_random_string():
  return ["*" + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(10)]) for j in range(100)]

def convert_json(file, index_hash, mecab_tag):
  xml_f = open(file, 'r')
  xml_content = xml_f.read()
  xml_f.close()
  xml_dict = xmltodict.parse(xml_content, encoding='utf-8')
  if not "error" in xml_dict["OAI-PMH"]:
    records = xml_dict["OAI-PMH"]["ListRecords"]["record"]
    info = {}
    for record in (records):
      if isinstance(record, collections.OrderedDict):
        record_header = record["header"]
        info["identifier"] = record["header"]["identifier"]
        info["set"] = get_text(record_header, "setSpec")
        record_body = record["metadata"]["junii2"]
        info["title"] = get_text(record_body, "title")
        info["dateofissued"] = get_text(record_body, "dateofissued")
        info["description"] = get_text(record_body, "description")
        info["index"] = str(index_hash.ix[info["set"], "StringIndex"])
        info["keywords"] = get_keywords(info, record_body)
        info["lexemes"] = parse_text(info, mecab_tag)
        puts_json(info)

def get_keywords(info, record_body):
  keywords = []
  # print(info["index"])
  indeces = info["index"].split(":")
  if len(indeces) > 1:
    keywords.append(":".join(indeces[0:1]).replace(" ", ""))
  if len(indeces) > 2:
    keywords.append(":".join(indeces[0:2]).replace(" ", ""))
  if len(indeces) > 3:
    keywords.append(":".join(indeces[0:3]).replace(" ", ""))
  add_keywords(keywords, record_body, "creator", "P:")
  add_keywords(keywords, record_body, "contributor", "O:")
  if "dateofissued" in record_body:
    keywords.append("Y:" + record_body["dateofissued"][0:4])
    keywords.append("M:" + record_body["dateofissued"][0:7])
  # print(keywords)
  return keywords

def add_keywords(keywords, record_body, key_name, prefix):
  nominates = get_text(record_body, key_name)
  if isinstance(nominates, list):
    for nominate in nominates:
      nominate = prefix + re.sub(r",\s*", "", nominate)
      keywords.append(nominate)
  elif nominates:
    nominate = prefix + re.sub(r",\s*", "", nominates)
    keywords.append(nominate)

def parse_text(info, mecab_tag):
  lexemes = []
  lexemes += parse_text2(info["title"], mecab_tag)
  lexemes += parse_text2(info["description"], mecab_tag)
  return lexemes

def concat_text(item):
  if isinstance(item, list):
    return " ".join(item)
  else:
    return item

def parse_text2(text, mecab_tag):
  if not text:
    return [];
  #text = mojimoji.han_to_zen(concat_text(text), digit=False)
  #text = mojimoji.zen_to_han(text, kana=False, ascii=False)
  text = concat_text(text).replace("　", " ")
  # print(text)
  lines = mecab_tag.parse(text).split("\n")
  # print(lines)
  lexemes = []
  for line in lines:
    # print(line)
    if line == "EOS" or line == "":
      continue
    words = re.split(r"[,\t]", line)
    if words[2] == "サ変接続" and words[7] == "*":
      pass # print("zz " + line)
    elif words[2] == "記号" or words[1] == "記号":
      pass
    #elif words[7][0:5] == "代表表記：":
    #  lexemes.append(words[7][6:])
    #elif words[5] != "*":
    #  lexemes.append(words[5])
    else:
      lexemes.append(words[0])
  # print(lexemes)
  return lexemes

# 解析結果をJSON出力
def puts_json(info):
  identifier = info["identifier"].split(":")[-1]
  json_file = "json/id_" + identifier + ".json"
  # print(json_file)
  json_text = json.dumps(info, sort_keys=True, ensure_ascii=False, indent=2, separators=(',', ': '))
  #print info["description"]
  #json_text = json.dumps(info, sort_keys=True, encoding="utf-8", indent=2, separators=(',', ': '))
  with open(json_file, "w", encoding='utf8') as fh:
    fh.write(json_text)

# Start up
if __name__ == '__main__':
  main(sys.argv)

 
