

dji = get_ticker_data('^DJI', startdate, enddate, 'dji')
make_pickle(dji, 'dji.pkl')


ixic = get_ticker_data('^IXIC', startdate, enddate, 'ixic')
make_pickle(ixic, 'nas.pkl')


sox = get_ticker_data('^SOX', startdate, enddate, 'sox')
make_pickle(sox, 'sox.pkl')


vix = get_ticker_data('^VIX', startdate, enddate, 'vix')
make_pickle(vix, 'vix.pkl')


gold = get_ticker_data('GC=F', startdate, enddate, 'gold')
make_pickle(gold, 'gold.pkl')

us_sector_list = US_SECTOR_LIST

for sector in us_sector_list:
    make_pickle(get_ticker_data(sector[0], startdate, enddate, sector[1]), sector[2])
