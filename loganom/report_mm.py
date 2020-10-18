"""Reports by MatterMost"""

import logging
import requests


def send_report_mm(plain_text, settings):
    """Send anomalies report by email

    Arguments:
        plain_text {string} -- Report body in plain text
        settings (dict) -- Settings from the class Config.MatterMost

    Returns:
        bool -- True/False depending the request result
    """

    report_text = "```\n"
    report_text += plain_text
    report_text += "\n```"

    payload = dict()
    payload['text'] = report_text
    payload['channel'] = settings['channel']
    payload['icon_url'] = settings['icon_url']
    payload['username'] = settings['username']
    mm_url = settings['url']

    try:
        response = requests.post(mm_url, json=payload)
    except requests.RequestException:
        logging.debug('Mattermost RequestException: %s', settings.mm_url)
        return False

    if response.status_code != 200:
        logging.debug('Mattermost status != 200: %s', settings.mm_url)
        return False

    return True
