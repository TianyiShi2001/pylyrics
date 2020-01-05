import requests
import lxml.etree as le
import re
from ..utils.cli import bcolors


class Utaten(object):

    def __init__(self, url):
        self.html = requests.get(url).text

    @classmethod
    def from_url(cls, url):
        return cls.__init__(cls, url)

    @classmethod
    def search(cls, title, author=None):
        r = requests.get(f'https://utaten.com/search/=/show_artists=1/layout_search_text={title}/layout_search_type=title/')
        x = le.HTML(r.text)
        results = []
        for i in x.xpath('(//main//table)[1]//tr[descendant::p]'):
            title = i.xpath('.//p[@class="searchResult__title"]/a/text()')[0].strip()
            artist = i.xpath('.//p[@class="searchResult__name"]/a/text()')[0].strip()
            summary = i.xpath('.//td[@class="lyricList__beginning"]/a/text()')[0].strip()
            url = 'https://utaten.com' + i.xpath('.//p[@class="searchResult__title"]/a/@href')[0]
            results.append((title, artist, summary, url))
        for i, (a, b, c, _) in enumerate(results):
            print(f'{bcolors.FAIL}{i:<2d}|{bcolors.OKBLUE}{a}|{bcolors.WARNING}{b}|{bcolors.ENDC}{c}')

        ans = input('Enter the ID.')

        a = cls(results[int(ans)][-1])
        print(a)
        return a

    def furigana(self, out='/Users/tianyishi/Downloads/kokoronashi.html'):
        l = re.search('<div class="hiragana".+?</div>', self.html, re.DOTALL).group(0)
        x = le.HTML(l)

        for i in x.xpath('//span[@class="ruby"]'):
            i.tag = 'ruby'
            for j in i.attrib.keys():
                del i.attrib[j]

        for i in x.xpath('//span[@class="rb"]'):
            i.tag = 'rb'
            for j in i.attrib.keys():
                del i.attrib[j]

        for i in x.xpath('//span[@class="rt"]'):
            i.tag = 'rt'
            for j in i.attrib.keys():
                del i.attrib[j]

        html = le.tostring(x, encoding='utf-8', pretty_print=True).decode('utf-8')

        if out:
            with open(out, 'w') as f:
                f.write(html)
            print(f'HTML written to {out}.')

        return html

    # def plain(self, out=None):
    #     l = re.search('<div class="romaji".+?</div>', self.html, re.DOTALL).group(0)

    #     l = re.sub('</?div.*?>', '', l).split('<br />')
    #     l = [i for i in l if re.match('\n', i)]

    #     lyrics = ''
    #     for i in l:
    #         try:
    #             x = le.HTML(i)
    #         except:
    #             pass
    #         if len(x):
    #             line = x.xpath('//*[@class="rb"]/text()')
    #             print(line)
    #             lyrics += ''.join(line)
    #             lyrics += '\n'

    #     return lyrics

    # def __str__(self):
    #     return self.plain()


if __name__ == "__main__":
    lyr = Utaten.search(input('title?'))
    lyr.furigana(input('where?'))
