#!/usr/bin/env python
# coding: utf-8

# #### 지표 UPDATE 
#    - 주요 주식시장 지수 : spx, dji, ixix, 코스피, 코스닥은 따로 krx 정보시스템에서 취득
#    - 반도체지수, VIX 지수: sox, vix
#    - 미국 채권 지수, 한국 채권 지수
#    - 원화 환율
#    - 선물 : 미국 3대 지수, wti, 달러지수 선물

# In[1]:


# from bs4 import BeautifulSoup as bs
import requests
import datetime, time
import pickle

import pandas as pd
import numpy as np

import os
import sys
import io
import shutil



# In[2]:



# from datetime import datetime
import yfinance as yf
yf.pdr_override()





import cloudscraper  # !pip install cfscrape # 403 forbidden, cloudflare error을 해결하기 위한 모듈
scraper = cloudscraper.create_scraper()
#  이후 403 error이 발생한 곳에는 requests 대신 scraper 사용


from data.constant.constants import US_SECTOR_LIST


headers = {'User-Agent': 'Mozilla/6.0 (Macintosh; Intel Mac OS X 10_11_5) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def correct_date_format(df):
# 시간, 미국, 한국 접속사이트에 따라 attribute 가 변경되서 나타나기 때문에 error  처리를 위해 try 사용
    try:
        df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x, "%b %d, %Y"))
    except:
        try:
            df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x, "%m/%d/%Y"))
        except:
            try:
                df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x, "%Y- %m- %d"))
            except:
                df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x, "%Y년 %m월 %d일"))
    
    try:  # convert timestamp to datetime.datetime.date
        df['date'] = df['date'].apply(lambda x: datetime.datetime.date(x))
    except:
        pass
    
    return df


def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


def make_pickle(df, pkl_name):
    pkl_directory = 'data/common/common_korea'
    try:
        if not os.path.exists(pkl_directory):
            os.makedirs(pkl_directory)
    except OSError:
        print("Error: Failed to create the directory.")

    # 데이터 저장: ../data/spx.pkl
    df.to_pickle(pkl_directory+pkl_name)
    df.to_csv(pkl_directory+pkl_name.replace('pkl','csv'))


def read_pickle(pkl_name):
# 데이터 로드
    pkl_directory = 'data/common_pkl/'
    df = pd.read_pickle(pkl_directory+pkl_name)
    
    return df


# In[12]:


def get_data(url, column):
           
    count = 0
    while True:
        try :
            res = scraper.get(url, headers=headers)
#             res = requests.get(url, headers=headers)
#             class_name = 'w-full text-xs leading-4 overflow-x-auto freeze-column-w-1'
# 위의 class_name 명칭은 수시로 바뀌므로 새롭게 수정해 주어야 함.
            class_name = 'freeze-column-w-1 w-full overflow-x-auto text-xs leading-4'
            # df = pd.read_html(res.text, attrs={"class": class_name}, flavor=["lxml", "bs4"])[0]
            df = pd.read_html(io.StringIO(str(res.text)), attrs={"class": class_name}, flavor=["lxml", "bs4"])[0]
#             res = scraper.get(url, headers=headers)  # 변경전
#             df = pd.read_html(res.text, attrs={"id": "curr_table"}, flavor=["lxml", "bs4"])[0]
            break
        except:
            # res = scraper.get(url, headers=headers)
            res = requests.get(url, headers=headers)
            # df = pd.read_html(res.text, attrs={"data-test": "historical-data-table"}, flavor=["lxml", "bs4"])[0]
            df = pd.read_html(io.StringIO(str(res.text)), attrs={"data-test": "historical-data-table"}, flavor=["lxml", "bs4"])[0]
            break
        finally:
            time.sleep(1)
            count += 1
            if count > 5 :
                raise ValueError('The url request is delaying')
                break           

    df.columns = column
    correct_date_format(df)
    df.sort_values(by=[df.columns[0]], inplace=True)
    df.index = np.arange(0, len(df))  # 일련 번호 오름차순으로 재 설정

    return df


# In[13]:


def concat_df(df_o, df):
    df_o = pd.concat([df_o, df], ignore_index=True)
    df_o.drop_duplicates(subset=['date'], keep='last', inplace=True)
