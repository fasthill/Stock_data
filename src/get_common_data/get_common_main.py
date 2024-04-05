from data.constant.constants import US_SECTOR_LIST
from src.get_common_data.get_common_data_korea.save_data_file import save_data


startdate = datetime.date(2021,12,25)
enddate = datetime.date.today() + datetime.timedelta(days=2)

# US Sector Summary
us_sector_list = US_SECTOR_LIST
for sector in us_sector_list:
    save_data(get_ticker_data(sector[0], startdate, enddate, sector[1]), sector[2])