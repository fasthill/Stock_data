from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import time
import datetime

from open_browser import open_browser
from open_investors_window import open_investors_window
from open_window_historical_data import open_window_historical_data
from set_current_unit import set_current_unit

def set_date_n_search(driver, start_date_str, end_date_str, his_inv):  # 일정 기간 데이터 취득
    # end_date를 먼저 입력하고 start date 입력. 반대로 하면 start date가 이전날짜로  reset되어짐
    # "2024-01-01" 형식의 string

    global id_name
    driver.find_element(By.ID, 'endDd').clear()
    driver.find_element(By.ID, 'endDd').send_keys(end_date_str)
    time.sleep(1)

    if his_inv == 1:
        id_name = 'strdDd'
    elif his_inv == 2:
        id_name = 'strtDd'

    driver.find_element(By.ID, id_name).clear()
    driver.find_element(By.ID, id_name).send_keys(start_date_str)
    time.sleep(1)

    # 테이블  취득 버튼 클릭 (우상귀)
    # 'jsSearchButton' element 까지 스크롤
    search_button = driver.find_element(By.ID, 'jsSearchButton')
    action = ActionChains(driver)
    action.move_to_element(search_button).perform()
    element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'jsSearchButton')))

    # element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, 'jsSearchButton')))
    # element = driver.find_element(By.ID, 'jsSearchButton')
    # # driver.execute_script("arguments[0].click();", element) # move the location
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.find_element(By.ID, 'jsSearchButton').click()
    time.sleep(2)

    return

if __name__ == '__main__':
    #
    his_inv = input("for historical data insert 1, for investors data insert 2" )
    # for historical data
    if his_inv == '1':
        main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'
    elif his_inv == '2':
        main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203'

    driver = open_browser()
    driver.get(main_url)

    # date형식 변환후 입력
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 3, 1)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    if his_inv == '1':
        set_current_unit(driver, 1) # historical = 1, investors = 2
        com_name = '005930/삼성전자'  # '000660/SK하이닉스'
        open_window_historical_data(driver, com_name)
        set_date_n_search(driver, start_str, end_str, 1)
    elif his_inv == '2':
        open_investors_window(driver)
        set_current_unit(driver, 2) # historical = 1, investors = 2
        code_n_name = '005930/삼성전자'  # '000660/SK하이닉스'
        set_date_n_search(driver, end_str, end_str, 2)
        # open_window_investors_data(driver, code_n_name)

    time.sleep(5)  # wait before close
    driver.close()