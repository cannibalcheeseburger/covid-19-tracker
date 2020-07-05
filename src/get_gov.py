import urllib.request
from bs4 import BeautifulSoup


def get_go():
    url = "https://www.mohfw.gov.in/"

    uClient = urllib.request.urlopen(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = BeautifulSoup(page_html,"html.parser")

    news = page_soup.find_all('div',class_ = 'update-box')
    newz = []
    for new in news:
        newz.append([new.strong.text,new.a.text.strip(),new.a['href']])
    return newz