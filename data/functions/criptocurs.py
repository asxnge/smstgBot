import json, requests

class Cripto():

    def ETHCurs(self):
        response = requests.get(url = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,RUB')
        data = json.loads(response.text)
        
        USD = data.get('USD')
        RUB = data.get('RUB')

        return USD, RUB

    def BTCCurs(self):
        response = requests.get(url = 'https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,RUB')
        data = json.loads(response.text)

        USD = data.get('USD')
        RUB = data.get('RUB')

        return USD, RUB

    def message_curs(self):
        eth = self.ETHCurs()
        btc = self.BTCCurs()
        msg = f"""
<b>🔅 BTC</b> - {btc[0]} $ | {btc[1]} ₽

<b>🔘 ETH</b> - {eth[0]} $ | {eth[1]} ₽
        """
        return msg

