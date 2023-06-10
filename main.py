import uuid

import networkx as nx
from datetime import datetime
import numpy as np
import pandas as pd
import math
import mysql.connector
from faker import Faker
import random
import requests


"(a.) erwthma"
# Connect to the MySQL server
cnx = mysql.connector.connect(
    host="192.168.2.6",
    user="bill",
    password="bill123",
    database="bill1"
)


# Create the cursor
cursor = cnx.cursor()


# Drop the "albums" table
drop_discs_table_query = "DROP TABLE IF EXISTS discs"
cursor.execute(drop_discs_table_query)

# Drop the "bands" table
drop_bands_table_query = "DROP TABLE IF EXISTS bands"
cursor.execute(drop_bands_table_query)

# Drop the "bands" table
drop_users_table_query = "DROP TABLE IF EXISTS users"
cursor.execute(drop_users_table_query)


# Create the Users, Bands, and Discs tables
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  username VARCHAR(255) PRIMARY KEY,
  email VARCHAR(255)
)
"""

create_bands_table = """
CREATE TABLE IF NOT EXISTS bands (
  band_id VARCHAR(255) PRIMARY KEY,
  band_name VARCHAR(255),
  username VARCHAR(255),
  FOREIGN KEY (username) REFERENCES users(username)
)
"""

create_discs_table = """
CREATE TABLE IF NOT EXISTS discs (
  disc_id VARCHAR(255) PRIMARY KEY,
  band_name VARCHAR(255),
  disc_name VARCHAR(255),
  price INT,
  band_id VARCHAR(255),
  username VARCHAR(255),
  FOREIGN KEY (band_id) REFERENCES bands(band_id),
  FOREIGN KEY (username) REFERENCES users(username)
)
"""

cursor.execute(create_users_table)
cursor.execute(create_bands_table)
cursor.execute(create_discs_table)



# Generate random user data
fake = Faker()

def generate_user_data(num_users):
    users_data = []
    used_usernames = set()  # To keep track of used usernames
    while len(users_data) < num_users:
        username = fake.user_name()
        if username not in used_usernames:
            used_usernames.add(username)
            user_data = {
                'username': username,
                'email': fake.email()
            }
            users_data.append(user_data)
    return users_data


# Insert random user data into the Users table
def insert_users(users_data):
    insert_query = "INSERT INTO Users (username, email) VALUES (%s, %s)"
    users_values = [(user['username'], user['email']) for user in users_data]
    cursor.executemany(insert_query, users_values)
    cnx.commit()


num_users = 20
users_data = generate_user_data(num_users)
insert_users(users_data)


"(b.) erwthma"
api_key = "bd0838c4bd7b715c5cd525eb6d6c614a"


# Function to fetch band data from Last.fm API and insert into Bands table
def fetch_bands_data(username):
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={api_key}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        artists_data = response.json().get('topartists').get('artist')
        if artists_data:
            # Limit the number of favorite bands to 2 for each user
            artists_data = artists_data[:2]

            for band in artists_data:
                insert_query = "INSERT IGNORE INTO Bands (band_id ,band_name, username) VALUES (%s, %s, %s)"
                bands_values = [(band.get('mbid'), band.get('name'), username)]
                cursor.executemany(insert_query, bands_values)
                cnx.commit()
    else:
        print(f"Failed to fetch band data for user {username} from Last.fm API")


# Function to fetch album data from Last.fm API and insert into Discs table
def fetch_discs_data(band_id, band_name, username):

    # Fetch album data for the band from Last.fm API (to get disc details)
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={band_name}&api_key={api_key}&format=json&limit=5"
    response = requests.get(url)

    if response.status_code == 200:
        albums_data = response.json().get('topalbums').get('album', [])

        if albums_data:
            # Limit the number of owned discs to 1 for each favorite band/artist of the given user
            owned_discs = albums_data[:1]

            for album in owned_discs:
                disc_id = str(uuid.uuid4())
                disc_name = album.get('name')
                price = random.randint(10, 50)  # Random price between 10 and 50

                insert_query = "INSERT INTO Discs (disc_id, band_name, disc_name, price, band_id, username) VALUES (%s, %s, %s, %s, %s, %s)"
                discs_values = (disc_id, band_name, disc_name, price, band_id, username)
                cursor.execute(insert_query, discs_values)
                cnx.commit()

        else:
            print(f"No albums found for band {band_name}")
    else:
        print(f"Failed to fetch album data for band {band_name} from Last.fm API")


# Retrieve data from the Users table
select_users_query = "SELECT * FROM Users"
cursor.execute(select_users_query)
users_data = cursor.fetchall()

# Fetch data for each user and populate tables
for user in users_data:
    username = user[0]

    # Fetch band data for the user and insert into Bands table
    fetch_bands_data(username)

    # Fetch album data for each band and insert into Albums table
    select_bands_query = "SELECT band_id, band_name FROM Bands"
    cursor.execute(select_bands_query)
    bands_data = cursor.fetchall()
    for band in bands_data:
        band_id = band[0]
        band_name = band[1]

        fetch_discs_data(band_id, band_name, username)


print("Users:")
for user in users_data:
    print(user)

# Retrieve data from the Bands table
select_bands_query = "SELECT band_name, username FROM Bands"
cursor.execute(select_bands_query)
bands_data = cursor.fetchall()
print("Bands:")
for band in bands_data:
    print(band)

# Retrieve data from the Albums table
select_discs_query = "SELECT band_name, disc_name, price, username FROM discs"
cursor.execute(select_discs_query)
discs_data = cursor.fetchall()
print("Discs:")
for disc in discs_data:
    print(disc)


# Close the cursor and the connection
cursor.close()
cnx.close()

