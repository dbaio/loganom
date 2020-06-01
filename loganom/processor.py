"""Processor postfix_sasl
"""

from collections import defaultdict
import logging
import ipaddress

from loganom import utils, process_mail, report_mail, report_mm, exec_cmd


def postfix_sasl(settings, args):
    """postfix_sasl

    Arguments:
        settings {object} -- Settings from the class Config
        args {object} -- Execution parameters, where is the log path
    """

    pattern_sasl = 'sasl_method='

    logging.debug('Log file: %s', args.log.name)
    logfile_path = args.log.name

    # Initialize empty dictionary
    dict_general = defaultdict(set)

    with open(logfile_path) as log_file:
        logging.debug('Start log reading...')

        for line in log_file:

            if pattern_sasl in line:
                lista = line.split()

                mail_user = lista.pop().split('sasl_username=')[-1]

                # >/dev/null, ignore this
                lista.pop()

                mail_ip_address = utils.clean_ip(lista.pop())

                logging.debug('%s - %s', mail_user, mail_ip_address)

                if ipaddress.ip_address(mail_ip_address).is_private:
                    logging.debug('%s private ip address, skipped', mail_ip_address)
                else:
                    dict_general[mail_user].add(mail_ip_address)

    logging.debug('End log reading...')
    temp_set = utils.process_dict(dict_general)
    temp_dict = process_mail.process_mail(dict_general, temp_set, settings)

    # Results
    report_text = ""
    if len(temp_dict) > 0:
        for email in temp_dict.keys():

            # Execute external script when an anomaly is found for each e-mail
            if args.exec:
                exec_cmd.external_exec(args.exec.name, email)

            report_text += "\nE-mail address: {}\n".format(email)
            for ip_auth in temp_dict[email]:
                report_text += "\t{}\n".format(ip_auth)

        # Report in screen
        print(report_text)

        if settings.smtp_enabled:
            report_mail.send_report_mail(report_text, settings)

        if settings.mm_enabled:
            report_mm.send_report_mm(report_text, settings)
    else:
        logging.debug('No anomalies')
