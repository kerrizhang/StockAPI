''' Project #3: Jack of All Trades
Name: Kerri Zhang
SID: 21529066
Date: 11/16/18
'''

import project3_indicators
import project3_signal_strategies
import project3_iex_api

def true_range_input(indicator: list, stock_data: [dict]) -> tuple:
    '''True Range indicator and signal strategies'''
    indicator_object = project3_indicators.TrueRange()
    indicator_object.set_data(stock_data)
    indicator_list = indicator_object.calc_indicator()
    signal_strat_object = project3_signal_strategies.TrueRangeStrategy()
    signal_strat_object.set_buy_relationship_threshold(indicator[1][0], float(indicator[1][1:]))
    signal_strat_object.set_sell_relationship_threshold(indicator[2][0], float(indicator[2][1:]))
    signal_strat_object.indicator_input(indicator_list)
    buy_sell_list = signal_strat_object.signal_strategies()
    return (indicator_list, buy_sell_list)

def simple_moving_average_input(field: str, indicator: list, stock_data: [dict]) -> tuple:
    '''Simple moving average indicator and signal strategies'''
    indicator_object = project3_indicators.SimpleMovingAverage()
    indicator_object.set_field(field)
    indicator_object.set_data(stock_data)
    indicator_object.set_n_days(int(indicator[1]))
    indicator_list = indicator_object.calc_indicator()
    signal_strat_object = project3_signal_strategies.SimpleMovingAverageStrategy()
    signal_strat_object.indicator_input(indicator_list)
    signal_strat_object.set_field(field)
    signal_strat_object.set_data(stock_data)
    buy_sell_list = signal_strat_object.signal_strategies()
    return (indicator_list, buy_sell_list)


def directional_indicator_input(field: str, indicator: list, stock_data:[dict]) -> tuple:
    '''Directional indicator and signal strategies'''
    indicator_object = project3_indicators.DirectionalIndicator()
    indicator_object.set_field(field)
    indicator_object.set_data(stock_data)
    indicator_object.set_n_days(int(indicator[1]))
    indicator_list = indicator_object.calc_indicator()
    signal_strat_object = project3_signal_strategies.DirectionalIndicatorStrategy()
    signal_strat_object.indicator_input(indicator_list)
    signal_strat_object.set_field(field)
    signal_strat_object.set_buy_limit(int(indicator[2]))
    signal_strat_object.set_sell_limit(int(indicator[3]))
    buy_sell_list = signal_strat_object.signal_strategies()
    return (indicator_list, buy_sell_list)

def indicator_signal_strategies(stock_data: [dict]) -> tuple:
    '''Read input and generate report'''
    input_string = input().split()
    indicator_type = input_string[0]
    length = len(input_string)
    if indicator_type == 'TR' and length == 3:
        indicator_list, buy_sell_list = true_range_input(input_string, stock_data)

    elif (indicator_type == 'MP' or indicator_type == 'MV') and length == 2:
        if indicator_type == 'MP':
            field = "close"
        elif indicator_type == 'MV':
            field = "volume"
        indicator_list, buy_sell_list = simple_moving_average_input(field, input_string, stock_data)

    elif (indicator_type == 'DP' or indicator_type == 'DV') and length == 4:
        if indicator_type == 'DP':
            field = "close"
        elif indicator_type == 'DV':
            field = "volume"
        indicator_list, buy_sell_list = directional_indicator_input(field, input_string, stock_data)

    return (indicator_list, buy_sell_list)

def print_header(symbol: str, header: dict) -> None:
    '''Print header which specific basic information about the stock'''
    print(symbol)
    print(header['companyName'])
    print(header['sharesOutstanding'])

def print_report(stock_data: [dict], indicator_list: list, buy_sell_list: list) -> None:
    '''Print report separated by tabs'''
    for day_record, indicator_value, buy_sell in zip(stock_data, indicator_list, buy_sell_list):
        print_string = "{}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{}".format(day_record["date"], \
            day_record["open"], day_record["close"], day_record["high"], \
            day_record["low"], day_record["volume"])
        if indicator_value == None:
            print_string += '\t'
        else:
            if type(indicator_list[-1]) == int:
                print_string += "\t{}".format(indicator_value)
            else:
                print_string += "\t{:.4f}".format(indicator_value)
        print_string += "\t{}\t{}".format(buy_sell[0], buy_sell[1])
        print(print_string)


def run() -> None:
    '''Main function'''
    symbol = input()
    stock_data = project3_iex_api.get_stock_data(symbol)
    indicator_list, buy_sell_list = indicator_signal_strategies(stock_data)
    header = project3_iex_api.get_header(symbol)
    print_header(symbol, header)
    print_report(stock_data, indicator_list, buy_sell_list)
    print("{}\t{}\t{}".format("Data provided for free by IEX", "View IEX's Terms of Use", \
                              "https://iextrading.com/api-exhibit-a/"))

if __name__ == '__main__':
    run()