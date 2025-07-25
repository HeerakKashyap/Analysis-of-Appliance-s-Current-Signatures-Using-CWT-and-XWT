"""
Test suite for utility functions.
"""

import unittest
import numpy as np
import pandas as pd
import tempfile
import os
from utils import (
    preprocess_signal,
    compute_cwt,
    compute_xwt,
    save_analysis_results,
    load_analysis_results
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self):
        """Set up test data."""
        # Create synthetic test signal
        self.test_signal = np.sin(2 * np.pi * np.linspace(0, 10, 1000))
        self.test_signal2 = np.sin(2 * np.pi * np.linspace(0, 10, 1000) + np.pi/4)
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_preprocess_signal_normalize(self):
        """Test signal preprocessing with normalization."""
        processed = preprocess_signal(self.test_signal, normalize=True, remove_dc=True)
        
        # Check that signal is normalized (std ≈ 1)
        self.assertAlmostEqual(np.std(processed), 1.0, places=1)
        
        # Check that DC component is removed (mean ≈ 0)
        self.assertAlmostEqual(np.mean(processed), 0.0, places=1)
    
    def test_preprocess_signal_no_normalize(self):
        """Test signal preprocessing without normalization."""
        processed = preprocess_signal(self.test_signal, normalize=False, remove_dc=True)
        
        # Check that DC component is removed but signal is not normalized
        self.assertAlmostEqual(np.mean(processed), 0.0, places=1)
        self.assertNotAlmostEqual(np.std(processed), 1.0, places=1)
    
    def test_compute_cwt(self):
        """Test CWT computation."""
        dt = 0.1
        wave, scales, freqs, coi, _, _ = compute_cwt(self.test_signal, dt=dt)
        
        # Check output shapes
        self.assertEqual(wave.shape[0], len(scales))
        self.assertEqual(wave.shape[1], len(self.test_signal))
        self.assertEqual(len(freqs), len(scales))
        self.assertEqual(len(coi), len(self.test_signal))
        
        # Check that scales and frequencies are positive
        self.assertTrue(np.all(scales > 0))
        self.assertTrue(np.all(freqs > 0))
    
    def test_compute_xwt(self):
        """Test XWT computation."""
        dt = 0.1
        xwt_power, xwt_phase, scales, freqs, coi = compute_xwt(
            self.test_signal, self.test_signal2, dt=dt
        )
        
        # Check output shapes
        self.assertEqual(xwt_power.shape[0], len(scales))
        self.assertEqual(xwt_power.shape[1], len(self.test_signal))
        self.assertEqual(xwt_phase.shape, xwt_power.shape)
        
        # Check that power is non-negative
        self.assertTrue(np.all(xwt_power >= 0))
        
        # Check that phase is in [-π, π]
        self.assertTrue(np.all(xwt_phase >= -np.pi))
        self.assertTrue(np.all(xwt_phase <= np.pi))
    
    def test_save_and_load_results(self):
        """Test saving and loading analysis results."""
        # Create test results
        test_results = {
            'signal': self.test_signal,
            'power': np.abs(self.test_signal) ** 2,
            'metadata': {'test': True}
        }
        
        # Save results
        filename = os.path.join(self.temp_dir, 'test_results.npz')
        save_analysis_results(test_results, filename)
        
        # Check that file exists
        self.assertTrue(os.path.exists(filename))
        
        # Load results
        loaded_results = load_analysis_results(filename)
        
        # Check that loaded results match original
        self.assertIsNotNone(loaded_results)
        np.testing.assert_array_equal(loaded_results['signal'], test_results['signal'])
        np.testing.assert_array_equal(loaded_results['power'], test_results['power'])
        self.assertEqual(loaded_results['metadata']['test'], test_results['metadata']['test'])
    
    def test_error_handling(self):
        """Test error handling in utility functions."""
        # Test with empty signal
        with self.assertRaises(Exception):
            compute_cwt([])
        
        # Test with invalid file path
        loaded = load_analysis_results('nonexistent_file.npz')
        self.assertIsNone(loaded)


if __name__ == '__main__':
    unittest.main() 