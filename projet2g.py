<<<<<<< HEAD
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

	#extract category urls from a tags:
	a_href_url_category = soup.findAll(href=re.compile("^catalogue/category/books/"))
	list_href_category= []
	for a in a_href_url_category:
		href_url_category=a['href']
		list_href_category.append('http://books.toscrape.com/'+href_url_category)
	return(list_href_category)

list_href_category_to_use = Get_categories_urls(url_site)
#récupération des liens des livres d'une category d'une page:


def File_creation_by_category(url2):
	#function: get category name from URL:

	def category_name(url2):
		
		split_url = url2.split('/')
		catgory_name = split_url[6]
		return catgory_name


	def Browse_category_all_pages(url2):
	#récupération des liens de toutes les pages d'une catégorie:


		reponse3 = requests.get(url2)

		listurlspercategory=[]

		listurlspercategory.append(url2)

		listindex = [1,2,3,4,5,6,7,8]
		i=1

		while i in listindex:
			i+=1
			url3 = url2.replace('index',"page-"+str(i))
			reponse4 = requests.get(url3)
			if reponse4.ok:
				listurlspercategory.append(url3)

		return(listurlspercategory)

	#je crée une liste pour stocker tous les url de livres:
	url_livres_contenu = []

	#je crée une fonction pour récupérer les livres d'une page html category:
	def recupererlivresdunepagecategory(j):
		#lien de la page category
		url = j


		reponse2 = requests.get(url)
		page2 = reponse2.content


		soup = BeautifulSoup(page2, "html.parser")

		#je vais chercher tous les url de livres de la catégorie:

		url_livres = soup.find_all("h3")
		for h3 in url_livres:
			a = h3.find('a')
			lienlivre = a['href']

		# je remets l'adresse url au complet:
			lienlivre2 = lienlivre.replace('../../../',"")

		#tout en ajoutant à la liste finale:
			url_livres_contenu.append('http://books.toscrape.com/catalogue/'+lienlivre2)
		


	#remplissage de [url_livres_contenu] avec les url de tous les livres d'une même catégorie, même s'il y a plusieurs pages pour cette catégorie:
	listurlspercategory = Browse_category_all_pages(url2)
	n=0
	j=listurlspercategory[0]
	recupererlivresdunepagecategory(j)
	while n < (len(listurlspercategory)-1):
		n+=1
		j=listurlspercategory[n]
		recupererlivresdunepagecategory(j)


	#récupération des détails des livres d'une page de category et transfert dans un fichier csv - reste à faire: quand il y a plusieurs pages 

	#j'utilise ci-dessous des listes pour ranger les données que je rapatrie, mais je me demande si un tuple ne serait pas préférable, au cas où la donnée manque sur une page? à suivres
	colonnes = ['product_page_url','universal_ product_code', 'title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']

	#get image_url: 
	def get_img_url(url):
		response_img = requests.get(url)
		page_img = response_img.content


		soup = BeautifulSoup(page_img, "html.parser")

		img_tag = soup.find("img")
		partial_img_url = img_tag['src']
		img_url = ('http://books.toscrape.com'+(partial_img_url.replace('../..',"")))
		return img_url


	#je crée une fonction rapatriement de données d'un livre:
	def detailslivre(x):
		url = x
		reponse = requests.get(url)
		page = reponse.content


		# transforme (parse) le HTML en objet BeautifulSoup
		soup = BeautifulSoup(page, "html.parser")

		values = []

		#récupération URL
		values.append(url)

		# récupération UPC
		# pour cela, d'abord: récupération de toutes les td (valeurs)
		valeurs = soup.find_all("td")
		valeurs_contenu = []
		for contenu in valeurs:
			valeurs_contenu.append(contenu.string)

		#puis:
		values.append(valeurs_contenu[0])

		# recupération title
		title = soup.find("h1")
		
		values.append(title.text)

		# add Price including Tax: problème d'encodage dans Excel mais pas dans Notes
		b = valeurs_contenu[3]
		values.append(b)

		# add Price excluding Tax
		values.append(valeurs_contenu[2])

		# add Number available
		values.append(valeurs_contenu[5])

		#add Product Description
		description = soup.find_all("p")
		product_description = []
		for desc in description:
			product_description.append(desc.string)

		values.append(product_description[3])


		#add category
		# pour cela, d'abord: récupération de tous les a
		navigateur_a = soup.find_all("a")
		a_textes = []
		for category in navigateur_a:
			a_textes.append(category.string)

		#puis:
		values.append(a_textes[3])

		#add review rating:
		paragraphes = soup.find_all("p")
		p_textes = []
		for classe in paragraphes:
			p_textes.append(paragraphes)

		tag = paragraphes[2]
		rating = tag['class']

		values.append(rating[1]+" stars")

		#append img_url:

		values.append(get_img_url(url))
		return values


	# création du fichier data.csv
	en_tete = ['caracteristique_produit', 'contenu']
	with open(category_name(url2)+'.csv', 'w',encoding='utf-8') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(colonnes)
	#je demande au fichier d'ecrire les detail de chaque livre pour tous les livres présents dans url_livres_contenu
		for y in url_livres_contenu:
			detailslivre(y)
			writer.writerow(detailslivre(y))

index_url2 = 0
url2 = list_href_category_to_use[index_url2]
File_creation_by_category(url2)
	
while index_url2 in range(0,51):
	index_url2+=1
	url2 = list_href_category_to_use[index_url2]
	File_creation_by_category(url2)
	
