import requests
import json

__name__ = 'Rates converter'

def get_rate(base, symbol):

    if base == symbol: return 1
    
    if base == 'EUR':
        resp = requests.get('http://api.openrates.io/latest?symbols={}'.format(symbol))
    else:
        resp = requests.get('http://api.openrates.io/latest?base={}'.format(base))

    #Wrong status code, raise error
    if resp.status_code != 200:
        raise Exception('Response code not 200. Check openrates.io availability!')
    else:
        return json.loads(resp.content)['rates'][symbol]

def convert(amt, base, symbol):

    
    try:
        return amt * get_rate(base, symbol)
    
    except Exception as e:
        raise e