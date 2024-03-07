from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime

from open_browser import open_browser
from open_window_individual_stock_trend import open_window_individual_stock_trend
from set_current_unit import set_current_unit

def set_date_n_search(driver, start_date_str, end_date_str):  # 일정 기간 데이터 취득
    # end_date를 먼저 입력하고 start date 입력. 반대로 하면 start date가 이전날짜로  reset되어짐
    # "2024-01-01" 형식의 string
    driver.find_element(By.ID, 'endDd').clear()
    driver.find_element(By.ID, 'endDd').send_keys(end_date_str)
    time.sleep(1)

    driver.find_element(By.ID, 'strdDd').clear()
    driver.find_element(By.ID, 'strdDd').send_keys(start_date_str)
    time.sleep(1)

    # 테이블  취득 버튼 클릭 (우상귀)
    id_name = 'jsSearchButton'
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, id_name)))
    driver.find_element(By.ID, id_name).click()
    time.sleep(1)

    return

if __name__ == '__main__':
    # open browser
    main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'
    # 개별종목 시세추이 data-menu-id: MDC0201020103
    driver = open_browser()
    driver.get(main_url)

    set_current_unit(driver)

    # test function
    com_name = '005930/삼성전자'  # '000660/SK하이닉스'
    open_window_individual_stock_trend(driver, com_name)

    # date형식 변환후 입력
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 3, 1)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    set_date_n_search(driver, start_str, end_str)

    time.sleep(5)  # wait before close
    driver.close()