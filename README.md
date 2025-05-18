*This repository presents an in-depth analysis of electrical appliance current signatures using Continuous Wavelet Transform (CWT) and Cross Wavelet Transform (XWT). The project demonstrates how time-frequency analysis techniques can be leveraged to extract, visualize, and compare the unique current signatures of different appliances, aiding in tasks such as appliance identification, monitoring, and non-intrusive load monitoring (NILM).
---
*Key Features
---
*Data Acquisition and Preprocessing*
The notebook loads and preprocesses current signal data for various household appliances. Data normalization and segmentation ensure robust analysis and visualization.

---
*Continuous Wavelet Transform (CWT) Application*
-
Implements CWT using the Morlet wavelet to analyze the time-frequency characteristics of appliance current signals.

Produces scalograms (time-frequency heatmaps) that reveal transient and steady-state behaviors of each appliance.

Utilizes scipy.signal.cwt for the transformation, with a note that PyWavelets is recommended for future work due to deprecation in SciPy.

---
**Cross Wavelet Transform (XWT) Analysis**
Compares the time-frequency features of two different appliance signals.
Highlights regions of high common power and phase relationships, useful for identifying correlated events or distinguishing between appliances.
-
*nterpretation and Conclusions*
-
Demonstrates that CWT effectively captures both steady-state and transient features in appliance current signatures.
Shows that XWT can reveal similarities and differences between appliances, supporting advanced NILM and event detection tasks.
Provides a foundation for further work in appliance classification and energy disaggregation.
