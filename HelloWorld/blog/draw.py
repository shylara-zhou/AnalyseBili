# 导入扩展库
import re                           # 正则表达式库
import jieba.posseg                 # 词性获取
import collections                  # 词频统计库
import matplotlib.pyplot as plt     # 图像展示库（这里以plt代表库的全称）
from pylab import mpl
import requests
import json
import chardet
import re
from wordcloud import WordCloud
from pprint import pprint



#  1.根据bvid请求得到cid
def get_cid(bvid):
    final_url = "https://www.bilibili.com/video/"+bvid+"?spm_id_from=333.851.b_7265706f7274466972737431.8"
    final_res = requests.get(final_url)
    final_res.encoding = chardet.detect(final_res.content)['encoding']
    final_res = final_res.text
    pattern1 = re.compile('stat\":\{\"aid.*"argue_msg"')
    data = pattern1.findall(final_res)
    str =data[0]
    str = str.split(':')
    view=str[3].split(',"')[0]
    danmu=str[4].split(',"')[0]
    reply=str[5].split(',"')[0]
    favorite = str[6].split(',"')[0]
    coin =str[7].split(',"')[0]
    share = str[8].split(',"')[0]
    like=str[11].split(',"')[0]
    dislike=str[12].split(',"')[0]
    data[0] ='观看'+view+'    弹幕'+danmu+'    回复'+reply+'\n'+'    喜欢='+like+'    讨厌='+dislike+ '    收藏=' + favorite + '    硬币=' + coin + '    分享=' + share
    with open("./blog/favorite.txt", mode="w", encoding="utf-8") as f:
        for i in data:
            f.write(i)
            f.write("\n")
    f.close()
    url = "https://api.bilibili.com/x/player/pagelist?bvid={0}&jsonp=jsonp".format(bvid)
    res = requests.get(url).text
    json_dict = json.loads(res)
    # pprint(json_dict)
    return json_dict["data"][0]["cid"]


#  2.根据cid请求弹幕，解析弹幕得到最终的数据
"""
注意：哔哩哔哩的网页现在已经换了，那个list.so接口已经找不到，但是我们现在记住这个接口就行了。
"""


def get_data(cid):
    final_url = "https://api.bilibili.com/x/v1/dm/list.so?oid=" + str(cid)
    final_res = requests.get(final_url)
    final_res.encoding = chardet.detect(final_res.content)['encoding']
    final_res = final_res.text
    pattern = re.compile('<d.*?>(.*?)</d>')
    data = pattern.findall(final_res)
    # pprint(final_res)
    return data


#  3.保存弹幕列表
def save_to_file(data):
    with open("./blog/dan_mu.txt", mode="w", encoding="utf-8") as f:
        for i in data:
            f.write(i)
            f.write("\n")
    f.close()


def draw(bvid):
    cid = get_cid(bvid)
    data = get_data(cid)
    save_to_file(data)

    with open("./blog/dan_mu.txt", encoding="utf-8")as file:
        # 1.读取文本内容
        text = file.read()
        # 2.设置词云的背景颜色、宽高、字数
        wordcloud = WordCloud(font_path="/usr/fonts/SIMFANG.TTF",
                              background_color="white", width=600,
                              height=500, max_words=80).generate(text)
        # 3.生成图片
        image = wordcloud.to_image()
        # 4.显示图片
        image.save('./static/imges/1.jpg')

