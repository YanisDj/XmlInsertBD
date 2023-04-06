# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:39:38 2023

@author: PC-15
"""

import mysql.connector

# Connexion à la base de données
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dblp"
)

cursor = db.cursor()

# Liste des noms de tables dans votre base de données
tables = ["publications", "publicationdetails", "authors", "publicationauthors", "coauthors","affiliation;"]

# Suppression des données de chaque table
for table in tables:
    cursor.execute("TRUNCATE TABLE " + table)
# Validation de la transaction
db.commit()
db.close()