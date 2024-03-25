import datetime
import pandas as pd

from data.constant.constants import COMPANY_CODE
from get_investors_data_table import get_investors_data_table
from merge_df import merge_df
from open_browser import open_browser
from open_investors_window import open_investors_window
from open_window_investors_data import open_window_investors_data
from set_current_unit import set_current_unit
from set_date_n_search_inv import set_date_n_search_inv

code = COMPANY_CODE

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

# date형식 변환후 입력
# start_date = datetime.date(2023, 1, 2)
# end_date = datetime.date(2023, 1, 5)
# start_str = start_date.strftime('%Y-%m-%d')
# end_str = end_date.strftime('%Y-%m-%d')

data_directory = 'data/investors_data/'
total = len(code)

for i, (key, val) in enumerate(code.items()):
    com_name = "/".join([key, val[0]])
    pkl_name = '{}_investors.pkl'.format(val[1])
    try:
        df_o = pd.read_pickle(data_directory + pkl_name)
        start_date = df_o['date'].iloc[len(df_o) - 1]
    except:
        start_date = datetime.date(2022, 1, 1)  # 데이터 취득 시작 일자

    open_window_investors_data(driver, com_name)

    start_date = datetime.date(2023, 1, 2)
    end_date = datetime.date(2023, 1, 5)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    # set_date_n_search_inv(driver, start_str, end_str)

    df_get = get_investors_data_table(driver, start_date, end_date)

    # delete "total" column
    df_col = ['date', 'retail', 'foreigner', 'institution', 'financial', 'invtrust',
              'pension', 'privequity', 'bank', 'insurance', 'financeetc',
              'corporateetc', 'foreigneretc']
    df_get = df_get[df_col]

    df_o = merge_df(df_o, df_get, 0)  # 0번 칼럼 기준으로 정렬

    df_o.to_pickle(data_directory + pkl_name)
    df_o.to_csv(data_directory + pkl_name.replace('pkl', 'csv'))

    print(com_name, f'{i + 1}/{total}', end=', ')  # 진행상황 확인용

driver.close()
driver.quit()
