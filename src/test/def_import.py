import pandas as pd


def test_import():
    data_ = '../../data/company/historical_data/sec_historical.csv'
    df = pd.read_csv(data_)

    assert isinstance(df, object)
    return df
