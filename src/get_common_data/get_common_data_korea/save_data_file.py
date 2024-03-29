import os

import pandas as pd
from concat_df import concat_df


def save_data(df_s, file_name, dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except OSError:
        print("Error: Failed to create the directory.")

    df_s.to_pickle(dir_name + file_name)
    df_s.to_csv(dir_name + file_name.replace('pkl', 'csv'))


def update_data(df_in, file_name, dir_name):
    df_o = pd.read_pickle(dir_name + file_name)
    try:  # convert timestamp to datetime.datetime.date
        df_o['date'] = df_o['date'].apply(lambda x: datetime.datetime.date(x))
    except:
        pass
    df_con = concat_df(df_o, df_in, 0)

    return df_con


if __name__ == '__main__':
    dir_name = '../../../data/common/test/'
    file_name = 'kospi.pkl'
    df = pd.read_pickle(dir_name + file_name)
    save_data(df, 'kospi_t.pkl', dir_name)
    print("test")
