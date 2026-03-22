#Write a Python function that takes a NetworkX graph 
# as input and returns the number of nodes in the graph.

import networkx as nx

# Function to count the nodes in the graph
def count_nodes(G):
    """
    Takes a NetworkX graph G as input and returns 
    the total number of nodes in the graph.
    """
    return G.number_of_nodes()

if __name__ == "__main__":
    # Initialize the graph
    my_network = nx.Graph()

    # Add nodes
    nodes_to_add = ["Server_A", "Server_B", "User_1", "User_2", "Database"]
    my_network.add_nodes_from(nodes_to_add)

    # Call function
    result = count_nodes(my_network)

    # Print the output to the console
    print("-" * 30)
    print(f"Nodes detected: {result}")
    print(f"Node List: {list(my_network.nodes())}")
    print("-" * 30)