import requests, argparse
from bs4 import BeautifulSoup

class PageDidntLoad(Exception):
    """Page didnt load for some reason"""
    def __init__(self, text):
        self.text = text

class Crypto:
    """Модель криптовалюты"""

    def __init__(self, name, price, market_cap):
        self.name = name
        self.price = price
        self.market_cap = market_cap

def FindCryptoInfo(name):
    url = "https://coinmarketcap.com/currencies/" + name
    page = requests.get(url)

    if (page.status_code != 200):
        raise PageDidntLoad(page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')

    #В этом div находится вся нужная нам информация
    body = soup.body.find('div', 
                          class_ = 'sc-16r8icm-0 kXPxnI container___lbFzk')
    price = body.find('div', class_ = 'priceValue___11gHJ').get_text()
    cap = body.find('div', class_ = 'statsValue___2iaoZ').get_text()

    return Crypto(name, price, cap)

def FindTopNCryptoInfo(n):
    url = "https://coinmarketcap.com"
    page = requests.get(url)

    if (page.status_code != 200):
        raise PageDidntLoad(page.status_code)
    
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.body.find(
               class_="cmc-table cmc-table___11lFC cmc-table-homepage___2_guh")
    table = table.tbody.find_all('tr')
    CryptoInf = []

    for i in range(0, n):
        name = table[i].find(
            'div', class_="sc-16r8icm-0 sc-1teo54s-1 lgwUsc").get_text()
        price = table[i].find('div', class_="price___3rj7O").get_text()
        cap = table[i].find('p', class_="sc-1eb5slv-0 kDEzev").get_text()
        CryptoInf.append(Crypto(name, price, cap))

    return CryptoInf

################################################################################
################################################################################
################################################################################

ArgsParser = argparse.ArgumentParser()
ArgsParser.add_argument("-find", default="null", help="Find crypto info")
ArgsParser.add_argument("-top", default=0, type=int, help="Shows top n cryptos")
args = ArgsParser.parse_args()

if (args.find != 'null'):
    try:
        crypto = FindCryptoInfo(args.find)
        print("Имя: {0}\nЦена: {1}\nКапитализация: {2}".format(
                                                        crypto.name.upper(),
                                                        crypto.price,
                                                        crypto.market_cap))
    except PageDidntLoad as e:
        print("Проблемы с обращением к серверу (Код ошибки: {0}).\n"
              "Убедитесь в корректности написания имени криптовалюты."
              .format(e.text))

if (args.top > 10):
    print("Максимальное количество - 10")
elif (args.top > 0):
    try:
        result = FindTopNCryptoInfo(args.top)
        print("Топ {0} криптовалют".format(args.top))
        for i in range(0, args.top):
            print("{0})\n  Name: {1}\n  Price: {2}\n  Cap: {3}"
                                                            .format(i + 1,
                                                            result[i].name,
                                                            result[i].price,
                                                            result[i].market_cap
                                                            ))
    except PageDidntLoad as e:
            print("Проблемы с обращением к серверу (Код ошибки: {0}).\n"
                .format(e.text))