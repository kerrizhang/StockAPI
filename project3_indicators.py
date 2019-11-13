''' Project #3: Jack of All Trades
Name: Kerri Zhang
SID: 21529066
Date: 11/16/18
'''

class TrueRange:
    '''If enter TR as an indicator'''
    def __init__(self) -> None:
        self.stock_data = []

    def set_data(self, data: [dict]) -> None:
        '''Stock data to generate indicators'''
        self.stock_data = data

    def calc_indicator(self) -> list:
        '''Range of prices for the current day'''
        true_range_percentage_return = []
        prev_close = None
        stock_data = self.stock_data
        for records in stock_data:
            if prev_close != None:
                high = records["high"]
                low = records["low"]
                if prev_close > high:
                    high = prev_close
                elif prev_close < low:
                    low = prev_close
                true_range = high - low
                true_range_percentage_value = (true_range / prev_close) * 100
            else:
                true_range_percentage_value = None

            true_range_percentage_return.append(true_range_percentage_value)
            prev_close = records["close"]

        return true_range_percentage_return

class SimpleMovingAverage:
    '''If enter MP or MV as an indicator'''
    def __init__(self):
        self.stock_data = []
        self.field = None
        self.days = 1

    def set_data(self, data: [dict]) -> None:
        '''Stock data to generate indicators'''
        self.stock_data = data

    def set_field(self, field: str) -> None:
        '''Field either close or volume'''
        self.field = field

    def set_n_days(self, days: int) -> None:
        '''The most recent N days to calculate average'''
        self.days = days

    def calc_indicator(self) -> list:
        '''The average of the most recent N closing prices'''
        stock_data = self.stock_data
        field = self.field
        days = self.days
        avg_list = []
        for current_day in range(len(stock_data)):
            if current_day < days - 1:
                avg_list.append(None)
            else:
                sum = 0
                for n_days in range((current_day - days) + 1, current_day + 1):
                    sum += stock_data[n_days][field]

                avg = sum/days
                avg_list.append(avg)
        return avg_list

class DirectionalIndicator:
    '''If enter DP or DV as an indicator'''
    def __init__(self):
        self.stock_data = []
        self.field = None
        self.days = 1

    def set_data(self, data: [dict]) -> None:
        '''Stock data to generate indicators'''
        self.stock_data = data

    def set_field(self, field: str) -> None:
        '''Field either close or volume'''
        self.field = field

    def set_n_days(self, days: int) -> None:
        '''The most recent N days to calculate directional indicator'''
        self.days = days

    def calc_indicator(self) -> list:
        '''The number of closing prices out of the most recent N on which the stock's price went up
         minus the number of days out of the previous N on which the stock's price went down'''
        stock_data = self.stock_data
        field = self.field
        days = self.days
        directional_list = []
        prev_close = None
        for current_day in range(len(stock_data)):
            sum = 0
            start_day = max(0, (current_day - days) + 1)
            for n_days in range(start_day, current_day + 1):
                if n_days != 0:
                    prev_close = stock_data[n_days - 1][field]
                    if stock_data[n_days][field] > prev_close:
                        sum += 1
                    elif stock_data[n_days][field] < prev_close:
                        sum -= 1

            directional_list.append(sum)

        return directional_list