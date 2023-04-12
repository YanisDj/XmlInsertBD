import xml.etree.ElementTree as ET
import mysql.connector

# Connect to the database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="dblp"
)
cursor = db.cursor()

# Parse the XML file
tree = ET.parse('dblpl5000.xml')
root = tree.getroot()

# Iterate through each data element
for data in root.findall('data'):
    # Get the publication details
    title = data.find('title').text
    year = int(data.find('year').text)
    venue = data.find('publisher').text
    nauthor = len(data.findall('author'))
    ptype = 'Conference'  # assume it's a conference publication

    # Insert publication record
    query = "INSERT INTO publications (title, year, venue, nauthor, type) VALUES (%s, %s, %s, %s, %s)"
    values = (title, year, venue, nauthor, ptype)
    cursor.execute(query, values)
    publication_id = cursor.lastrowid  # get the ID of the newly inserted publication

    # Insert publication details
    query = "INSERT INTO publicationdetails (publication_id, authors, mdate, key_id) VALUES (%s, %s, %s, %s)"
    values = (publication_id, nauthor, data.get('mdate'), data.get('key'))
    cursor.execute(query, values)

    # Iterate through each author
    for author in data.findall('author'):
        # Check if the author is already in the database
        query = "SELECT id FROM authors WHERE name = %s"
        values = (author.text,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None:
            # Author already exists, use the existing ID
            author_id = result[0]
        else:
            # Author does not exist, insert a new record
            query = "INSERT INTO authors (name) VALUES (%s)"
            values = (author.text,)
            cursor.execute(query, values)
            author_id = cursor.lastrowid

            # Check if the author has an affiliation
            aff = author.get('affiliation')
            if aff is not None:
                # Check if the affiliation is already in the database
                query = "SELECT idAff FROM affiliation WHERE name = %s"
                values = (aff,)
                cursor.execute(query, values)
                result = cursor.fetchone()
                if result is not None:
                    # Affiliation already exists, use the existing ID
                    affiliation_id = result[0]
                else:
                    # Affiliation does not exist, insert a new record
                    query = "INSERT INTO affiliation (name) VALUES (%s)"
                    values = (aff,)
                    cursor.execute(query, values)
                    affiliation_id = cursor.lastrowid

            

      
