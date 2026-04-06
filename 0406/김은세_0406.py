import pandas as pd
import urllib.request
import datetime
import json
from config import *


def get_request_url(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def getNaverSearchResult(sNode, search_text, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % sNode
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(search_text),
                                                    page_start, display)

    url = base + node + parameters

    retData = get_request_url(url)

    if (retData == None):
        return None
    else:
        return json.loads(retData)


def getNewsData(news, jsonResult):
    title = news['title']
    description = news['description']
    originallink = news['originallink']
    link = news['link']
    pubDate = news['pubDate']

    jsonResult.append({'title': title, 'description': description,
                       'originallink': originallink, 'link': link,
                       'pubDate': pubDate})
    return


def main():
    jsonResult = []
    sNode = "news"
    search_text = input('검색 키워드 입력 => ')
    display_count = 100

    jsonSearch = getNaverSearchResult(sNode, search_text, 1, display_count)
    while ((jsonSearch != None) and (jsonSearch['display'] != 0)):
        for news in jsonSearch['items']:
            getNewsData(news, jsonResult)

        if jsonSearch['display'] == display_count:
            break

    # 데이터프레임 생성
    naver_news_tbl = pd.DataFrame(jsonResult, columns=('title', 'description', 'originallink', 'link', 'pubDate'))
    # 파일명 설정
    file_name = f'{search_text}_naver.csv'
    # 저장
    naver_news_tbl.to_csv(file_name, encoding='utf-8', mode='w', index=False)
    print('\n저장 완료 :', file_name)



if __name__ == "__main__":
    main()








