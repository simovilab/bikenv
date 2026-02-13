"""
Simplified Demo - Testing Platform Proof of Concept

This script demonstrates the platform with synthetic/mock data for cities,
allowing testing without API dependencies.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os


def generate_mock_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate mock altitude and distance indices based on expected patterns.
    
    This is for demonstration purposes only.
    Top-performing cities (high scores) should have:
    - Lower altitude indices (flatter terrain)
    - Distance indices closer to 1 (better connectivity)
    """
    np.random.seed(42)
    
    # Generate altitude indices with negative correlation to score
    # Top cities (high score) get low A_i, bottom cities get high A_i
    df['altitude_index'] = 5.0 - (df['score'] / 100) * 4.0 + np.random.normal(0, 0.5, len(df))
    df['altitude_index'] = df['altitude_index'].clip(lower=0.5)
    
    # Generate distance indices with values closer to 1 for high-scoring cities
    # Top cities get D_i close to 1, others deviate more
    base_distance = 1.0
    df['distance_index'] = base_distance + ((100 - df['score']) / 200) + np.random.normal(0, 0.1, len(df))
    df['distance_index'] = df['distance_index'].clip(lower=0.5, upper=2.0)
    
    return df


def demo_hypothesis_testing():
    """Run a simplified demonstration of the hypothesis testing."""
    
    print("="*70)
    print("BIKENV PREDICTION PLATFORM - DEMO MODE")
    print("Testing with Mock Data")
    print("Data: Copenhagenize Index 2025 Edition")
    print("="*70)
    
    # Load the Copenhagenize data
    df = pd.read_csv('../data/copenhagenize_index_2025.csv')
    print(f"\n✓ Loaded {len(df)} cities from Copenhagenize Index 2025")
    
    # Sample 15 cities across the spectrum
    sampled = pd.concat([
        df.head(5),        # Top performers
        df.iloc[12:17],    # Middle
        df.iloc[25:30]     # Lower
    ]).reset_index(drop=True)
    
    # Generate mock indices
    sampled = generate_mock_indices(sampled)
    
    print(f"\n✓ Generated mock indices for {len(sampled)} cities\n")
    print(sampled[['city', 'score', 'altitude_index', 'distance_index']].to_string(index=False))
    
    # Test Hypothesis 1: Lower A_i = Better for cycling
    print("\n" + "="*70)
    print("HYPOTHESIS 1: Lower A_i = Better for Cycling")
    print("="*70)
    
    corr_altitude, p_altitude = pearsonr(sampled['altitude_index'], sampled['score'])
    print(f"\nPearson correlation: {corr_altitude:.3f} (p-value: {p_altitude:.4f})")
    
    if corr_altitude < -0.3 and p_altitude < 0.05:
        print("✓ HYPOTHESIS SUPPORTED: Significant negative correlation")
    else:
        print("~ Result: Check with real data")
    
    # Test Hypothesis 2: D_i closer to 1 = Better for cycling
    print("\n" + "="*70)
    print("HYPOTHESIS 2: D_i Closer to 1 = Better for Cycling")
    print("="*70)
    
    sampled['distance_from_optimal'] = abs(1 - sampled['distance_index'])
    corr_distance, p_distance = pearsonr(sampled['distance_from_optimal'], sampled['score'])
    print(f"\nPearson correlation: {corr_distance:.3f} (p-value: {p_distance:.4f})")
    
    if corr_distance < -0.3 and p_distance < 0.05:
        print("✓ HYPOTHESIS SUPPORTED: Significant negative correlation")
    else:
        print("~ Result: Check with real data")
    
    # Create visualization
    print("\n" + "="*70)
    print("Creating Visualizations")
    print("="*70)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Altitude Index
    sns.scatterplot(data=sampled, x='altitude_index', y='score', s=100, alpha=0.7, ax=ax1)
    z = np.polyfit(sampled['altitude_index'], sampled['score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(sampled['altitude_index'].min(), sampled['altitude_index'].max(), 100)
    ax1.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
    ax1.set_xlabel('Altitude Index (A_i)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Bicycle Cities Index Score', fontsize=12, fontweight='bold')
    ax1.set_title('Hypothesis 1: Lower A_i = Better Cycling', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Distance Index
    sns.scatterplot(data=sampled, x='distance_index', y='score', s=100, alpha=0.7, ax=ax2)
    ax2.axvline(x=1, color='green', linestyle=':', linewidth=2, alpha=0.5, label='Optimal (D_i=1)')
    z = np.polyfit(sampled['distance_index'], sampled['score'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(sampled['distance_index'].min(), sampled['distance_index'].max(), 100)
    ax2.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2)
    ax2.set_xlabel('Distance Index (D_i)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Bicycle Cities Index Score', fontsize=12, fontweight='bold')
    ax2.set_title('Hypothesis 2: D_i Closer to 1 = Better Cycling', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs('../results', exist_ok=True)
    output_path = '../results/demo_results.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved visualization to: {output_path}")
    
    # Save data
    output_csv = '../results/demo_cities_with_indices.csv'
    sampled.to_csv(output_csv, index=False)
    print(f"✓ Saved data to: {output_csv}")
    
    plt.show()
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nNOTE: This demo uses mock data for demonstration.")
    print("Run prediction_platform.py for analysis with real geographic data.")
    print("\nNext steps:")
    print("  1. Install OSMnx: pip install osmnx")
    print("  2. Run: python prediction_platform.py")
    print("  3. Wait for real data calculation (10-30 minutes)")


if __name__ == "__main__":
    demo_hypothesis_testing()
