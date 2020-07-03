import urllib.request
from bs4 import BeautifulSoup

def get_who():
    url = "https://www.who.int/news-room/headlines"

    uClient = urllib.request.urlopen(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = BeautifulSoup(page_html,"html.parser")

    news = page_soup.find_all('div',class_='list-view--item vertical-list-item')
    newz = []
    for new in news:
        newz.append([new.span.text,new.a['aria-label'],"https://www.who.int/"+new.a['href']])
    return newz