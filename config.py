"""
Configuration file for appliance current signature analysis.
"""

# Analysis Parameters
ANALYSIS_CONFIG = {
    # Sampling parameters
    'sampling_interval': 0.1,  # seconds
    'scale_resolution': 0.125,
    'smallest_scale': None,  # Will be set to 2*dt
    'number_of_scales': None,  # Will be set to 7/dj
    
    # Wavelet parameters
    'mother_wavelet': 'Morlet',
    'omega0': 6,  # For Morlet wavelet
    
    # Preprocessing parameters
    'normalize_signal': True,
    'remove_dc_component': True,
    
    # Visualization parameters
    'figure_size': (12, 6),
    'colormap': 'viridis',
    'dpi': 100,
    
    # Output parameters
    'save_plots': True,
    'plot_format': 'png',
    'results_filename': 'appliance_analysis_results.npz'
}

# File patterns
FILE_PATTERNS = {
    'data_files': '*.csv',
    'processed_files': '*_processed.csv',
    'exclude_patterns': ['*_processed.csv', '*.git*']
}

# Plotting styles
PLOT_STYLES = {
    'default_style': 'seaborn-v0_8',
    'font_size': 12,
    'line_width': 2,
    'marker_size': 6
}

# Error handling
ERROR_CONFIG = {
    'max_file_size_mb': 100,  # Skip files larger than this
    'min_signal_length': 100,  # Minimum signal length to process
    'verbose': True
}

# Performance settings
PERFORMANCE_CONFIG = {
    'use_multiprocessing': False,
    'max_workers': 4,
    'chunk_size': 1000
} 