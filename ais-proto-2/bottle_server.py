# -*- coding:utf-8 -*-
"""
d2vdのHTTPサーバクラス。Bottleのラッパクラスとして実装。
"""

from bottle import Bottle
from bottle import static_file
from bottle import get, post, request, template
import json

class BottleServer:
    def __init__(self, model, host, port, reloader = False):
        """
        クラスの初期化。引数の保持および、ルートの設定。
        """
        self._model = model
        self._host = host
        self._port = port
        self._reloader = reloader
        self._app  = Bottle()
        self._route()

    def _route(self):
        """
        ルート（アクセスされたパスと呼び出すメソッドの関係）を設定。文法はBottle参照。
        """
        self._app.route('/search', method="GET", callback=self._search)
        self._app.route('/search_words', method="GET", callback=self._search_words)
        self._app.route('/newpaper/<description>', callback=self._newpaper)
        self._app.route('/semantic/dist/:path#.+#', name='semantic/dist', callback=self._semantic)
        self._app.route('/tabulator/dist/:path#.+#', name='tabulator/dist', callback=self._tabulator)
        self._app.route('/javascript/<script>', callback=self._tsne)
        self._app.route('/presentation/<ppt_file>', callback=self._presentation)

    def start(self):
        """
        Bottleサーバの開始。
        """
        self._app.run(host=self._host, port=self._port, reloader = self._reloader)

    def _search(self):
        """
        初期画面の生成。パラメタがあるときは画面に反映してからテンプレート出力。
        """
        positive_words = request.query.positive_words
        negative_words = request.query.negative_words
        outline_area   = request.query.outline_area
        if request.query.output_types == '':
          output_types = ["article"]
        else:
          output_types = request.query.output_types.split(" ")
        if request.query.output_formats == '':
          output_formats = ["list"]
        else:
          output_formats = request.query.output_formats.split(" ")
        if request.query.model_type == '':
          model_type = "dbow"
        else:
          model_type = request.query.model_type
        print(output_types)
        params = self._set_params(positive_words, negative_words, output_types, output_formats, model_type)
        return template("ipsj_search", params=params)

    def _search_words(self):
        """
        指定された（複数）単語と類似の情報をモデルから検索。
        """
        print(request.query.__dict__)
        positive_words = request.query.positive_words
        negative_words = request.query.negative_words
        outline_area   = request.query.outline_area
        if request.query.output_types == '':
          output_types = ["article"]
        else:
          output_types = request.query.output_types.split(" ")
        print(output_types)
        model_type = request.query.model_type
        result = self._model.search(positive_words, negative_words, outline_area, output_types, model_type)
        print(result["message"])
        return json.dumps(result)

    def _newpaper(self, description):
        """
        指定された文章と類似の情報をモデルから検索。
        """
        result = self._model.search_paper(description)
        return json.dumps(result)

    # Semantic UI & Tabulator resources
    def _semantic(self, path):
        """
        SemanticUIのJavascriptをダウンロード
        """
        print(path)
        return static_file(path, root='semantic/dist')

    def _tabulator(self, path):
        """
        TabulatorのJavascriptをダウンロード
        """
        print(path)
        return static_file(path, root='tabulator/dist')

    def _tsne(self, script):
        """
        tsne.jsのJavascriptをダウンロード
        """
        return static_file(script, root = 'javascript')

    def _presentation(self, ppt_file):
        """
        ドキュメント(PPT)をダウンロード
        """
        print(ppt_file)
        return static_file(ppt_file, root = 'presentation')

    def _set_params(self, positive_words, negative_words, output_types, output_formats, model_type):
        """
        パラメタを格納したディクショナリの作成
        """
        params = {}
        params["positive_words"] = positive_words
        params["negative_words"] = negative_words
        # params["input_types"] = input_types
        params["output_types"] = output_types
        params["output_formats"] = output_formats
        params["model_type"] = model_type
        return params
