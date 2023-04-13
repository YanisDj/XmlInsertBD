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
    password="caca123",
    database="dblp"
)

cursor = db.cursor()

# Parsing du fichier XML
tree = ET.parse("dblpl5000.xml")
root = tree.getroot()

nbauteur = 0
idPub = 0
idauthor = 0
idcoauthor = 0
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

    # Itération à travers tous les éléments 'author' du noeud 'data'
    for author in data.findall('author'):
        idauthor += 1
        # Récupération de l'attribut 'orcid' de l'élément 'author'
        orcid = author.get('orcid')

        # Récupération du nom de l'auteur
        name = author.text

        # Insertion des données dans la table 'authors'
        cursor.execute("""
            INSERT INTO authors (id,name, firstpaper, lastpaper, affiliation)
            VALUES (%s,%s, NULL, NULL, NULL)
        """, (idauthor, name[:40]))

        # Insertion des données dans la table 'publicationauthors'
        cursor.execute("""
            INSERT INTO publicationauthors (author_id, publication_id)
            VALUES (%s, %s)
        """, (idauthor, idPub))

        # Remplissage des données dans la table 'coauthors'
        cursor.execute("""select * from publicationauthors""")
        results = cursor.fetchall()
        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                a = results[i]
                b = results[j]
                if a[1] == b[1] & a[0] != b[0]:
                    sql = "SELECT * FROM coauthors WHERE author_id = %s AND coauthor_id = %s"
                    cursor.execute(sql, (a[0], b[0]))
                    if cursor.fetchone() is None:
                        sql = "INSERT INTO coauthors (author_id, coauthor_id) VALUES (%s, %s)"
                        cursor.execute(sql, (a[0], b[0]))




        # # Itération à travers tous les autres éléments 'author' du noeud 'data'
        # for coauthor in data.findall('author'):
        #     # Récupération de l'attribut 'orcid' de l'élément 'author'
        #     coauthor_orcid = coauthor.get('orcid')

        #     # Récupération du nom de l'auteur
        #     coauthor_name = coauthor.text

        #     # Vérification si l'auteur courant est différent de l'auteur collaborateur
        #     if name != coauthor_name:
        #         idcoauthor=idauthor+1
        #         # Insertion des données dans la table 'authors'
        #         cursor.execute("""
        #             INSERT INTO authors (id,name, firstpaper, lastpaper, affiliation)
        #             VALUES (%s,%s, NULL, NULL, NULL)
        #         """, (idcoauthor,coauthor_name))

        #         # Insertion des données dans la table 'publicationauthors'
        #         cursor.execute("""
        #             INSERT INTO publicationauthors (author_id, publication_id)
        #             VALUES (%s, %s)
        #         """, (idcoauthor, idPub))

        #         # Insertion des données dans la table 'authorcoauthors'
        #         cursor.execute("""
        #             INSERT INTO coauthors (author_id, coauthor_id)
        #             VALUES (%s, %s)
        #         """, (idauthor, idcoauthor))

# Validation de la transaction
db.commit()

db.close()