#     df_o.drop_duplicates(subset=['date'], keep='first', inplace=True)
    df_o.sort_values(by=[df_o.columns[0]], inplace=True)
    df_o.index = np.arange(0, len(df_o))  # 일련 번호 오름차순으로 재 설정
    return df_o


# In[14]:


def update_pickle(df, pkl_name):
    df_o = read_pickle(pkl_name)
    try:  # convert timestamp to datetime.datetime.date
        df_o['date'] = df_o['date'].apply(lambda x: datetime.datetime.date(x))
    except:
        pass
    df_o = concat_df(df_o, df)
    
    make_pickle(df_o, pkl_name)


# In[15]:


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


# In[16]:


def get_ticker_data(ticker, startdate, enddate, col_name):
    ydata = yf.Ticker(ticker)
    rdata = ydata.history(period="2y") # 오늘부터 2년치
    rdata.reset_index('Date', inplace=True)
    rdata['Date'] = rdata['Date'].dt.date  # datetime64 to datetime.date()
    rdata = rdata[(rdata['Date'] <= enddate) & (rdata['Date'] >= startdate)] 
    rdata['temp'] = rdata['Close'].shift(1)
    val_temp = (rdata['Close'] - rdata['temp'])/rdata['temp']*100
    rdata[f'{col_name}_cr'] = val_temp.map("{:.2f}%".format)
    rdata = rdata[['Date', 'Close', 'Open', 'High', 'Low', 'Volume', f'{col_name}_cr']] # 필요한 column만 남김
    rdata.columns = ['date', f'{col_name}', 'open', 'high', 'low', 'volume', f'{col_name}_cr'] # column이름 통일
    rdata.reset_index(drop=True, inplace=True) # index번호를 0부터 재정리
    return rdata


# In[17]:

# startdate = datetime.datetime(2021,12,25)
startdate = datetime.date(2021,12,25)
# enddate = datetime.datetime(2023,3,23)
enddate = datetime.date.today() + datetime.timedelta(days=2)


# In[18]:


# spx = pdr.get_data_yahoo('^SPX', start=startdate, end=enddate)
# df = reformat_df(spx, 'spx')
# make_pickle(df, 'spx.pkl')

# spx는 yahoo에서 최근 하루만 제공하기 때문에 investing을 계속 사용함
spx_url = 'https://kr.investing.com/indices/us-spx-500-historical-data'
spx = ['date', 'spx', 'open', 'high', 'low', 'volume', 'spx_cr']
pkl_name = 'spx.pkl'
df = get_data(spx_url,spx)

update_pickle(df, pkl_name)


# In[19]:


dji = get_ticker_data('^DJI', startdate, enddate, 'dji')
make_pickle(dji, 'dji.pkl')

# 시간대별로 막혀 있어서 아래 것은 사용하지 않음 (미국 개장시간대에서만 열림)
# dji = pdr.get_data_yahoo('^DJI', start=startdate, end=enddate)
# df = reformat_df(dji, 'dji')
# make_pickle(df, 'dji.pkl')

# 아래 investing은 vol자료에 차이가 있어 사용하지 않음.
# dji_url = 'https://www.investing.com/indices/us-30-historical-data'
# dji = ['date', 'dji', 'open', 'high', 'low', 'volume', 'dji_cr']
# pkl_name = 'dji.pkl'
# df = get_data(dji_url,dji)

# update_pickle(df, pkl_name)


# In[20]:


ixic = get_ticker_data('^IXIC', startdate, enddate, 'ixic')
make_pickle(ixic, 'nas.pkl')

# ixic = pdr.get_data_yahoo('^IXIC', start=startdate, end=enddate)
# df = reformat_df(ixic, 'ixic')
# make_pickle(df, 'nas.pkl')

# nas_url = 'https://kr.investing.com/indices/nasdaq-composite-historical-data'
# ixic = ['date', 'ixic', 'open', 'high', 'low', 'volume', 'ixic_cr']
# pkl_name = 'nas.pkl'
# df = get_data(nas_url,ixic)

# update_pickle(df, pkl_name)


# In[21]:


sox = get_ticker_data('^SOX', startdate, enddate, 'sox')
make_pickle(sox, 'sox.pkl')

# sox = pdr.get_data_yahoo('^SOX', start=startdate, end=enddate)
# df = reformat_df(sox, 'sox')
# make_pickle(df, 'sox.pkl')

