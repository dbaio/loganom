"""Reports by email
"""

# Workaround Python3.8 issue
# https://github.com/marrow/mailer/issues/87
# pylint: disable=C0413
import sys
sys.modules["cgi.parse_qsl"] = None
from marrow.mailer import Message, Mailer


def send_report_mail(plain_text, settings):
    """Send anomalies report by email

    Arguments:
        plain_text {string} -- Report body in plain text
        settings (dict) -- Settings from the class Config.Smtp

    Returns:
    """

    mailer = Mailer({
        'manager.use': 'futures',
        'transport.use': 'smtp',
        'transport.host': settings['host'],
        'transport.tls': settings['ssl'],
        'transport.debug': False,
        'transport.username': settings['username'],
        'transport.password': settings['password'],
        'transport.max_messages_per_connection': 5
    })

    mailer.start()

    message = Message(author=settings['mailfrom'], to=settings['mailto'])
    message.subject = settings['subject']
    message.plain = plain_text

    mailer.send(message)
    mailer.stop()

    return True
