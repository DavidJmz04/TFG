import time
from spade.agent import Agent

import requests, json, secrets, string
from random import random, choice

from behaviours import AggressiveBehav, ShyBehav, ArbitraryBehav, KnownBehav

""" Spade Agent """
class BidAgent(Agent):
    async def setup(self):
        print("Agent starting . . .")
        self.password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
        """ r = requests.post(url='http://localhost:8000/api/users/', headers={'Content-Type': 'application/json'}, data=json.dumps({'username': ''.join(choice(string.ascii_lowercase) for i in range(10)), 'password': self.password}))
        if r.status_code == 201: self.user = r.json()

        while r.status_code != 201:
            self.password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))
            r = requests.post(url='http://localhost:8000/api/users/', headers={'Content-Type': 'application/json'}, data=json.dumps({'username': ''.join(choice(string.ascii_lowercase) for i in range(10)), 'password': self.password}))
            if r.status_code == 201: self.user = r.json() """

""" Create user on openfire """
def create_user(user, password):
    r = requests.post(url='http://localhost:9090/plugins/restapi/v1/users', headers={'Authorization': 'Basic YWRtaW46MTIzNDU=', 'Content-Type': 'application/json'}, data=json.dumps({'username': user, 'password': password}), auth=('admin','[6\$tyxQT4'))
    
    if r.status_code != 201:
        create_user('a'+str(random()),''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8))))

    return (user, password)

if __name__ == "__main__":
    product = requests.get(url='http://localhost:8000/api/products/' + '19')
    """ (user, password) = create_user('a'+str(random()),''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))) """
    user = 'admin'
    password = '[6\$tyxQT4'
    dummy = BidAgent(user + "@desktop-bkd2suh", password)
    dummy.add_behaviour(KnownBehav(product.json(), 40, 0.25, [(30, 40), (20, 30), (10, 30)]))
    future = dummy.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")
    while dummy.behaviours:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    dummy.stop()