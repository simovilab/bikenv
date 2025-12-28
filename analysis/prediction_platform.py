"""
Prediction Platform for Testing Altitude and Distance Index Hypotheses

This script tests the following hypotheses using the Copenhagenize Index 2025:
1. The lower the A_i (altitude index), the better for cycling
2. The closer to 1 the D_i (distance index), the better for cycling

Data Source: The Global Ranking of Bicycle-Friendly Cities (Copenhagenize Index)
https://copenhagenizeindex.eu/
Edition: 2025 (EIT Urban Mobility Edition)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os
import sys
import signal
import time
from contextlib import contextmanager

# Add parent directory to path to import bikenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.calculate_indices import calculate_indices_for_city


class TimeoutException(Exception):
    """Exception raised when operation times out"""
    pass


@contextmanager
def time_limit(seconds):
    """Context manager to limit execution time"""
    def signal_handler(signum, frame):
        raise TimeoutException(f"Timed out after {seconds} seconds")
    
    # Set the signal handler and alarm
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)  # Disable the alarm


def load_bicycle_index_data(filepath: str) -> pd.DataFrame:
    """Load the Copenhagenize Bicycle Cities Index data."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} cities from the index")
    return df


def calculate_indices_for_cities(df: pd.DataFrame, sample_size: int = 15) -> pd.DataFrame:
    """
    Calculate A_i and D_i for a sample of cities from the index.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with city information
    sample_size : int
        Number of cities to sample (default: 15 for computational efficiency)
        
    Returns
    -------
    pd.DataFrame
        DataFrame with added altitude_index and distance_index columns
    """
    # Sample cities from different score ranges to get good distribution
    # Top performers, middle performers, and lower performers
    top_cities = df.head(5)
    middle_cities = df.iloc[12:17]  # Around rank 13-17
    lower_cities = df.iloc[25:30]  # Around rank 26-30
    
    sampled_df = pd.concat([top_cities, middle_cities, lower_cities]).reset_index(drop=True)
    
    total_cities = len(sampled_df)
    print(f"\nCalculating indices for {total_cities} cities...", flush=True)
    print("This may take several minutes...", flush=True)
    print("(Cities with very large areas will be skipped automatically)", flush=True)
    print(f"\n{'='*70}", flush=True)
    
    altitude_indices = []
    distance_indices = []
    successful_count = 0
    failed_cities = []
    
    for idx, row in sampled_df.iterrows():
        city = row['city']
        country = row['country']
        city_num = idx + 1
        
        print(f"\n[{city_num}/{total_cities}] Processing: {city}, {country}", flush=True)
        start_time = time.time()
        
        try:
            # Set timeout to 5 minutes per city (300 seconds)
            # Cities like Québec that take too long will be skipped
            print(f"  → Downloading network data...", flush=True)
            with time_limit(300):
                a_i, d_i = calculate_indices_for_city(city, country)
                elapsed = time.time() - start_time
                
                if a_i is not None and d_i is not None:
                    altitude_indices.append(a_i)
                    distance_indices.append(d_i)
                    a_i_str = f"{a_i:.3f}"
                    d_i_str = f"{d_i:.3f}"
                    print(f"  ✓ SUCCESS: A_i={a_i_str}, D_i={d_i_str} (took {elapsed:.1f}s)", flush=True)
                    successful_count += 1
                else:
                    elapsed = time.time() - start_time
                    print(f"  ✗ FAILED: Calculation returned None (took {elapsed:.1f}s)", flush=True)
                    altitude_indices.append(None)
                    distance_indices.append(None)
                    failed_cities.append(f"{city} (returned None)")
                    
        except TimeoutException as e:
            elapsed = time.time() - start_time
            print(f"  ✗ SKIPPED: Area too large, would take >5 minutes (stopped at {elapsed:.1f}s)", flush=True)
            altitude_indices.append(None)
            distance_indices.append(None)
            failed_cities.append(f"{city} (timeout)")
            
        except KeyboardInterrupt:
            elapsed = time.time() - start_time
            print(f"\n  ⚠ INTERRUPTED by user at {elapsed:.1f}s", flush=True)
            print(f"\nStopping analysis. Processed {successful_count}/{city_num} cities so far.", flush=True)
            # Add None for remaining cities
            remaining = len(sampled_df) - len(altitude_indices)
            altitude_indices.extend([None] * remaining)
            distance_indices.extend([None] * remaining)
            break
            
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e)
            if "900 times your configured" in error_msg:
                print(f"  ✗ SKIPPED: Area too large for Overpass API (at {elapsed:.1f}s)", flush=True)
                failed_cities.append(f"{city} (area too large)")
            else:
                print(f"  ✗ ERROR: {error_msg[:100]} (at {elapsed:.1f}s)", flush=True)
                failed_cities.append(f"{city} ({type(e).__name__})")
            altitude_indices.append(None)
            distance_indices.append(None)
    
    sampled_df['altitude_index'] = altitude_indices
    sampled_df['distance_index'] = distance_indices
    
    # Remove cities where calculation failed
    original_count = len(sampled_df)
    sampled_df = sampled_df.dropna(subset=['altitude_index', 'distance_index'])
    
    print(f"\n{'='*70}", flush=True)
    print(f"SUMMARY: Successfully calculated indices for {len(sampled_df)}/{original_count} cities", flush=True)
    
    if failed_cities:
        print(f"\nSkipped cities ({len(failed_cities)}):", flush=True)
        for city in failed_cities:
            print(f"  - {city}", flush=True)
    print(f"{'='*70}\n", flush=True)
    
    return sampled_df


