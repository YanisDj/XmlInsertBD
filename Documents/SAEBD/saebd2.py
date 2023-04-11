# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:18:24 2023

@author: PC-15
"""

import xml.etree.ElementTree as ET
import mysql.connector

# Connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dblp"
)

cursor = db.cursor()

# Parsing du fichier XML
tree = ET.parse("dblpl5000.xml")
root = tree.getroot()

nbauteur = 0
idPub = 0
# Itération à travers tous les éléments 'data' du fichier XML
for data in root.findall('data'):
    idPub = idPub + 1
    # Récupération des attributs du noeud 'data'
    mdate = data.get('mdate')
    key_id = data.get('key')

    # Récupération des éléments enfants du noeud 'data'
    title = data.find('title').text
    year = data.find('year').text

    # Vérification si l'élément 'ee' existe
    ee = data.find('ee')
    if ee is not None:
        ee = ee.text

    # Vérification si l'élément 'month' existe
    month = data.find('month')
    if month is not None:
        month = month.text

    # Vérification si l'élément 'publisher' existe
    publisher = data.find('publisher')
    if publisher is not None:
        publisher = publisher.text

    # Insertion des données dans la table 'publications'
    cursor.execute("""
        INSERT INTO publications (id, title, year, venue, nauthor, type)
        VALUES (%s, %s, %s, %s, NULL, %s)
    """, (idPub, title[:150], year, publisher, "conference"))



    # Insertion des données dans la table 'publicationdetails'
    cursor.execute("""
        INSERT INTO publicationdetails (publication_id, authors, mdate, key_id)
        VALUES (%s, NULL, %s, %s)
    """, (idPub, mdate, key_id))

    print(idPub)
    # # Itération à travers tous les éléments 'author' du noeud 'data'
    # for author in data.findall('author'):
    #
    #     # Récupération de l'attribut 'orcid' de l'élément 'author'
    #     orcid = author.get('orcid')
    #
    #     # Récupération du nom de l'auteur
    #     name = author.text
    #
    #     # Insertion des données dans la table 'authors'
    #     cursor.execute("""
    #         INSERT INTO authors (name, firstpaper, lastpaper, affiliation)
    #         VALUES (%s, NULL, NULL, NULL)
    #     """, (name,))
    #
    #     # Récupération de l'identifiant de la dernière insertion
    #     author_id = cursor.lastrowid
    #
    #     # Insertion des données dans la table 'publicationauthors'
    #     cursor.execute("""
    #         INSERT INTO publicationauthors (author_id, publication_id)
    #         VALUES (%s, %s)
    #     """, (author_id, publication_id))
    #
    #     # Itération à travers tous les autres éléments 'author' du noeud 'data'
    #     for coauthor in data.findall('author'):
    #         # Récupération de l'attribut 'orcid' de l'élément 'author'
    #         coauthor_orcid = coauthor.get('orcid')
    #
    #         # Récupération du nom de l'auteur
    #         coauthor_name = coauthor.text
    #
    #         # Vérification si l'auteur courant est différent de l'auteur collaborateur
    #         if name != coauthor_name:
    #             # Insertion des données dans la table 'authors'
    #             cursor.execute("""
    #                 INSERT INTO authors (name, firstpaper, lastpaper, affiliation)
    #                 VALUES (%s, NULL, NULL, NULL)
    #             """, (coauthor_name,))
    #
    #             # Récupération de l'identifiant de la dernière insertion
    #             coauthor_id = cursor.lastrowid
    #
    #             # Insertion des données dans la table 'publicationauthors'
    #             cursor.execute("""
    #                 INSERT INTO publicationauthors (author_id, publication_id)
    #                 VALUES (%s, %s)
    #             """, (coauthor_id, publication_id))
    #
    #             # Insertion des données dans la table 'authorcoauthors'
    #             cursor.execute("""
    #                 INSERT INTO authorcoauthors (author1_id, author2_id)
    #                 VALUES (%s, %s)
    #             """, (author_id, coauthor_id))

# Validation de la transaction
db.commit()

db.close()
