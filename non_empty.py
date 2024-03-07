from selenium import webdriver as wd
from selenium.webdriver import ActionChains # scroll down 사용하기 위하여 선서
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup as bs

import datetime, time
from datetime import date

import pandas as pd
import numpy as np
import requests
import time
import os, sys, io

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from open_browser import open_browser
from set_current_unit import set_current_unit
from open_window_individual_stock_trend import open_window_individual_stock_trend
from set_date_n_search import set_date_n_search
from get_data_table import get_data_table

def non_empty_index_df(df_input, start_date, end_date): # 토,일,공휴일등 거래가 없는 일자도 모두 포함
    date_range_ts = pd.date_range(start=start_date, end=end_date)
    df_input.set_index('date', inplace=True)
    df_out = pd.DataFrame(columns = df_input.columns)
    df_out.insert(0, 'date', date_range_ts)
    df_out.set_index('date', inplace=True)
    df_out.update(df_input)
    df_out.reset_index(inplace=True)
    return df_out


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

    df = non_empty_index_df(df, start_date, end_date)

    time.sleep(5)  # wait before close
    driver.close()

