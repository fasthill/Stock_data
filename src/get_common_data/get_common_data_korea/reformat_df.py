import numpy as np
import pandas as pd

# reformat data from yfinance
def reformat_df(df, col_name):
    df = df.reset_index('Date')
    df.drop(labels='Adj Close', axis=1, inplace=True)
    df = df[['Date', 'Close', 'Open', 'High', 'Low', 'Volume']]
    df.columns = ['date', col_name, 'open', 'high', 'low', 'volume']
    df['temp'] = df[col_name].shift(1)
    df[col_name+'_cr'] = ((df[col_name] - df['temp'])/df['temp']*100).apply(lambda x: f'{x:.2f}%')
    df.drop(labels='temp', axis=1, inplace=True)
    return df


if __name__ == '__main__':
    df_old = pd.read_csv('../../../data/test/d_old.csv', index_col=0)
    df_add = pd.read_csv('../../../data/test/d_new.csv', index_col=0)

    df_merge = concat_df(df_old, df_add, 0)
    # df_merge.to_csv('data/test/d_merge.csv')
    # df_merge.to_pickle('data/test/d_merge.pkl')
