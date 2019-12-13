# coding: utf-8
import lxml.html
import requests
import re
import json
import os
import time

def get_page(page=1):
    """検索フォームの指定したページからすべての作品を取得する
    """
    url = "https://yomou.syosetu.com/search.php"
    params = {
        'search_type': 'novel',
        'order_former': 'search',
        'order': 'new',
        'notnizi': 1,
        'p': page
    }
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    r = requests.get(url, params=params, headers=headers)
    html = lxml.html.fromstring(r.text.encode())
    results = html.xpath("//div[@class='searchkekka_box']")
    return results


def get_index(link):
    """指定したURLにある目次からリンク一覧を取得する
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    r = requests.get(link, headers=headers)
    html = lxml.html.fromstring(r.text.encode())
    index = html.xpath("//div[@class='index_box']/dl[@class='novel_sublist2']")
    return index


def get_sentence(path):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    r = requests.get("https://ncode.syosetu.com/{}".format(path),
                     headers=headers)
    r.encoding = r.apparent_encoding
    html = lxml.html.fromstring(r.text.encode())
    lineList = html.xpath("//div[@class='novel_view']/p")

    text = ""
    for line in lineList:
        textList = line.xpath("text()")
        sentence = ""
        if len(textList) == 0:
            # 改行
            continue
        elif len(textList) == 1:
            sentence = textList[0].strip()
        else:
            # ルビに対応
            ruby = line.xpath("ruby/rb/text()")
            if len(ruby) != len(textList) - 1:
                if len(textList) == 2:
                    sentence = textList[0] + ''.join(ruby) + textList[1]
                else:
                    print("[Error] Unknown pattern detected :(")
                    print(path)
                    print(textList)
                    print(ruby)
                    print("Reverting changes...")
                    return False
            else:
                sentence = ""
                for i in range(len(ruby)):
                    sentence += textList[i].strip() + ruby[i].strip()
                else:
                    sentence += textList[-1].strip()
        text += sentence + "\n"
    
    return text


def get_main(link):
    """指定したURLにある小説をテキストとしてすべて取得する
    """
    for index in get_index(link):
        path = index.xpath("dd[@class='subtitle']/a/@href")[0]
        yield get_sentence(path)


def retrieve(result, path="database"):
    """1つの結果から本文およびメタ情報を取得する
    """
    ncode = re.findall("：([A-Z0-9]+)", result.xpath("text()")[3])[0]
    elm = result.xpath("table/tr/td[position()=1]/text()")
    attribute = ''.join(elm).strip()
    main = result.xpath("table/tr/td")[1]
    textList = result.xpath("table/tr/td/text()")
    category = re.findall('〔(.+)〕', ''.join(textList))[0]

    if attribute == '短編':
        return None
    
    # Get title and link
    elm = result.xpath("div[@class='novel_h']/a[@class='tl']")[0]
    link = elm.xpath("@href")[0]
    title = elm.text
    
    # Get abstract
    abstract = main.xpath("div[@class='ex']")[0].text

    # Get category and tags
    elmList = main.xpath("a[contains(@href, 'search.php')]")
    tagList = []
    for elm in elmList:
        tagList.append(elm.text)
    genre = tagList[0]
    tags = tagList[1:]

    # Get score
    elm = main.xpath("span[@class='attention']")[0].text
    total_point = int(re.findall("[\d\,]+", elm)[0].replace(",", ""))
    elm = main.xpath("span[@class='marginleft']")
    number = int(re.findall("[\d\,]+", elm[2].text)[0].replace(",", ""))
    point = int(re.findall("[\d\,]+", elm[3].text)[0].replace(",", ""))

    data = {
        'title': title,
        'ncode': ncode,
        'attribute': attribute,
        'abstract': abstract,
        'category': category,
        'genre': genre,
        'tag': tags,
        'score': {
            'total': total_point,
            'count': number,
            'point': point
        }
    }
    savepath = os.path.join(path, "{}.txt".format(ncode))
    if os.path.exists(savepath):
        print("Already taken: {}".format(ncode))
        return None
    with open(savepath, "w") as f:
        # Write meta
        f.write(json.dumps(data) + "\n")
        
        # Write main sentence
        for sentence in get_main(link):
            if sentence == False:
                # Unknown Error
                os.unlink(os.path.join(path, "{}.txt".format(ncode)))
                break
            else:
                f.write(sentence)

    return title

if __name__ == '__main__':
    for page in range(100, 0, -1):
        results = get_page(page)
        for r in results:
            try:
                title = retrieve(r)
            except:
                continue
            if title:
                print("Saved: {}".format(title))
                time.sleep(10)
