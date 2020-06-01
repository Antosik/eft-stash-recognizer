import json
from store import PricesFetcher

store = PricesFetcher()
items = []


for i in range(0, 100):
    new_items = store.get_list(skip=i*20, limit=20)
    items.extend(new_items)

f = open("data.json", "w")
f.write(json.dumps(items))
f.close()
