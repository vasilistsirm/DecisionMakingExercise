import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Connect to the MySQL server using SQLAlchemy
engine = create_engine('mysql+mysqlconnector://bill:bill123@192.168.2.6/bill1')

# Fetch data from the Discs, Genres, and Users tables
discs_query = "SELECT * FROM discs"
genres_query = "SELECT * FROM genres"
users_query = "SELECT * FROM users"

discs_df = pd.read_sql(discs_query, engine)
genres_df = pd.read_sql(genres_query, engine)
users_df = pd.read_sql(users_query, engine)

# Close the connection
engine.dispose()

# Drop rows with missing genre_id values
discs_df = discs_df.dropna(subset=['genre_id'])

# Convert the data type of genre_id column in discs_df to int64
discs_df['genre_id'] = discs_df['genre_id'].astype('int64')

# Merge Discs and Genres tables on genre_id
merged_df = pd.merge(discs_df, genres_df, on='genre_id')

# Print the users_df columns to identify the correct user identifier column name
print(users_df.columns)

# Merge merged_df and Users table on username (replace 'user_id_column' with 'username')
merged_df = pd.merge(merged_df, users_df, on='username')

# Calculate genre frequency distribution
genre_distribution = merged_df['genre_name'].value_counts(normalize=True)

# Check the genre distribution
print(genre_distribution)

most_common_genre = genre_distribution.idxmax()
print("\nThe most common genre is:", most_common_genre)

# Plot the genre distribution
plt.bar(genre_distribution.index, genre_distribution.values)
plt.xlabel('Genre')
plt.ylabel('Frequency')
plt.title('Distribution of Music Genres')
plt.xticks(rotation=90)
plt.show()

# Calculate correlation between age and genre preference
age_genre_corr = merged_df.groupby('genre_name')['age'].mean()

# Plot the correlation
plt.bar(age_genre_corr.index, age_genre_corr.values)
plt.xlabel('Genre')
plt.ylabel('Average Age')
plt.title('Correlation between Age and Genre Preference')
plt.xticks(rotation=90)
plt.show()
