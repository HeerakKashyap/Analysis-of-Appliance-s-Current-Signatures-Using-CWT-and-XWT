*This repository presents an in-depth analysis of electrical appliance current signatures using Continuous Wavelet Transform (CWT) and Cross Wavelet Transform (XWT). The project demonstrates how time-frequency analysis techniques can be leveraged to extract, visualize, and compare the unique current signatures of different appliances, aiding in tasks such as appliance identification, monitoring, and non-intrusive load monitoring (NILM).
---

**Key Features**
*Data Acquisition and Preprocessing*
The notebook loads and preprocesses current signal data for various household appliances. Data normalization and segmentation ensure robust analysis and visualization.

---
*Continuous Wavelet Transform (CWT) Application*
Implements CWT using the Morlet wavelet to analyze the time-frequency characteristics of appliance current signals.

Produces scalograms (time-frequency heatmaps) that reveal transient and steady-state behaviors of each appliance.

Utilizes scipy.signal.cwt for the transformation, with a note that PyWavelets is recommended for future work due to deprecation in SciPy.

---
**Cross Wavelet Transform (XWT) Analysis**
