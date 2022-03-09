
import requests
from bs4 import BeautifulSoup
import csv
import re

# page to scrape's url:
url_site = "http://books.toscrape.com"
def Get_categories_urls(url_site):
	reponse = requests.get(url_site)
	page = reponse.content


	# transforme (parse) le HTML en objet BeautifulSoup
	soup = BeautifulSoup(page, "html.parser")

	#extract category urls from "a" tags:
	a_href_url_category = soup.findAll(href=re.compile("^catalogue/category/books/"))
	list_href_category= []
	for a in a_href_url_category:
		href_url_category=a['href']
		list_href_category.append('http://books.toscrape.com/'+href_url_category)
	return(list_href_category)

list_href_category_to_use = Get_categories_urls(url_site)
#récupération des liens des livres d'une category d'une page (remarque: la variable url2 est l'url extrait d'une liste des urls des category du site- voir en bas du code) :


def File_creation_by_category(url2):
	#function: get category name from URL:

	def category_name(url2):
		
		split_url = url2.split('/')
		catgory_name = split_url[6]
		return catgory_name


	def browse_category_all_pages(url2):
	#récupération des liens de toutes les pages d'une catégorie:


		reponse3 = requests.get(url2)

		list_urls_per_category=[]

		list_urls_per_category.append(url2)

		listindex = [1,2,3,4,5,6,7,8]
		i=1

		while i in listindex:
			i+=1
			url3 = url2.replace('index',"page-"+str(i))
			reponse4 = requests.get(url3)
			if reponse4.ok:
				list_urls_per_category.append(url3)

		return(list_urls_per_category)

	#je crée une liste pour stocker tous les url de livres:
	books_details_urls = []

	#je crée une fonction pour récupérer les livres d'une page html category:
	def get_all_books_from_category(j):
		#lien de la page category
		url = j


		reponse2 = requests.get(url)
		page2 = reponse2.content


		soup = BeautifulSoup(page2, "html.parser")

		#je vais chercher tous les url de livres de la catégorie:

		books_urls = soup.find_all("h3")
		for h3 in books_urls:
			a = h3.find('a')
			book_url = a['href']

		# je remets l'adresse url au complet:
			book_url2 = book_url.replace('../../../',"")

		#tout en ajoutant à la liste finale:
			books_details_urls.append('http://books.toscrape.com/catalogue/'+book_url2)
		


	#remplissage de [books_details_urls] avec les url de tous les livres d'une même catégorie, même s'il y a plusieurs pages pour cette catégorie:
	list_urls_per_category = browse_category_all_pages(url2)
	n=0
	j=list_urls_per_category[0]
	get_all_books_from_category(j)
	while n < (len(list_urls_per_category)-1):
		n+=1
		j=list_urls_per_category[n]
		get_all_books_from_category(j)


	#récupération des détails des livres d'une page de category et transfert dans un fichier csv :

	#j'utilise ci-dessous des listes pour ranger les données que je rapatrie, mais je me demande si un tuple ne serait pas préférable, au cas où la donnée manque sur une page? à suivres
	columns = ['product_page_url','universal_ product_code', 'title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']

	#get image_url: 
	def get_img_url(url):
		response_img = requests.get(url)
		page_img = response_img.content


		soup = BeautifulSoup(page_img, "html.parser")

		img_tag = soup.find("img")
		partial_img_url = img_tag['src']
		img_url = ('http://books.toscrape.com'+(partial_img_url.replace('../..',"")))
		return img_url


	#get book details:
	def single_book_details(x):
		url = x
		reponse = requests.get(url)
		page = reponse.content


		# transforme (parse) le HTML en objet BeautifulSoup
		soup = BeautifulSoup(page, "html.parser")

		# values list to stash book details
		values = []

		#stash book URL
		values.append(url)

		# stash UPC
		# for that, first: get all  "td" data (text)
		get_td = soup.find_all("td")
		td_content_list = []
		for content in get_td:
			td_content_list.append(content.string)

		#puis:
		values.append(td_content_list[0])

		# recupération title
		title = soup.find("h1")
		
		values.append(title.text)

		# add Price including Tax: problème d'encodage dans Excel mais pas dans Notes
		values.append(td_content_list[3])

		# add Price excluding Tax
		values.append(td_content_list[2])

		# add Number available
		values.append(td_content_list[5])

		#add Product Description
		description = soup.find_all("p")
		product_description = []
		for desc in description:
			product_description.append(desc.string)

		values.append(product_description[3])


		#add category
		# For that, first get all "a" tags: 
		navigator_a = soup.find_all("a")
		a_textes = []
		for category in navigator_a:
			a_textes.append(category.string)

		#puis:
		values.append(a_textes[3])

		#add review rating:
		paragraphs = soup.find_all("p")
		p_texts = []
		for classe in paragraphs:
			p_texts.append(paragraphs)

		tag = paragraphs[2]
		rating = tag['class']

		values.append(rating[1]+" stars")

		#append img_url:

		values.append(get_img_url(url))
		return values


	# création du fichier data.csv
	en_tete = ['product_data', 'content']
	with open(category_name(url2)+'.csv', 'w',encoding='utf-8') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(columns)
	#je demande au fichier d'ecrire les detail de chaque livre pour tous les livres présents dans books_details_urls
		for y in books_details_urls:
			single_book_details(y)
			writer.writerow(single_book_details(y))

index_url2 = 0
url2 = list_href_category_to_use[index_url2]
File_creation_by_category(url2)
	
while index_url2 in range(0,49):
	index_url2+=1
	url2 = list_href_category_to_use[index_url2]
	File_creation_by_category(url2)
	