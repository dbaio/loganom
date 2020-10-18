"""Processor postfix_sasl
"""

from collections import defaultdict
import logging
import ipaddress
import re

from loganom import utils, process_mail, report_mail, report_mm, exec_cmd
from loganom.report import Report


def postfix_sasl(settings, args):
    """postfix_sasl

    Arguments:
        settings {object} -- Settings from the class Config
        args {object} -- Execution parameters, where is the log path
    """

    pattern_sasl = 'sasl_method='

    logging.debug('Log file: %s', args.log.name)

    # Initialize empty dictionary
    dict_general = defaultdict(set)

    for line in utils.read_logfile(args.log.name, pattern_sasl):
        lista = line.split()
        mail_user = lista.pop().split('sasl_username=')[-1]

        # >/dev/null, ignore this
        lista.pop()

        mail_ip_address = utils.clean_ip(lista.pop())

        logging.debug('%s - %s', mail_user, mail_ip_address)

        if mail_user not in settings.email_skip:
            if ipaddress.ip_address(mail_ip_address).is_private:
                logging.debug('%s private ip address, skipped', mail_ip_address)
            else:
                dict_general[mail_user].add(mail_ip_address)
        else:
            logging.debug('\tskipped by email_skip config')


    temp_set = utils.process_dict(dict_general)
    temp_dict = process_mail.process_mail(dict_general, temp_set, settings)

    # Results
    if len(temp_dict) > 0:
        for email in temp_dict.keys():

            # Execute external script when an anomaly is found for each e-mail
            if args.exec:
                exec_cmd.external_exec(args.exec.name, email)

            report_obj = Report('multi', temp_dict)

        # Report in screen
        print(report_obj.generate_table())

        if settings.smtp.enabled:
            report_mail.send_report_mail(
                report_obj.generate_table(border=False, short=False),
                settings.get_smtp_config())

        if settings.mattermost.enabled:
            report_mm.send_report_mm(
                report_obj.generate_table(),
                settings.get_mm_config())
    else:
        logging.debug('No anomalies')


def quota_high(settings, args):
    """quota_high

    Arguments:
        settings {object} -- Settings from the class Config
        args {object} -- Execution parameters, where is the log path
    """

    pattern = args.quota_message

    logging.debug('Log file: %s', args.log.name)

    # Initialize empty dictionary
    dict_general = defaultdict(int)

    for line in utils.read_logfile(args.log.name, pattern):
        mail_user_raw = re.search('from=<.*?>', line)

        mail_user = utils.clean_email(mail_user_raw.group(0))

        if mail_user:
            dict_general[mail_user] += 1

    # Results
    email_quota_count = 0
    dict_final = defaultdict(int)

    for email, quota_counter in dict_general.items():
        logging.debug('%s (%i)', email, quota_counter)

        if quota_counter > int(args.quota_limit):

            if email not in settings.email_skip:
                dict_final[email] = quota_counter
                email_quota_count += 1

                # Execute external script when an anomaly is found for each e-mail
                if args.exec:
                    exec_cmd.external_exec(args.exec.name, email)
            else:
                logging.debug('\tskipped by email_skip config')

    if email_quota_count > 0:
        report_obj = Report('single', dict_final)
        report_text  = f"Email address(es) that hit quota limit (> {args.quota_limit}):\n\n"

        report_text_mm = report_text
        report_text_mm += report_obj.generate_table()

        report_text_email = report_text
        report_text_email += report_obj.generate_table(border=False, short=False)

        # Report in screen
        print(report_text_mm)

        if settings.smtp.enabled:
            report_mail.send_report_mail(report_text_email, settings.get_smtp_config())

        if settings.mattermost.enabled:
            report_mm.send_report_mm(report_text_mm, settings.get_mm_config())
    else:
        logging.debug('No anomalies')
