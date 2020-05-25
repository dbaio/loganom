"""Read and set user configurations."""

import sys
import logging
import configparser
from distutils.util import strtobool


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
        my_config = Config(config.get('GENERAL', 'pattern_ip'),
                           config.get('GENERAL', 'pattern_org'),
                           config.get('GENERAL', 'ipinfo_token'),
                           config.get('GENERAL', 'country_ignore'))

    except configparser.NoOptionError:
        logging.info('Error reading config, GENERAL section')
        sys.exit(1)

    # Get SMTP Section
    try:
        smtp_enabled = config.get('SMTP', 'enabled')
    except configparser.NoOptionError:
        smtp_enabled = False

    if strtobool(smtp_enabled):
        try:
            my_config.set_smtp(True,
                               config.get('SMTP', 'from'),
                               config.get('SMTP', 'to'))

            my_config.set_smtp_host(config.get('SMTP', 'host'),
                                    config.get('SMTP', 'port'),
                                    config.get('SMTP', 'ssl'))

            my_config.set_smtp_auth(config.get('SMTP', 'user'),
                                    config.get('SMTP', 'pass'))

            my_config.set_smtp_subject(config.get('SMTP', 'subject'))

        except configparser.NoOptionError:
            logging.info('Error reading config, SMTP section')
            sys.exit(1)

    # Get MatterMost Section
    try:
        mm_enabled = config.get('MATTERMOST', 'enabled')
    except configparser.NoOptionError:
        mm_enabled = False

    if strtobool(mm_enabled):
        try:
            my_config.set_mm(True,
                             config.get('MATTERMOST', 'url'),
                             config.get('MATTERMOST', 'api_key'))

            my_config.set_mm_options(config.get('MATTERMOST', 'channel'),
                                     config.get('MATTERMOST', 'icon_url'),
                                     config.get('MATTERMOST', 'username'))

        except configparser.NoOptionError:
            logging.info('Error reading config, MATTERMOST section')
            sys.exit(1)

    return my_config


class Config():
    """Config

    Class to store configurations
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, pattern_ip, pattern_org, ipinfo_token, country_ignore):

        self.pattern_ip = pattern_ip
        self.pattern_org = pattern_org
        self.ipinfo_token = ipinfo_token
        self.country_ignore = country_ignore

        self.smtp_enabled = False
        self.smtp_from = None
        self.smtp_to = None
        self.smtp_host = None
        self.smtp_port = None
        self.smtp_ssl = None
        self.smtp_user = None
        self.smtp_pass = None
        self.smtp_subject = None

        self.mm_enabled = False
        self.mm_url = None
        self.mm_api_key = None
        self.mm_channel = None
        self.mm_icon_url = None
        self.mm_username = None


    def set_smtp(self, enabled, smtp_from, smtp_to):
        """Define SMTP Notifications

        Arguments:
            enabled {bool} -- SMTP Notifications (Enabled/Disabled)
            smtp_from {string} -- E-mail from
            smtp_to {string} -- E-mail to
        """
        self.smtp_enabled = enabled
        self.smtp_from = smtp_from
        self.smtp_to = smtp_to


    def set_smtp_host(self, smtp_host, smtp_port, smtp_ssl):
        """Set SMTP Server

        Arguments:
            smtp_host {string} -- SMTP server
            smtp_port {integer} -- SMTP port
            smtp_ssl {string} -- SMTP ssl (True/False)
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_ssl = smtp_ssl


    def set_smtp_auth(self, smtp_user, smtp_pass):
        """Set SMTP Authentication Credentials

        Arguments:
            smtp_user {string} -- SMTP User Authentication
            smtp_pass {string} -- SMTP User Password
        """
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass


    def set_smtp_subject(self, smtp_subject):
        """Set SMTP Subject

        Arguments:
            smtp_subject {string} -- SMTP Subject
        """
        self.smtp_subject = smtp_subject


    def set_mm(self, enabled, mm_url, mm_api_key):
        """Define MatterMost Notifications

        Arguments:
            enabled {string} -- MatterMost Notifications (Enabled/Disabled)
            mm_url {string} -- MatterMost URL
        """
        self.mm_enabled = enabled
        self.mm_url = mm_url
        self.mm_api_key = mm_api_key


    def set_mm_options(self, mm_channel, mm_icon_url, mm_username):
        """Define MatterMost Options

        Arguments:
            channel {string} -- Name of the channel
            icon_url {string} -- URL with an image
            username {string} -- Username from
        """

        self.mm_channel = mm_channel
        self.mm_icon_url = mm_icon_url
        self.mm_username = mm_username
