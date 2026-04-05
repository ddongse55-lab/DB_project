## [문제] 벅스 뮤직의 벅스차트에서 입력받은 날짜에 대한 일간 순위를 크롤링하여 파일로 저장하는 프로그램을 작성하시오.

## <처리조건>
# 1. 저장할 파일명: bugschart_입력날짜.csv 예) bugschart_20260402
# 2. 입력날짜(search_day),랭킹(rank), 가수이름(singer), 곡타이틀(title) 형식으로 파일에 출력한다.
# 3. 입력 가능한 날짜는 2006년09월22일 부터 현재날짜 하루전까지이며 입력형식은 다음 예시와 같다. 예) 20260402

# bs4
from bs4 import BeautifulSoup
import pandas as pd

# selenium
from selenium import webdriver
import time

# 날짜 계산을 위한 모듈
from datetime import datetime, timedelta


def date_limit():
    """조건 3번: 2006.09.22 ~ 어제 날짜까지의 범위를 체크하는 함수"""
    # 시작 기준일 설정
    start_date = datetime(2006, 9, 22)
    # 현재 시간에서 1일을 빼서 '어제' 날짜 생성
    yesterday = datetime.now() - timedelta(days=1)
    # 비교를 위해 시, 분, 초 정보를 자정(00:00:00)으로 초기화
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    while True:
        try:
            date = int(input('날짜를 입력하세요 (ex.20260402) : '))

            # 유효성 검사를 위해 문자열로 변환 후 datetime 객체 생성
            date_str = str(date)
            input_date = datetime.strptime(date_str, '%Y%m%d')

            # 범위 체크
            if input_date < start_date:
                print("[오류] 2006년 09월 22일 이후의 날짜를 입력해 주세요.\n")
            elif input_date > yesterday:
                print(f"[오류] {yesterday.strftime('%Y%m%d')}까지만 조회가 가능합니다. (오늘 기준 하루 전)\n")
            else:
                # 모든 조건을 만족하면 정수형 날짜 반환
                return date

        except ValueError:
            print("[오류] 올바른 날짜 형식이 아닙니다. 8자리 숫자로 입력해주세요.\n")


def bugs_chart(result):
    # 날짜 입력을 위해 date_limit() 함수 호출
    date = date_limit()
    bugs_url = 'https://music.bugs.co.kr/chart/track/day/total?chartdate=%d' % date

    wd = webdriver.Chrome()
    wd.get(bugs_url)
    time.sleep(2)
    html = wd.page_source
    soupBugs = BeautifulSoup(html, 'html.parser')

    # 실제 차트의 정보가 담긴 행 찾기
    chart_info = soupBugs.select('table.list.trackList.byChart > tbody > tr')
    print('\n\t\t\t\t★오늘의 랭킹( %d )★' % date)
    for track in chart_info:
        try:
            # 랭킹 추출
            rank = track.select_one('td > div.ranking > strong').text.strip()
            # 곡 타이틀 추출
            title = track.select_one('th > p.title > a').text.strip()
            # 가수 이름 추출
            singer = track.select_one('td > p.artist > a').text.strip()
            # 추출 결과를 리스트에 추가
            result.append([date, rank, singer, title])
            print('랭킹(순위) :', [rank], ', 가수 이름 :', [singer], ', 곡 타이틀 :', [title])
        except:
            continue
    wd.quit()
    return date     # 파일명을 위해 날짜 반환


def main():
    result = []
    print('Bugs chart crawling >>>>>>>>>>>>>>>>>>>>>>\n')
    # 날짜 받기
    search_day = bugs_chart(result)

    if result:
        # 데이터프레임 생성
        bugs_chart_tbl = pd.DataFrame(result, columns=('search_day', 'rank', 'singer', 'title'))
        # 파일명 설정
        file_name = f'bugs_chart_{search_day}.csv'
        # 저장
        bugs_chart_tbl.to_csv(file_name, encoding='utf-8', mode='w', index=False)
        print('\n저장 완료 :', file_name)
    else:
        # 해당 데이터가 없을 경우 출력
        print('\n데이터를 찾지 못했습니다.\n날짜를 확인해주세요.')

    del result[:]



if __name__ == '__main__':
    main()

