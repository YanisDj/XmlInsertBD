# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:43:43 2023

@author: PC-15
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:18:24 2023

@author: PC-15
"""

import mysql.connector
import time
from lxml import etree

# Connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dblp"
)

cursor = db.cursor()

# Parsing du fichier XML
try:
    parser = etree.XMLParser(remove_blank_text=True, huge_tree=True)
    tree = etree.parse("dblplsae.xml", parser)
    root = tree.getroot()
except etree.XMLSyntaxError as e:
    print("Erreur de parsing : ", e)
    exit()

nbauthor = 0
idPub = 0
idauthor = 0
idcoauthor=0

start_time = time.time()

# Utilisation d'une transaction pour regrouper les insertions dans la base de données
cursor.execute("START TRANSACTION")

# Fonction pour insérer les données
def process_data(data, publication_type):
    global idPub, idauthor
    nbauthor = 0
    idPub += 1
    mdate = data.get('mdate')
    key_id = data.get('key')

    title = data.find('title').text
    year = data.find('year').text
    publisher = data.find(publication_type).text if data.find(publication_type) is not None else None

    for author in data.findall('author'):
        nbauthor += 1
        idauthor += 1
        name = author.text

        cursor.execute("INSERT INTO authors (id,name, firstpaper, lastpaper, affiliation) VALUES (%s,%s, NULL, NULL, NULL)", (idauthor,name))
        cursor.execute("INSERT INTO publicationauthors (author_id, publication_id) VALUES (%s, %s)", (idauthor, idPub))

    cursor.execute("INSERT INTO publications (id, title, year, venue, nauthor, type) VALUES (%s, %s, %s, %s, %s, %s)", (idPub, title[:150], year, publisher, nbauthor, "conference"))
    cursor.execute("INSERT INTO publicationdetails (publication_id, authors, mdate, key_id) VALUES (%s, %s, %s, %s)", (idPub, nbauthor, mdate, key_id))

# Parcours des noeuds 'data', 'inproceedings' et 'article'
for node_name in ['data', 'inproceedings', 'article']:
    for data in root.findall(node_name):
        publication_type = 'publisher' if node_name == 'data' else 'booktitle' if node_name == 'inproceedings' else 'journal'
        process_data(data, publication_type)

# Fin de la transaction
cursor.execute("COMMIT")

# Optimisation de la mise à jour des auteurs
cursor.execute("UPDATE authors, (SELECT publicationauthors.author_id, MIN(publications.year) AS first_paper, MAX(publications.year) AS last_paper FROM publications INNER JOIN publicationauthors ON publications.id = publicationauthors.publication_id GROUP BY publicationauthors.author_id) AS author_years SET authors.firstpaper = author_years.first_paper, authors.lastpaper = author_years.last_paper WHERE authors.id = author_years.author_id")

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Temps d'exécution : {elapsed_time:.2f} secondes")
db.commit()
db.close()
