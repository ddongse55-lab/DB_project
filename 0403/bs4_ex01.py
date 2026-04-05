# pip install beautifulsoup4

from bs4 import BeautifulSoup
import urllib.request as MYURL

# fp = open('song.xml', 'r')
# soup = BeautifulSoup(fp, 'html.parser')
#
# for song in soup.find_all('song'):
#     print(song['album'])
#     print(song.title.string)
#     print(song.length.string)
#     print()


fp = open('song.xml', 'r', encoding='utf-8')
openFile = fp.read()
soup = BeautifulSoup(openFile, 'html.parser')

for song in soup.find_all('song'):
    print(song['album'])
    print(song.title.string)
    print(song.length.string)
    print()




