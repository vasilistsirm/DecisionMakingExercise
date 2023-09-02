import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to the MySQL server
engine = create_engine('mysql+mysqlconnector://')

# Read the 'discs' table into a DataFrame
discs_df = pd.read_sql_table('discs', engine)

# Plot histogram for 'band_name'
plt.hist(discs_df['band_name'], bins=10)
plt.xlabel('Band Name')
plt.ylabel('Count')
plt.title('Distribution of Band Names')
plt.xticks(rotation=45)
plt.show()


# Plot histogram for 'disc_name'
plt.hist(discs_df['disc_name'], bins=10)
plt.xlabel('Disc Name')
plt.ylabel('Count')
plt.title('Distribution of Disc Names')
plt.xticks(rotation=45)
plt.show()

# Plot a histogram of the 'price' attribute
plt.hist(discs_df['price'], bins=10)
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Distribution of Disc Prices')
plt.show()
