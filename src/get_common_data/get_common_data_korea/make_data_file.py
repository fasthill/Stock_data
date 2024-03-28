import os

import pandas as pd


def make_pickle(df_mp, file_name, dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except OSError:
        print("Error: Failed to create the directory.")

    df_mp.to_pickle(dir_name + file_name)
    df_mp.to_csv(dir_name + file_name.replace('pkl', 'csv'))


if __name__ == '__main__':
    dir_name = '../../../data/common/test/'
    file_name = 'kospi.pkl'
    df = pd.read_pickle(dir_name + file_name)
    make_pickle(df, 'kospi_t.pkl', dir_name)
    print("test")
