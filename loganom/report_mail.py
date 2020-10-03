"""Reports by email
"""

# Workaround Python3.8 issue
# https://github.com/marrow/mailer/issues/87
import sys
sys.modules["cgi.parse_qsl"] = None
from marrow.mailer import Message, Mailer


def send_report_mail(plain_text, settings):
    """Send anomalies report by email

    Arguments:
        plain_text {string} -- Report body in plain text
        settings {object} -- Settings from the class Config

    Returns:
    """

    report_text = '\n'.join(plain_text)

    mailer = Mailer({
        'manager.use': 'futures',
        'transport.use': 'smtp',
        'transport.host': settings.smtp_host,
        'transport.tls': settings.smtp_ssl,
        'transport.debug': False,
        'transport.username': settings.smtp_user,
        'transport.password': settings.smtp_pass,
        'transport.max_messages_per_connection': 5
    })

    mailer.start()

    message = Message(author=settings.smtp_from, to=settings.smtp_to)
    message.subject = settings.smtp_subject
    message.plain = report_text

    mailer.send(message)
    mailer.stop()

    return True