def test_altitude_hypothesis(df: pd.DataFrame) -> dict:
    """
    Test Hypothesis 1: Lower A_i = better for cycling
    
    Expected: Negative correlation between altitude_index and score
    """
    print("\n" + "="*70)
    print("HYPOTHESIS 1: The lower the A_i, the better for cycling")
    print("="*70)
    
    # Calculate correlations
    pearson_corr, pearson_p = pearsonr(df['altitude_index'], df['score'])
    spearman_corr, spearman_p = spearmanr(df['altitude_index'], df['score'])
    
    # Linear regression
    X = df[['altitude_index']].values
    y = df['score'].values
    
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    
    print(f"\nCorrelation Analysis:")
    print(f"  Pearson correlation: {pearson_corr:.3f} (p-value: {pearson_p:.4f})")
    print(f"  Spearman correlation: {spearman_corr:.3f} (p-value: {spearman_p:.4f})")
    print(f"\nLinear Regression:")
    print(f"  R² score: {r2:.3f}")
    print(f"  Slope: {model.coef_[0]:.3f}")
    print(f"  Intercept: {model.intercept_:.3f}")
    
    # Interpret results
    print(f"\nInterpretation:")
    if pearson_corr < -0.3 and pearson_p < 0.05:
        print(f"  ✓ HYPOTHESIS SUPPORTED: Significant negative correlation found")
        print(f"    Lower altitude index is associated with higher bicycle scores")
    elif pearson_corr < 0 and pearson_p < 0.05:
        print(f"  ~ HYPOTHESIS PARTIALLY SUPPORTED: Weak negative correlation")
    elif pearson_p >= 0.05:
        print(f"  ✗ HYPOTHESIS NOT SIGNIFICANT: No statistically significant relationship")
    else:
        print(f"  ✗ HYPOTHESIS NOT SUPPORTED: Positive or no correlation found")
    
    return {
        'pearson_r': pearson_corr,
        'pearson_p': pearson_p,
        'spearman_r': spearman_corr,
        'spearman_p': spearman_p,
        'r2': r2,
        'slope': model.coef_[0],
        'intercept': model.intercept_
    }


