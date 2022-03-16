
import requests
from bs4 import BeautifulSoup
import csv
import re

#avec l'aide de BeautifulSoup, je récupère l'url des catégories
def get_categories_urls(url_site):
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

#récupération des liens des livres d'une category d'une page (remarque: la variable url2 est l'url extrait d'une liste des urls des category du site- voir en bas du code) :
def file_creation_by_category(url_category):
	#function: get category name from URL:
	def category_name(url_category):
		split_url = url_category.split('/')
		catgory_name = split_url[6]
		return catgory_name

	def category_all_pages_list(url_category):
	#récupération des liens de toutes les pages d'une catégorie:
		list_urls_per_category=[]
		list_urls_per_category.append(url_category)
		listindex = [1,2,3,4,5,6,7,8]
		i=1
		while i in listindex:
			i+=1
			url_next = url_category.replace('index',"page-"+str(i))
			reponse4 = requests.get(url_next)
			if reponse4.ok:
				list_urls_per_category.append(url_next)
		return(list_urls_per_category)

	#je crée une liste pour stocker tous les url de livres:
	books_details_urls = []
	#je crée une fonction pour récupérer les livres d'une page html category:
	def get_all_books_from_category(url_category):
		#lien de la page category		
		reponse2 = requests.get(url_category)
		page2 = reponse2.content
		soup = BeautifulSoup(page2, "html.parser")
		#je vais chercher tous les url de livres de la catégorie:
		books_urls = soup.find_all("h3")
		for h3 in books_urls:
			a_tag = h3.find('a')
			book_url = a_tag['href']
		# je remets l'adresse url au complet:
			clean_book_url = book_url.replace('../../../',"")
		#tout en ajoutant à la liste finale:
			books_details_urls.append('http://books.toscrape.com/catalogue/'+clean_book_url)
		
	#remplissage de [books_details_urls] avec les urls de tous les livres d'une même catégorie, même s'il y a plusieurs pages pour cette catégorie:
	list_urls_per_category = category_all_pages_list(url_category)
	i=0
	url=list_urls_per_category[0]
	get_all_books_from_category(url)
	while i < (len(list_urls_per_category)-1):
		i+=1
		url=list_urls_per_category[i]
		get_all_books_from_category(url)

	#récupération des détails des livres d'une page de category et transfert dans un fichier csv :
	#j'utilise ci-dessous des listes pour ranger les données que je rapatrie, mais je me demande si un tuple ne serait pas préférable, au cas où la donnée manque sur une page? à suivres
	columns = ['product_page_url','universal_ product_code', 'title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']

	#get book details:
	def single_book_details(url):
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
		#get image_url: 
		def get_img_url(url):
			img_tag = soup.find("img")
			partial_img_url = img_tag['src']
			img_url = ('http://books.toscrape.com'+(partial_img_url.replace('../..',"")))
			return img_url

		values.append(get_img_url(url))

		url_pic = get_img_url(url)
		print(url_pic)
		string_title = title.text
		title_slashless = string_title.replace("/","_").replace("(","_").replace(")","_")
		with open(title_slashless+'_pic.jpg', 'wb') as handle:
		        response = requests.get(url_pic, stream=True)
		        if not response.ok:
		           	print(response)
		        for block in response.iter_content(1024):		           	            	
		            handle.write(block)
		return values

	# création du fichier data.csv
	en_tete = ['product_data', 'content']
	with open(category_name(url_category)+'.csv', 'w',encoding='utf-8') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(columns)
	#je demande au fichier d'ecrire les detail de chaque livre pour tous les livres présents dans books_details_urls
		for url in books_details_urls:
			writer.writerow(single_book_details(url))

# page to scrape's url:
url_site = "http://books.toscrape.com"
list_href_category_to_use = get_categories_urls(url_site)
for index_url2 in range(0,50):
	print(index_url2)
	url_category = list_href_category_to_use[index_url2]
	print(url_category)
	file_creation_by_category(url_category)


	