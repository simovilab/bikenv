"""
Quick analysis using the 13 cities that worked successfully
Skipping problematic cities like Québec (too large area)
"""
import pandas as pd
from prediction_platform import (
    test_altitude_hypothesis,
    test_distance_hypothesis,
    create_visualizations,
    save_results
)

# Cities that worked successfully
successful_cities = [
    {"rank": 1, "city": "Utrecht", "country": "Netherlands", "score": 71.1, "altitude_index": 1.653, "distance_index": 1.061},
    {"rank": 2, "city": "Copenhagen", "country": "Denmark", "score": 68.9, "altitude_index": 2.212, "distance_index": 1.018},
    {"rank": 3, "city": "Ghent", "country": "Belgium", "score": 68.3, "altitude_index": 1.778, "distance_index": 1.078},
    {"rank": 4, "city": "Amsterdam", "country": "Netherlands", "score": 67.8, "altitude_index": 1.751, "distance_index": 1.056},
    {"rank": 5, "city": "Paris", "country": "France", "score": 67.6, "altitude_index": 5.103, "distance_index": 1.026},
    {"rank": 13, "city": "Strasbourg", "country": "France", "score": 61.1, "altitude_index": 4.175, "distance_index": 1.076},
    {"rank": 14, "city": "Lyon", "country": "France", "score": 61.1, "altitude_index": 5.509, "distance_index": 1.056},
    {"rank": 15, "city": "Montréal", "country": "Canada", "score": 60.0, "altitude_index": 4.090, "distance_index": 1.075},
    {"rank": 16, "city": "Malmö", "country": "Sweden", "score": 59.4, "altitude_index": 2.603, "distance_index": 1.066},
    {"rank": 17, "city": "Munich", "country": "Germany", "score": 58.9, "altitude_index": 3.661, "distance_index": 1.044},
    {"rank": 26, "city": "Stockholm", "country": "Sweden", "score": 53.9, "altitude_index": 4.743, "distance_index": 1.077},
    {"rank": 27, "city": "Vitoria-Gasteiz", "country": "Spain", "score": 53.3, "altitude_index": 4.381, "distance_index": 1.077},
    {"rank": 28, "city": "Wroclaw", "country": "Poland", "score": 52.8, "altitude_index": 4.044, "distance_index": 1.064},
]

# Create DataFrame
df = pd.DataFrame(successful_cities)

print("="*70)
print("BIKENV PREDICTION PLATFORM")
print("Testing Altitude and Distance Index Hypotheses")
print("Data: Copenhagenize Index 2025 Edition")
print("="*70)
print(f"Using {len(df)} successfully calculated cities\n")

# Display sample of data
print("Sample of cities included:")
print(df[['city', 'country', 'score', 'altitude_index', 'distance_index']].head(10).to_string(index=False))
print("...")

# Test hypotheses
h1_results = test_altitude_hypothesis(df)
h2_results = test_distance_hypothesis(df)

# Create visualizations
create_visualizations(df)

# Save results
save_results(df, h1_results, h2_results)

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print("\nResults saved to:")
print("  - results/cities_with_indices.csv")
print("  - results/analysis_results.png")
print("  - results/hypothesis_test_results.txt")