# sox_url = 'https://kr.investing.com/indices/phlx-semiconductor-historical-data'
# sox = ['date', 'sox', 'open', 'high', 'low', 'volume', 'sox_cr']
# pkl_name = 'sox.pkl'
# df = get_data(sox_url,sox)

# update_pickle(df, pkl_name)


# In[22]:


vix = get_ticker_data('^VIX', startdate, enddate, 'vix')
make_pickle(vix, 'vix.pkl')

# vix = pdr.get_data_yahoo('^VIX', start=startdate, end=enddate)
# df = reformat_df(vix, 'vix')
# make_pickle(df, 'vix.pkl')

# vix_url = 'https://kr.investing.com/indices/volatility-s-p-500-historical-data'
# vix = ['date', 'vix', 'open', 'high', 'low', 'volume', 'vix_cr']
# pkl_name = 'vix.pkl'
# df = get_data(vix_url,vix)

# update_pickle(df, pkl_name)


# In[23]:


kor_bond_10yr_url = 'https://kr.investing.com/rates-bonds/south-korea-10-year-bond-yield-historical-data'
kor_10yr = ['date', 'bond_kor_10', 'open', 'high', 'low', 'bond_kor_10_cr']
pkl_name = 'kor_10yr_bond.pkl'
df = get_data(kor_bond_10yr_url,kor_10yr)

update_pickle(df, pkl_name)


# In[24]:


kor_bond_2yr_url = 'https://kr.investing.com/rates-bonds/south-korea-2-year-bond-yield-historical-data'
kor_2yr = ['date', 'bond_kor_2', 'open', 'high', 'low','bond_kor_2_cr']
pkl_name = 'kor_2yr_bond.pkl'
df = get_data(kor_bond_2yr_url,kor_2yr)

update_pickle(df, pkl_name)


# In[25]:


krw_rate_url = 'https://kr.investing.com/currencies/usd-krw-historical-data'
krw_rate = ['date', 'krw', 'open', 'high', 'low', 'vol', 'krw_cr']
pkl_name = 'krw_rate.pkl'
df = get_data(krw_rate_url,krw_rate)

update_pickle(df, pkl_name)


# #### get append cpi

# In[26]:


cpi_url = 'https://www.investing.com/economic-calendar/cpi-733'
cpi_column = ['date', 'time', 'cpi', 'cpi_anticipated', 'cpi_previous', 'none']
pkl_name = 'cpi.pkl'


# In[27]:


res = scraper.get(cpi_url, headers=headers)
# res = requests.get(cpi_url, headers=headers)
# df = pd.read_html(res.text, flavor=["lxml", "bs4"])[0]
df = pd.read_html(io.StringIO(str(res.text)), flavor=["lxml", "bs4"])[0]
df.columns = cpi_column
df['time'] = df['time'].apply(lambda x : datetime.datetime.strptime(x, "%H:%M").time())
df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x[:12], "%b %d, %Y"))

df = df[['date', 'cpi', 'cpi_anticipated', 'cpi_previous']]

try: # convert timestamp to datetime.datetime.date
    df['date'] = df['date'].apply(lambda x: datetime.datetime.date(x))
except:
    pass

df.sort_values(by=['date'], inplace=True)

update_pickle(df, pkl_name)


# #### get append fear and greed
# ##### 2020년 9월 21일부터  2021년 1월 21일까지 데이터는 이상 데이터 로 나중에 수정해야 함.

# In[28]:


import pytz, json


# In[29]:


def convert_timestamp_to_date(x):
    dt = datetime.datetime.fromtimestamp(x / 1000, tz=pytz.utc) # UTC에서 변환 불필요.
#     tzone = pytz.timezone('US/Eastern')
#     tzone = pytz.timezone('Asia/Seoul')
#     loc_dt = dt.astimezone(tzone)
    loc_dt = dt
    return loc_dt.date()


# In[30]:


# 과거 데이터 (fear_greed_old_to_20200918.pkl) 에 rating column을 추가한 내용
# 한번만 사용하고 이후 사용하지 않음

def convert_to_rating(x):
    if x < 25 :
        rating = 'extreme fear'
    elif x < 45 :
        rating = 'fear'
    elif x < 55 :
        rating = 'neutral'
    elif x < 75 :
        rating = 'greed'
    elif x <= 100 :
        rating = 'extreme greed'

    return rating


