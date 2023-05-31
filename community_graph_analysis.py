import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector

# Connect to the MySQL server
cnx = mysql.connector.connect(
    host="192.168.2.6",
    user="bill",
    password="bill123",
    database="bill1"
)

# Create the cursor
cursor = cnx.cursor()

# Generate the community graph
community_graph = nx.barabasi_albert_graph(20, 3)

# Draw the community graph
nx.draw(community_graph, with_labels=True)
plt.show()

# Retrieve users from the database
select_users_query = "SELECT username FROM users"
cursor.execute(select_users_query)
users_result = cursor.fetchall()
users = [user[0] for user in users_result]

# Map usernames to node names in the community graph
username_to_node = {username: node for username, node in zip(users, community_graph.nodes)}

# Recommend a disc to each user
for user in users:
    # Retrieve selected discs for the user from the database
    select_owned_discs_query = "SELECT disc_name FROM discs WHERE username = %s"
    cursor.execute(select_owned_discs_query, (user,))
    owned_discs_result = cursor.fetchall()
    owned_discs = [disc[0] for disc in owned_discs_result]

    # Find the available disc recommendation
    recommended_disc = None
    node = username_to_node[user]
    for neighbor in community_graph.neighbors(node):
        neighbor_user = users[neighbor]
        # Retrieve discs owned by the neighbor from the database
        select_neighbor_discs_query = "SELECT disc_name FROM discs WHERE username = %s"
        cursor.execute(select_neighbor_discs_query, (neighbor_user,))
        neighbor_discs_result = cursor.fetchall()
        neighbor_discs = [disc[0] for disc in neighbor_discs_result]

        # Find a disc that the user doesn't have
        for disc in neighbor_discs:
            if disc not in owned_discs:
                recommended_disc = disc
                break

        if recommended_disc:
            break

    # Print the recommendation for the user
    if recommended_disc:
        print(f"Recommended disc for user {user}: {recommended_disc}")
    else:
        print(f"No disc recommendation available for user {user}")

# Close the cursor and the connection
cursor.close()
cnx.close()
