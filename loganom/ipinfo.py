"""IP geolocation from ipinfo.io service.

https://ipinfo.io
"""

import requests


def check_geoip(ip_address, token):
    """check_geoip

    Arguments:
        ip_address {string} -- IP address to be checked
        token {string}      -- ipinfo token

    Returns:
        {json} -- IP address information returned from ipinfo.io
    """

    url = 'http://ipinfo.io/' + ip_address + '?token=' + token

    try:
        response = requests.get(url)
    except requests.RequestException:
        return False

    return response.json()