# In[31]:


today = datetime.date.today()
today_p = today.strftime('%Y%m%d')
diff_days = datetime.timedelta(days=40)
today = today - diff_days
start_date = today.strftime('%Y-%m-%d')  # 30일전부터 자료 수집


# In[32]:


url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
pkl_name = 'fear_greed.pkl'
# start_date = '2020-07-15'


# In[33]:


r = requests.get("{}/{}".format(url, start_date), headers=headers)
data = r.json()

fg_data = data['fear_and_greed_historical']['data']
df = pd.DataFrame(fg_data)

df.columns = ['date', 'fg_index', 'rating']
df['date'] = df['date'].apply(lambda x: convert_timestamp_to_date(x))
df['fg_index'] = df['fg_index'].apply(lambda x: round(x))

df.sort_values(by=[df.columns[0]], inplace=True)
df.index = np.arange(0, len(df))  # 일련 번호 오름차순으로 재 설정
df.drop_duplicates(subset=['date'], inplace=True) 


# In[34]:


df_o = read_pickle(pkl_name)
df_o['date'] = df_o['date'].apply(lambda x : datetime.datetime.strftime(x, "%Y-%m-%d"))
df_o['date'] = df_o['date'].apply(lambda x : datetime.datetime.strptime(x, "%Y-%m-%d"))
try:  # convert timestamp to datetime.datetime.date
    df_o['date'] = df_o['date'].apply(lambda x: datetime.datetime.date(x))
except:
    pass

df_o = concat_df(df_o, df)

# 분석시 제외. 추후 보강 2023년 8월 이후에 추가 할지 결정해야 함.
make_pickle(df_o, pkl_name)


# #### get and append gold price

# In[35]:


# gold_url = 'https://www.usagold.com/daily-gold-price-history/'
# pkl_name = 'gold.pkl'

# res = requests.get(gold_url, headers=headers)
## df = pd.read_html(res.text, flavor=["lxml", "bs4"])
# df = pd.read_html(io.StringIO(str(res.text)), flavor=["lxml", "bs4"])
# df = df[0].drop(0) # delete empty first row
# df.columns = ['date', 'gold']
# df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x, "%d %b %Y"))
# df.sort_values(by=['date'], inplace=True)
# df.drop_duplicates(subset=['date'], inplace=True) 

# # 분석시 제외. 추후 보강 현재는 빠짐.
# update_pickle(df, pkl_name)


# In[36]:


gold = get_ticker_data('GC=F', startdate, enddate, 'gold')
make_pickle(gold, 'gold.pkl')

# # Gold Apr 23 (GC=F)
# df = pdr.get_data_yahoo('GC=F', start=startdate, end=enddate)
# df = reformat_df(df, 'gold')
# make_pickle(df, 'gold.pkl')


# ### fed 금리 get append

# In[37]:


interest_url = 'https://www.investing.com/economic-calendar/interest-rate-decision-168/'
interest_column = ['date', 'time', 'fed_rate', 'fed_rate_fore', 'fed_rate_prev', 'none']
pkl_name = 'fed_rate.pkl'


# In[38]:


res = scraper.get(interest_url, headers=headers)
# res = requests.get(interest_url, headers=headers)
# df = pd.read_html(res.text, flavor=["lxml", "bs4"])[0]
df = pd.read_html(io.StringIO(str(res.text)), flavor=["lxml", "bs4"])[0]
df.columns = interest_column

df.replace(np.nan, '', inplace=True)

df['date'] = df['date'].apply(lambda x : datetime.datetime.strptime(x[:12], "%b %d, %Y"))
df['time'] = df['time'].apply(lambda x : datetime.datetime.strptime(x, "%H:%M").time())
df.sort_values(by=['date'], inplace=True)
df.drop_duplicates(subset=['date'], inplace=True) 
# convert from timestampe to datetime
df['date'] = df['date'].apply(lambda x: datetime.datetime.date(x)) 


# In[39]:


# 매일매일의 데이터가 없어서 분석시 제외. 추후 보강 현재는 빠짐.
update_pickle(df, pkl_name)


# ### 한국은행 금리 get append

# In[40]:


