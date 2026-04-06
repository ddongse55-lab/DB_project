import urllib.request
import datetime
import json
from config import *
import pymysql
import re       # 정규표현식 사용을 위해 import


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


def getPostData(post, jsonResult):
    title = post['title']
    description = post['description']
    bloggerlink = post['bloggerlink']
    link = post['link']
    postdate = post['postdate']
    bloggername = post['bloggername']

    jsonResult.append({'title': title, 'description': description,
                       'bloggerlink': bloggerlink, 'link': link,
                       'postdate': postdate, 'bloggername': bloggername})
    return

def connect_db():
    dbconn = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             db='tabledb',
                             charset='utf8')
    return dbconn

def save_DB(jsonResult):
    dbconn = connect_db()
    dbcursor = dbconn.cursor()
    dbcursor.execute('drop table if exists naver_blog')
    dbcursor.execute('''create table if not exists naver_blog(
                        id int auto_increment primary key,
                        title varchar(100),
                        bloggername varchar(50),
                        description varchar(500),
                        bloggerlink varchar(200),
                        link varchar(200),
                        postdate varchar(100));''')
    sql = 'insert into naver_blog (title, bloggername, description, bloggerlink, link, postdate) values (%s, %s, %s, %s, %s, %s)'
    for rec in jsonResult:
        try:
            dbcursor.execute(sql, (rec['title'], rec['bloggername'], rec['description'], rec['bloggerlink'], rec['link'], rec['postdate']))
        except:
            for reckey in rec:
                rec[reckey] = re.sub('[^가-힣0-9a-zA-Z<>&.?:/#\[\]\\s]', ' ', rec[reckey])
                dbcursor.execute(sql, (rec['title'], rec['bloggername'], rec['description'], rec['bloggerlink'], rec['link'], rec['postdate']))
    dbconn.commit()
    dbcursor.close()
    dbconn.close()

def main():
    jsonResult = []
    sNode = "blog"
    search_text = "엔트로픽"
    display_count = 100

    jsonSearch = getNaverSearchResult(sNode, search_text, 1, display_count)
    while ((jsonSearch != None) and (jsonSearch['display'] != 0)):
        for post in jsonSearch['items']:
            getPostData(post, jsonResult)

        if jsonSearch['display'] == display_count:
            break

    with open('%s_naver_%s.json' % (search_text, sNode), 'w', encoding='utf8') as outfile:
        retJson = json.dumps(jsonResult,
                             indent=4,
                             sort_keys=True,
                             ensure_ascii=False)
        outfile.write(retJson)

    print("%s_naver_%s.json SAVED" % (search_text, sNode))

    save_DB(jsonResult)
    print('DB SAVED')


if __name__ == "__main__":
    main()