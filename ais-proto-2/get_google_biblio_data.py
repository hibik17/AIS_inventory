#!/usr/bin/python
# coding: UTF-8

import sys
import json
import pandas as pd
import requests
import os
import time

# 学術情報課からもらったTSVからISBNを取り出し、Google Booksから情報を取得する。
# 失敗することがあるため、失敗分について3回リトライしている。
def main(argv):
  max_retry = 3
  df = get_df_biblio()
  isbns = get_biblio_isbns(df)
  for i in range(max_retry):
    isbns = get_biblio_data_from_google(isbns, i)
    if len(isbns) == 0: # 全部成功した場合は抜ける。
      break
  if len(isbns) > 0:
    print("Failed to get isbns:", isbns)

# 学術情報課からもらった、TSVデータを読み込み、ISBN欠損データを除き、リスト化する
def get_biblio_isbns(df):
  isbns = [key for key in df.index if not pd.isna(key)]
  return isbns

def get_df_biblio():
  return pd.read_csv( './相1F300.txt',  delimiter='\t', index_col='ISBN/ISSN', encoding="cp932" )



# 与えられたISBNをキーにGoogle Bookの情報をJSON形式で得て格納する。失敗したISBNをリストにして返却する。
def get_biblio_data_from_google(isbns, retry_count):
  failed_isbns = []
  success_count = 0
  skip_count = 0
  failure_count = 0
  for isbn_code in isbns:
    # Googleから持ってきたデータをファイルからjsonに格納するファイル
    json_file = "google_biblio_data/id_%s.json" % isbn_code
    # ファイルがあったらデータを格納しない。ディレクトリのパス関連を扱う
    if not os.path.isfile(json_file):
      rq = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:%s' % isbn_code)
      if rq.status_code == 200:
        json_text = rq.text
        with open(json_file, "w", encoding='utf8') as fh:
          fh.write(json_text)
        time.sleep(0.01)
        success_count += 1
      else:
        print("Error: %d" % rq.status_code)
        failed_isbns.append(isbn_code)
        failure_count += 1
    else:
      skip_count += 1
  print("Retry count: %d, success: %d, skip: %d, fail: %d" % (retry_count, success_count, skip_count, failure_count))
  return failed_isbns

# Start up
if __name__ == '__main__':
  main(sys.argv)