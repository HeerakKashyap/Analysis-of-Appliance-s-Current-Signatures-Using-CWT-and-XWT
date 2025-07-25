# Analysis of Appliance Current Signatures Using CWT and XWT

This repository presents an in-depth analysis of electrical appliance current signatures using Continuous Wavelet Transform (CWT) and Cross Wavelet Transform (XWT). The project demonstrates how time-frequency analysis techniques can be leveraged to extract, visualize, and compare the unique current signatures of different appliances, aiding in tasks such as appliance identification, monitoring, and non-intrusive load monitoring (NILM).

## 🚀 Key Features

### Data Acquisition and Preprocessing
- Loads and preprocesses current signal data for various household appliances
- Data normalization and segmentation ensure robust analysis and visualization
- Automatic handling of different data formats and file structures

### Continuous Wavelet Transform (CWT) Application
- Implements CWT using the Morlet wavelet to analyze time-frequency characteristics
- Produces scalograms (time-frequency heatmaps) revealing transient and steady-state behaviors
- Utilizes PyWavelets for robust wavelet transformations
- Configurable parameters for different analysis requirements

### Cross Wavelet Transform (XWT) Analysis
- Compares time-frequency features between different appliance signals
- Highlights regions of high common power and phase relationships
- Useful for identifying correlated events or distinguishing between appliances
- Provides quantitative measures of similarity between appliance signatures

## 📁 Project Structure

```
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── config.py                    # Configuration parameters
├── utils.py                     # Utility functions
├── analyze_appliances.py        # Main analysis script
├── test_utils.py                # Unit tests
├── cwt_test.ipynb              # CWT demonstration notebook
├── Implementation.ipynb         # Main implementation notebook
└── *.csv                       # Appliance data files
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Analysis-of-Appliance-s-Current-Signatures-Using-CWT-and-XWT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📊 Usage

### Quick Start
Run the main analysis script:
```bash
python analyze_appliances.py
```

### Using Jupyter Notebooks
1. Start Jupyter:
```bash
jupyter notebook
```

2. Open `Implementation.ipynb` for the main analysis
3. Open `cwt_test.ipynb` for CWT demonstrations

### Custom Analysis
```python
from utils import load_appliance_data, compute_cwt, plot_scalogram

# Load data
data = load_appliance_data('appliance_data.csv')

# Compute CWT
wave, scales, freqs, coi, _, _ = compute_cwt(data['current'].values)

# Plot results
plot_scalogram(time, freqs, np.abs(wave)**2, title="Appliance Signature")
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest test_utils.py
```

Or run individual tests:
```bash
python test_utils.py
```

## 📈 Results and Interpretation

### CWT Analysis
- **Steady-state features**: Captures the characteristic frequency components of each appliance
- **Transient features**: Reveals startup/shutdown behaviors and load changes
- **Time-frequency localization**: Provides precise timing of events

### XWT Analysis
- **Similarity detection**: Identifies common patterns between appliances
- **Phase relationships**: Shows temporal correlations between different signals
- **Feature extraction**: Enables automated appliance classification

## 🔧 Configuration

Modify `config.py` to adjust analysis parameters:
- Sampling intervals and scale resolutions
- Wavelet parameters and preprocessing options
- Visualization settings and output formats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- PyWavelets library for wavelet transformations
- SciPy and NumPy for numerical computations
- Matplotlib for visualization capabilities
