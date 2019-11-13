''' Project #3: Jack of All Trades
Name: Kerri Zhang
SID: 21529066
Date: 11/16/18
'''

class TrueRangeStrategy:
    '''Generate buy and sell signals based on the true range'''
    def __init__(self):
        self.indicator = []
        self.buy_relationship = None
        self.sell_relationship = None
        self.buy_threshold = None
        self.sell_threshold = None

    def set_buy_relationship_threshold(self, relationship: str, threshold: float) -> None:
        '''Buy relationship threshold'''
        self.buy_relationship = relationship
        self.buy_threshold = threshold

    def set_sell_relationship_threshold(self, relationship: str, threshold: float) -> None:
        '''Sell relationship threshold'''
        self.sell_relationship = relationship
        self.sell_threshold = threshold

    def indicator_input(self, indicator: list) -> None:
        '''Input with indicator and signal strategy'''
        self.indicator = indicator

    def signal_strategies(self) -> [tuple]:
        '''Generate buy and sell strategies when true range divided by
         closing price meets treshold'''
        indicator = self.indicator
        true_range_percentage_return = []
        buy_relationship = self.buy_relationship
        sell_relationship = self.sell_relationship
        buy_threshold = self.buy_threshold
        sell_threshold = self.sell_threshold

        for true_range_percentage_value in indicator:
            buy_strategy = ''
            sell_strategy = ''
            if true_range_percentage_value != None:
                buy_strategy = ''
                sell_strategy = ''
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

            true_range_percentage_return.append((buy_strategy, sell_strategy))

        return true_range_percentage_return

class SimpleMovingAverageStrategy:
    '''Generate buy and sell signals based on the N-day simple moving average of closing
    prices or volumes'''
    def __init__(self):
        self.indicator = []
        self.stock_data = []
        self.field = ''

    def indicator_input(self, indicator: list) -> None:
        '''Input with indicator and signal strategy'''
        self.indicator = indicator

    def set_data(self, data: [dict]) -> None:
        '''Stock data to generate signal strategies'''
        self.stock_data = data

    def set_field(self, field: str) -> None:
        '''Field either close or volume'''
        self.field = field

    def signal_strategies(self) -> [tuple]:
        '''Generate buy and sell strategies when closing price or volume crosses
         simple moving average'''
        stock_data = self.stock_data
        field = self.field
        buy_sell_list = []
        current_state = None
        for current_day_record, avg_float in zip(stock_data, self.indicator):
            buy_strategy = ''
            sell_strategy = ''

            if avg_float != None:
                if current_day_record[field] > avg_float:
                    if current_state == 'below':
                        buy_strategy = 'BUY'
                    current_state = 'above'

                elif current_day_record[field] < avg_float:
                    if current_state == 'above':
                        sell_strategy = 'SELL'
                    current_state = 'below'

            buy_sell_list.append((buy_strategy, sell_strategy))

        return buy_sell_list

class DirectionalIndicatorStrategy:
    '''Generate buy and sell signals based on the N-day directional indicator of closing
    prices or volumes'''
    def __init__(self):
        self.indicator = []
        self.field = ''
        self.sell_limit = None
        self.buy_limit = None

    def indicator_input(self, indicator: list) -> None:
        '''Input with indicator and signal strategy'''
        self.indicator = indicator

    def set_field(self, field: str) -> None:
        '''Field either close or volume'''
        self.field = field

    def set_buy_limit(self, buy_limit: int) -> None:
        '''Buy relationship threshold'''
        self.buy_limit = buy_limit

    def set_sell_limit(self, sell_limit: int) -> None:
        '''Sell relationship threshold'''
        self.sell_limit = sell_limit

    def signal_strategies(self) -> [tuple]:
        '''Generate buy and sell strategies when directional indicator crosses treshold'''
        buy_sell_list = []
        buy_threshold = self.buy_limit
        sell_threshold = self.sell_limit

        current_buy_state = None
        current_sell_state = None
        for sum in self.indicator:
            buy_strategy = ''
            sell_strategy = ''

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

            buy_sell_list.append((buy_strategy, sell_strategy))

        return buy_sell_list
