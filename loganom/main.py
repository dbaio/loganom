"""loganom main

Check parameters and user settings then execute the selected processor.
"""

import os
import sys
import argparse
import logging

from datetime import datetime
from loganom import config
from loganom.processor import postfix_sasl, quota_high


logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"),
    format="%(levelname)s:\t%(message)s")


def main():
    """loganom main function
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('processor',
                        choices=['postfix-sasl', 'quota-high'],)

    parser.add_argument('-c', '--config',
                        type=argparse.FileType('r'),
                        help='Path for configuration file (default: ./config.ini)',
                        default='./config.ini')

    parser.add_argument('-l', '--log',
                        type=argparse.FileType('r'),
                        help='Path for log file (default: /var/log/maillog)',
                        default='/var/log/maillog')

    parser.add_argument('-e', '--exec',
                        type=argparse.FileType('r'),
                        help='External script to be executed when an anomaly is found',
                        required=False)

    parser.add_argument('-q', '--quota-message',
                        help='''
                        Quota reject message used in the mail server
                        (default: 'Quota per hour exceeded')
                        [Processor quota-high]''',
                        default='Quota per hour exceeded',
                        required=False)

    parser.add_argument('--quota-limit',
                        help='''
                        Quota limit occurrences, above this it will be considered
                        an anomaly (default: 150)
                        [Processor quota-high]''',
                        default=150,
                        required=False)

    args = parser.parse_args()

    settings = config.read_config(args.config)

    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if args.processor == 'quota-high':
        print(f'Starting quota-high ({current_datetime})')
        quota_high(settings, args)
        sys.exit(0)
    elif args.processor == 'postfix-sasl':
        print(f'Starting postfix-sasl ({current_datetime})')
        postfix_sasl(settings, args)
        sys.exit(0)


if __name__ == "__main__":
    main()
