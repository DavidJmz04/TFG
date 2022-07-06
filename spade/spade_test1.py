from agent import main
from behaviours import AggressiveBehav, ShyBehav, ArbitraryBehav, KnownBehav

import requests, json
from datetime import datetime, timedelta
import random

import time

def stop(agent_list, product):
    for agent in agent_list:
        while agent.behaviours:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
        agent.stop()
    
    winner = requests.get(url='http://localhost:8000/api/products/' + str(product.json()['id']), headers={'Content-Type': 'application/json'}, auth=(agent1.user['username'], agent1.password)).json()['winner']
    for agent in agent_list:
        if agent.user['id'] ==  winner: print('Ganador: ' + str(agent.user['username']))

if __name__ == "__main__":
    agent1 = main()
    product = requests.post(url='http://localhost:8000/api/products/', headers={'Content-Type': 'application/json'}, data=json.dumps({'title': "Test", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "clock", 'initial_bid': 20, 'origin': "Spain", 'created_date': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), 'finished_date': (datetime.utcnow() + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ"), 'seller': agent1.user['id']}, default= str), auth=(agent1.user['username'], agent1.password))
    agent2 = main()
    agent3 = main()
    agent4 = main()

    max_price1= random.randint(20, 30)
    max_price2= random.randint(20, 30)
    max_price3= random.randint(20, 30)
    max_price4= random.randint(20, 30)

    agent1.add_behaviour(AggressiveBehav(product.json(), max_price1, 0.8))
    agent2.add_behaviour(ShyBehav(product.json(), max_price2, 0.9))
    agent3.add_behaviour(ArbitraryBehav(product.json(), max_price3))
    agent4.add_behaviour(KnownBehav(product.json(), max_price4, [(max_price1 - random.randint(0, 5), max_price1 + random.randint(0, 5)), (max_price2 - random.randint(0, 5), max_price2 + random.randint(0, 5)), (max_price3 - random.randint(0, 5), max_price3 + random.randint(0, 5))], 0.4))
        
    print('Agente agresivo: ' + agent1.user['username'] + '   ------------- Máxima puja: ' + str(max_price1))
    print('Agente tímido: ' + agent2.user['username'] + '     ------------- Máxima puja: ' + str(max_price2))
    print('Agente arbitrario: ' + agent3.user['username'] + ' ------------- Máxima puja: ' + str(max_price3))
    print('Agente conocedor: ' + agent4.user['username'] + '  ------------- Máxima puja: ' + str(max_price4))

    stop([agent1, agent2, agent3, agent4], product)