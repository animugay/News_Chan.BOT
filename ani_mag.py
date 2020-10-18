from bs4 import BeautifulSoup
import urllib.request


class Parser_class:
    
    raw_html = ''
    html = '' 
    results = []
    current_post = []
    last_post = None

    def __init__(self, url):
        self.url = url


    def get_html(self):
        req = urllib.request.urlopen(self.url)
        self.raw_html = req.read()
        self.html = BeautifulSoup(self.raw_html, 'html.parser')


    def parsing(self):
        news = self.html.find_all('div', class_='views-row')
        URL = 'https://www.animag.ru'

        for item in news:
            title = item.find('h3', class_='field-content') 
            if title == None:
                continue
            elif title is not None:
                title = title.get_text()

            image = item.find('img').get('src')

            desc = item.find('p').get_text()

            link = item.find('a').get('href')
            link = URL + link

            self.results.append({
                'title': title,
                'image': image, 
                'desc' : desc, 
                'link' : link
            })

    def save_last_post(self):
        news = self.html.find_all('div', class_='views-row')

        for i in news:
            title = i.find('h3', class_='field-content') 
            if title == None:
                continue
            elif title is not None:
                title = title.get_text(strip=True)
                self.current_post.append(title)

        f = open('last_post.txt', encoding='utf-8')
        self.last_post = f.read()
        f.close()      
         
    
    def compare(self):
        if self.results[0] != self.last_post:
            f = open('last_post.txt', 'w', encoding='utf-8')
            f.write(self.current_post[0])
            f.close()


    def run(self):
        self.get_html()
        self.parsing()          
        self.save_last_post()
        self.compare()




