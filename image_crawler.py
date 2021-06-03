from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request, urlopen
import scrapy
# url = "https://tambour.co.il/private/inspiration/rooms-design/babies-room-design/"

if __name__ == '__main__':
    url = "https://tambour.co.il/private/inspiration/rooms-design/babies-room-design/"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # html = webpage.read().decode("utf-8")
    soup = BeautifulSoup(webpage, "html.parser")
    images = soup.findAll('img')
    for image in images:
        try:
            # print(image)
            # cur_src = image['data-lazy-src']
            cur_alt = image['alt']
            # if 'גוון' in cur_alt:
            # print(cur_src, cur_alt)
            print(cur_alt)
            #print image source
            # print(image['src'])
            #print alternate text
            # print(image['alt'])
        except:
            continue
        # print(soup)
        # images =[[i.title for i in soup.find_all(class_='figcaption')]]
    # print(images)
    #
