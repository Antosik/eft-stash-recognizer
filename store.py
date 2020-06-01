import requests


class PricesFetcher(object):
    def __init__(self):
        self.cookies = []

    def authorize(self):
        url = "https://tarkov-market.com"
        response = requests.get(url)
        if response.status_code == 200:
            self.cookies = response.cookies

    def get_list(self, skip=0, limit=20):
        if len(self.cookies) == 0:
            self.authorize()
        try:
            url = "https://tarkov-market.com/api/items?skip={skip}&limit={limit}".format(
                skip=skip,
                limit=limit
            )

            response = requests.get(url, cookies=self.cookies)
            response.raise_for_status()

            data = response.json()
            return data["items"]

        except requests.HTTPError as e:
            if e.response.status_code == 401:
                self.authorize()
            return []

    def get_price(self, name: str, retries=3):
        if len(self.cookies) == 0:
            self.authorize()

        try:
            url = "https://tarkov-market.com/api/items?search={name}".format(
                name=name)

            response = requests.get(url, cookies=self.cookies)
            response.raise_for_status()

            data = response.json()
            item = data["items"][0]

            if item:
                price = item["avgDayPrice"]
                trader = (item["traderName"], item["traderPrice"])

                return (price, trader)

            return 0, 0

        except requests.HTTPError as e:
            if retries == 0:
                return 0, 0

            if e.response.status_code == 401:
                self.authorize()

            return self.get_price(name, retries=retries-1)
