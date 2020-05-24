"""Test for the Auxiliary functions"""

import unittest

from collections import defaultdict
from loganom.utils import clean_ip, process_dict, check_ip_on_whitelist, check_org_on_whitelist


class TestCleanIp(unittest.TestCase):
    """Unittest for utils.clean_ip()."""

    def test_clean_ip(self):
        """Test for Clean a raw ip address from the log file."""

        raw_ip = 'client=mail-ed1-f51.google.com[209.85.208.51]'
        result = clean_ip(raw_ip)
        self.assertEqual(result, '209.85.208.51')


class TestProcessDict(unittest.TestCase):
    """Unittest for utils.process_dict()."""

    def setUp(self):
        """Populate dictionary."""

        self.dict_general = defaultdict(set)

        mail_ip_address = clean_ip('client=mail-ed1-f51.google.com[209.85.208.51]')
        self.dict_general['userA@domain'].add(mail_ip_address)

        mail_ip_address = clean_ip('client=mail-ed1-f51.google.com[209.85.208.52]')
        self.dict_general['userA@domain'].add(mail_ip_address)

        mail_ip_address = clean_ip('client=mail-ed1-f51.google.com[209.85.208.51]')
        self.dict_general['userB@domain'].add(mail_ip_address)

        self.temp_set = process_dict(self.dict_general)


    def test_process_dict_true(self):
        """Test for Processor of the General Dictionary."""

        self.assertIn('userA@domain', self.temp_set)


    def test_process_dict_false(self):
        """Test for Processor of the General Dictionary."""

        self.assertNotIn('userB@domain', self.temp_set)


class TestCheckIpOnWhitelist(unittest.TestCase):
    """Unittest for utils.check_ip_on_whitelist()."""

    def setUp(self):
        """Populate list."""

        self.pattern_ip = ['amazonaws.com',
                           'google',
                           '.com.br',
                           '.net.br']


    def test_check_ip_on_whitelist_true(self):
        """Test for Check if the ip address can be ignored."""

        ip_name = 'mail-ed1-f51.google.com'

        result = check_ip_on_whitelist(ip_name, self.pattern_ip)

        self.assertTrue(result)


    def test_check_ip_on_whitelist_false(self):
        """Test for Check if the ip address can be ignored."""

        ip_name = 'f11.my.com'

        result = check_ip_on_whitelist(ip_name, self.pattern_ip)

        self.assertFalse(result)


class TestCheckOrgOnWhitelist(unittest.TestCase):
    """Unittest for utils.check_org_on_whitelist()."""

    def setUp(self):
        """Populate list."""

        self.pattern_org = ['AS8075', 'AS36351']


    def test_check_org_on_whitelist_true(self):
        """Test for Check if the ip address can be ignored based on it's ASN."""

        org_name = 'AS36351'

        result = check_org_on_whitelist(org_name, self.pattern_org)

        self.assertTrue(result)


    def test_check_org_on_whitelist_false(self):
        """Test for Check if the ip address can be ignored based on it's ASN."""

        org_name = 'AS10429'

        result = check_org_on_whitelist(org_name, self.pattern_org)

        self.assertFalse(result)