=======
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

	#extract category urls from a tags:
	a_href_url_category = soup.findAll(href=re.compile("^catalogue/category/books/"))
	list_href_category= []
	for a in a_href_url_category:
		href_url_category=a['href']
		list_href_category.append('http://books.toscrape.com/'+href_url_category)
	return(list_href_category)

list_href_category_to_use = Get_categories_urls(url_site)
#récupération des liens des livres d'une category d'une page:


def File_creation_by_category(url2):
	#function: get category name from URL:

	def category_name(url2):
		
		split_url = url2.split('/')
		catgory_name = split_url[6]
		return catgory_name


	def Browse_category_all_pages(url2):
	#récupération des liens de toutes les pages d'une catégorie:


		reponse3 = requests.get(url2)

		listurlspercategory=[]

		listurlspercategory.append(url2)

		listindex = [1,2,3,4,5,6,7,8]
		i=1

		while i in listindex:
			i+=1
			url3 = url2.replace('index',"page-"+str(i))
			reponse4 = requests.get(url3)
			if reponse4.ok:
				listurlspercategory.append(url3)

		return(listurlspercategory)

	#je crée une liste pour stocker tous les url de livres:
	url_livres_contenu = []

	#je crée une fonction pour récupérer les livres d'une page html category:
	def recupererlivresdunepagecategory(j):
		#lien de la page category
		url = j


		reponse2 = requests.get(url)
		page2 = reponse2.content


		soup = BeautifulSoup(page2, "html.parser")

		#je vais chercher tous les url de livres de la catégorie:

		url_livres = soup.find_all("h3")
		for h3 in url_livres:
			a = h3.find('a')
			lienlivre = a['href']

		# je remets l'adresse url au complet:
			lienlivre2 = lienlivre.replace('../../../',"")

		#tout en ajoutant à la liste finale:
			url_livres_contenu.append('http://books.toscrape.com/catalogue/'+lienlivre2)
		


	#remplissage de [url_livres_contenu] avec les url de tous les livres d'une même catégorie, même s'il y a plusieurs pages pour cette catégorie:
	listurlspercategory = Browse_category_all_pages(url2)
	n=0
	j=listurlspercategory[0]
	recupererlivresdunepagecategory(j)
	while n < (len(listurlspercategory)-1):
		n+=1
		j=listurlspercategory[n]
		recupererlivresdunepagecategory(j)


	#récupération des détails des livres d'une page de category et transfert dans un fichier csv - reste à faire: quand il y a plusieurs pages 

	#j'utilise ci-dessous des listes pour ranger les données que je rapatrie, mais je me demande si un tuple ne serait pas préférable, au cas où la donnée manque sur une page? à suivres
	colonnes = ['product_page_url','universal_ product_code', 'title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']

	#get image_url: 
	def get_img_url(url):
		response_img = requests.get(url)
		page_img = response_img.content


		soup = BeautifulSoup(page_img, "html.parser")

		img_tag = soup.find("img")
		partial_img_url = img_tag['src']
		img_url = ('http://books.toscrape.com'+(partial_img_url.replace('../..',"")))
		return img_url


	#je crée une fonction rapatriement de données d'un livre:
	def detailslivre(x):
		url = x
		reponse = requests.get(url)
		page = reponse.content


		# transforme (parse) le HTML en objet BeautifulSoup
		soup = BeautifulSoup(page, "html.parser")

		values = []

		#récupération URL
		values.append(url)

		# récupération UPC
		# pour cela, d'abord: récupération de toutes les td (valeurs)
		valeurs = soup.find_all("td")
		valeurs_contenu = []
		for contenu in valeurs:
			valeurs_contenu.append(contenu.string)

		#puis:
		values.append(valeurs_contenu[0])

		# recupération title
		title = soup.find("h1")
		
		values.append(title.text)

		# add Price including Tax: problème d'encodage dans Excel mais pas dans Notes
		b = valeurs_contenu[3]
		values.append(b)

		# add Price excluding Tax
		values.append(valeurs_contenu[2])

		# add Number available
		values.append(valeurs_contenu[5])

		#add Product Description
		description = soup.find_all("p")
		product_description = []
		for desc in description:
			product_description.append(desc.string)

		values.append(product_description[3])


		#add category
		# pour cela, d'abord: récupération de tous les a
		navigateur_a = soup.find_all("a")
		a_textes = []
		for category in navigateur_a:
			a_textes.append(category.string)

		#puis:
		values.append(a_textes[3])

		#add review rating:
		paragraphes = soup.find_all("p")
		p_textes = []
		for classe in paragraphes:
			p_textes.append(paragraphes)

		tag = paragraphes[2]
		rating = tag['class']

		values.append(rating[1]+" stars")

		#append img_url:

		values.append(get_img_url(url))
		return values


	# création du fichier data.csv
	en_tete = ['caracteristique_produit', 'contenu']
	with open(category_name(url2)+'.csv', 'w',encoding='utf-8') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(colonnes)
	#je demande au fichier d'ecrire les detail de chaque livre pour tous les livres présents dans url_livres_contenu
		for y in url_livres_contenu:
			detailslivre(y)
			writer.writerow(detailslivre(y))

index_url2 = 0
url2 = list_href_category_to_use[index_url2]
File_creation_by_category(url2)
	
while index_url2 in range(0,51):
	index_url2+=1
	url2 = list_href_category_to_use[index_url2]
	File_creation_by_category(url2)
	
>>>>>>> 208db9a39569110214ce692e45090971c74f9285