kor_url = 'https://www.bok.or.kr/portal/singl/baseRate/list.do?dataSeCd=01&menuNo=200643'
pkl_name = 'bok_rate.pkl'


# In[41]:


# res = requests.get(kor_url, headers=headers, verify=certifi.where())
res = requests.get(kor_url, headers=headers)
df = pd.read_html(io.StringIO(str(res.text)), attrs = {'class': 'fixed'}, flavor=["lxml", "bs4"])[0]


# In[42]:


df.columns=  ['release_yr', 'release_date', 'bok_rate']
df_date_temp = df['release_yr'].astype('str')+df['release_date']
df['date'] = df_date_temp.apply(lambda x : datetime.datetime.strptime(x, "%Y%m월 %d일"))
df.sort_values(by=['date'], inplace=True)
df.drop_duplicates(subset=['date'], inplace=True) 

df = df[['date', 'bok_rate']] # leave only valid columns

# convert from timestampe to datetime
df['date'] = df['date'].apply(lambda x: datetime.datetime.date(x)) 

# 매일매일의 데이터가 없어서 분석시 제외. 추후 보강 현재는 빠짐.
update_pickle(df, pkl_name)


# ### US Sector Summary

# In[43]:


# startdate = datetime.datetime(2021,12,25)
# enddate = datetime.datetime(2023,3,23)


# In[44]:


# [ticker, shortname, filename]
us_sector_list = US_SECTOR_LIST


# In[45]:


for sector in us_sector_list:
    make_pickle(get_ticker_data(sector[0], startdate, enddate, sector[1]), sector[2])


# ### 여기까지 완료

# In[ ]:





# In[ ]:





# ### 아래는 삭제 예정

# In[ ]:


# # S&P 500 Financials (SPSY), ^SP500-40
# # spsy_url = 'https://www.investing.com/indices/s-p-500-financial-historical-data'
# spsy = get_ticker_data('^SP500-40', startdate, enddate, 'spsy')
# make_pickle(spsy, 'spsy.pkl')

# # df = pdr.get_data_yahoo('^SP500-40', start=startdate, end=enddate)
# # df = reformat_df(df, 'spsy')
# # make_pickle(df, 'spsy.pkl')


# In[ ]:


# # S&P 500 Energy (SPNY), ^GSPE
# # spny_url = 'https://www.investing.com/indices/s-p-500-energy-historical-data'
# spny = get_ticker_data('^GSPE', startdate, enddate, 'spny')
# make_pickle(spny, 'spny.pkl')

# # df = pdr.get_data_yahoo('^GSPE', start=startdate, end=enddate)
# # df = reformat_df(df, 'spny')
# # make_pickle(df, 'spny.pkl')


# In[ ]:


# # spxhc_url = 'https://www.investing.com/indices/s-p-500-health-care-historical-data'
# # S&P 500 Health Care (SPXHC), ^SP500-35
# spxhc = get_ticker_data('^SP500-35', startdate, enddate, 'spxhc')
# make_pickle(spxhc, 'spxhc.pkl')

# # spxhc = pdr.get_data_yahoo('^SP500-35', start=startdate, end=enddate)
# # df = reformat_df(spxhc, 'spxhc')
# # make_pickle(df, 'spxhc.pkl')


# In[ ]:


# # splrcd_url = 'https://www.investing.com/indices/s-p-500-consumer-discretionary-historical-data'
# # S&P 500 Consumer Discretionary (SPLRCD), ^SP500-25
# splrcd = get_ticker_data('^SP500-25', startdate, enddate, 'splrcd')
# make_pickle(splrcd, 'splrcd.pkl')

# # splrcd = pdr.get_data_yahoo('^SP500-25', start=startdate, end=enddate)
# # df = reformat_df(splrcd, 'splrcd')
# # make_pickle(df, 'splrcd.pkl')


# In[ ]:


# # splrci_url = 'https://www.investing.com/indices/s-p-500-industrials-historical-data'
# # S&P 500 Industrials (SPLRCI), ^SP500-20
# splrci = get_ticker_data('^SP500-20', startdate, enddate, 'splrci')
# make_pickle(splrci, 'splrci.pkl')

# # splrci = pdr.get_data_yahoo('^SP500-20', start=startdate, end=enddate)
# # df = reformat_df(splrci, 'splrci')
# # make_pickle(df, 'splrci.pkl')


