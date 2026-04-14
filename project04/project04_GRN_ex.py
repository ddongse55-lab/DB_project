from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def grn_crawling(result):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    # GRN 50대 이상 카테고리 URL
    url = 'https://grnplus.co.kr/product/list.html?cate_no=402'
    print(f"Crawling: {url}")

    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, 'html.parser')

        # 제품 정보 리스트 영역 선택 (GRN은 보통 prdList grid4 또는 grid5 형태)
        product_items = soup.select('ul.prdList > li')

        for item in product_items:
            try:
                # 제품 이름이 들어있는 p.name 또는 span 태그 선택
                name_tag = item.select_one('p.name')
                if name_tag:
                    # '상품명 :' 이라는 텍스트가 같이 수집될 경우를 대비해 처리
                    product_name = name_tag.get_text(strip=True).replace('상품명 :', '')
                    if product_name:
                        result.append([product_name])
            except Exception as e:
                print(f"제품 추출 중 오류 발생: {e}")
                continue # 개별 제품 추출 실패 시 다음 제품으로 진행

    except Exception as e:
        print(f"페이지 접속 중 오류 발생: {e}")

    return

def main():
    result = []
    print('GRN crawling started >>>>>>>>>>>>>>>>>>>>>>\n')
    grn_crawling(result)

    if result:
        # 중복 제거 포함
        senior_tbl = pd.DataFrame(result, columns=['name']).drop_duplicates()
        senior_tbl.to_csv('senior2.csv', encoding='utf-8-sig', index=False)
        print(f'\nCrawling finished. Saved {len(senior_tbl)} items to senior2.csv')
    else:
        print("\n수집된 데이터가 없습니다. URL의 카테고리 번호(cate_no)나 HTML 구조를 확인하세요.")

if __name__ == '__main__':
    main()