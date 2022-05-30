import asyncio
from spade.behaviour import CyclicBehaviour

import requests, json

from datetime import datetime
import random

""" A very participative behaviour on clock auctions and a risky behaviour on dutch auctions """
class AggressiveBehav(CyclicBehaviour):
    def __init__(self, product, max_price, aggressiveness):
        self.product = product
        self.max_price = max_price
        self.aggressiveness = 1 - aggressiveness
        super().__init__()

    async def run(self):
        #Stop the agent if the auction is finished
        if (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() < datetime.now().timestamp()): self.kill()

        if self.product['type'] == 'sealed':
            while float(self.product['initial_bid']) >= round(self.max_price * self.aggressiveness, 2): self.aggressiveness = round(self.aggressiveness + 0.01, 2)
            if self.aggressiveness >= 1: self.kill()
            r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': round(self.max_price * self.aggressiveness, 2), 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
            if r.status_code == 201: self.kill()

        else:
            # Get the higher bid and buyer if exists
            r = requests.get(url='http://localhost:8000/api/bids/' + str(self.product['id']))
            self.higher_bid = 0 if len(r.json()) == 0 else float(r.json()[0]['price'])
            self.higher_buyer = 0 if len(r.json()) == 0 else r.json()[0]['buyer']

            if self.product['type'] == 'clock': #and higher_buyer != self.agent.user['id']):
                while self.higher_bid >= round(self.max_price * self.aggressiveness, 2) or float(self.product['initial_bid']) >= round(self.max_price * self.aggressiveness, 2): self.aggressiveness = round(self.aggressiveness + 0.01, 2)
                if self.aggressiveness >= 1: self.kill()
                r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': round(self.max_price * self.aggressiveness, 2), 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))

            elif self.product['type'] == 'dutch':
                price = round(float(self.product['initial_bid']) - (((float(self.product['initial_bid']) - float(self.product['final_bid'])) * float(100 - (((datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.now().timestamp()) * 100) / (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.strptime(self.product['created_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp())))) / 100),2)
                if self.higher_bid == 0 and price <= round(self.max_price * self.aggressiveness, 2):
                    r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
                    if r.status_code == 201: self.kill()

        await asyncio.sleep(1)

""" A non participative behaviour on clock auctions and a safe behaviour on dutch auctions """
class ShyBehav(CyclicBehaviour):
    def __init__(self, product, max_price, shyness):
        self.product = product
        self.max_price = max_price
        self.shyness = shyness
        super().__init__()

    async def run(self):
        #Stop the agent if the auction is finished
        if (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() < datetime.now().timestamp()): self.kill()

        if self.product['type'] == 'sealed':
            while float(self.product['initial_bid']) >= round(self.max_price * self.shyness, 2): self.shyness = round(self.shyness + 0.01, 2)
            if self.shyness >= 1: self.kill()
            r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': round(self.max_price * self.shyness, 2), 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
            if r.status_code == 201: self.kill()

        else:
            # Get the higher bid and buyer if exists
            r = requests.get(url='http://localhost:8000/api/bids/' + str(self.product['id']))
            self.higher_bid = 0 if len(r.json()) == 0 else float(r.json()[0]['price'])
            self.higher_buyer = 0 if len(r.json()) == 0 else r.json()[0]['buyer']

            if self.product['type'] == 'clock': #and higher_buyer != self.agent.user['id']):
                while self.higher_bid >= round(self.max_price * self.shyness, 2) or float(self.product['initial_bid']) >= round(self.max_price * self.shyness, 2): self.shyness = round(self.shyness + 0.01, 2)
                if self.shyness >= 1: self.kill()
                r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': round(self.max_price * self.shyness, 2), 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))

            elif self.product['type'] == 'dutch':
                price = round(float(self.product['initial_bid']) - (((float(self.product['initial_bid']) - float(self.product['final_bid'])) * float(100 - (((datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.now().timestamp()) * 100) / (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.strptime(self.product['created_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp())))) / 100),2)
                if self.higher_bid == 0 and price <= round(self.max_price * self.shyness, 2):
                    r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
                    if r.status_code == 201: self.kill()

        await asyncio.sleep(1)

""" A random attitude behaviour on sealed, clock and dutch auctions """
class ArbitraryBehav(CyclicBehaviour):
    def __init__(self, product, max_price):
        self.product = product
        self.max_price = max_price
        self.array = []
        for number in range(1, self.max_price * 100): self.array.append(round(number * 0.01, 2))
        self.array.append(self.max_price)
        super().__init__()

    async def on_start(self):
        self.price = self.array[random.randint(0, len(self.array)-1)]
        
    async def run(self):
        #Stop the agent if the auction is finishedn
        if (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() < datetime.now().timestamp()): self.kill()

        if self.product['type'] == 'sealed':
            while float(self.product['initial_bid']) >= self.price: self.price = self.array[random.randint(0, len(self.array)-1)]
            if self.array.index(self.price) == len(self.array) - 1: self.kill()
            r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': self.price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
            if r.status_code == 201: self.kill()

        else:
            # Get the higher bid and buyer if exists
            r = requests.get(url='http://localhost:8000/api/bids/' + str(self.product['id']))
            self.higher_bid = 0 if len(r.json()) == 0 else float(r.json()[0]['price'])
            self.higher_buyer = 0 if len(r.json()) == 0 else r.json()[0]['buyer']
                
            if self.product['type'] == 'clock': #and self.higher_buyer != self.agent.user['id']:
                while self.higher_bid >= self.price or float(self.product['initial_bid']) >= self.price: self.price = self.array[random.randint(self.array.index(self.price), len(self.array)-1)]
                if self.array.index(self.price) == len(self.array) - 1: self.kill()
                r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': self.price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))

            elif self.product['type'] == 'dutch':
                price = round(float(self.product['initial_bid']) - (((float(self.product['initial_bid']) - float(self.product['final_bid'])) * float(100 - (((datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.now().timestamp()) * 100) / (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.strptime(self.product['created_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp())))) / 100),2)
                if self.higher_bid == 0 and price <= self.price:
                    r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
                    if r.status_code == 201: self.kill()

        await asyncio.sleep(1)

""" A bigger bid than others on sealed auctions, one big bid behaviour on clock auctions and a bigger bid than others on dutch auctions """
class KnownBehav(CyclicBehaviour):
    def __init__(self, product, max_price, risk, others_range):
        self.product = product
        self.max_price = max_price
        self.risk = 1 - risk
        self.others_range = others_range
        self.price = 0
        super().__init__()

    async def on_start(self):
        for element in self.others_range:
            value = element[0] + ((element[1] - element[0]) * self.risk) if element[0] + ((element[1] - element[0]) * self.risk) < self.max_price else self.max_price
            self.price = value if self.price < value else self.price

    async def run(self):
        #Stop the agent if the auction is finished
        if (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() < datetime.now().timestamp()): self.kill()

        if self.product['type'] == 'sealed':
            while float(self.product['initial_bid']) >= self.price: self.price = round(self.price + 0.01, 2)
            if self.price >= self.max_price: self.kill()
            r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': self.price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
            if r.status_code == 201: self.kill()

        else:
            # Get the higher bid and buyer if exists
            r = requests.get(url='http://localhost:8000/api/bids/' + str(self.product['id']))
            self.higher_bid = 0 if len(r.json()) == 0 else float(r.json()[0]['price'])
            self.higher_buyer = 0 if len(r.json()) == 0 else r.json()[0]['buyer']
                
            if self.product['type'] == 'clock': #and self.higher_buyer != self.agent.user['id']:
                while self.higher_bid >= self.price or float(self.product['initial_bid']) >= self.price: self.price = round(self.price + 0.01, 2)
                if self.price >= self.max_price: self.kill()
                r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': self.price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password)) 

            elif self.product['type'] == 'dutch':
                price = round(float(self.product['initial_bid']) - (((float(self.product['initial_bid']) - float(self.product['final_bid'])) * float(100 - (((datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.now().timestamp()) * 100) / (datetime.strptime(self.product['finished_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp() - datetime.strptime(self.product['created_date'], "%Y-%m-%dT%H:%M:%SZ").timestamp())))) / 100),2)
                if self.higher_bid == 0 and price <= self.price:
                    r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': price, 'product': self.product['id'], 'buyer': self.agent.user['id']}), auth=(self.agent.user['username'], self.agent.password))
                    if r.status_code == 201: self.kill()

        await asyncio.sleep(1)