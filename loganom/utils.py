"""Auxiliary functions for the program
"""

import re
import logging


def clean_email(raw_email):
    """Clean a raw email address from the log file.

    Arguments:
        raw_email [string] -- from=<user@domain.com>

    Returns:
        [string] -- user@domain.com
    """
    temp1 = raw_email.split('from=<')[1]

    return temp1.rstrip('>')


def clean_ip(raw_ip):
    """Clean a raw ip address from the log file.

    Arguments:
        raw_ip [string] -- client=mail-ed1-f51.google.com[209.85.208.51]

    Returns:
        [string] -- 209.85.208.51
    """
    temp1 = re.search(r"\[.+\]", raw_ip)

    temp2 = ''
    if temp1.group(0):
        for char in temp1.group(0):
            if char in ('[', ']'):
                continue
            temp2 += char
    else:
        return raw_ip

    return temp2


def process_dict(dict_general):
    """Processor of the General Dictionary

    Receives a dictionary with all email addresses and their ip address(es)
    of authentication.

    Returns a set with email addresses that authenticated from more than
    one ip address.

    Arguments:
        dict_general {defaultdict(set)} -- Dictionary of sets
                                         dict_general[mail_user].(mail_ip_addresses)

    Returns:
        [set] -- Set with email addresses that authenticated from more than one ip
    """
    logging.debug('Start processing the dictionary...')
    temp_set = set()

    for email_address in dict_general.keys():
        email_address_qtd_ips = len(dict_general[email_address])
        logging.debug('%s (%s)', email_address, email_address_qtd_ips)
        if email_address_qtd_ips > 1:
            temp_set.add(email_address)

    return temp_set


def check_ip_on_whitelist(ip_name, pattern_ip):
    """Check if the ip address can be ignored, based on a list of name patterns.

    Examples:
                179.184.9.54.static.gvt.net.br
                177.66.162.138.static.bs2.net.br

    Arguments:
        ip_name {string}   -- Host from the dns reverse
        pattern_ip {list} -- List with the name patterns

    Returns:
        [bool] -- False if it's not matched
                  True if it matches
    """

    for pattern in pattern_ip:
        if pattern in ip_name:
            logging.debug('    %s skipped by %s', ip_name, pattern)
            return True

    return False


def check_org_on_whitelist(org_name, pattern_org):
    """Check if the ip address can be ignored based on it's ASN.

    Arguments:
        org_name {string} -- Organization info (GeoIP)
        pattern_org {lista} -- List with ASN numbers

    Returns:
        [bool] -- False if it's not matched
                  True if it matches
    """

    org = org_name.split()[0]

    for pattern in pattern_org:
        if org == pattern:
            logging.debug('    %s skipped by %s', org_name, pattern)
            return True

    return False


def trim_report(report_text):
    """Let report text smaller for it not generate spam in the output

    Args:
        report_text ([list]): List of email address and its offending IPs

    Returns:
        ([list]): List of email address and its offending IPs (Smaller)
    """

    report_trimmed = []

    for report_full in report_text:
        if len(report_full) > 500:
            report_temp = report_full[0:500]
            report_temp += "\t[...]\n"
            report_trimmed.append(report_temp)
        else:
            report_trimmed.append(report_full)

    return report_trimmed


def read_logfile(file, pattern):
    """Read a log file and return just the lines that match with a simple pattern.

    Args:
        file (path): Path for log file (default: /var/log/maillog)
        pattern (string): Simple string pattern
    """

    with open(file) as log_file:
        logging.debug('Start log reading...')

        for line in log_file:
            if pattern in line:
                yield line

    logging.debug('End log reading...')
