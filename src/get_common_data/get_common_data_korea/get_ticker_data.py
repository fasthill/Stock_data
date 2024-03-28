import datetime
import numpy as np
import pandas as pd
import yfinance as yf

from make_data_file import make_pickle

yf.pdr_override()


def get_ticker_data(ticker, startdate, enddate, col_name):
    ydata = yf.Ticker(ticker)
    rdata = ydata.history(period="2y")  # 오늘부터 2년치
    rdata.reset_index('Date', inplace=True)
    rdata['Date'] = rdata['Date'].dt.date  # datetime64 to datetime.date()
    rdata = rdata[(rdata['Date'] <= enddate) & (rdata['Date'] >= startdate)]
    rdata['temp'] = rdata['Close'].shift(1)
    val_temp = (rdata['Close'] - rdata['temp']) / rdata['temp'] * 100
    rdata[f'{col_name}_cr'] = val_temp.map("{:.2f}%".format)
    rdata = rdata[['Date', 'Close', 'Open', 'High', 'Low', 'Volume', f'{col_name}_cr']]  # 필요한 column만 남김
    rdata.columns = ['date', f'{col_name}', 'open', 'high', 'low', 'volume', f'{col_name}_cr']  # column이름 통일
    rdata.reset_index(drop=True, inplace=True)  # index번호를 0부터 재정리
    return rdata


if __name__ == '__main__':
    startdate = datetime.date(2021, 12, 25)
    enddate = datetime.date.today() + datetime.timedelta(days=2)

    ticker_ = '^DJI'
    col_name_ = 'dji'
    dji = get_ticker_data(ticker_, startdate, enddate, col_name_)

    file_name = col_name_ + '.pkl'
    dir_name = '../../../data/common/test/'
    make_pickle(dji, file_name, dir_name)
    print("test")
