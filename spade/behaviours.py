import asyncio
from spade.behaviour import CyclicBehaviour

class MyBehav(CyclicBehaviour):
    async def on_start(self):
        self.counter = 0

    async def run(self):
        """ print("Counter: {}".format(self.counter))
        self.counter += 1 """
        #r = requests.get(url='http://localhost:8000/api/bids/')
        #r = requests.get(url='http://localhost:8000/api/bids/70/')
        #r = requests.post(url='http://localhost:8000/api/bids/', headers={'Content-Type': 'application/json'}, data=json.dumps({'price': 1, 'product': 20, 'buyer': 1}))
        await asyncio.sleep(1)
