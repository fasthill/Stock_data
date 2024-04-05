import datetime
import io

import cloudscraper
import pandas as pd

from data.constant.constants import US_SECTOR_LIST
from save_data_file import update_data, save_data

us_sector_list = US_SECTOR_LIST
# reformat data from yfinance
for sector in us_sector_list:
    make_pickle(get_ticker_data(sector[0], startdate, enddate, sector[1]), sector[2])


if __name__ == '__main__':
    startdate = datetime.date(2021, 12, 25)
    enddate = datetime.date.today() + datetime.timedelta(days=2)
    start_str = startdate.strftime('%Y-%m-%d')
    end_str = enddate.strftime('%Y-%m-%d')
    spx = pdr.get_data_yahoo('^SPX', start=start_str, end=end_str)
    df = reformat_df(spx, 'spx')
    print(df.head())
