"""
Calculate altitude and distance indices for cities.

The altitude index (A_i) measures the hilliness of a city.
The distance index (D_i) measures the network connectivity/compactness.
"""

import osmnx as ox
import networkx as nx
import numpy as np
from typing import Tuple, Optional

# Configure OSMnx to use free Open Topo Data API instead of Google
ox.settings.elevation_url_template = \
    "https://api.opentopodata.org/v1/aster30m?locations={locations}"


def calculate_altitude_index(city_name: str, country: Optional[str] = None) -> float:
    """
    Calculate the altitude index (A_i) for a city.
    
    The altitude index quantifies how hilly a city is. Lower values indicate
    flatter terrain, which is better for cycling.
    
    A_i = (mean_elevation_change / mean_edge_length) * 100
    
    Where:
    - mean_elevation_change: Average elevation difference across road segments
    - mean_edge_length: Average length of road segments
    
    The result is multiplied by 100 to get a percentage-like value.
    
    Hypothesis: Lower A_i = better for cycling (less climbing required)
    
    Parameters
    ----------
    city_name : str
        Name of the city
    country : str, optional
        Country name to disambiguate cities
        
    Returns
    -------
    float
        Altitude index value (lower is better for cycling)
    """
    try:
        # Construct query
        query = f"{city_name}, {country}" if country else city_name
        
        # Get the road network with elevation data
        G = ox.graph_from_place(query, network_type="bike")
        
        # Add elevation data using free Open Topo Data API (no key needed)
        G = ox.add_node_elevations_google(G, api_key=None, batch_size=100, pause=0.5)
        
        # Calculate elevation changes for each edge
        elevation_changes = []
        edge_lengths = []
        
        for u, v, data in G.edges(data=True):
            if 'length' in data:
                # Get elevations of start and end nodes
                elev_u = G.nodes[u].get('elevation', 0)
                elev_v = G.nodes[v].get('elevation', 0)
                
                # Calculate absolute elevation change
                elev_change = abs(elev_v - elev_u)
                elevation_changes.append(elev_change)
                edge_lengths.append(data['length'])
        
        # Calculate mean values
        mean_elev_change = np.mean(elevation_changes)
        mean_edge_length = np.mean(edge_lengths)
        
        # Calculate altitude index
        if mean_edge_length > 0:
            altitude_index = (mean_elev_change / mean_edge_length) * 100
        else:
            altitude_index = 0
        
        return altitude_index
        
    except Exception as e:
        print(f"Error calculating altitude index for {city_name}: {e}")
        return None


def calculate_distance_index(city_name: str, country: Optional[str] = None) -> float:
    """
    Calculate the distance index (D_i) for a city.
    
    The distance index measures how connected/compact a city's bike network is.
    Values closer to 1 indicate better connectivity.
    
    D_i = circuity / (1 + normalized_node_density)
    
    Where:
    - circuity: Ratio of network distances to straight-line distances (closer to 1 is better)
    - normalized_node_density: Nodes per km² normalized to [0, 1]
    
    Hypothesis: D_i closer to 1 = better for cycling (more direct routes, better connectivity)
    
    Parameters
    ----------
    city_name : str
        Name of the city
    country : str, optional
        Country name to disambiguate cities
        
    Returns
    -------
    float
        Distance index value (closer to 1 is better)
    """
    try:
        # Construct query
        query = f"{city_name}, {country}" if country else city_name
        
        # Get the road network
        G = ox.graph_from_place(query, network_type="bike")
        
        # Calculate basic stats
        stats = ox.basic_stats(G)
        
        # Get circuity (how direct the routes are)
        # Circuity = 1 means perfectly direct routes
        circuity = stats.get('circuity_avg', 1.0)
        
        # Get node density (nodes per km²)
        node_density = stats.get('node_density_km', 0)
        
        # Normalize node density (assuming max typical density of 500 nodes/km²)
        max_density = 500
        normalized_density = min(node_density / max_density, 1.0)
        
        # Calculate distance index
        # Lower circuity is better (more direct)
        # Higher node density is better (more connected)
        distance_index = circuity / (1 + normalized_density)
        
        return distance_index
        
    except Exception as e:
        print(f"Error calculating distance index for {city_name}: {e}")
        return None


def calculate_indices_for_city(city_name: str, country: Optional[str] = None) -> Tuple[float, float]:
    """
    Calculate both altitude and distance indices for a city.
    
    Parameters
    ----------
    city_name : str
        Name of the city
    country : str, optional
        Country name to disambiguate cities
        
    Returns
    -------
    tuple
        (altitude_index, distance_index)
    """
    print(f"Calculating indices for {city_name}...")
    
    altitude_idx = calculate_altitude_index(city_name, country)
    distance_idx = calculate_distance_index(city_name, country)
    
    return altitude_idx, distance_idx


if __name__ == "__main__":
    # Test with a sample city
    test_city = "Amsterdam"
    test_country = "Netherlands"
    
    a_i, d_i = calculate_indices_for_city(test_city, test_country)
    
    print(f"\n{test_city} Results:")
    print(f"Altitude Index (A_i): {a_i:.3f}")
    print(f"Distance Index (D_i): {d_i:.3f}")
