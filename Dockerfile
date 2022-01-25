# python3.9のイメージをダウンロード
FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /src

RUN apt update
RUN apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8

# RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
#     ./mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y && \
#     sudo mv /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd /var/lib/mecab/dic/ && \
#     sed -i 's/debian/mecab-ipadic-neologd/' /etc/mecabrc && \
#     rm -rf ./mecab-ipadic-neologd && \
#     echo "完了"


#＠TODO: 辞書（mecab-ipadic-neologd）のインストールうまく動かないため保留しているが、ローカル開発環境作りたい。。。
# # 日本設定
# ENV TZ Asia/Tokyo
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# ENV LANG ja_JP.UTF-8

# RUN apt update -yqq && \
#     apt install -y --no-install-recommends \
#     build-essential curl ca-certificates \
#     file git locales sudo \
#     mecab libmecab-dev mecab-ipadic-utf8 && \
#     locale-gen ja_JP.UTF-8 && \
#     apt clean && \
#     rm -rf /var/lib/apt/lists/*


# # mecab-ipadic-neologdインストール
# RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
#     ./mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y && \
#     sudo mv /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd /var/lib/mecab/dic/ && \
#     sed -i 's/debian/mecab-ipadic-neologd/' /etc/mecabrc && \
#     rm -rf ./mecab-ipadic-neologd && \
#     echo "完了"



# pipを使ってpoetryをインストール＆アップデート
RUN pip install -U poetry

# poetryの定義ファイルをコピー (存在する場合)
COPY pyproject.toml* poetry.lock* ./

# poetryでライブラリをインストール (pyproject.tomlが既にある場合)
RUN poetry config virtualenvs.in-project false
RUN if [ -f pyproject.toml ]; then poetry install; fi

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]