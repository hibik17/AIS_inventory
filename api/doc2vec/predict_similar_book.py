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
from api.utils.text import replaceTextFromNewsText, convert_full_width_to_half_width


# @TODO: 全てreturn値や引数の型定義する
def predict_similar_book_by_news(news):
    text = news["title"] + news["summary"]
    # 準備
    model = Doc2Vec.load("api/doc2vec/d2v_ipsj_desc_0.model")
    mt = MeCab.Tagger("mecab-ipadic-neologd")

    lexemes = parse_text(text, mt)
    lexemes = lexemes[:30]
    print(lexemes)

    # モデルを使うときではなく、新しい文章のベクトルを図るもの
    # 単語なら不要、今まで出てきた単語の範囲で新しい文章のベクトルを予測する
    vector = model.infer_vector(lexemes, alpha=0.1, min_alpha=0.0001, steps=10)  #
    # positiveはニュースのコサイン類似度が高い1個出して、そのコサイン類似度の高い本を出力する
    nominates = model.docvecs.most_similar(positive=[vector], topn=1)

    for nominate in nominates:
        explanation_dict = get_explanation(nominate)

    return explanation_dict

def parse_text(text, mecab_tag):
    lexemes = []

    text = convert_full_width_to_half_width(text)
    print(text)

    for line in mecab_tag.parse(text).split("\n"):
        if line == "EOS" or line == "":
            continue
        words = re.split(r"[,\t]", line)
        # 助詞が重要ではない
        if words[2] == "サ変接続" and words[7] == "*":
            pass  # print("zz " + line)
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
    # @TODO: ここはID以外も可能性があるのか確認する
    if word[0:3] == "ID:":
        json_file = "api/json/id_" + word[3:] + ".json"
        # json_file = word[3:]
        with open(json_file, "r") as json_f:
            json_dict = json.load(json_f)
        explanation_dict = {
            "title": json_dict["title"],
            "author": json_dict["biblio_authors"],
            "description": json_dict["description"][0:150],
            "publisher": json_dict["biblio_publisher"][0:150],
            "published_year": json_dict["biblio_year_published"][0:150],
            "location": json_dict["biblio_location"][0:150],
            "isbn": json_dict["identifier"][0:150],
            "similarity": similarity,
        }
    return explanation_dict


# tt = "消される天安門事件の記憶。香港の大学、親中派が圧力。香港の大学で、民主化を求める学生らが北京で武力弾圧された1989年の天安門事件"
# predict_similar_book_by_news(tt)
