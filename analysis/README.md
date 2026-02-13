# Bikenv Prediction Platform

**Issue #2**: Platform to test prediction capabilities of altitude and distance indices

## Overview

This platform evaluates the prediction capabilities of the proposed `altitude_index (A_i)` and `distance_index (D_i)` using data from the **Copenhagenize Index 2025 Edition** as a reference.

**Data Source**: [The Global Ranking of Bicycle-Friendly Cities](https://copenhagenizeindex.eu/) (Copenhagenize Index - EIT Urban Mobility Edition 2025)

## Hypotheses

This platform tests two hypotheses:

1. **Hypothesis 1**: The lower the `A_i` (altitude index), the better for cycling
2. **Hypothesis 2**: The closer to 1 the `D_i` (distance index), the better for cycling

## Methodology

### Altitude Index (A_i)

The altitude index quantifies the hilliness of a city by measuring elevation changes across the road network:

```
A_i = (mean_elevation_change / mean_edge_length) × 100
```

Where:
- `mean_elevation_change`: Average elevation difference across road segments (meters)
- `mean_edge_length`: Average length of road segments (meters)

**Interpretation**: Lower values indicate flatter terrain, which is expected to correlate with better cycling conditions.

### Distance Index (D_i)

The distance index measures the connectivity and compactness of a city's cycling network:

```
D_i = circuity / (1 + normalized_node_density)
```

Where:
- `circuity`: Ratio of network distances to straight-line distances (1.0 = perfectly direct routes)
- `normalized_node_density`: Number of intersections per km², normalized to [0, 1]

**Interpretation**: Values closer to 1 indicate better connectivity with more direct routes.

### Data Source

The **Copenhagenize Index 2025 Edition** (official name: "The Global Ranking of Bicycle-Friendly Cities") ranks the top 100 bicycle-friendly cities globally based on 13 indicators across 3 pillars: Infrastructure, Usage, and Policy.

This platform uses the **top 30 cities** as reference data, with scores ranging from 50.3 (Vancouver) to 71.1 (Utrecht).

**Source**: https://copenhagenizeindex.eu/  
**Publisher**: Copenhagenize Design Company & EIT Urban Mobility  
**Data retrieved**: December 2025

## Project Structure

```
bikenv/
├── data/
│   ├── copenhagenize_index_2025.csv    # Reference data (2025 edition)
│   └── copenhagenize_index_2022.csv    # Legacy data (deprecated)
├── scripts/
│   ├── retrieve_data.py                # Script to fetch latest index data
│   └── calculate_indices.py            # Functions to calculate A_i and D_i
├── analysis/
│   └── prediction_platform.py          # Main analysis script
├── results/                            # Output directory
│   ├── cities_with_indices.csv         # Cities with calculated indices
│   ├── statistical_results.csv         # Correlation and regression results
│   └── hypothesis_testing_results.png  # Visualization plots
└── requirements-platform.txt           # Python dependencies
```

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/simovilab/bikenv.git
   cd bikenv
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements-platform.txt
   ```

   Or using conda:
   ```bash
   conda install pandas numpy matplotlib seaborn scipy scikit-learn
   conda install -c conda-forge osmnx
   ```

## Usage

### Running the Complete Analysis

From the `analysis/` directory:

```bash
cd analysis
python prediction_platform.py
```

This will:
1. Load the Copenhagenize Index 2025 data
2. Sample 15 cities across different performance tiers
3. Calculate `A_i` and `D_i` for each city using OpenStreetMap data
4. Perform statistical analysis (correlation, regression)
5. Generate visualizations
6. Save results to the `results/` directory

**Note**: The analysis may take 10-30 minutes depending on network speed and API rate limits, as it downloads geographic data for each city.

### Calculating Indices for Individual Cities

```python
from scripts.calculate_indices import calculate_indices_for_city

# Calculate indices for a single city
altitude_idx, distance_idx = calculate_indices_for_city("Amsterdam", "Netherlands")

print(f"Altitude Index: {altitude_idx:.3f}")
print(f"Distance Index: {distance_idx:.3f}")
```

## Statistical Methods

The platform employs multiple statistical approaches:

1. **Pearson Correlation**: Measures linear relationship strength
2. **Spearman Correlation**: Measures monotonic relationship (rank-based)
3. **Linear Regression**: Models the relationship and calculates R² score
4. **Significance Testing**: p-values < 0.05 indicate statistical significance

### Interpretation Criteria

- **Strong support**: |r| > 0.5 and p < 0.05
- **Moderate support**: 0.3 < |r| < 0.5 and p < 0.05
- **Weak support**: |r| < 0.3 and p < 0.05
- **Not significant**: p ≥ 0.05

## Output Files

After running the analysis, the following files are generated in `results/`:

1. **cities_with_indices.csv**: Complete dataset with calculated indices
2. **statistical_results.csv**: Summary of correlation and regression analysis
3. **hypothesis_testing_results.png**: 4-panel visualization showing:
   - Altitude Index vs Score scatter plot
   - Distance Index vs Score scatter plot
   - Distance from Optimal D_i vs Score
   - Correlation heatmap

## Expected Results

Based on urban cycling research, we expect:

- **Negative correlation** between `A_i` and cycling scores (flatter cities rank higher)
- **Cities with D_i ≈ 1** to have higher scores (better network connectivity)

Top-performing cities like Utrecht, Copenhagen, and Amsterdam are expected to have:
- Low `A_i` values (< 2.0, indicating flat terrain)
- `D_i` values close to 1.0 (indicating efficient, direct networks)

## Limitations

1. **Sample Size**: Analysis uses 15 cities for computational efficiency
2. **API Dependencies**: Requires OpenStreetMap data access
3. **Elevation Data**: May require Google Elevation API key for accurate altitude calculations
4. **Network Complexity**: Simplified metrics may not capture all aspects of cyclability

## Future Improvements

- [ ] Expand sample size to all 30 cities
- [ ] Add weather/climate index
- [ ] Incorporate bike infrastructure data (protected lanes, bike parking)
- [ ] Test against modal share data (% of trips by bicycle)
- [ ] Develop combined predictive model

## References

- **Copenhagenize Index**: https://copenhagenizeindex.eu/
- **OSMnx Documentation**: https://osmnx.readthedocs.io/
- **GTFS and Urban Mobility**: https://gtfs.org/

## License

MIT License - See repository LICENSE file

## Author

**Brandon Trigueros Lara**  
TCU Project - SIMOVI Lab, Universidad de Costa Rica  
December 2025

---

## Quick Start Example

```python
# Quick test with sample cities
import pandas as pd
from scripts.calculate_indices import calculate_indices_for_city

# Test with Amsterdam
print("Calculating indices for Amsterdam...")
a_i, d_i = calculate_indices_for_city("Amsterdam", "Netherlands")

print(f"\nAmsterdam Results:")
print(f"  Altitude Index: {a_i:.3f} (lower is better)")
print(f"  Distance Index: {d_i:.3f} (closer to 1 is better)")

# Load reference data to compare
df = pd.read_csv('../data/copenhagenize_index_2022.csv')
amsterdam_score = df[df['city'] == 'Amsterdam']['score'].values[0]

print(f"  Copenhagenize Score: {amsterdam_score} (rank #4)")
```

## Contact

For questions or issues, please open an issue on GitHub or contact:
- brandon.trigueros@ucr.ac.cr
- Laboratory: SIMOVI - UCR
