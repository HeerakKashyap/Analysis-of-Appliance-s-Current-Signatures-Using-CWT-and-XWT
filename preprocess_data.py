#!/usr/bin/env python3
"""
Data preprocessing script for appliance current signatures.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def clean_data(data, remove_outliers=True, threshold=3):
    """
    Clean the data by removing outliers and invalid values.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Input data
    remove_outliers : bool
        Whether to remove outliers using z-score
    threshold : float
        Z-score threshold for outlier detection
        
    Returns:
    --------
    pandas.DataFrame
        Cleaned data
    """
    # Remove NaN values
    data = data.dropna()
    
    # Remove infinite values
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.dropna()
    
    if remove_outliers:
        # Remove outliers using z-score
        z_scores = np.abs((data - data.mean()) / data.std())
        data = data[(z_scores < threshold).all(axis=1)]
    
    return data


def normalize_data(data, method='zscore'):
    """
    Normalize the data using different methods.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Input data
    method : str
        Normalization method ('zscore', 'minmax', 'robust')
        
    Returns:
    --------
    pandas.DataFrame
        Normalized data
    """
    if method == 'zscore':
        return (data - data.mean()) / data.std()
    elif method == 'minmax':
        return (data - data.min()) / (data.max() - data.min())
    elif method == 'robust':
        return (data - data.median()) / (data.quantile(0.75) - data.quantile(0.25))
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def segment_data(data, segment_length=1000, overlap=0.5):
    """
    Segment the data into smaller chunks for analysis.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Input data
    segment_length : int
        Length of each segment
    overlap : float
        Overlap ratio between segments (0-1)
        
    Returns:
    --------
    list
        List of data segments
    """
    segments = []
    step = int(segment_length * (1 - overlap))
    
    for i in range(0, len(data) - segment_length + 1, step):
        segment = data.iloc[i:i + segment_length]
        segments.append(segment)
    
    return segments


def process_csv_file(file_path, output_dir='processed_data'):
    """
    Process a single CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    output_dir : str
        Output directory for processed files
    """
    print(f"Processing {file_path}...")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load data
    data = pd.read_csv(file_path)
    
    # Clean data
    data_clean = clean_data(data)
    
    # Normalize data
    data_normalized = normalize_data(data_clean)
    
    # Save processed data
    base_name = Path(file_path).stem
    output_path = Path(output_dir) / f"{base_name}_processed.csv"
    data_normalized.to_csv(output_path, index=False)
    
    print(f"Saved processed data to {output_path}")
    
    return data_normalized


def main():
    """Main preprocessing function."""
    print("Data Preprocessing for Appliance Current Signatures")
    print("=" * 50)
    
    # Get all CSV files in current directory
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and not f.endswith('_processed.csv')]
    
    if not csv_files:
        print("No CSV files found in current directory.")
        return
    
    print(f"Found {len(csv_files)} CSV files to process:")
    for file in csv_files:
        print(f"  - {file}")
    
    # Process each file
    for file in csv_files:
        try:
            process_csv_file(file)
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    print("\nPreprocessing complete!")


if __name__ == "__main__":
    main() 