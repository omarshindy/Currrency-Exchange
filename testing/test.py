import requests as rq
import os
import pandas as pd
from datetime import date
from dotenv import load_dotenv
from faker import Faker

f = Faker()
load_dotenv()  # Loads .env file


class CurrencyExchangeRates():
    data = None
    prod = None

    def __init__(self, prod=True):
        self.prod = prod

    def extract(self, symbols, date=None):
        query = {
            'app_id': os.getenv('appID'),
            'symbols': symbols
        }

        if self.prod:
            r = rq.get('https://openexchangerates.org/api/latest.json', params=query)
        else:
            r = rq.get('https://openexchangerates.org/api/historical/' + date.strftime("%Y-%m-%d") + '.json',
                       params=query)

        if r.status_code == 200:
            usdEgpRate, usdEurRate = r.json()['rates']['EGP'], r.json()['rates']['EUR']
            self.transform(usdEgpRate, usdEurRate, date)
        else:
            raise Exception(r.json()['message'])

    def transform(self, usdEgpRate, usdEurRate, date=None):
        egpToEur = usdEurRate / usdEgpRate
        egpToUSD = 1 / usdEgpRate

        self.data = pd.DataFrame([[egpToUSD, egpToEur]],
                                 columns=['usdRate', 'euroRate'])

        self.load(self.data, date)

    def load(self, df, date=None):
        
        if 'exchange-rates' in os.listdir('.'):
            dirs = os.listdir('exchange-rates')
        else:
            os.mkdir(f'exchange-rates')
            dirs = os.listdir('exchange-rates')

        if self.prod:
            currMonth, currYear, currDay = date.today().strftime("%b").lower(), date.today().strftime(
                "%Y").lower(), date.today().strftime("%-d")
        else:
            currMonth, currYear, currDay = date.strftime("%b").lower(), date.strftime(
                "%Y").lower(), date.strftime("%-d")
                
        # year, month and day check
        if currYear in dirs:
            pass
        else:
            os.mkdir(f'exchange-rates/{currYear}')

        if currMonth in os.listdir(f'exchange-rates/{currYear}'):
            pass
        else:
            os.mkdir(f'exchange-rates/{currYear}/{currMonth}')

        if currDay in os.listdir(f'exchange-rates/{currYear}/{currMonth}'):
            pass
        else:
            df.to_csv('exchange-rates/' + currYear + '/' + currMonth + '/' + currDay + '.csv', index=False)


if __name__ == '__main__':

    prod = False

    if prod:
        c = CurrencyExchangeRates(True)
        c.extract("egp,eur")
    else:
        c = CurrencyExchangeRates(False)

        dates = [f.date_between_dates(date_start=date(2015, 1, 1), date_end=date(2021, 4, 19)) for i in range(20)]

        for date in dates:
            c.extract("egp,eur", date=date)
