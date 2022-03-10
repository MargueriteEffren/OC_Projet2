import requests
from bs4 import BeautifulSoup
import csv
import re


#si on veut demander l'url de la category dans le terminal:

print('Copy/Paste Category url, please:')
category_url = input ()

#fonction pour chercher l'url d'une image d'un livre du site:
def get_img_url(book_url):
				response_img = requests.get(book_url)
				page_img = response_img.content


				soup = BeautifulSoup(page_img, "html.parser")

				img_tag = soup.find("img")
				partial_img_url = img_tag['src']
				img_url = ('http://books.toscrape.com'+(partial_img_url.replace('../..',"")))
				return img_url


#je crée une liste pour stocker tous les url de livres:
books_urls_list = []

#je crée une fonction pour récupérer les livres d'une page html category:
def get_all_books_from_category(url):


	response = requests.get(url)
	page = response.content

	soup = BeautifulSoup(page, "html.parser")

	#je vais chercher tous les urls de livres de la catégorie:

	category_h3s = soup.find_all("h3")
	for h3 in category_h3s:
		a_tag = h3.find('a')
		partial_book_url = a_tag['href']

	# je remets l'adresse url au complet:
		book_clean_url = partial_book_url.replace('../../../',"")
		
#tout en ajoutant à la liste finale:

		books_urls_list.append('http://books.toscrape.com/catalogue/'+book_clean_url)

	return books_urls_list

def browse_category_all_pages(category_url):
	#récupération des liens de toutes les pages d'une catégorie:


	reponse3 = requests.get(category_url)

	list_urls_per_category=[]

	list_urls_per_category.append(category_url)

	listindex = [1,2,3,4,5,6,7,8]
	i=1

	while i in listindex:
		i+=1
		url_next = category_url.replace('index',"page-"+str(i))
		response4 = requests.get(url_next)
		if response4.ok:
			list_urls_per_category.append(url_next)

	return(list_urls_per_category)


list_all_category_urls = browse_category_all_pages(category_url)


for url in list_all_category_urls:

	list_of_books_urls = get_all_books_from_category(url)


	for book_url in list_of_books_urls:

		#titre du livre:
		reponse = requests.get(book_url)
		page = reponse.content

		soup = BeautifulSoup(page, "html.parser")

		title = soup.find("h1")
		book_title = title.text

		url_pic = get_img_url(book_url)

		with open(book_title+'_pic.jpg', 'wb') as handle:
		        response = requests.get(url_pic, stream=True)

		        if not response.ok:
		           	print(response)

		        for block in response.iter_content(1024):
		           	            	
		            handle.write(block)