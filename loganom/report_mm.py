"""Reports by MatterMost"""

import logging
import requests


def mm_url_hook(url, api_key):
    """Build MammerMost URL with Api_key

    Arguments:
        url {[type]} -- Mattermost URL
        api_key {[type]} -- Mattermost Api_key

    Returns:
        string - full MM url with api_key
    """
    return '{}/hooks/{}'.format(url, api_key)


def send_report_mm(plain_text, settings):
    """Send anomalies report by email

    Arguments:
        plain_text {string} -- Report body in plain text
        settings {object} -- Settings from the class Config

    Returns:
        bool -- True/False depending the request result
    """

    payload = dict()
    payload['text'] = plain_text
    payload['channel'] = settings.mm_channel
    payload['icon_url'] = settings.mm_icon_url
    payload['username'] = settings.mm_username

    mm_url = mm_url_hook(settings.mm_url, settings.mm_api_key)

    try:
        response = requests.post(mm_url, json=payload)
    except requests.RequestException:
        logging.debug('Mattermost RequestException: %s', settings.mm_url)
        return False

    if response.status_code != 200:
        logging.debug('Mattermost status != 200: %s', settings.mm_url)
        return False

    return True
