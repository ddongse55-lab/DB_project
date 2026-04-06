from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import requests
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

serviceKey = '7c29473aa56ce5ab79bf2dfa46eb89dba1475649113840cf15c381203cdb924a'
YM = '202206'

URL = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
URL += '?serviceKey=' + serviceKey
URL += '&YM=' + YM
print(URL)

response = requests.get(URL)
soup = BeautifulSoup(response.content.decode(encoding='UTF-8', errors='strict'), 'html.parser')

print(soup.prettify())
for item in soup.find_all('item'):
    print('ed:', item.ed.string)
    print('edCd:',item.edcd.string)
    print('natCd:', item.natCd.string)
    print('natKorNm', item.natKorNm.string)
    print('num:', item.num.string)
    print('rnum:', item.rnum.string)
    print('ym:', item.ym.string)
    print('---------------------------------')