# In[ ]:


# # splrcu_url = 'https://www.investing.com/indices/s-p-500-utilities-historical-data'
# # S&P 500 Utilities (SPLRCU), ^SP500-55
# splrcu = get_ticker_data('^SP500-55', startdate, enddate, 'splrcu')
# make_pickle(splrcu, 'splrcu.pkl')

# # splrcu = pdr.get_data_yahoo('^SP500-55', start=startdate, end=enddate)
# # df = reformat_df(splrcu, 'splrcu')
# # make_pickle(df, 'splrcu.pkl')


# In[ ]:


# # splrcs_url = 'https://www.investing.com/indices/s-p-500-consumer-staples-historical-data'
# # S&P 500 Consumer Staples (SPLRCS), ^SP500-30
# splrcs = get_ticker_data('^SP500-30', startdate, enddate, 'splrcs')
# make_pickle(splrcs, 'splrcs.pkl')

# # splrcs = pdr.get_data_yahoo('^SP500-30', start=startdate, end=enddate)
# # df = reformat_df(splrcs, 'splrcs')
# # make_pickle(df, 'splrcs.pkl')


# In[ ]:


# # splrct_url = 'https://www.investing.com/indices/s-p-500-information-technology-historical-data'
# # S&P 500 Information Technology (SPLRCT), ^SP500-45
# splrct = get_ticker_data('^SP500-45', startdate, enddate, 'splrct')
# make_pickle(splrct, 'splrct.pkl')

# # splrct = pdr.get_data_yahoo('^SP500-45', start=startdate, end=enddate)
# # df = reformat_df(splrct, 'splrct')
# # make_pickle(df, 'splrct.pkl')


# In[ ]:


# # splrcl_url = 'https://www.investing.com/indices/s-p-500-telecom-services-historical-data'
# # S&P 500 Telecom Services (SPLRCL), ^SP500-50
# splrcl = get_ticker_data('^SP500-50', startdate, enddate, 'splrcl')
# make_pickle(splrcl, 'splrcl.pkl')

# # splrcl = pdr.get_data_yahoo('^SP500-50', start=startdate, end=enddate)
# # df = reformat_df(splrcl, 'splrcl')
# # make_pickle(df, 'splrcl.pkl')


# In[ ]:


# # splrcm_url = 'https://www.investing.com/indices/s-p-500-materials-historical-data'
# # S&P 500 Materials (SPLRCM), ^SP500-15
# splrcm = get_ticker_data('^SP500-15', startdate, enddate, 'splrcm')
# make_pickle(splrcm, 'splrcm.pkl')

# # splrcm = pdr.get_data_yahoo('^SP500-15', start=startdate, end=enddate)
# # df = reformat_df(splrcm, 'splrcm')
# # make_pickle(df, 'splrcm.pkl')


# In[ ]:


# # ixbk_url = 'https://www.investing.com/indices/nasdaq-bank-historical-data'
# # NASDAQ Bank (IXBK), ^BANK
# ixbk = get_ticker_data('^BANK', startdate, enddate, 'ixbk')
# make_pickle(ixbk, 'ixbk.pkl')

# # ixbk = pdr.get_data_yahoo('^BANK', start=startdate, end=enddate)
# # df = reformat_df(ixbk, 'ixbk')
# # make_pickle(df, 'ixbk.pkl')


# In[ ]:


# yahoo에서는 하루만 잡힘. investing.com에서는 자료가 있으나 skip (나중에 보강)
# ixf_url = 'https://www.investing.com/indices/nasdaq-financial-100-historical-data'
# # NASDAQ Financial 100 (IXF), ^IXF
# ixf = pdr.get_data_yahoo('^IXF', start=startdate, end=enddate)
# df = reformat_df(ixf, 'ixf')
# make_pickle(df, 'ixf.pkl')


# In[ ]:


# # ixfn_url = 'https://www.investing.com/indices/nasdaq-other-finance-historical-data'
# # NASDAQ Other Finance (IXFN), ^OFIN
# ixfn = get_ticker_data('^OFIN', startdate, enddate, 'ixfn')
# make_pickle(ixfn, 'ixfn.pkl')

