import pandas as pd
from sqlalchemy import create_engine


def handle_data_issues():
    # Connect to the MySQL server
    engine = create_engine('mysql+mysqlconnector://bill:bill123@192.168.2.6/bill1')

    # Read the Bands, Discs, and Users tables into DataFrames
    bands_df = pd.read_sql_table('bands', engine)
    discs_df = pd.read_sql_table('discs', engine)
    users_df = pd.read_sql_table('users', engine)

    # Handle missing values
    discs_df.dropna(inplace=True)
    bands_df.dropna(inplace=True)
    users_df.dropna(inplace=True)

    # Handle duplicate values
    discs_df.drop_duplicates(inplace=True)
    bands_df.drop_duplicates(inplace=True)
    users_df.drop_duplicates(inplace=True)

    # Handle outlier values (if applicable, based on the columns in the 'users' table)

    # Write the cleaned DataFrames back to the database
    discs_df.to_sql('discs', engine, if_exists='replace', index=False)
    bands_df.to_sql('bands', engine, if_exists='replace', index=False)
    users_df.to_sql('users', engine, if_exists='replace', index=False)

    # Close the connection
    engine.dispose()


# Call the function to handle data issues
handle_data_issues()
