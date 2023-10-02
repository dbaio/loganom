"""Reports by Microsoft Teams"""

import logging
import pymsteams


def send_report_teams(plain_text, settings):
    """Send anomalies report by Microsoft Teams webhook

    Arguments:
        plain_text {string} -- Report body in plain text
        settings (dict) -- Settings from the class Config.Teams

    Returns:
        bool -- True/False depending the request result
    """

    report_text = "```\n"
    report_text += plain_text
    report_text += "\n```"

    teams_message = pymsteams.connectorcard(settings['url'])
    teams_message.title(settings['title'])
    teams_message.addLinkButton(settings['button_caption'], settings['button_url'])
    teams_message.text(report_text)

    try:
        teams_message.send()
    except pymsteams.TeamsWebhookException:
        logging.debug('TeamsWebhookException: %s', settings['url'])
        return False

    return True
