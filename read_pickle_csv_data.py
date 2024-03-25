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

data_directory = 'data/investors_data/'
total = len(code)

for i, (key, val) in enumerate(code.items()):
    com_name = "/".join([key, val[0]])
    pkl_name = '{}_investors.pkl'.format(val[1])
    df_o = pd.read_pickle(data_directory + pkl_name)

    df_col = ['date', 'retail', 'foreigner', 'institution', 'financial', 'invtrust',
              'pension', 'privequity', 'bank', 'insurance', 'financeetc',
              'corporateetc', 'foreigneretc']
    df_o = df_o[df_col]

    df_o.to_pickle(data_directory + pkl_name)
    df_o.to_csv(data_directory + pkl_name.replace('pkl', 'csv'))

    print(com_name, f'{i + 1}/{total}', end=', ')  # 진행상황 확인용
