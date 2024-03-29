import datetime
import io

import cloudscraper
import pandas as pd

from data.constant.constants import HEADERS
from save_data_file import update_data, save_data


def get_cpi(url, column, sel_column):
    scraper = cloudscraper.create_scraper()
    res = scraper.get(url, headers=HEADERS)
    df = pd.read_html(io.StringIO(str(res.text)), flavor=["lxml", "bs4"])[0]
    df.columns = column
    df['time'] = df['time'].apply(lambda x: datetime.datetime.strptime(x, "%H:%M").time())
    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x[:12], "%b %d, %Y"))

    df = df[sel_column]

    try:  # convert timestamp to datetime.datetime.date
        df['date'] = df['date'].apply(lambda x: datetime.datetime.date(x))
    except:
        pass

    df.sort_values(by=['date'], inplace=True)

    return df


if __name__ == '__main__':
    cpi_url = 'https://www.investing.com/economic-calendar/cpi-733'
    cpi_column = ['date', 'time', 'cpi', 'cpi_anticipated', 'cpi_previous', 'none']
    file_name = 'cpi.pkl'
    cpi_sel_col = ['date', 'cpi', 'cpi_anticipated', 'cpi_previous']
    df = get_cpi(cpi_url, cpi_column, cpi_sel_col)

    dir_name = '../../../data/common/test/'
    df_up = update_data(df, file_name, dir_name)
    save_data(df_up, file_name, dir_name)

# 2023년 5월부터 11월 사이의 데이터가 없음. 추가로 일자를 확인하여 빠짐없이 추가해야 함.
