"""Configuration Tests"""

import unittest
from collections import OrderedDict
import pytest
from loganom.config import read_config, Config


class TestConfigDefault(unittest.TestCase):
    """Unittest for config.read_config()."""

    def setUp(self):
        """Populate config dictionary."""

        # Simulating argparse dictionary
        self.config = OrderedDict()
        self.config.name = "tests/data/config-sample.ini"

    def test_config_read_sample(self):
        """Test for Read the Sample Config File."""

        try:
            open(self.config.name)
        except FileNotFoundError:
            pytest.skip("config file not found")

        config_obj = read_config(self.config)
        self.assertIsInstance(config_obj, Config)

    def test_config_smtp_false(self):
        """Test for Read the Sample Config File (Smtp Section)."""

        try:
            open(self.config.name)
        except FileNotFoundError:
            pytest.skip("config file not found")

        config_obj = read_config(self.config)
        self.assertFalse(config_obj.smtp_enabled)

    def test_config_mm_false(self):
        """Test for Read the Sample Config File (MM Section)."""

        try:
            open(self.config.name)
        except FileNotFoundError:
            pytest.skip("config file not found")

        config_obj = read_config(self.config)
        self.assertFalse(config_obj.mm_enabled)


class TestConfigTrue(unittest.TestCase):
    """Unittest for config.read_config() with True values"""

    def setUp(self):
        """Populate config dictionary."""

        # Simulating argparse dictionary
        self.config = OrderedDict()
        self.config.name = "tests/data/config2.ini"

    def test_config_smtp_true(self):
        """Test for Read the Sample Config File (Smtp Section)."""

        try:
            open(self.config.name)
        except FileNotFoundError:
            pytest.skip("config file not found")

        config_obj = read_config(self.config)
        self.assertTrue(config_obj.smtp_enabled)

    def test_config_mm_true(self):
        """Test for Read the Sample Config File (MM Section)."""

        try:
            open(self.config.name)
        except FileNotFoundError:
            pytest.skip("config file not found")

        config_obj = read_config(self.config)
        self.assertTrue(config_obj.mm_enabled)