# # ixfn = pdr.get_data_yahoo('^OFIN', start=startdate, end=enddate)
# # df = reformat_df(ixfn, 'ixfn')
# # make_pickle(df, 'ixfn.pkl')


# In[ ]:


# # ixid_url = 'https://www.investing.com/indices/nasdaq-industrial-historical-data'
# # NASDAQ Industrial (IXID), ^INDS
# ixid = get_ticker_data('^INDS', startdate, enddate, 'ixid')
# make_pickle(ixid, 'ixid.pkl')

# # ixid = pdr.get_data_yahoo('^INDS', start=startdate, end=enddate)
# # df = reformat_df(ixid, 'ixid')
# # make_pickle(df, 'ixid.pkl')


# In[ ]:


# # ixis_url = 'https://www.investing.com/indices/nasdaq-insurance-historical-data'
# # NASDAQ Insurance (IXIS), ^INSR
# ixis = get_ticker_data('^INSR', startdate, enddate, 'ixis')
# make_pickle(ixis, 'ixis.pkl')

# # ixis = pdr.get_data_yahoo('^INSR', start=startdate, end=enddate)
# # df = reformat_df(ixis, 'ixis')
# # make_pickle(df, 'ixis.pkl')


# In[ ]:


# # ixk_url = 'https://www.investing.com/indices/nnasdaq-computer-historical-data'
# # NASDAQ Computer (IXK), ^IXCO
# ixk = get_ticker_data('^IXCO', startdate, enddate, 'ixk')
# make_pickle(ixk, 'ixk.pkl')

# # ixk = pdr.get_data_yahoo('^IXCO', start=startdate, end=enddate)
# # df = reformat_df(ixk, 'ixk')
# # make_pickle(df, 'ixk.pkl')


# In[ ]:


# # ixtr_url = 'https://www.investing.com/indices/nasdaq-transportation-historical-data'
# # NASDAQ Transportation (IXTR), ^TRAN
# ixtr = get_ticker_data('^TRAN', startdate, enddate, 'ixtr')
# make_pickle(ixtr, 'ixtr.pkl')

# # ixtr = pdr.get_data_yahoo('^TRAN', start=startdate, end=enddate)
# # df = reformat_df(ixtr, 'ixtr')
# # make_pickle(df, 'ixtr.pkl')


# In[ ]:


# # ixut_url = 'https://www.investing.com/indices/nasdaq-telecommunications-historical-data'
# # NASDAQ Telecommunications (IXUT), ^IXTC
# ixut = get_ticker_data('^IXTC', startdate, enddate, 'ixut')
# make_pickle(ixut, 'ixut.pkl')

# # ixut = pdr.get_data_yahoo('^IXTC', start=startdate, end=enddate)
# # df = reformat_df(ixut, 'ixut')
# # make_pickle(df, 'ixut.pkl')


# In[ ]:


# # nbi_url = 'https://www.investing.com/indices/nasdaq-biotechnology-historical-data'
# # NASDAQ Biotechnology (NBI), ^NBI
# nbi = get_ticker_data('^NBI', startdate, enddate, 'nbi')
# make_pickle(nbi, 'nbi.pkl')

# # nbi = pdr.get_data_yahoo('^NBI', start=startdate, end=enddate)
# # df = reformat_df(nbi, 'nbi')
# # make_pickle(df, 'nbi.pkl')


# In[ ]:


# yahoo에서는 하루만 잡힘. investing.com에서는 자료가 있으나 skip (나중에 보강)
# qnet_url = 'https://www.investing.com/indices/nasdaq-internet-historical-data'
# # NASDAQ Internet (QNET), ^QNET
# qnet = pdr.get_data_yahoo('^QNET', start=startdate, end=enddate)
# df = reformat_df(qnet, 'qnet')
# make_pickle(df, 'qnet.pkl')


# In[ ]:


# bkx_url = 'https://www.investing.com/indices/kbw-bank-historical-data'
# # KBW NASDAQ Bank (BKX), ^BKX
# bkx = get_ticker_data('^BKX', startdate, enddate, 'bkx')
# make_pickle(bkx, 'bkx.pkl')

# # bkx = pdr.get_data_yahoo('^BKX', start=startdate, end=enddate)
# # df = reformat_df(bkx, 'bkx')
# # make_pickle(df, 'bkx.pkl')


# In[ ]:





# In[ ]:




