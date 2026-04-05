from bs4 import BeautifulSoup
import urllib.request as MYURL

## 오류 무시 
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

fp = open('joins.xml', 'r', encoding='utf-8')
soup = BeautifulSoup(fp, 'html.parser')

# tag_item = soup.item
# print(tag_item.title.string)
# print(tag_item.description.string)

for data in soup.find_all('item'):
    print('title :', data.title.string)
    print('description :', data.description.string)
    print()





















