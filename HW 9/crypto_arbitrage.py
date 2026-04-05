import requests
import networkx as nx

def fetch_crypto_data():
    """
    Fetches live cryptocurrency exchange rates from CoinGecko.
    Returns a dictionary of the JSON response.
    """
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,litecoin,ripple,cardano,bitcoin-cash,eos&vs_currencies=eth,btc,ltc,xrp,ada,bch,eos"
    response = requests.get(url)
    return response.json()

def build_crypto_graph(api_data):
    """
    Converts the API dictionary into a directed graph using ticker symbols 
    as nodes and the exchange rate as the edge weight.
    """
    name_to_ticker = {
        'ripple': 'xrp', 
        'cardano': 'ada', 
        'bitcoin-cash': 'bch',
        'eos': 'eos', 
        'litecoin': 'ltc', 
        'ethereum': 'eth', 
        'bitcoin': 'btc'
    }

    g = nx.DiGraph()
    edges = []

    # Loop through the outer dictionary (Base coins)
    for full_name, rates in api_data.items():
        if full_name in name_to_ticker:
            node_from = name_to_ticker[full_name]
            
            # Loop through the inner dictionary (Target coins and rates)
            for node_to, weight in rates.items():
                if node_from != node_to:
                    edges.append((node_from, node_to, weight))

    # Load all edges into the graph at once
    g.add_weighted_edges_from(edges)
    return g

def calculate_path_weight(g, path):
    """
    Calculates the total weight of a given path. 
    Returns None if the API data is missing an edge for the path.
    """
    total_weight = 1.0
    
    # Loop through the list using an index to grab node pairs
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        
        # IMPROVEMENT: Check if the edge exists before doing the math
        if g.has_edge(current_node, next_node):
            total_weight *= g[current_node][next_node]['weight']
        else:
            # The edge is missing from the API data; this path is a dead end.
            return None
            
    return total_weight

def find_arbitrage(g):
    """
    Hunts for arbitrage opportunities by finding all paths, calculating 
    their factors (forward * reverse), and tracking the extremes.
    """
    min_factor = float('inf')
    max_factor = 0.0
    best_min_paths = ([], [])
    best_max_paths = ([], [])

    for start_node in g.nodes:
        for end_node in g.nodes:
            if start_node != end_node:
                
                print(f"paths from {start_node} to {end_node} ----------------------------------")
                
                # Get all forward paths
                paths = nx.all_simple_paths(g, start_node, end_node)
                
                for path in paths:
                    # Create the reverse path using slice notation
                    reverse_path = path[::-1]
                    
                    # Calculate weights
                    forward_weight = calculate_path_weight(g, path)
                    reverse_weight = calculate_path_weight(g, reverse_path)
                    
                    # IMPROVEMENT: Only proceed if BOTH paths actually exist in the graph
                    if forward_weight is not None and reverse_weight is not None:
                        factor = forward_weight * reverse_weight
                        
                        # Output formatting per assignment requirements
                        print(f"{path} {forward_weight}")
                        print(f"{reverse_path} {reverse_weight}")
                        print(f"{factor}")
                        
                        # Track the highest and lowest factors
                        if factor < min_factor:
                            min_factor = factor
                            best_min_paths = (path, reverse_path)
                            
                        if factor > max_factor:
                            max_factor = factor
                            best_max_paths = (path, reverse_path)

    # Print the final summary at the end of the script
    print("\nSmallest Paths weight factor: ", min_factor)
    print("Paths: ", best_min_paths[0], best_min_paths[1])
    print("Greatest Paths weight factor: ", max_factor)
    print("Paths: ", best_max_paths[0], best_max_paths[1])

def main():
    """
    Main execution block.
    """
    # 1. Get the data
    api_data = fetch_crypto_data()
    
    # 2. Build the graph
    graph = build_crypto_graph(api_data)
    
    # 3. Analyze and print output
    find_arbitrage(graph)

if __name__ == "__main__":
    main()