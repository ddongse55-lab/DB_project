from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def jonggeundang1(result):
    # 서버 차단을 방지하기 위해 브라우저인 척 헤더를 추가합니다.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    for page in range(1, 7):
        url = 'https://www.ckdhc.com/product/productList.do?r=CKD_CATE00000005&page=%d&category=CKD_CATE00000049&searchKeyword=' % page
        print(f"Crawling: {url}")

        try:
            # Request 객체를 생성하여 헤더를 포함시킵니다.
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req)
            soupSenior = BeautifulSoup(html, 'html.parser')

            # 제품 정보가 담긴 영역 선택
            senior_info = soupSenior.select('ul.search_result_list > li div.title_area')

            for info in senior_info:
                # select_one을 사용하여 첫 번째 a 태그를 찾습니다.
                anchor = info.select_one('a')
                if anchor:
                    # get_text(strip=True)로 앞뒤 공백을 제거합니다.
                    product_name = anchor.get_text(strip=True)
                    if product_name:
                        result.append([product_name])

        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue

    return


def main():
    result = []
    print('crawling >>>>>>>>>>>>>>>>>>>>>>\n')
    jonggeundang1(result)

    if result:
        senior_tbl = pd.DataFrame(result, columns=['name'])
        # 한글 깨짐 방지를 위해 utf-8-sig 권장
        senior_tbl.to_csv('senior.csv', encoding='utf-8-sig', index=False)
        print(f'\nCrawling finished. Saved {len(result)} items to senior.csv')
    else:
        print("\n수집된 데이터가 없습니다. HTML 구조나 연결을 확인하세요.")


if __name__ == '__main__':
    main()