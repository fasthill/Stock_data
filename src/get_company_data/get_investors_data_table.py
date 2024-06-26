import datetime
import io
import pandas as pd
import time

from src.get_company_data.open_browser import open_browser
from src.get_company_data.open_investors_window import open_investors_window
from src.get_company_data.open_window_investors_data import open_window_investors_data
from src.get_company_data.set_current_unit import set_current_unit
from src.get_company_data.set_date_n_search_inv import set_date_n_search_inv


def convert_date(s_date, e_date):
    date_range_ts = pd.date_range(start=s_date, end=e_date)
    date_range = []
    for x in date_range_ts:
        date_range.append(datetime.datetime.strftime(x, "%Y%m%d"))
    return date_range


def get_investors_data_table(driver_, s_date, e_date):  # table data 취득 and return dataframe
    # 여기에 set data n search를 같이 집어 넣어서 table를 찾아야 함.
    # 매일 매일의 테이블을 append 시켜서 한개의 table로 만들어 반환해야함.
    index_name = ['investor', 'sell_quantity', 'buy_quantity', 'pure_buy_quantity', 'sell', 'buy', 'pure_buy']
    column_name = ['financial', 'insurance', 'invtrust', 'privequity', 'bank', 'financeetc', 'pension',
                   'institution', 'corporateetc', 'retail', 'foreigner', 'foreigneretc', 'total']

    base_data_directory = '../../data/base_data/stock_market_holydays/'
    opening_days_kor = pd.read_pickle(base_data_directory + 'opening_days_kor.pkl')  # 한국 개장일 데이터

    date_range = convert_date(s_date, e_date)

    df_org = None
    for datei in date_range:

        date = datetime.datetime.strptime(datei, "%Y%m%d").date()
        if date not in list(opening_days_kor):
            continue

        date_str = date.strftime('%Y-%m-%d')
        set_date_n_search_inv(driver_, date_str, date_str)

        df = pd.read_html(io.StringIO(str(driver_.page_source)),
                          attrs={"class": "CI-GRID-BODY-TABLE"}, flavor=["lxml", "bs4"])[0]

        df.columns = index_name
        df_new = df[['investor', 'pure_buy']]  # 순매수 금액
        df_new.set_index('investor', inplace=True)
        dft = df_new.T
        dft.columns = column_name
        dft.insert(0, "date", datetime.datetime.strptime(datei, "%Y%m%d"))
        dft.reset_index(drop=True, inplace=True)
        if df_org is None:
            df_org = dft.copy()
            continue
        #         df_org = df_org.append(dft, ignore_index=True) # append will be depreciated
        df_org = pd.concat([df_org, dft], ignore_index=True)

    return df_org


if __name__ == '__main__':
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
    open_window_investors_data(driver, code_n_name)

    # date형식 변환후 입력
    start_date = datetime.date(2024, 3, 4)
    end_date = datetime.date(2024, 3, 6)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    df = get_investors_data_table(driver, start_date, end_date)

    df.to_csv('sec.csv')

    time.sleep(5)  # wait before close
    driver.close()
