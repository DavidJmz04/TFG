from agent import main
from behaviours import AggressiveBehav, ShyBehav

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
    product = requests.post(url='http://localhost:8000/api/products/', headers={'Content-Type': 'application/json'}, data=json.dumps({'title': "Test3", 'description': "This is a test", 'quantity': 3, 'measure': 'units', 'type': "dutch", 'initial_bid': 50, 'final_bid': 20, 'origin': "Spain", 'created_date': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), 'finished_date': (datetime.utcnow() + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ"), 'seller': agent1.user['id']}, default= str), auth=(agent1.user['username'], agent1.password))
    agent2 = main()
    
    max_price1= random.randint(40, 50)
    max_price2= random.randint(26, 34)
    
    agent1.add_behaviour(AggressiveBehav(product.json(), max_price1, 0.4))
    agent2.add_behaviour(ShyBehav(product.json(), max_price2, 0.9))
           
    print('Agente agresivo: ' + agent1.user['username'] + ' ------------- Máxima puja: ' + str(max_price1))
    print('Agente timido: ' + agent2.user['username'] + '   ------------- Máxima puja: ' + str(max_price2))
   
    stop([agent1, agent2], product)