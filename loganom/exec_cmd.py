"""Execute external script when an anomaly is found
"""

import subprocess
import logging


def external_exec(script, argument):
    """Execute external script when an anomaly is found
    Timeout 10s

    Arguments:
        script {string} -- External script to be executed when an anomaly is found
        argument {string} -- E-mail address
    """

    logging.debug('Calling `%s %s`', script, argument)

    try:
        subprocess.run([script, argument],
                       check=True,
                       timeout=10)
    except subprocess.TimeoutExpired:
        logging.debug('Timeout (10s) in the external script')
        return False
    except subprocess.SubprocessError:
        logging.debug('External script returned error')
        return False
    except FileNotFoundError:
        logging.debug('External script not found')
        return False

    return True
