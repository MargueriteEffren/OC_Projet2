<<<<<<< HEAD
import requests
from bs4 import BeautifulSoup
import csv
import re


#si on veut demander l'url du livre dans le terminal:
print('Copy/Paste Book url, please:')
url = input ()

def get_img_url(url):
		response_img = requests.get(url)
		page_img = response_img.content


		soup = BeautifulSoup(page_img, "html.parser")

		img_tag = soup.find("img")
		partial_img_url = img_tag['src']
		img_url = ('http://books.toscrape.com'+(partial_img_url.replace('../..',"")))
		return img_url

#titre du livre:
reponse = requests.get(url)
page = reponse.content

soup = BeautifulSoup(page, "html.parser")

title = soup.find("h1")
book_title = title.text


with open(book_title+'_pic.jpg', 'wb') as handle:
        response = requests.get(get_img_url(url), stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

=======
import requests
from bs4 import BeautifulSoup
import csv
import re


#si on veut demander l'url du livre dans le terminal:
print('Copy/Paste Book url, please:')
url = input ()

def get_img_url(url):
		response_img = requests.get(url)
		page_img = response_img.content


		soup = BeautifulSoup(page_img, "html.parser")

		img_tag = soup.find("img")
		partial_img_url = img_tag['src']
		img_url = ('http://books.toscrape.com'+(partial_img_url.replace('../..',"")))
		return img_url

#titre du livre:
reponse = requests.get(url)
page = reponse.content

soup = BeautifulSoup(page, "html.parser")

title = soup.find("h1")
book_title = title.text


with open(book_title+'_pic.jpg', 'wb') as handle:
        response = requests.get(get_img_url(url), stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

>>>>>>> 208db9a39569110214ce692e45090971c74f9285
            handle.write(block)