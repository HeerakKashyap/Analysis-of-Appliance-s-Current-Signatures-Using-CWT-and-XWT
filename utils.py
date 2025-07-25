"""
Utility functions for CWT and XWT analysis of appliance current signatures.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import pycwt as wavelet


def load_appliance_data(file_path):
    """
    Load appliance current signature data from CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing appliance data
        
    Returns:
    --------
    pandas.DataFrame
        Loaded data with time and current columns
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def preprocess_signal(signal_data, normalize=True, remove_dc=True):
    """
    Preprocess the signal data for analysis.
    
    Parameters:
    -----------
    signal_data : array-like
        Input signal data
    normalize : bool, optional
        Whether to normalize the signal (default: True)
    remove_dc : bool, optional
        Whether to remove DC component (default: True)
        
    Returns:
    --------
    numpy.ndarray
        Preprocessed signal
    """
    signal_array = np.array(signal_data)
    
    if remove_dc:
        signal_array = signal_array - np.mean(signal_array)
    
    if normalize:
        signal_array = signal_array / np.std(signal_array)
    
    return signal_array


def compute_cwt(signal_data, dt=0.1, dj=0.125, s0=None, J=None, mother=None):
    """
    Compute Continuous Wavelet Transform.
    
    Parameters:
    -----------
    signal_data : array-like
        Input signal
    dt : float
        Sampling interval
    dj : float
        Scale resolution
    s0 : float, optional
        Smallest scale (default: 2*dt)
    J : float, optional
        Number of scales (default: 7/dj)
    mother : wavelet object, optional
        Mother wavelet (default: Morlet with omega0=6)
        
    Returns:
    --------
    tuple
        (wave, scales, freqs, coi, fft, fftfreqs)
    """
    if s0 is None:
        s0 = 2 * dt
    if J is None:
        J = 7 / dj
    if mother is None:
        mother = wavelet.Morlet(6)
    
    return wavelet.cwt(signal_data, dt, dj, s0, J, mother)


def plot_scalogram(time, freqs, power, title="Scalogram", cmap='viridis'):
    """
    Plot scalogram (time-frequency representation).
    
    Parameters:
    -----------
    time : array-like
        Time axis
    freqs : array-like
        Frequency axis
    power : array-like
        Power values
    title : str, optional
        Plot title
    cmap : str, optional
        Colormap for the plot
    """
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(time, freqs, power, shading='auto', cmap=cmap)
    plt.title(title)
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.ylim(freqs[-1], freqs[0])
    plt.colorbar(label='Power')
    plt.tight_layout()
    plt.show()


def compute_xwt(signal1, signal2, dt=0.1, dj=0.125, s0=None, J=None, mother=None):
    """
    Compute Cross Wavelet Transform between two signals.
    
    Parameters:
    -----------
    signal1, signal2 : array-like
        Input signals
    dt : float
        Sampling interval
    dj : float
        Scale resolution
    s0 : float, optional
        Smallest scale
    J : float, optional
        Number of scales
    mother : wavelet object, optional
        Mother wavelet
        
    Returns:
    --------
    tuple
        (xwt_power, xwt_phase, scales, freqs, coi)
    """
    # Compute CWT for both signals
    wave1, scales, freqs, coi, _, _ = compute_cwt(signal1, dt, dj, s0, J, mother)
    wave2, _, _, _, _, _ = compute_cwt(signal2, dt, dj, s0, J, mother)
    
    # Compute XWT
    xwt = wave1 * np.conj(wave2)
    xwt_power = np.abs(xwt)
    xwt_phase = np.angle(xwt)
    
    return xwt_power, xwt_phase, scales, freqs, coi


def save_analysis_results(results, filename):
    """
    Save analysis results to a file.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing analysis results
    filename : str
        Output filename
    """
    try:
        np.savez(filename, **results)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


def load_analysis_results(filename):
    """
    Load analysis results from a file.
    
    Parameters:
    -----------
    filename : str
        Input filename
        
    Returns:
    --------
    dict
        Dictionary containing loaded results
    """
    try:
        results = np.load(filename)
        return dict(results)
    except Exception as e:
        print(f"Error loading results: {e}")
        return None 