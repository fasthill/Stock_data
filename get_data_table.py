import pandas as pd

import io
import time
import datetime

from open_browser import open_browser
from set_current_unit import set_current_unit
from open_window_individual_stock_trend import open_window_individual_stock_trend
from set_date_n_search import set_date_n_search

def get_data_table(driver):  # table data 취득 and return dataframe
    df = \
    pd.read_html(io.StringIO(str(driver.page_source)), attrs={"class": "CI-GRID-BODY-TABLE"}, flavor=["lxml", "bs4"])[0]

    column_name = \
    ['date', 'close', 'change', 'close_cr', 'open', 'high', 'low', 'vol', 'vol_amount','total_amount', 'total_counts']
    # ['일자', '종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '시가총액', '상장주식수']

    df.columns = column_name
    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y/%m/%d"))
    df_get = df[['date', 'open', 'high', 'low', 'close', 'close_cr', 'vol']]

    return df_get


if __name__ == '__main__':
    # open browser
    main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'
    # 개별종목 시세추이 data-menu-id: MDC0201020103
    driver = open_browser()
    driver.get(main_url)

    set_current_unit(driver)

    # test function
    com_name = '005930/삼성전자'  # '000660/SK하이닉스'
    open_window_individual_stock_trend(driver, com_name)

    # date형식 변환후 입력
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 3, 1)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    set_date_n_search(driver, start_str, end_str)

    df = get_data_table(driver)

    time.sleep(5)  # wait before close
    driver.close()
