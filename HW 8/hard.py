# Write a Python function that takes a NetworkX graph as input 
# and returns the number of nodes in the graph that have a degree greater than 5

import networkx as nx

# Function to return the number of nodes in the graph that have a degree greater than 5
def count_high_degree_nodes(G):
    """
    Takes a NetworkX graph G as input and returns the 
    number of nodes that have a degree greater than 5.
    """
    # G.degree() returns (node, degree) pairs.
    # We count 1 for every node where the degree is > 5.
    count = sum(1 for node, degree in G.degree() if degree > 5)
    return count


if __name__ == "__main__":
    test_network = nx.complete_graph(10)

    result = count_high_degree_nodes(test_network)

    print("-" * 35)
    print(f"Total nodes in graph: {test_network.number_of_nodes()}")
    print(f"Nodes with degree > 5: {result}")
    
    # Show the degree of the first node
    first_node_degree = test_network.degree(0)
    print(f"Example: Node 0 has a degree of {first_node_degree}")
    print("-" * 35)