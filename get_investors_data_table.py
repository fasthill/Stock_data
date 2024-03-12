from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import pandas as pd
import numpy as np

import io
import time
import datetime

from open_browser import open_browser
from set_current_unit import set_current_unit
from open_investors_window import open_investors_window
from open_window_investors_data import open_window_investors_data
from set_date_n_search import set_date_n_search

def get_investors_data_table(driver, s_date, e_date):  # table data 취득 and return dataframe
    # 여기에 set data n search를 같이 집어 넣어서 table를 찾아야 함.
    # 매일 매일의 테이블을 append 시켜서 한개의 table로 만들어 반환해야함.

    return df_get_c


if __name__ == '__main__':

    # open browser
    main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203'
    # 개별종목 시세추이 data-menu-id: MDC0201020103
    driver = open_browser()
    driver.get(main_url)

    open_investors_window(driver)
    #
    set_current_unit(driver, 2)

    # test function
    code_n_name = '005930/삼성전자'  # '000660/SK하이닉스'
    open_window_investors_data(driver, code_n_name)

    # date형식 변환후 입력
    start_date = datetime.date(2021, 12, 27)
    end_date = datetime.date(2024, 3, 7)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    set_date_n_search(driver, start_str, end_str, 2)

    df = get_investors_data_table(driver)

    df.to_csv('sec.csv')

    time.sleep(5)  # wait before close
    driver.close()
