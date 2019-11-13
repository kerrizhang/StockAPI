''' Project #3: Jack of All Trades
Name: Kerri Zhang
SID: 21529066
Date: 11/16/18
'''

import json
import ssl
import urllib
import urllib.request

URL = 'https://api.iextrading.com/1.0'


def get_header(symbol: str) -> dict:
    '''Header formed from response'''
    url = URL + '/stock/' + symbol + '/stats'
    header = _get_result(url)
    return header


def get_stock_data(symbol) -> [dict]:
    '''Stock data formed from URL'''
    url = _complete_url(symbol)
    stock_data = _get_result(url)
    return stock_data

def _get_result(url: str) -> dict:
    '''This function takes a URL and returns a Python dictionary representing the
    parsed JSON response.'''
    response = None

    try:
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(url, context=context)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)

    finally:
        if response != None:
            response.close()

def _complete_url(symbol: str) -> str:
    '''Adds range to the URL'''
    range_input = input()
    if range_input == 'M':
        range = '1m'
    elif range_input == 'Y':
        range = '1y'
    elif range_input == 'F':
        range = '5y'

    url = URL+ '/stock/' + symbol + '/chart/' + range
    return url
