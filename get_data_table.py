from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import pandas as pd
import numpy as np

import io
import time
import datetime

from open_browser import open_browser
from set_current_unit import set_current_unit
from open_window_individual_stock_trend import open_window_individual_stock_trend
from set_date_n_search import set_date_n_search

def get_data_table(driver):  # table data 취득 and return dataframe
    # bottom_open_button = '#jsMdiContent > div > div.result_bottom.CI-MDI-COMPONENT-FOOTER.on2 > button'
    #
    # scroll = driver.find_element(By.CSS_SELECTOR, bottom_open_button)
    # action = ActionChains(driver)
    # action.move_to_element(scroll).perform()

    # read_html로 먼저 읽고 같은 column형식으로 70~80개씩 끊어서 df를 형성하여 concat으로 처리하는 로직 필요

    # c_tr = '#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS.CI-GRID-CLICKED > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody > tr'
    # no_of_rows = driver.find_elements(By.CSS_SELECTOR, c_tr)
    # print("*************", len(no_of_rows))

    df = \
    pd.read_html(io.StringIO(str(driver.page_source)), attrs={"class": "CI-GRID-BODY-TABLE"}, flavor=["lxml", "bs4"])[0]

    column_name = \
    ['date', 'close', 'change', 'close_cr', 'open', 'high', 'low', 'vol', 'vol_amount','total_amount', 'total_counts']
    # ['일자', '종가', '대비', '등락률', '시가', '고가', '저가', '거래량', '거래대금', '시가총액', '상장주식수']

    df.columns = column_name
    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(x, "%Y/%m/%d"))
    df_get = df[['date', 'open', 'high', 'low', 'close', 'close_cr', 'vol']]

    df_get_c = df_get.sort_values(by='date').copy()
    df_get_c.index = np.arange(0, len(df_get_c))

    return df_get_c


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
    start_date = datetime.date(2021, 12, 27)
    end_date = datetime.date(2024, 3, 7)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    set_date_n_search(driver, start_str, end_str)

    df = get_data_table(driver)

    df.to_csv('sec.csv')

    time.sleep(5)  # wait before close
    driver.close()
