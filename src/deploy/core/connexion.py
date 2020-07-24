import os
import time
import requests

registerAddress = "register"


def init(logger, service):
    """register to the register service so service can be requested"""

    payload = {'type': service, 'address': os.getenv('name')}
    r = requests.post('http://' + registerAddress + ':5000/registration', params=payload)
    atempt = 1
    while r.status_code != 200:
        if atempt == 3:
            logger.error('error while ' + service + ' registration')
            return 1
        time.sleep(5)
        r = requests.post('http://' + registerAddress + ':5000/registration', params=payload)
        atempt += 1
    logger.info(service + ' successfully registered')
    return 0


def getService(serviceName):
    """request the address of a service which have the name serviceName"""

    r = requests.get('http://' + registerAddress + ':5000/address/' + serviceName)
    if r.status_code == 200:
        return "0", r.json()['address']
    else:
        return "01001", r.status_code
