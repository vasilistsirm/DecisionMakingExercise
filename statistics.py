import pandas as pd
from sqlalchemy import create_engine

# Connect to the MySQL server using SQLAlchemy
engine = create_engine('mysql+mysqlconnector://')

# Fetch data from the Users, Bands, and Discs tables
users_query = "SELECT * FROM users"
bands_query = "SELECT * FROM bands"
discs_query = "SELECT * FROM discs"

users_df = pd.read_sql(users_query, engine)
bands_df = pd.read_sql(bands_query, engine)
discs_df = pd.read_sql(discs_query, engine)

# Close the connection
engine.dispose()

# Calculate statistics for numerical features in the Discs table
discs_numerical_stats = discs_df.describe()

# Grouping and aggregation on Bands table
bands_grouped_stats = bands_df.groupby('username')['band_id'].count()

# Value counts for a categorical feature in the Discs table
discs_value_counts = discs_df['band_name'].value_counts()

# Display the statistics
print("Numerical statistics for Discs:")
print(discs_numerical_stats)
print()

print("Bands grouped statistics:")
print(bands_grouped_stats)
print()

print("Value counts for band_name in Discs:")
print(discs_value_counts)
