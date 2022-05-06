import time
from spade.agent import Agent

import requests, json, secrets, string
from random import random

from behaviours import MyBehav

""" Spade Agent """
class Bid(Agent):
    async def setup(self):
        print("Agent starting . . .")

""" Create user on openfire """
def create_user(user, password):
    r = requests.post(url='http://localhost:9090/plugins/restapi/v1/users', headers={'Authorization': 'Basic YWRtaW46MTIzNDU=', 'Content-Type': 'application/json'}, data=json.dumps({'username': user, 'password': password}), auth=('admin','[6\$tyxQT4'))
    
    if r.status_code != 201:
        create_user('a'+str(random()),''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8))))

    return (user, password)

if __name__ == "__main__":
    """ (user, password) = create_user('a'+str(random()),''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(8)))) """
    user = 'admin'
    password = '[6\$tyxQT4'
    dummy = Bid(user + "@desktop-bkd2suh", password)
    dummy.add_behaviour(MyBehav())
    future = dummy.start()
    future.result()
    #dummy.web.start(hostname="127.0.0.1", port="10000") #No va

    print("Wait until user interrupts with ctrl+C")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    
    dummy.stop()