def test_distance_hypothesis(df: pd.DataFrame) -> dict:
    """
    Test Hypothesis 2: D_i closer to 1 = better for cycling
    
    Expected: Correlation between (1 - abs(1 - D_i)) and score
    """
    print("\n" + "="*70)
    print("HYPOTHESIS 2: The closer to 1 the D_i, the better for cycling")
    print("="*70)
    
    # Calculate "closeness to 1" metric
    df['distance_to_optimal'] = abs(1 - df['distance_index'])
    
    # Calculate correlations (negative correlation expected with distance from 1)
    pearson_corr, pearson_p = pearsonr(df['distance_to_optimal'], df['score'])
    spearman_corr, spearman_p = spearmanr(df['distance_to_optimal'], df['score'])
    
    # Linear regression
    X = df[['distance_to_optimal']].values
    y = df['score'].values
    
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    
    print(f"\nCorrelation Analysis:")
    print(f"  Pearson correlation: {pearson_corr:.3f} (p-value: {pearson_p:.4f})")
    print(f"  Spearman correlation: {spearman_corr:.3f} (p-value: {spearman_p:.4f})")
    print(f"\nLinear Regression:")
    print(f"  R² score: {r2:.3f}")
    print(f"  Slope: {model.coef_[0]:.3f}")
    print(f"  Intercept: {model.intercept_:.3f}")
    
    # Interpret results
    print(f"\nInterpretation:")
    if pearson_corr < -0.3 and pearson_p < 0.05:
        print(f"  ✓ HYPOTHESIS SUPPORTED: Significant negative correlation found")
        print(f"    D_i values closer to 1 are associated with higher bicycle scores")
    elif pearson_corr < 0 and pearson_p < 0.05:
        print(f"  ~ HYPOTHESIS PARTIALLY SUPPORTED: Weak negative correlation")
    elif pearson_p >= 0.05:
        print(f"  ✗ HYPOTHESIS NOT SIGNIFICANT: No statistically significant relationship")
    else:
        print(f"  ✗ HYPOTHESIS NOT SUPPORTED: Positive or no correlation found")
    
    return {
        'pearson_r': pearson_corr,
        'pearson_p': pearson_p,
        'spearman_r': spearman_corr,
        'spearman_p': spearman_p,
        'r2': r2,
        'slope': model.coef_[0],
        'intercept': model.intercept_
    }


