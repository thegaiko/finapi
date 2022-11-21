from pprint import pprint

import requests
import json


def get_binance(asset, bank_list, amount, fiat, trade_type):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = json.dumps({
        "asset": asset,
        "fiat": fiat,
        "page": 1,
        "payTypes": bank_list,
        "rows": 1,
        "tradeType": trade_type,
        "transAmount": amount
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'cid=jl3jMVsg'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    x = response['data'][0]
    bank_list = []
    for bank in x['adv']['tradeMethods']:
        bank_list.append(bank['tradeMethodName'])
    user_no = x['advertiser']['userNo']
    return {
        "exchange": "Binance",
        "asset": x['adv']['asset'],
        "price": round(float(x['adv']['price']), 2),
        "supply": x['adv']['surplusAmount'],
        "max": x['adv']['maxSingleTransAmount'],
        "min": x['adv']['minSingleTransAmount'],
        "bank": bank_list,
        "link": f'https://p2p.binance.com/ru/advertiserDetail?advertiserNo={user_no}',
        "nick": x['advertiser']['nickName'],
        "orders": x['advertiser']['monthOrderCount'],
        "rate": x['advertiser']['monthFinishRate'] * 100,
    }

def get_huobi(asset, bank_list, amount, fiat, trade_type):
    for i in range(len(bank_list)):
        if bank_list[i] == "Tinkoff":
            bank_list[i] = 9
        if bank_list[i] == "RosBank":
            bank_list[i] = 29
        if bank_list[i] == "QIWI":
            bank_list[i] = 28
        if bank_list[i] == "RaiffeisenBank":
            bank_list[i] = 356
        if bank_list[i] == "MTSBank":
            bank_list[i] = 24
        if bank_list[i] == "Payeer":
            bank_list[i] = 36
        if bank_list[i] == "Advcash":
            bank_list[i] = 19
        if bank_list[i] == "YandexMoneyNew":
            bank_list[i] = 20

    if asset == "USDT":
        req_asset = 2
    if asset == "BTC":
        req_asset = 1
    if asset == "ETH":
        req_asset = 3

    url = f'https://otc-api.trygofast.com/v1/data/trade-market?coinId={req_asset}&currency=11&tradeType=sell&currPage=1&payMethod=0&acceptOrder=0&country=&blockType=general&online=1&range=0&amount={amount}&onlyTradable=false&isFollowed=false'
    response = requests.request("GET", url).json()
    response = response['data'][0]

    decrypt_banks = {
        "Sberbank": "RosBankNew",
        "Tinkoff": "TinkoffNew",
        "Raiffeisenbank": "RaiffeisenBank",
        "ADVCash": "Advcash",
        "PAYEER": "Payeer",
        "QIWI": "QIWI",
        "MTS-Bank": "MTSBank"
    }

    pay_methods = []
    for method in response['payMethods']:
        try:
            pay_methods.append(decrypt_banks[method['name']])
        except KeyError:
            continue


    uid = response['uid']
    result = {
        "exchange": "Huobi",
        "asset": asset,
        "price": round(float(response['price'])),
        "supply": response['tradeCount'],
        "max": response['maxTradeLimit'],
        "min": response['minTradeLimit'],
        "bank": pay_methods,
        "link": f'https://www.huobi.com/ru-ru/fiat-crypto/trader/{uid}',
        "nick": response['userName'],
        "orders": response['tradeMonthTimes'],
        "rate": response['orderCompleteRate'],
    }

    return result


def get_bybit(asset, bank_list, amount, fiat, trade_type):
    result = []
    banks_reform = {
        "TinkoffNew": "75",
        "RosBankNew": "185",
        "RaiffeisenBank": "64",
        "QIWI": "62",
        "YandexMoneyNew": "88",
        "MTSBank": "44",
        "Payeer": "51",
        "ADvcash": "5",
    }
    bank_nums = {
        "75": "TinkoffNew",
        "185": "RosBankNew",
        "64": "RaiffeisenBank",
        "62": "QIWI",
        "88": "YandexMoneyNew",
        "44": "MTSBank",
        "51": "Payeer",
        "5": "ADvcash",
    }

    side_list = {
        "SELL": 0,
        "BUY": 1,
    }
    url = "https://api2.bybit.com/spot/api/otc/item/list"

    headers = {
        'authority': 'api2.bybit.com',
        'accept': 'application/json',
        'accept-language': 'ru-RU',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '_ym_uid=16584053911016622631; _ym_d=1658405391; _gcl_au=1.1.1454342403.1661774170; tmr_lvid=718b11584a3cc4af750ce00cb8fa0743; tmr_lvidTS=1658405391033; _by_l_g_d=63af44bb-34b2-3734-4d8a-0a1fd5958ee1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22182e9758cb515b8-085c3758008fd68-1b525635-1764000-182e9758cb666b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_a_u_v%22%3A%220.0.5%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyZTk3NThjYjUxNWI4LTA4NWMzNzU4MDA4ZmQ2OC0xYjUyNTYzNS0xNzY0MDAwLTE4MmU5NzU4Y2I2NjZiIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22182e9758cb515b8-085c3758008fd68-1b525635-1764000-182e9758cb666b%22%7D; _cc_id=bb0565e394e848f1445abf977a0a10c2; _clck=1lg6myp|1|f53|0; _tt_enable_cookie=1; _ttp=d9c9b9ee-de0c-49ec-9dd7-82f669bff388; tmr_reqNum=180; _abck=0C487C9B41B425D4BADF20A1FFA1FA70~0~YAAQk2pkX8CQC4yEAQAAN4GKjAg0refZUtM1kV7FiE5Rhjukjdu44KLAZeRrujXbJtdfesaq0JfWDM7roGkh/5SQR9U3EaLxdORLpu8C2I4Ro7lZefII8Wa+PzYj/AUcZo50Xpbq14RBU8n/9N7vX3dpwfN+Eu1F+QcQh+LnwY+rg9V8O7zjhBOytogx/cOU5yVSg1uX7RGjrcS3TgFlNW6fJ9jh+0zlM4bEtSEz//R925BMHrkCxKhoPWxd7L+n4+OsBzx+AygmMBE8k6Hy9gFz4OsbW5W3nCgFkFosPw1lXfd1TVEerMYVNyl51dCxURbwjQ/N1CDvLNrtcgNeONkZfYuy6VVZW7k/3fcxbMRw2HFFhrPjtQD8lpWqz6OfX1Yql/aVw/IpsZ8cTAKVljkGRyq42gg=~-1~-1~-1; bm_sz=6E7FE7D7E6D18631A78A6A4118963A14~YAAQk2pkX8OQC4yEAQAAN4GKjBHUarKmFi/SCALm6v0Q0GB10gw8b6hbVYGW0qkfPGvZT0w+xniS9dBArQUadUfX9tuc5XAisl8fyiZ3r6N19TJrqadjcxNeKuiYGUsZGSQwLSOL47ya0988NzdvP+he5umuBBHDq6dUuGhfHLfEPXOWMH6ZZ/W3C/SefxUNNq9TXA73nXH7CPEw5I7ZqjOsXeFKFW/M1r2eOqWpmS9GNQ5vbBgjdII7CYIh9FAl981b0A9oAty6PlowTgObOHcNRGPqzGOvRabT33SHCP+mKQ==~4408883~4604980; bm_mi=57DF451DDACB256DBA3D140969D8A7A5~YAAQk2pkX9SQC4yEAQAA8oOKjBH+sGFUqvP9u2nJ2mmOatTj/fAZa+cEru6uIuOcWox4HtBbzp99yj0Cj5SbKrsLCg2SpeCSmOfWcymgjqtHj7miGsayeCDs+cOhIStAJ16fvmv832b1fEt1LOepUeNj6Ly58Z0lZ8Zlza6iUbZmOj3WaSbIdpQjZE4YYkKG9ae9fvKUH5fO08ZCiE8ewUXMybiGw8zkKTZoXLGjt8iJza8tq7w8MPDshy3mjNYm2HIUEtWB4gRFxE6AkzZp+NvBfDQQHgK3ITfgkzU8x2EhN8+Vqii51qI8Nt23ahjpXvz6~1; BYBIT_REG_REF_prod={"lang":"ru-RU","g":"63af44bb-34b2-3734-4d8a-0a1fd5958ee1","referrer":"www.bybit.com/","source":"bybit.com","medium":"other","url":"https://www.bybit.com/ru-RU/"}; b_t_c_k=; ak_bmsc=76AA9F2B8AE6952309E143C4B5AC59F9~000000000000000000000000000000~YAAQk2pkXweRC4yEAQAAeYiKjBGiLeBHOd3f6+GZHJc5pc32eWxisWiWJ1/wRyH3h4ya5+F1xt8IdeCNByp+w24RUvPU2Zh2lWntyafKq2lic1cwpDEPFgZyD3/S92qm9X4rehwo9NweJ4wwcf+r5XdQYh3ayUogG6DQnCgKToyRoPZj1lqmMj3m8hHCgwCoaI4U46RQ44lj14P/2CibaRmAM/4p+FFQ9EqTjYa6fmQZuMppcJdLKYYHEyBLN/CiAH4mKVRykUPkKM7jNVZ11aMBHorHjl4pEO7mUoZoIxdBeaMDXsQz/5U8OZsCYo1sGEiKbM4xZRqTrwg4lKPvz9zhlraThnTHtx/aJNEixAt/DoWwS7Js0KqEvqyJyUSr9ZDrCynqqu9sOkHxgIwnnqrw9SNZUEhJniOKTctirlAqpVD+L7B2U2wtvXbsSUTrL7ZcjYdGZMWngVmNX9HCrz/oehG6itpdAB3AUD+5gFSbitmeGUrUtMTSHvRxltSGkKmo5Qhf; _ga=GA1.1.1052144741.1661774171; _ym_isad=1; _ga_SPS4ND2MGC=GS1.1.1668805205.1.1.1668805254.0.0.0; bm_sv=8E0C7310483ED2AEE48E2BEE471816EB~YAAQk2pkX3WZC4yEAQAAbWeLjBHw9wkvzj1zR/Euddaots2xkESqaG9WOtbup5e3ciP2jVOQWuUGqupn1QTzkxITsUg80H2Duyzpi3xygODooxJpT8TcckfI0xsqiJQTqV4e9eSaf3MN33wpHKc43U3IQ8hANr/XuHJuHt/q4xgPMPsm3F4AFHnoIYCWcFtmc0cv5wTwXXMqL71TfCTD5htUIyO4IBS4rySSmJwqL2WRn2vpHLo88dD4RxjFqiLI~1; _abck=0C487C9B41B425D4BADF20A1FFA1FA70~-1~YAAQRv1zPjm4KFeEAQAAT9cXZwipiN/D0M7ds29dVmR7gF7BPv46bHhOHF7zIsTCyuwTaFiJxBsABUN8pi3sWav9O8V4Duo3I0FhYAVWrkx+ZIlYM2iDQq7sM8Cr235y60xK4HrMoqhqjYSln17ZNjlcyUnRKa1wthzPMvuA90m3aV6raVQmEudmqZRZ+E8HWk5UO8W1CJLJPyzdMVHCRMOHkEBDBNdDUfXgStzOwajInDzxmA7kYdowGwXjNxpfqu90qBoExQpN/l7ZKEU5HrPls2lyytW/aZeAekVhU1l/69HNxzJ7bJ5kVdeveCWgRktAMMqZF+zaiPf11tWZzQ6Cd1uaANU2JjgoFGVgT2g9QHTgyNwfetzZX0+U~0~-1~-1',
        'guid': '63af44bb-34b2-3734-4d8a-0a1fd5958ee1',
        'lang': 'ru-RU',
        'origin': 'https://www.bybit.com',
        'platform': 'PC',
        'referer': 'https://www.bybit.com/',
        'risktoken': 'uOHw6+M2v2dq0qjp2DpK04gN1ptPIBvEKzcLdxjR4dFf6/HxyNELWLcX38KtdCefEvrMwjCDji5/MihUBP2odk7iUWgTJmx84TBElzrAr1AZLm67EtUQfFg+gsIIeuOo1h9lGTrRSeEGE9wAG1JdPfJ4pUm0uwR/vZsFXU+97mXrUotI3ygxUU/nzbhjLhjDrglXdwjHuyFZ2QICSVweUUZ2vbc/2CamwsdAHdHqbqdR/mCOGzmz2TM8SoQNQt5jO31GTxEQN/db0XqcPYU/tZJoZWRlrPbX2XUA8Q==',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    for bank in bank_list:
        try:
            bank_name = banks_reform[bank]
        except KeyError:
            pass
        payload = f'userId=&tokenId={asset}&currencyId={fiat}&payment={bank_name}&side={side_list[trade_type]}&size=10&page=1&amount={amount}'

        x = requests.request("POST", url, headers=headers, data=payload).json()
        x = x['result']['items']
        if len(x) == 0:
            continue
        x = x[0]
        payment_types = []
        payments = x['payments']
        for payment in payments:
            try:
                bank_number = bank_nums[str(payment)]
            except KeyError:
                continue
            payment_types.append(bank_number)
        uid = x['userId']
        res = {
            "exchange": "ByBit",
            "asset": asset,
            "price": round(float(x['price'])),
            "supply": x['lastQuantity'],
            "max": x['maxAmount'],
            "min": x['minAmount'],
            "bank": payment_types,
            "link": f'https://www.bybit.com/fiat/trade/otc/profile/{uid}/{asset}/{fiat}/item',
            "nick": x['nickName'],
            "orders": x['orderNum'],
            "rate": x['recentExecuteRate'],
        }
        result.append(res)
    return result

def get_spot_price(asset):
    url = f'https://api.binance.com/api/v3/avgPrice?symbol={asset}'
    payload={}

    result = requests.request("GET", url, data=payload).json()
    return result['price']