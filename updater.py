import json
import time

from exchanges import get_binance, get_huobi, get_bybit, get_spot_price
from threading import Thread

banks_list = ["TinkoffNew", "RosBankNew", "RaiffeisenBank", "QIWI", "MTSBank", "Payeer", "Advcash"]
assets = ["USDT", "BTC", "BNB", "BUSD", "ETH"]
amount = 10000
fiat = "RUB"


def add_binance():
    banks_list = ["TinkoffNew", "RosBankNew", "RaiffeisenBank", "QIWI", "MTSBank", "Payeer", "Advcash"]
    while True:
        buy_orders = []
        sell_orders = []
        for asset in assets:
            buy_orders.append(get_binance(asset, banks_list, amount, fiat, "BUY"))
            sell_orders.append(get_binance(asset, banks_list, amount, fiat, "SELL"))
        data = {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }
        with open('binance_orders.json', 'w') as f:
            json.dump(data, f)
        f.close()
        print("Binance orders done.")


def add_huobi():
    banks_list = ["TinkoffNew", "RosBankNew", "RaiffeisenBank", "QIWI", "MTSBank", "Payeer", "Advcash"]
    while True:
        buy_orders = []
        sell_orders = []
        for asset in assets:
            if asset != "BUSD" and asset != "BNB":
                buy_orders.append(get_huobi(asset, banks_list, amount, fiat, "BUY"))
                sell_orders.append(get_huobi(asset, banks_list, amount, fiat, "SELL"))
        data = {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }
        with open('huobi_orders.json', 'w') as f:
            json.dump(data, f)
        f.close()
        print("Huobi orders done.")


def add_bybit():
    while True:
        buy_orders = []
        sell_orders = []
        for asset in assets:
            if asset != "BUSD" and asset != "BNB":
                orders = get_bybit(asset, banks_list, amount, fiat, "BUY")
                for order in orders:
                    buy_orders.append(order)
                orders = get_bybit(asset, banks_list, amount, fiat, "SELL")
                for order in orders:
                    sell_orders.append(order)
        data = {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }
        with open('bybit_orders.json', 'w') as f:
            json.dump(data, f)
        f.close()
        print("Bybit orders done.")


def spots_orders():
    while True:
        spot_prices = {
            "BTCUSDT": get_spot_price("BTCUSDT"),
            "BTCBUSD": get_spot_price("BTCBUSD"),

            "BUSDUSDT": get_spot_price("BUSDUSDT"),
            "BNBUSDT": get_spot_price("BNBUSDT"),
            "BNBBTC": get_spot_price("BNBBTC"),
            "BNBBUSD": get_spot_price("BNBBUSD"),
            "BNBETH": get_spot_price("BNBETH"),

            "ETHUSDT": get_spot_price("ETHUSDT"),
            "ETHBTC": get_spot_price("ETHBTC"),
            "ETHBUSD": get_spot_price("ETHBUSD"),
        }
        with open('spot_orders.json', 'w') as f:
            json.dump(spot_prices, f)
        f.close()
        print("Spot orders done.")


binance = Thread(target=add_binance)
huobi = Thread(target=add_huobi)
bybit = Thread(target=add_bybit)
spot = Thread(target=spots_orders)
binance.start()
huobi.start()
bybit.start()
spot.start()