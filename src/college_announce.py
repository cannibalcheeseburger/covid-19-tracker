import urllib.request
from bs4 import BeautifulSoup


def announce():

    url = "https://nith.ac.in/"

    uClient = urllib.request.urlopen(url)
    page_html = uClient.read()
    uClient.close()

    page_soup = BeautifulSoup(page_html,"html.parser")
    announce_container = page_soup.find_all("ul",class_ = "allnithlinks")[0]
    announcements = announce_container.find_all("a")

    a = []
    for announce in announcements:
        b = []
        b.append(announce.text.strip())
        if announce['href'] != "#":
            b.append(announce['href'])
        else:
            b.append('#')
        a.append(b)    
    return a