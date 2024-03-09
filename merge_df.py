import pandas as pd
import numpy as np

def merge_df(df_old, df_add, subset_col):
    df_merge = pd.concat([df_old, df_add], ignore_index=True)
    df_merge.drop_duplicates(subset=[subset_col], keep='last', inplace=True)
    df_merge.sort_values(by=[df_merge.columns[0]], inplace=True)
    df_merge.index = np.arange(0, len(df_merge))  # 일련 번호 오름차순으로 재 설정

    return df_merge


if __name__ == '__main__':
    df_old = pd.read_csv('data/test/d_old.csv',  index_col=0)
    df_add = pd.read_csv('data/test/d_new.csv',  index_col=0)

    df_merge = merge_df(df_old, df_add, 'date')
    df_merge.to_csv('data/test/d_merge.csv')
    df_merge.to_pickle('data/test/d_merge.pkl')


