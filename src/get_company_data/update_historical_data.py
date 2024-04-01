import datetime
import pandas as pd

from data.constant.constants import COMPANY_CODE
from set_date_n_search_his import set_date_n_search_his
from src.get_company_data.concat_df import merge_df
from src.get_company_data.get_historical_data_table import get_historical_data_table
from src.get_company_data.open_browser import open_browser
from src.get_company_data.open_window_historical_data import open_window_historical_data
from src.get_company_data.set_current_unit import set_current_unit

code = COMPANY_CODE

# open browser
main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'
# 개별종목 시세추이 data-menu-id: MDC0201020103
driver = open_browser()
driver.get(main_url)

set_current_unit(driver, 1)

data_directory = '../../data/company/historical_data/'
total = len(code)

for i, (key, val) in enumerate(code.items()):
    com_name = "/".join([key, val[0]])
    pkl_name = '{}_historical.pkl'.format(val[1])
    try:
        df_o = pd.read_pickle(data_directory + pkl_name)
        start_date = df_o['date'].iloc[len(df_o) - 1]
    except:
        start_date = datetime.date(2022, 1, 1)  # 데이터 취득 시작 일자

    open_window_historical_data(driver, com_name)

    start_date = datetime.date(2023, 1, 2)
    end_date = datetime.date(2023, 1, 5)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    set_date_n_search_his(driver, start_str, end_str)

    df_get = get_historical_data_table(driver)

    df_o = merge_df(df_o, df_get, 0)  # 0번 칼럼 기준으로 정렬

    df_o.to_pickle(data_directory + pkl_name)
    df_o.to_csv(data_directory + pkl_name.replace('pkl', 'csv'))

    print(com_name, f'{i + 1}/{total}', end=', ')  # 진행상황 확인용

    # if i == 0:
    #     break

driver.close()
driver.quit()
