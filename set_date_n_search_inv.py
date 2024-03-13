from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime

from open_browser import open_browser
from open_investors_window import open_investors_window
from set_current_unit import set_current_unit

def set_date_n_search_inv(driver, start_date_str, end_date_str):  # 일정 기간 데이터 취득
    # end_date를 먼저 입력하고 start date 입력. 반대로 하면 start date가 이전날짜로  reset되어짐
    # "2024-01-01" 형식의 string

    driver.find_element(By.ID, 'endDd').clear()
    driver.find_element(By.ID, 'endDd').send_keys(end_date_str)
    time.sleep(1)

    driver.find_element(By.ID, 'strtDd').clear()
    driver.find_element(By.ID, 'strtDd').send_keys(start_date_str)
    time.sleep(1)

    # 테이블  취득 버튼 클릭 (우상귀)
    xp = '/html/body/div[2]/section[2]/section/section/div/div[2]/form/div[1]/div/a'
    # use full xpath to avoid 'Message: element not interactable' Error
    driver.find_element(By.XPATH, xp).click()
    time.sleep(1)  # 여유시간 배분

    css_sel = 'div.loading-bar-wrap.small'  # 각기 다른 loading 페이지에서 공통적으로 사용됨
    element = WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, css_sel)))
    # 위 라인은 pop up 창이 사라질 때까지 기다리게 해 줌
    time.sleep(1)  # 여유시간 배분

    return

if __name__ == '__main__':
    #
    main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203'

    driver = open_browser()
    driver.get(main_url)

    # date형식 변환후 입력
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 3, 4)
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    open_investors_window(driver)
    set_current_unit(driver, 2) # historical = 1, investors = 2
    code_n_name = '005930/삼성전자'  # '000660/SK하이닉스'
    set_date_n_search_inv(driver, end_str, end_str)
    # open_window_investors_data(driver, code_n_name)

    time.sleep(5)  # wait before close
    driver.close()