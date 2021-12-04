from binance.client import Client

api_key = '39IIhxL3vYq2dQRMUKNO8HosQbHuY26SmcvROOfjdKF0n1tzRSkLWQlByGzbaKzq'
api_secret = '0P7PvqZaOEqzxUwDF1WlsMpp4mdHJ5SDLD6h30TZSSIHgd7lPe5z72lXa0fYdQz1'

"""api_key = 'yhDT4t0fM4DErCJjmOrGI88PKANmQMwDjLjxELZclLurKB6VzeBHZ6YV3v7mpdyE'
api_secret = 'CT1XgMA3fyvAzztqHesUAvyKMSTyWNPLwKcN8JygdT6VzEEvJW5HhAYp0GRpnO57'"""

client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'


def eth_dispo():
    return round(float(client.get_asset_balance(asset='ETH')['free']), 2)


def usdt_dispo():
    return int(float(client.get_asset_balance(asset='USDT')['free']) * 0.6) - 1


def prix_eth():
    return round(float(client.get_symbol_ticker(symbol="ETHUSDT")['price']), 2)


def eth_max_achetable():
    return round(usdt_dispo() / prix_eth(), 2)


def annuler_tous_les_ordres(paire):
    ordres = client.get_open_orders(symbol=paire)
    for ordre in ordres:
        print(client.cancel_order(
            symbol=paire,
            orderId=ordre['orderId']))


def ordre_strategique(taille):
    if taille not in [-4, -3, -2, 2, 3, 4]:
        raise Exception("La taille de l'ordre stratégique est invalide")
    price = prix_eth()
    stop_loss = round(taille / 2, 2)
    if taille > 0:
        quantite = eth_max_achetable()
        buy_market_order = client.order_market_buy(symbol='ETHUSDT',
                                                   quantity=quantite)  # ATTENTION, c'est la quantité en ETH qui est demandé
        oco_sell_order = client.order_oco_sell(symbol='ETHUSDT', quantity=quantite, price=price + taille,
                                               stopPrice=price - stop_loss, stopLimitPrice=price - stop_loss - 15,
                                               stopLimitTimeInForce='GTC')
        print(buy_market_order, oco_sell_order)
    elif taille < 0:
        eth = eth_dispo()
        eth_emprunte = round(0.9 * eth, 2)  # Il faudra mettre la somme empruntée
        sell_market_order = client.order_market_sell(symbol='ETHUSDT',
                                                     quantity=eth_emprunte)
        oco_buy_order = client.order_oco_buy(symbol='ETHUSDT', quantity=eth_emprunte, price=price - taille,
                                             stopPrice=price + stop_loss, stopLimitPrice=price + stop_loss + 15,
                                             stopLimitTimeInForce='GTC')
        print(sell_market_order, oco_buy_order)
    else:
        raise Exception("IMPOSSIBLE !")


def a_atteint_objectif(objectif):
    return True
