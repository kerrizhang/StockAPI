'''
Name: Kerri Zhang
SID: 21529066
Date: 11/16/18
'''


import json
import ssl
import urllib
import urllib.request

URL = 'https://api.iextrading.com/1.0'

def get_result(url: str) -> dict:
    '''
    This function takes a URL and returns a Python dictionary representing the
    parsed JSON response.
    '''
    #print(url)
    response = None

    try:
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(url, context=context)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)

    finally:
        if response != None:
            response.close()


def complete_url(symbol: str) -> str:
    URL = 'https://api.iextrading.com/1.0'

    range_input = input()
    if range_input == 'M':
        range = '1m'
    elif range_input == 'Y':
        range = '1y'
    elif range_input == 'F':
        range = '5y'
    else:
        print('ERROR')
    url = URL+ '/stock/' + symbol + '/chart/' + range
    return url

def print_header(symbol: str) -> None:
    URL = 'https://api.iextrading.com/1.0'
    url = URL + '/stock/' + symbol + '/stats'
    header = get_result(url)
    print(symbol.upper())
    print(header['companyName'])
    print(header['sharesOutstanding'])


def indicator_signal_strategies(stock_data: dict) -> [tuple]:
    indicator = input().split()
    indicator_type = indicator[0]
    length = len(indicator)
    if indicator_type == 'TR' and length == 3:
        return_list = true_range(indicator, stock_data)

    elif (indicator_type == 'MP' or indicator_type == 'MV') and length == 2:
        if indicator_type == 'MP':
            field = "close"
        elif indicator_type == 'MV':
            field = "volume"
        return_list = moving_average(indicator, stock_data, field)

    elif (indicator_type == 'DP' or indicator_type == 'DV') and length == 4:
        if indicator_type == 'DP':
            field = "close"
        elif indicator_type == 'DV':
            field = "volume"
        return_list = directional_indicator(indicator, stock_data, field)

    return return_list




def true_range(indicator: list, stock_data: dict) -> [tuple]:
    true_range_percentage_return = []
    prev_close = None
    buy_relationship = indicator[1][0]
    sell_relationship = indicator[2][0]
    buy_threshold = float(indicator[1][1:])
    sell_threshold = float(indicator[2][1:])

    for records in stock_data:
        buy_strategy = ''
        sell_strategy = ''
        if prev_close != None:
            high = records["high"]
            low = records["low"]
            if prev_close > high:
                high = prev_close
            elif prev_close < low:
                low = prev_close
            true_range = high - low
            true_range_percentage_value = (true_range/prev_close) * 100
            if buy_relationship == '>':
                if true_range_percentage_value > buy_threshold:
                    buy_strategy = 'BUY'

            else:
                if true_range_percentage_value < buy_threshold:
                    buy_strategy = 'BUY'

            if sell_relationship == '>':
                if true_range_percentage_value > sell_threshold:
                    sell_strategy = 'SELL'

            else:
                if true_range_percentage_value < sell_threshold:
                    sell_strategy = 'SELL'


            true_range_percentage = "{:.4f}".format(true_range_percentage_value)
        else:
            true_range_percentage = ""

        true_range_percentage_return.append((true_range_percentage, buy_strategy, sell_strategy))
        prev_close = records["close"]

    return true_range_percentage_return


def moving_average(indicator: list, stock_data: dict, field: str) -> [tuple]:
    avg_list = []
    days = int(indicator[1])
    current_state = None
    for current_day in range(len(stock_data)):
        buy_strategy = ''
        sell_strategy = ''
        if current_day < days - 1:
            avg_list.append(('', '', ''))

        else:
            sum = 0
            for n_days in range((current_day - days) + 1, current_day + 1):
                sum += stock_data[n_days][field]

            avg_float = sum/days
            avg = "{:.4f}".format(sum/days)
            if stock_data[current_day][field] > avg_float:
                if current_state == 'below':
                    buy_strategy = 'BUY'
                current_state = 'above'

            elif stock_data[current_day][field] < avg_float:
                if current_state == 'above':
                    sell_strategy = 'SELL'
                current_state = 'below'

            avg_list.append((avg, buy_strategy, sell_strategy))

    return avg_list

def directional_indicator(indicator: list, stock_data: dict, field: str) -> [tuple]:
    directional_list = []
    days = int(indicator[1])
    buy_threshold = int(indicator[2])
    sell_threshold = int(indicator[3])
    prev_close = None
    current_buy_state = None
    current_sell_state = None
    for current_day in range(len(stock_data)):
        buy_strategy = ''
        sell_strategy = ''
        sum = 0
        start_day = max(0, (current_day - days) + 1)
        for n_days in range(start_day, current_day +1):
            if n_days != 0:
                prev_close = stock_data[n_days - 1][field]
                if stock_data[n_days][field] > prev_close:
                    sum += 1
                elif stock_data[n_days][field] < prev_close:
                    sum -= 1

        if sum > buy_threshold:
            if current_buy_state == 'below':
                buy_strategy = 'BUY'
            current_buy_state = 'above'
        elif sum < buy_threshold:
            current_buy_state = 'below'

        if sum < sell_threshold:
            if current_sell_state == 'above':
                sell_strategy = 'SELL'
            current_sell_state = 'below'
        elif sum > sell_threshold:
            current_sell_state = 'above'

        directional_list.append((sum, buy_strategy, sell_strategy))

    return directional_list

def run() -> None:
    symbol = input()
    url = complete_url(symbol)
    stock_data = get_result(url)
    return_list = indicator_signal_strategies(stock_data)
    print_header(symbol)

    for day_record, return_value in zip(stock_data, return_list):
        print("{}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{}\t{}\t{}\t{}".format(day_record["date"], \
            day_record["open"], day_record["close"], day_record["high"], \
            day_record["low"], day_record["volume"], return_value[0], return_value[1], return_value[2]))
    print("{}\t{}\t{}".format("Data provided for free by IEX", "View IEX's Terms of Use", \
                            "https://iextrading.com/api-exhibit-a/"))

if __name__ == '__main__':
    run()