import re

# ニュースのデータから 空白や、 「12/30 21:38更新」のような文字を取り除く
def replaceTextFromNewsText(text):
    # 全角空白を半角空白にする
    text = convert_full_width_to_half_width(text)

    # 12/30 21:38更新」のような文字を取り除く
    regular_expression = r"\s\d+/+\d+\s\d+:\d+\w{2}"
    shouldReplaceText = re.search(regular_expression, text)
    if shouldReplaceText:
        text = re.sub(regular_expression, " ", text)

    return text

def convert_full_width_to_half_width(text):
    return text.replace("　", " ")
