import pandas as pd

from data.constant.constants import COMPANY_CODE

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
