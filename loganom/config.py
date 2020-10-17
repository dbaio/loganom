"""Read and set user configurations."""

import sys
import logging
import configparser
from distutils.util import strtobool


class Smtp():
    """SMTP Config Options"""

    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        """Initialize SMTP Config"""
        self.enabled = False
        self.mailfrom = None
        self.mailto = None
        self.host = None
        self.port = None
        self.ssl = None
        self.username = None
        self.password = None
        self.subject = None


    def enable_smtp(self, mailfrom, mailto):
        """Enable SMTP

        Args:
            mailfrom (string): E-mail from
            mailto (string): E-mail to
        """
        self.enabled = True
        self.mailfrom = mailfrom
        self.mailto = mailto


    def set_smtp_host(self, host, port, ssl):
        """Set SMTP Host Details

        Args:
            host (string): SMTP server
            port (integer): SMTP port
            ssl (bool): SMTP ssl (True/False)
        """
        self.host = host
        self.port = port
        self.ssl = ssl


    def set_auth(self, username, password):
        """Set SMTP Authentication Credentials

        Arguments:
            username {string} -- SMTP User Authentication
            password {string} -- SMTP User Password
        """
        self.username = username
        self.password = password


class MatterMost():
    """MatterMost Config Options"""

    def __init__(self):
        """Initialize MatterMost Config"""
        self.enabled = False
        self.url = None
        self.api_key = None
        self.channel = None
        self.icon_url = None
        self.username = None


    def enable_mm(self, url, api_key):
        """Initialize MatterMost Config

        Arguments:
            url {string} -- MatterMost URL
            api_key {string} -- MatterMost API Key
        """
        self.enabled = True
        self.url = url
        self.api_key = api_key


    def set_options(self, channel, icon_url, username):
        """Define MatterMost Options

        Arguments:
            channel {string} -- Name of the channel
            icon_url {string} -- URL with an image
            username {string} -- Username from
        """
        self.channel = channel
        self.icon_url = icon_url
        self.username = username


    def get_url_hook(self):
        """Build MammerMost URL with Api_key

        Returns:
            string - full MM url with api_key
        """
        return f'{self.url}/hooks/{self.api_key}'


class Config():
    """Config Class to store all configurations."""

    def __init__(self, pattern_ip, pattern_org, ipinfo_token, country_ignore):
        """Initialize Configuration

        Args:
            pattern_ip (list): List of ip name patterns that will be ignored
            pattern_org (list): List of ASN's that will be ignored
            ipinfo_token (string): IPInfo Api Token
            country_ignore (list): List of country codes that will be ignored
        """
        self.pattern_ip = pattern_ip
        self.pattern_org = pattern_org
        self.ipinfo_token = ipinfo_token
        self.country_ignore = country_ignore
        self.email_skip = []
        self.smtp = Smtp()
        self.mattermost = MatterMost()


    def set_email_skip(self, email_skip):
        """ Set Email Skip

        REMOVER ISSO

        Args:
            email_skip (list): List of email address
        """
        self.email_skip = email_skip


    def get_smtp_config(self):
        """If SMTP is enabled, return it's configuration

        Returns:
            Dict - All SMTP config
        """
        if self.smtp:
            config = {}
            config['mailfrom'] = self.smtp.mailfrom
            config['mailto'] = self.smtp.mailto
            config['host'] = self.smtp.host
            config['port'] = self.smtp.port
            config['ssl'] = self.smtp.ssl
            config['username'] = self.smtp.username
            config['password'] = self.smtp.password
            config['subject'] = self.smtp.subject
            return config

        return None


    def get_mm_config(self):
        """If MatterMost is enabled, return it's configuration

        Returns:
            Dict - All MatterMost config
        """
        if self.smtp:
            config = {}
            config['url'] = self.mattermost.get_url_hook()
            config['channel'] = self.mattermost.channel
            config['icon_url'] = self.mattermost.icon_url
            config['username'] = self.mattermost.username
            return config

        return None


def read_config(config_file):
    """read_config

    Read user configurations and save it to the Config class.

    Arguments:
        config_file {string} -- Path of the config file
    """

    logging.debug('Starting validating configuration file...')
    config = configparser.ConfigParser()
    config.read(config_file.name)

    # Get General Section
    try:
        my_config = Config(
            config.get('GENERAL', 'pattern_ip'),
            config.get('GENERAL', 'pattern_org'),
            config.get('GENERAL', 'ipinfo_token'),
            config.get('GENERAL', 'country_ignore'))

    except configparser.NoOptionError:
        logging.info('Error reading config, GENERAL section')
        sys.exit(1)

    try:
        my_config.set_email_skip(config.get('GENERAL', 'email_skip'))
    except configparser.NoOptionError:
        logging.debug('Optional config (email_skip) not found')

    # Get SMTP Section
    try:
        smtp_enabled = config.get('SMTP', 'enabled')
    except configparser.NoOptionError:
        smtp_enabled = 'False'

    if strtobool(smtp_enabled):
        try:
            my_config.smtp.enable_smtp(
                config.get('SMTP', 'from'),
                config.get('SMTP', 'to'))

            my_config.smtp.set_smtp_host(
                config.get('SMTP', 'host'),
                config.get('SMTP', 'port'),
                config.get('SMTP', 'ssl'))

            my_config.smtp.set_auth(
                config.get('SMTP', 'user'),
                config.get('SMTP', 'pass'))

            my_config.smtp.subject = config.get('SMTP', 'subject')

        except configparser.NoOptionError:
            logging.info('Error reading config, SMTP section')
            sys.exit(1)

    # Get MatterMost Section
    try:
        mm_enabled = config.get('MATTERMOST', 'enabled')
    except configparser.NoOptionError:
        mm_enabled = 'False'

    if strtobool(mm_enabled):
        try:
            my_config.mattermost.enable_mm(
                config.get('MATTERMOST', 'url'),
                config.get('MATTERMOST', 'api_key'))

            my_config.mattermost.set_options(
                config.get('MATTERMOST', 'channel'),
                config.get('MATTERMOST', 'icon_url'),
                config.get('MATTERMOST', 'username'))

        except configparser.NoOptionError:
            logging.info('Error reading config, MATTERMOST section')
            sys.exit(1)

    return my_config