def create_visualizations(df: pd.DataFrame, output_dir: str = '../results'):
    """Create visualization plots for the analysis."""
    print("\n" + "="*70)
    print("Creating Visualizations")
    print("="*70)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 10)
    
    # Create a 2x2 subplot figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Altitude Index vs Score
    ax1 = axes[0, 0]
    sns.scatterplot(data=df, x='altitude_index', y='score', s=100, alpha=0.7, ax=ax1)
    
    # Add regression line
    z = np.polyfit(df['altitude_index'], df['score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['altitude_index'].min(), df['altitude_index'].max(), 100)
    ax1.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='Linear fit')
    
    ax1.set_xlabel('Altitude Index (A_i)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Bicycle Cities Index Score', fontsize=12, fontweight='bold')
    ax1.set_title('Hypothesis 1: Altitude Index vs Cycling Performance', fontsize=14, fontweight='bold')
    ax1.legend()
    
    # Add text annotations for some cities
    for idx, row in df.iterrows():
        if idx % 3 == 0:  # Annotate every 3rd city to avoid crowding
            ax1.annotate(row['city'], (row['altitude_index'], row['score']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.7)
    
    # Plot 2: Distance Index vs Score
    ax2 = axes[0, 1]
    sns.scatterplot(data=df, x='distance_index', y='score', s=100, alpha=0.7, ax=ax2)
    
    # Add regression line
    z = np.polyfit(df['distance_index'], df['score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['distance_index'].min(), df['distance_index'].max(), 100)
    ax2.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='Linear fit')
    
    # Add vertical line at D_i = 1 (optimal)
    ax2.axvline(x=1, color='green', linestyle=':', linewidth=2, alpha=0.5, label='Optimal (D_i=1)')
    
    ax2.set_xlabel('Distance Index (D_i)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Bicycle Cities Index Score', fontsize=12, fontweight='bold')
    ax2.set_title('Hypothesis 2: Distance Index vs Cycling Performance', fontsize=14, fontweight='bold')
    ax2.legend()
    
    # Plot 3: Distance from Optimal (|1 - D_i|) vs Score
    ax3 = axes[1, 0]
    df['distance_to_optimal'] = abs(1 - df['distance_index'])
    sns.scatterplot(data=df, x='distance_to_optimal', y='score', s=100, alpha=0.7, ax=ax3)
    
    # Add regression line
    z = np.polyfit(df['distance_to_optimal'], df['score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['distance_to_optimal'].min(), df['distance_to_optimal'].max(), 100)
    ax3.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='Linear fit')
    
    ax3.set_xlabel('Distance from Optimal (|1 - D_i|)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Bicycle Cities Index Score', fontsize=12, fontweight='bold')
    ax3.set_title('Distance from Optimal D_i vs Cycling Performance', fontsize=14, fontweight='bold')
    ax3.legend()
    
    # Plot 4: Combined heatmap showing relationships
    ax4 = axes[1, 1]
    
    # Create correlation matrix
    corr_data = df[['altitude_index', 'distance_index', 'distance_to_optimal', 'score']].corr()
    
    sns.heatmap(corr_data, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax4)
    ax4.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(output_dir, 'hypothesis_testing_results.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved visualization to: {output_path}")
    
    # Also save individual plots for the README
    fig2, ax = plt.subplots(1, 1, figsize=(10, 6))
    sns.scatterplot(data=df, x='altitude_index', y='score', s=150, alpha=0.7)
    z = np.polyfit(df['altitude_index'], df['score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['altitude_index'].min(), df['altitude_index'].max(), 100)
    ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
    ax.set_xlabel('Altitude Index (A_i)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bicycle Cities Index Score', fontsize=12, fontweight='bold')
    ax.set_title('Altitude Index vs Cycling Performance', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'altitude_index_plot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved individual plot: altitude_index_plot.png")
    
    plt.show()


def save_results(df: pd.DataFrame, altitude_results: dict, distance_results: dict, 
                 output_dir: str = '../results'):
    """Save analysis results to CSV files."""
    print("\n" + "="*70)
    print("Saving Results")
    print("="*70)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Save city data with calculated indices
    output_path = os.path.join(output_dir, 'cities_with_indices.csv')
    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved city data to: {output_path}")
    
    # Save statistical results
    results_summary = {
        'Hypothesis': ['Altitude Index (Lower is better)', 'Distance Index (Closer to 1 is better)'],
        'Pearson_r': [altitude_results['pearson_r'], distance_results['pearson_r']],
        'Pearson_p': [altitude_results['pearson_p'], distance_results['pearson_p']],
        'Spearman_r': [altitude_results['spearman_r'], distance_results['spearman_r']],
        'Spearman_p': [altitude_results['spearman_p'], distance_results['spearman_p']],
        'R2_score': [altitude_results['r2'], distance_results['r2']],
        'Slope': [altitude_results['slope'], distance_results['slope']],
        'Intercept': [altitude_results['intercept'], distance_results['intercept']]
    }
    
    results_df = pd.DataFrame(results_summary)
    output_path = os.path.join(output_dir, 'statistical_results.csv')
    results_df.to_csv(output_path, index=False)
    print(f"✓ Saved statistical results to: {output_path}")


def main():
    """Main execution function."""
    print("="*70, flush=True)
    print("BIKENV PREDICTION PLATFORM", flush=True)
    print("Testing Altitude and Distance Index Hypotheses", flush=True)
    print("Data: Copenhagenize Index 2025 Edition", flush=True)
    print("="*70, flush=True)
    
    try:
        # Load data
        data_path = '../data/copenhagenize_index_2025.csv'
        print(f"\nLoading data from: {data_path}", flush=True)
        df = load_bicycle_index_data(data_path)
        print(f"✓ Loaded {len(df)} cities from index", flush=True)
        
        # Calculate indices for sampled cities
        df_with_indices = calculate_indices_for_cities(df, sample_size=15)
        
        # Check if we have enough data to proceed
        if len(df_with_indices) < 5:
            print("\n⚠ ERROR: Not enough cities calculated successfully.", flush=True)
            print(f"Need at least 5 cities, got {len(df_with_indices)}", flush=True)
            print("Cannot perform statistical analysis.", flush=True)
            return
        
        print(f"\nProceeding with analysis using {len(df_with_indices)} cities...", flush=True)
        
        # Test hypotheses
        print("\n" + "="*70, flush=True)
        print("TESTING HYPOTHESES", flush=True)
        print("="*70, flush=True)
        altitude_results = test_altitude_hypothesis(df_with_indices)
        distance_results = test_distance_hypothesis(df_with_indices)
        
        # Create visualizations
        create_visualizations(df_with_indices)
        
        # Save results
        save_results(df_with_indices, altitude_results, distance_results)
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print("\nResults and visualizations have been saved to the 'results/' directory.")
        print("Review the plots and statistical summaries to evaluate the hypotheses.")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Analysis interrupted by user.")
        print("Partial results may be available in the results/ directory.")
        
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        print("Analysis could not be completed.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
