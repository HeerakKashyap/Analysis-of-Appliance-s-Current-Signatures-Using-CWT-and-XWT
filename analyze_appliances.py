#!/usr/bin/env python3
"""
Appliance Current Signature Analysis Script

This script analyzes electrical appliance current signatures using CWT and XWT.
It processes multiple appliance datasets and generates comparative analysis.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils import (
    load_appliance_data, 
    preprocess_signal, 
    compute_cwt, 
    compute_xwt,
    plot_scalogram,
    save_analysis_results
)


def analyze_single_appliance(file_path, appliance_name):
    """
    Analyze a single appliance's current signature.
    
    Parameters:
    -----------
    file_path : str
        Path to the appliance data file
    appliance_name : str
        Name of the appliance for labeling
        
    Returns:
    --------
    dict
        Analysis results
    """
    print(f"Analyzing {appliance_name}...")
    
    # Load data
    data = load_appliance_data(file_path)
    if data is None:
        return None
    
    # Extract current signal (assuming first column is time, second is current)
    if len(data.columns) >= 2:
        current_signal = data.iloc[:, 1].values
    else:
        current_signal = data.iloc[:, 0].values
    
    # Preprocess signal
    processed_signal = preprocess_signal(current_signal)
    
    # Compute CWT
    dt = 0.1  # Sampling interval
    wave, scales, freqs, coi, _, _ = compute_cwt(processed_signal, dt=dt)
    power = np.abs(wave) ** 2
    
    # Create time axis
    time = np.arange(len(processed_signal)) * dt
    
    # Plot results
    plot_scalogram(time, freqs, power, title=f"CWT Scalogram - {appliance_name}")
    
    # Store results
    results = {
        'appliance_name': appliance_name,
        'signal': processed_signal,
        'cwt_power': power,
        'scales': scales,
        'frequencies': freqs,
        'time': time,
        'cone_of_influence': coi
    }
    
    return results


def compare_appliances(file1, file2, name1, name2):
    """
    Compare two appliances using Cross Wavelet Transform.
    
    Parameters:
    -----------
    file1, file2 : str
        Paths to appliance data files
    name1, name2 : str
        Names of the appliances
        
    Returns:
    --------
    dict
        Comparison results
    """
    print(f"Comparing {name1} vs {name2}...")
    
    # Load and preprocess both signals
    data1 = load_appliance_data(file1)
    data2 = load_appliance_data(file2)
    
    if data1 is None or data2 is None:
        return None
    
    # Extract current signals
    if len(data1.columns) >= 2:
        signal1 = data1.iloc[:, 1].values
    else:
        signal1 = data1.iloc[:, 0].values
        
    if len(data2.columns) >= 2:
        signal2 = data2.iloc[:, 1].values
    else:
        signal2 = data2.iloc[:, 0].values
    
    # Preprocess signals
    processed_signal1 = preprocess_signal(signal1)
    processed_signal2 = preprocess_signal(signal2)
    
    # Ensure same length for comparison
    min_length = min(len(processed_signal1), len(processed_signal2))
    processed_signal1 = processed_signal1[:min_length]
    processed_signal2 = processed_signal2[:min_length]
    
    # Compute XWT
    dt = 0.1
    xwt_power, xwt_phase, scales, freqs, coi = compute_xwt(
        processed_signal1, processed_signal2, dt=dt
    )
    
    # Create time axis
    time = np.arange(min_length) * dt
    
    # Plot XWT results
    fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # XWT Power
    pcm = axs[0].pcolormesh(time, freqs, xwt_power, shading='auto', cmap='viridis')
    axs[0].plot(time, 1/coi, 'w--', linewidth=2, label='Cone of Influence')
    axs[0].set_title(f'Cross Wavelet Power: {name1} vs {name2}')
    axs[0].set_ylabel('Frequency (Hz)')
    axs[0].set_ylim(freqs[-1], freqs[0])
    fig.colorbar(pcm, ax=axs[0], label='Power')
    axs[0].legend()
    
    # XWT Phase
    pcm2 = axs[1].pcolormesh(time, freqs, xwt_phase, shading='auto', cmap='twilight')
    axs[1].plot(time, 1/coi, 'w--', linewidth=2)
    axs[1].set_title(f'Cross Wavelet Phase Difference: {name1} vs {name2}')
    axs[1].set_ylabel('Frequency (Hz)')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylim(freqs[-1], freqs[0])
    fig.colorbar(pcm2, ax=axs[1], label='Phase (radians)')
    
    plt.tight_layout()
    plt.show()
    
    # Store results
    results = {
        'appliance1': name1,
        'appliance2': name2,
        'signal1': processed_signal1,
        'signal2': processed_signal2,
        'xwt_power': xwt_power,
        'xwt_phase': xwt_phase,
        'scales': scales,
        'frequencies': freqs,
        'time': time,
        'cone_of_influence': coi
    }
    
    return results


def main():
    """Main analysis function."""
    print("Appliance Current Signature Analysis")
    print("=" * 40)
    
    # Get list of CSV files
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and not f.endswith('_processed.csv')]
    
    if not csv_files:
        print("No CSV files found in current directory.")
        return
    
    print(f"Found {len(csv_files)} CSV files:")
    for i, file in enumerate(csv_files):
        print(f"  {i+1}. {file}")
    
    # Analyze each appliance individually
    all_results = {}
    
    for file in csv_files[:3]:  # Limit to first 3 files for demonstration
        appliance_name = file.replace('.csv', '').replace('_', ' ').title()
        results = analyze_single_appliance(file, appliance_name)
        if results:
            all_results[appliance_name] = results
    
    # Compare appliances pairwise
    if len(csv_files) >= 2:
        print("\nPerforming pairwise comparisons...")
        for i in range(min(2, len(csv_files))):
            for j in range(i+1, min(3, len(csv_files))):
                name1 = csv_files[i].replace('.csv', '').replace('_', ' ').title()
                name2 = csv_files[j].replace('.csv', '').replace('_', ' ').title()
                
                comparison_results = compare_appliances(
                    csv_files[i], csv_files[j], name1, name2
                )
                
                if comparison_results:
                    all_results[f"{name1}_vs_{name2}"] = comparison_results
    
    # Save all results
    if all_results:
        save_analysis_results(all_results, 'appliance_analysis_results.npz')
        print("\nAnalysis complete! Results saved to 'appliance_analysis_results.npz'")


if __name__ == "__main__":
    main() 