# Inventory_inspection_application


## ローカル環境開発のセットアップ 

１，docker 及び docker-compose のインストール

https://docs.docker.jp/compose/install.html

２，docker でのビルド、コンテナー立ち上げ

```
$ docker-compose build

$ docker-compose up
...
start Uvicorn running on http://0.0.0.0:8000...
```


３, API仕様書を確認。こちらを元にフロントエンド開発。

http://localhost:8000/docs#/



４， (現在はoptional)DBのマイグレーション
```
$ docker-compose exec app poetry run python -m api.migrate_db
```


### doc2vecのテスト動作
```
$ docker-compose exec app poetry run python doc2vec/index.py
```

### figma(プロトタイプ)

[こちら](https://www.figma.com/file/H0VYuqLH1hPPNQjrWU2knl/AIS-inventory-product?node-id=0%3A1)からfigmaで、プロトタイプの確認を行なってください。



