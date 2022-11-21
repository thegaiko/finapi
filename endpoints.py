import json
from pprint import pprint


def check_token(token):
    f = open('user_list.json')
    data = json.load(f)
    f.close()
    for user in data:
        if user['token'] == token:
            return {
                "status": 1,
                "user": user
            }
    return {
        "status": 0,
    }


def bank_checker(my_banks, order_banks):
    for my_bank in my_banks:
        if my_bank not in order_banks:
            return False
    return True


def triple(asset_list, bank_list, amount, fiat):
    f = open('binance_orders.json')
    binance_orders = json.load(f)
    f.close()

    f = open('huobi_orders.json')
    huobi_orders = json.load(f)
    f.close()

    f = open('bybit_orders.json')
    bybit_orders = json.load(f)
    f.close()

    f = open('spot_orders.json')
    spot_orders = json.load(f)
    f.close()

    buy_orders = []
    sell_orders = []

    for order in binance_orders['buy_orders']:
        if order['asset'] in asset_list and bank_checker(order['bank'], bank_list):
            buy_orders.append(order)
    for order in binance_orders['sell_orders']:
        if order['asset'] in asset_list and bank_checker(order['bank'], bank_list):
            sell_orders.append(order)
    for order in huobi_orders['buy_orders']:
        if order['asset'] in asset_list and bank_checker(order['bank'], bank_list):
            buy_orders.append(order)
    for order in huobi_orders['sell_orders']:
        if order['asset'] in asset_list and bank_checker(order['bank'], bank_list):
            sell_orders.append(order)
    for order in bybit_orders['buy_orders']:
        if order['asset'] in asset_list and bank_checker(order['bank'], bank_list):
            buy_orders.append(order)
    for order in bybit_orders['sell_orders']:
        if order['asset'] in asset_list and bank_checker(order['bank'], bank_list):
            sell_orders.append(order)

    orders = []
    for buy_order in buy_orders:
        for sell_order in sell_orders:
            buy_order_asset = buy_order['asset']
            sell_order_asset = sell_order['asset']
            try:
                middle_price = spot_orders[f"{buy_order_asset}{sell_order_asset}"]
                logic_type = 0
            except KeyError:
                try:
                    middle_price = spot_orders[f"{sell_order_asset}{buy_order_asset}"]
                    logic_type = 1
                except KeyError:
                    continue

            if logic_type == 1:
                take_money = (((amount / buy_order["price"]) / float(middle_price)) * sell_order["price"]) - amount
            else:
                take_money = (((amount / buy_order["price"]) * float(middle_price)) * sell_order["price"]) - amount
            if take_money > 10:
                orders.append(
                    {
                        "buy_order": buy_order,
                        "sell_order": sell_order,
                        "other_info": {
                            "middle_price": middle_price,
                            "take_money": round(take_money, 2),
                            "take_money_proc": round(((take_money / amount) * 100), 2)
                        }
                    }
                )
    return orders


pprint(triple(['USDT', "ETH", "BTC", "BUSD", "BNB"], ["TinkoffNew", "RosBankNew", "RaiffeisenBank", "QIWI", "MTSBank", "Payeer", "Advcash"], 10000, "RUB"))
