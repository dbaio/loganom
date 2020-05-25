""" Process Mail Module
"""

import logging
from collections import defaultdict
from dns import reversename, resolver
from dns import exception as dns_exception
from loganom.ipinfo import check_geoip
from loganom.utils import check_ip_on_whitelist, check_org_on_whitelist


def process_mail(dict_general, temp_set, settings):
    """process_mail

    Arguments:
        dict_general {defaultdict(set)} -- Dictionary of sets
                                         dict_general[mail_user].(mail_ip_addresses)
        temp_set {set} -- Set with email addresses that authenticated from more than one ip
        settings {object} -- Settings from the class Config
    """

    # pylint: disable=too-many-locals

    country_ignore = list(settings.country_ignore.split('\n'))
    pattern_org = list(settings.pattern_org.split('\n'))
    pattern_ip = list(settings.pattern_ip.split('\n'))

    dict_issues = defaultdict(list)

    for email_address in temp_set:
        logging.debug('Start processing email: %s', email_address)
        temp_list = []
        for ip_address in dict_general[email_address]:

            # Check dns reverse name from the ip address
            rev_name = reversename.from_address(ip_address)
            try:
                reverse_dns = str(resolver.query(rev_name, "PTR", lifetime=2)[0])
            except dns_exception.DNSException:
                reverse_dns = 'unknown'

            logging.debug('  IP: %s - Reverse: %s', ip_address, reverse_dns)

            # Request geoip from the not skipped ip addresses with dns reverse name
            if not check_ip_on_whitelist(reverse_dns, pattern_ip):
                json_ip = check_geoip(ip_address, settings.ipinfo_token)
                if 'bogon' not in json_ip:
                    country = json_ip['country']
                    city = json_ip['city']
                    org = json_ip['org']
                else:
                    # IP Invalid/Bogon
                    continue

                logging.debug('  Contry: %s - %s - %s', country, city, org)

                if country not in country_ignore:
                    if not check_org_on_whitelist(org, pattern_org):
                        temp_list.append('{} - {} - {} - {} - {}'.format(
                            ip_address,
                            country,
                            city,
                            reverse_dns,
                            org))
                else:
                    logging.debug('    %s skipped', country)

        if len(temp_list) > 1:
            dict_issues[email_address] = temp_list


    return dict_issues
