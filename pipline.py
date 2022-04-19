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

    def extract(self, symbols):
        query = {
            'app_id': os.getenv('appID'),
            'symbols': symbols
        }

        r = rq.get('https://openexchangerates.org/api/latest.json', params=query)
        
        if r.status_code == 200:
            usdEgpRate, usdEurRate = r.json()['rates']['EGP'], r.json()['rates']['EUR']
            self.transform(usdEgpRate, usdEurRate)
        else:
            raise Exception(r.json()['message'])

    def transform(self, usdEgpRate, usdEurRate):
        egpToEur = usdEurRate / usdEgpRate
        egpToUSD = 1 / usdEgpRate

        self.data = pd.DataFrame([[egpToUSD, egpToEur]],
                                columns=['usdRate', 'euroRate'])

        self.load(self.data)

    def load(self, df):
        
        if 'exchange-rates' in os.listdir('.'):
            dirs = os.listdir('exchange-rates')
        else:
            os.mkdir(f'exchange-rates')
            dirs = os.listdir('exchange-rates')

        currMonth, currYear, currDay = date.today().strftime("%b").lower(), date.today().strftime(
            "%Y").lower(), date.today().strftime("%-d")                
            
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
    c = CurrencyExchangeRates()
    c.extract("egp,eur")