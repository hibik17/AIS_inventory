#!/usr/bin/python
# coding: UTF-8

import sys
import re
import json
import MeCab
import pandas as pd
import glob
import pprint
from get_google_biblio_data import get_biblio_isbns
from get_google_biblio_data import get_df_biblio

# Main procedure
def main(argv):
    biblio_dir = "./google_biblio_data"  
    json_dir = "./json"
    # ハードコーディングしてる
    df = get_df_biblio()
    isbns = get_biblio_isbns(df)
    for isbn_code in isbns:
        filename = "%s/id_%s.json" % (biblio_dir, isbn_code)
        book_summary = get_book_summary(filename)
        if book_summary:
            authors = get_authors(book_summary)
            # 形態素解析
            text_lexemes = get_segmented_text(book_summary)
            workfilename = "%s/id_%s.json" % (json_dir, isbn_code)
            book_title = book_summary["title"]
            book_description = book_summary["description"]
            biblio_info = df.loc[isbn_code]
             
            # 分割したものをまとめる
            put_workfile(isbn_code, book_title, book_description, biblio_info, workfilename, authors, text_lexemes)

def get_authors(book_summary):
    authors = []
    for item in book_summary["items"]:
        authors.extend(item["authors"])
    return authors

# 解析結果をJSON出力
def put_workfile(isbn_code, title, description, biblio_info, filename, authors, text_lexemes):
    # print(type(information_id).__name__)
    info = {}
    info["identifier"] = isbn_code
    info["title"] = title
    info["description"] = description
    info["lexemes"] = text_lexemes

    info["biblio_location"] = get_biblio_string(biblio_info, "所在名称")
    info["biblio_publisher"] = get_biblio_string(biblio_info, "出版社")
    info["biblio_year_published"] = get_biblio_string(biblio_info, "出版年")
    info["biblio_authors"] = get_biblio_string(biblio_info, "著者名")
    info["keywords"] = []
    # info["keywords"] = ["P:" + author for author in authors]
    # 図書館の中の配置図が抜けている
    json_text = json.dumps(info, sort_keys=True, ensure_ascii=False, indent=2, separators=(',', ': '))
    with open(filename, "w", encoding='utf8') as fh:
        fh.write(json_text)

def get_biblio_string(biblio_info, col_name):
    item = biblio_info[col_name]
    if isinstance(item, str):
        biblio_string = item
    elif type(item).__name__ == "Series":
        uniq_str_elem = [str(i) for i in set(item)]
        biblio_string = ",".join(uniq_str_elem)
        # print(biblio_string)
    elif pd.isna(item):
        biblio_string = ""
    else:
        print(item)
        quit()
    return biblio_string

def get_segmented_text(book_summary):
    # 単語分割している
    mecab_tag = MeCab.Tagger('mecab-ipadic-neologd')
    lexemes = []
    for item_summary in book_summary["items"]:
        # 分割された単語＝語彙素に分ける
        if "description" in item_summary:
            lexemes += parse_text(item_summary["description"], mecab_tag)
        else:
            lexemes += parse_text(item_summary["title"], mecab_tag)
            if "subtitle" in item_summary:
                lexemes += parse_text(item_summary["subtitle"], mecab_tag)
    return lexemes

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

def get_book_summary(filename):
    book_summary = {}
    book_summary["items"] = []
    # 形態素解析のために使っているために表示するのではなく結果表示として必要
    with open(filename) as f:
        df = json.load(f)
        # for i in range(df["totalItems"]):
        if "items" not in df:
            return None
        book_description = []
        for item in df["items"]:
            item_summary = {}
            # item-summary 一つの本だけどISBNが複数ある。
            volume_info = item["volumeInfo"]
            if "authors" in volume_info:
                item_summary["authors"] = volume_info["authors"]
                # print("Authors: %s" % (", ".join(volume_info["authors"])))
            else:
                item_summary["authors"] = []
            #    pprint.pprint(volume_info)
            #    quit()
            item_summary["title"] = volume_info["title"]
            # print("Title: %s" % volume_info["title"])
            if "subtitle" in volume_info:
                item_summary["subtitle"] = volume_info["subtitle"]
                # print("Subtitle: %s" % volume_info["subtitle"])
            if "description" in volume_info:
                item_summary["description"] = volume_info["description"]
                book_description.append(item_summary["description"])
                # print("Description: %s" % volume_info["description"])
            book_summary["items"].append(item_summary)
        book_title = ", ".join([item["title"] for item in book_summary["items"]])
        book_summary["title"] = book_title
        book_summary["description"] = ", ".join(book_description)
    return book_summary

# Start up
if __name__ == '__main__':
    main(sys.argv)