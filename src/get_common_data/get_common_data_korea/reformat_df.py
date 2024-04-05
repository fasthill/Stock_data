import datetime

import yfinance as yf  # 아래와 함께 pandas_datareader, yf.pdr_override 같이 사용해야 함.
from pandas_datareader import data as pdr

yf.pdr_override()


# reformat data from yfinance
def reformat_df(df, col_name):
    df = df.reset_index('Date')
    df.drop(labels='Adj Close', axis=1, inplace=True)
    df = df[['Date', 'Close', 'Open', 'High', 'Low', 'Volume']]
    df.columns = ['date', col_name, 'open', 'high', 'low', 'volume']
    df['temp'] = df[col_name].shift(1)
    df[col_name + '_cr'] = ((df[col_name] - df['temp']) / df['temp'] * 100).apply(lambda x: f'{x:.2f}%')
    df.drop(labels='temp', axis=1, inplace=True)
    return df


if __name__ == '__main__':
    startdate = datetime.date(2021, 12, 25)
    enddate = datetime.date.today() + datetime.timedelta(days=2)
    start_str = startdate.strftime('%Y-%m-%d')
    end_str = enddate.strftime('%Y-%m-%d')
    spx = pdr.get_data_yahoo('^SPX', start=start_str, end=end_str)
    df = reformat_df(spx, 'spx')
    print(df.head())
