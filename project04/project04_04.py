from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def jonggeundang1(result):
    for page in range(1, 7):
        url = 'https://www.ckdhc.com/product/productList.do?r=CKD_CATE00000005&page=%d&category=CKD_CATE00000049&searchKeyword=' % page
        print(url)
        html = urllib.request.urlopen(url)
        soupSenior = BeautifulSoup(html, 'html.parser')

        senior_info = soupSenior.select('ul.search_result_list > li > div.title_area')
        for info in senior_info:
            # select_one을 사용하여 첫 번째 a 태그를 찾습니다.
            anchor = info.select_one('a')
            if anchor:
                # get_text(strip=True)로 앞뒤 공백을 제거합니다.
                product_name = anchor.get_text(strip=True)
                if product_name:
                    result.append([product_name])
    return

def main():
    result = []
    print('crawling >>>>>>>>>>>>>>>>>>>>>>\n')
    jonggeundang1(result)
    senior_tbl = pd.DataFrame(result, columns=['name'])
    senior_tbl.to_csv('senior.csv', encoding='utf-8', mode='w', index=False)
    print(f'\nCrawling finished. Saved {len(result)} items to senior.csv')
    del result[:]


if __name__ == '__main__':
    main()


