# Changelog - Bikenv Prediction Platform

## 2025-12-27 - Initial Implementation

### Added
- **Data Retrieval Script** (`scripts/retrieve_data.py`)
  - Manual data entry from Copenhagenize Index 2025 edition
  - Function to fetch and save top 30 cities with scores
  - Notes for future automated scraping implementation

- **Index Calculation Functions** (`scripts/calculate_indices.py`)
  - `calculate_altitude_index()`: Measures city hilliness using OSM elevation data
  - `calculate_distance_index()`: Measures network connectivity/compactness
  - Both functions integrated with OSMnx for real geographic data

- **Analysis Platform** (`analysis/prediction_platform.py`)
  - Comprehensive hypothesis testing framework
  - Statistical analysis (Pearson, Spearman correlations)
  - Linear regression modeling
  - Automated visualization generation
  - CSV export of results

- **Demo Mode** (`analysis/demo_platform.py`)
  - Simplified version with synthetic data
  - No API dependencies required
  - Quick testing and validation

- **Project Structure**
  - `data/` - Reference datasets
  - `scripts/` - Data retrieval and calculation utilities
  - `analysis/` - Main platform and demo scripts
  - `results/` - Output directory for plots and CSVs

- **Documentation**
  - Comprehensive README with methodology and usage
  - Structure verification script
  - Requirements file for dependencies

### Changed
- **Updated to Copenhagenize Index 2025 Edition**
  - Previous: Referenced "Global Bicycle Cities Index 2022"
  - Current: **Copenhagenize Index 2025 (EIT Urban Mobility Edition)**
  - Reason: 2025 is the latest available edition
  - Source: https://copenhagenizeindex.eu/

- **Data Attribution Improvements**
  - Added full source citation: "The Global Ranking of Bicycle-Friendly Cities"
  - Included publisher: Copenhagenize Design Company & EIT Urban Mobility
  - Added direct link to official website
  - Clarified data retrieval date and method

### Dataset Details

**Copenhagenize Index 2025 Edition**
- Top 30 cities included (from 100 total ranked)
- Score range: 50.3 (Vancouver) to 71.1 (Utrecht)
- Countries represented: 15
- Top countries: France (5), Netherlands (4), Germany (3), Canada (3)

### Hypotheses Tested

1. **H1**: Lower altitude index (A_i) correlates with higher bicycle scores
   - Expected: Flat cities are more bike-friendly
   
2. **H2**: Distance index (D_i) closer to 1 correlates with higher bicycle scores
   - Expected: Better-connected networks are more bike-friendly

### Technical Stack

- Python 3.12+
- pandas, numpy, matplotlib, seaborn
- scipy (statistical analysis)
- scikit-learn (regression)
- osmnx, networkx (geographic analysis)
- geopandas (spatial data)

### Known Limitations

1. Sample size limited to 15 cities for computational efficiency
2. Requires OpenStreetMap API access for real data
3. Elevation data may require Google Elevation API key
4. Analysis time: 10-30 minutes per run with real data

### Future Enhancements

- [ ] Automated web scraping for data updates
- [ ] Expand to all 100 cities in index
- [ ] Add weather/climate indices
- [ ] Integrate bike infrastructure metrics
- [ ] Develop combined predictive model
- [ ] Real-time data validation

---

**Contributors**: Brandon Trigueros Lara  
**Project**: TCU - SIMOVI Lab, Universidad de Costa Rica  
**Issue**: bikenv#2
