from pathlib import Path

import io
import json
from boto3.session import Session
from api.utils.text import replaceTextFromNewsText, convert_full_width_to_half_width


import api.settings as settings

session = Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID,
)
s3_bucket = "crawling-news-bucket"

# @TODO:全体的に関数分けてリファクタしたい
def fetch_updated_news_data_from_s3(limit):
    s3 = session.resource("s3")
    bucket = s3.Bucket(s3_bucket)

    # ファイルリストオブジェクトを作成
    objs = bucket.meta.client.list_objects_v2(Bucket=bucket.name)
    # ディレクトリ配下のファイルについてLOOP処理
    loop_first_f = True
    for o in objs.get("Contents"):
        # LOOP初回処理
        if loop_first_f:
            download_target_file = o.get("Key")
            modified_datetime_mid = o.get("LastModified")
            loop_first_f = False
        # 2回目以降
        else:
            # 最新更新日時のファイルにターゲットを移動する
            if modified_datetime_mid <= o.get("LastModified"):
                modified_datetime_mid = o.get("LastModified")
                download_target_file = o.get("Key")

    try:
        # S3からファイルのbodyを取得
        obj = bucket.Object(download_target_file)
        body = obj.get()["Body"].read()
        news_data = json.loads(body.decode("utf-8"))
        print(f"download {download_target_file} is completed.")

        crawled_at = download_target_file[:-5]

        result = convert_news_to_correct_schema(news_data, limit, crawled_at)

        return result

    except Exception:
        print(f"download {download_target_file} is failed.")


def convert_news_to_correct_schema(news_data, limit, crawled_at):
    news_array = []

    for num in range(limit):
        news = news_data["news" + str(num)]
        news_dict = {
            "title": replaceTextFromNewsText(news["title"]),
            "summary": convert_full_width_to_half_width(news["summary"]),
            "url": news["link"],
            "crawled_at": crawled_at,
        }
        news_array.append(news_dict)

    return news_array


def make_news_for_demo():
    crawled_at = "2022年01月06日06時13分44秒"
    news_data = {
        "news0": {
            "title": "デモ暴徒化　カザフに“平和維持部隊”派遣　1/6 15:03更新",
            "summary": "中央アジア・カザフスタンで、燃料価格引き上げに抗議するデモが一部暴徒化するなどの事態を受け、ロシアが主導する軍事同盟は６日、カザフスタンに部隊を派遣すると発表しました。",
            "link": "http://www.news24.jp/articles/2022/01/06/101007951.html",
        },
        "news1": {
            "title": "「消費動向調査」１年後“物価上昇見込む”　1/5 16:05更新",
            "summary": "内閣府は消費者の心理を示す１２月の「消費動向調査」の結果を５日、公表。調査では、２人以上世帯の消費者に１年後の物価見通しを調べています。それによる、物価が「上昇する」と見込む割合は、前月比０．９ポイント高の８８．５％へ増加していました。",
            "link": "http://www.news24.jp/articles/2022/01/05/061007137.html"
        },
         "news2": {
            "title": "原発再稼働も　経験者枯渇の実態　1/3 20:00更新",
            "summary": "原発は今、脱炭素の流れを追い風に、再び一定のポジションを確保しつつある。そんな中、大きな課題のひとつとされるのが社員たちの「経験不足」である。中国電力では原発の運転を経験したことがない発電所員の割合は、約４割にまでのぼっているという─。",
            "link": "http://www.news24.jp/articles/2022/01/03/071005747.html"
        },
        "news3": {
            "title": "松野長官　北発射は“新型の弾道ミサイル”　1/6 14:54更新",
            "summary": "５日に北朝鮮が発射したミサイルについて、松野官房長官は分析の結果、新型の弾道ミサイルだったとした上で、北朝鮮に抗議したことを明らかにしました。",
            "link": "http://www.news24.jp/articles/2022/01/06/041007943.html",
        },
        "news4": {
            "title": "また発射…北朝鮮、「食糧難」解消が狙い？　1/6 9:19更新",
            "summary": "北朝鮮が５日、弾道ミサイルとみられる飛翔体を発射しました。国際社会からの経済制裁で厳しい状況にある北朝鮮は、なぜミサイル発射を繰り返すのでしょうか。背景を探るヒントは、現地のテレビが報じた黒い鳥、コクチョウにありました。",
            "link": "http://www.news24.jp/articles/2022/01/06/101007730.html",
        },
        "news5": {
            "title": "経済３団体トップら　景気回復の課題に見解　1/6 0:33更新",
            "summary": "経団連、日商、経済同友会の経済３団体のトップらが会見し、景気回復の課題について見解を示しました。オミクロン株への対応や「したたかな外交」について言及しています。",
            "link": "http://www.news24.jp/articles/2022/01/06/061007553.html",
        },
        "news6": {
            "title": "米「飛翔体は弾道ミサイル」北朝鮮を非難　1/5 23:54更新",
            "summary": "北朝鮮が５日に発射した飛翔体について、アメリカのインド太平洋軍は「弾道ミサイル」だとの認識を示した上で、発射を非難しました。",
            "link": "http://www.news24.jp/articles/2022/01/05/101007530.html",
        },
        "news7": {
            "title": "カザフスタン非常事態宣言　燃料高騰で衝突　1/5 21:13更新",
            "summary": "中央アジア・カザフスタンでは、燃料価格の高騰に抗議するデモが各地に広がっています。最大都市アルマトイでは、デモ隊と警官隊の衝突で１９０人が負傷するなどしたため、大統領が５日、非常事態宣言を出しました。",
            "link": "http://www.news24.jp/articles/2022/01/05/101007443.html",
        },
        "news8": {
            "title": "賃上げ、景気は…？ワタミ・渡辺会長に聞く　1/5 20:42更新",
            "summary": "ことし日本経済はコロナ禍から脱却できるのか？　景気回復の「キーワード」と賃上げについて、５日、ワタミの渡辺美樹会長兼社長が日本テレビの取材に答えた。",
            "link": "http://www.news24.jp/articles/2022/01/05/061007427.html",
        },
        "news9": {
            "title": "“文通費見直し”自民が各党に協議呼びかけ　1/5 19:05更新",
            "summary": "国会議員に月額１００万円が支給される文書通信交通滞在費の見直しをめぐり、自民党の茂木幹事長は、各党との協議の枠組みを立ち上げたいとの考えを明らかにしました。",
            "link": "http://www.news24.jp/articles/2022/01/05/041007301.html",
        },
            "news10": {
            "title": "韓国大統領選の構図変化…尹候補“出直し”　1/5 16:12更新",
            "summary": "韓国の大統領選挙で支持率が急落している最大野党の尹錫悦候補は５日、選挙対策チームをいったん解体して出直しを図ると表明しました。若者の支持率では３番手に後退し、およそ２か月後に迫った選挙戦の構図が変わりつつあります。",
            "link": "http://www.news24.jp/articles/2022/01/05/101007146.html"
        },
    }
    
    result = convert_news_to_correct_schema(news_data, 11, crawled_at)
    
    return result

