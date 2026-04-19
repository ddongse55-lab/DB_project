import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def SearchNaverBlog(result):
    keyword = input('검색 키워드 입력 : ').strip()

    # 브라우저 설정 (크롬)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 10개 이상 수집을 위해 페이지 반복
        for page in range(1, 3):
            url = f'https://section.blog.naver.com/Search/Post.naver?pageNo={page}&rangeType=ALL&orderBy=sim&keyword={keyword}'
            driver.get(url)
            time.sleep(2)  # 페이지 로딩 대기

            # 블로그 포스트 아이템들 찾기
            items = driver.find_elements(By.CSS_SELECTOR, "div.info_post")

            for item in items:
                # 1. 제목 추출 (span.title 태그 내부의 텍스트)
                title_element = item.find_element(By.CSS_SELECTOR, "span.title")
                title = title_element.text

                # 2. 링크 추출 (수정된 부분: 제목을 감싸고 있는 a 태그의 href 가져오기)
                # .desc_inner 클래스를 가진 a 태그가 실제 블로그 주소를 담고 있습니다.
                try:
                    link_element = item.find_element(By.CSS_SELECTOR, "a.desc_inner")
                    link = link_element.get_attribute('href')
                except:
                    # 만약 위 코드로 실패할 경우, 부모 태그 중 a 태그를 직접 찾음
                    link = item.find_element(By.XPATH, ".//a").get_attribute('href')

                # 결과 리스트에 추가
                result.append([title, link])

                # 화면 출력 형식 준수
                print(f"제목: {title}")
                print(f"링크: {link}")
                print("-" * 32)

                # 10개 이상 수집 시 즉시 반환
                if len(result) >= 10:
                    return keyword

    finally:
        driver.quit()

    return keyword


def main():
    result = []
    keyword = SearchNaverBlog(result)

    # 결과 저장
    if result:
        # 정확히 10개만 저장
        df = pd.DataFrame(result[:10], columns=['제목', '링크'])
        file_path = f'naver_{keyword}.csv'

        # utf-8-sig로 저장해야 엑셀에서 한글이 깨지지 않습니다.
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f'\n[시스템] {file_path} 파일 저장 완료.')
    else:
        print("\n[시스템] 검색 결과가 없어 파일을 저장하지 못했습니다.")


if __name__ == '__main__':
    main()