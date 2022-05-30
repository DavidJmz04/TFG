from agent import main
from behaviours import AggressiveBehav, ShyBehav, ArbitraryBehav, KnownBehav

import requests, json
from datetime import datetime, timedelta

import time

def stop(agent_list):
    for agent in agent_list:
        while agent.behaviours:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
        agent.stop()


if __name__ == "__main__":
    agent1 = main()
    product = requests.post(url='http://localhost:8000/api/products/', headers={'Content-Type': 'application/json'}, data=json.dumps({'title': "Test1", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "clock", 'initial_bid': 20, 'origin': "Spain", 'created_date': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), 'finished_date': (datetime.now() + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), 'seller': agent1.user['id']}, default= str), auth=(agent1.user['username'], agent1.password))
    """ agent2 = main()
    agent3 = main() """

    agent1.add_behaviour(KnownBehav(product.json(), 40, 0.25, [(30, 40), (20, 30)]))
    """ agent2.add_behaviour(AggressiveBehav(product.json(), 38, 0.80))
    agent3.add_behaviour(ShyBehav(product.json(), 27, 0.5)) """
    
    stop([agent1])