import os
from glob import glob
os.chdir('text')

from janome.tokenizer import Tokenizer
tokenaizer_instance = Tokenizer(wakati=True)


###
    #ニュースのファイル読み込み、リストに保存
###
news = []
#家電チャンネル読み込み
for file in glob('kaden-channel/*.txt'):
    with open(file,encoding="utf-8") as f:
        news.append(f.read())
# print(news[0])
l_kaden = len(news)
# print('家電チャンネル記事数：',l_kaden)



#スポーツウォッチ読み込み
for file in glob('sports-watch/*.txt'):
    with open(file,encoding="utf-8") as f:
        news.append(f.read())

# print('スポーツチャンネル記事数：',len(news)-l_kaden)

###
    #形態素解析
###
text_wakati = []
for tes in news:
    # print("=============================================")
    # print(tes)
    text_wakati.append([token for token in tokenaizer_instance.tokenize(tes)])

# print(text_wakati)
##
    #学習用データ準備
##
from gensim.models.doc2vec import TaggedDocument
cnt = 0
doc_train = []
for words in text_wakati:
    doc_train.append(TaggedDocument(words,[cnt]))
    cnt += 1

print(len(doc_train))
##
    #モデル作成
##
from gensim.models.doc2vec import Doc2Vec
model = Doc2Vec(doc_train,dm=1, vector_size=200, min_count=10, epochs=20)


##
    #評価
##
index = 1500
sims = model.docvecs.most_similar(index)
print(sims)

# print(news[index],'\n')
# print(doc_train[index])

for i in (sims):
    print(news[i[0]],'\n')
