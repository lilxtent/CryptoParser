import requests, argparse, sys
from bs4 import BeautifulSoup

class PageDidntLoad(Exception):
    """Page didnt load for some reason"""
    def __init__(self, text):
        self.text = text

class Crypto:
    """Cryptocurrencie model"""

    def __init__(self, name, price, market_cap):
        self.name = name
        self.price = price
        self.market_cap = market_cap

def FindCryptoInfo(name):
    url = "https://coinmarketcap.com/currencies/{0}".format(name
                                                            .replace(' ','-')
                                                            .lower())
    page = requests.get(url)

    if (page.status_code != 200):
        raise PageDidntLoad(page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')

    #This div contains all information we need
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
            'div', class_="sc-16r8icm-0 sc-1teo54s-1 lgwUsc").p.get_text()
        price = table[i].find('div', class_="price___3rj7O").get_text()
        cap = table[i].find('p', class_="sc-1eb5slv-0 kDEzev").get_text()
        CryptoInf.append(Crypto(name, price, cap))

    return CryptoInf

def ShowCryptoInfo(name):
    try:
        crypto = FindCryptoInfo(args.find)
        print("Name: {0}\nPrice: {1}\nCap: {2}".format(
                                                        crypto.name.upper(),
                                                        crypto.price,
                                                        crypto.market_cap))
    except PageDidntLoad as e:
        print("Problems accessing the server (Error code: {0}).\n"
              "Make sure the spelling of the cryptocurrency name is correct."
              .format(e.text))

def ShowTopNCryptoInfo(n):
    try:
        result = FindTopNCryptoInfo(args.top)
        print("Top {0} cryptocurrencies:".format(args.top))
        for i in range(0, args.top):
            print("{0})\n  Name: {1}\n  Price: {2}\n  Cap: {3}"
                                                            .format(i + 1,
                                                            result[i].name,
                                                            result[i].price,
                                                            result[i].market_cap
                                                            ))
    except PageDidntLoad as e:
        print("Problems accessing the server (Error code: {0}).\n"
                                                                .format(e.text))

def GetArgumetns():
    ArgsParser = argparse.ArgumentParser()
    ArgsParser.add_argument("-find", default=None, help="Find crypto info")
    ArgsParser.add_argument("-top", default=None,
                            type=int, help="Shows top n cryptos")
    
    return ArgsParser.parse_args()

def IsAnyArgumentsPassed():
    return len(sys.argv) > 1

################################################################################
################################################################################
################################################################################
"""                              MAIN                                        """

args = GetArgumetns()

if not IsAnyArgumentsPassed():
    print("No arguments were passed.\nUse --help for help.")
    raise SystemExit

if (args.find is not None):
    ShowCryptoInfo(args.find)

if (args.top is not None):
    if (args.top > 10):
        print("Maximum amount - 10")
    elif (args.top < 1):
        print("Minimum amount - 1")
    elif (args.top > 0):
        ShowTopNCryptoInfo(args.top)