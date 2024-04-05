# KRX 정보데이터 시스템에서 취득 대상 회사 시세 추이 (개벌종목 시세 추이) 화면으로 이동하기 위한 function
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from src.get_company_data.open_browser import open_browser
from src.get_company_data.set_current_unit import set_current_unit


# def get_data_company(code_n_name):
def open_window_historical_data(driver, code_n_name):
    com_ticker = code_n_name[:6]
    # 회사이름 입력 Q 버튼
    css_name = '#btnisuCd_finder_stkisu0_0'
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_name)))
    driver.find_element(By.CSS_SELECTOR, css_name).click()
    time.sleep(2)

    # pop up된 입력창에서 회사이름 입력
    id_name = 'searchText__finder_stkisu0_0'
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, id_name)))
    driver.find_element(By.ID, id_name).clear()
    time.sleep(1)

    driver.find_element(By.ID, id_name).send_keys(code_n_name)
    time.sleep(2)

    # 검색 버튼 푸시
    css_name = '#searchBtn__finder_stkisu0_0'
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_name)))
    driver.find_element(By.CSS_SELECTOR, css_name).click()
    time.sleep(2)

    # 테이블에서 최종 선택
    css_sel = '#jsGrid__finder_stkisu0_0 > tbody > tr:nth-child(1) > td:nth-child(1)'

    element = WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, css_sel), com_ticker))
    # 위 라인은 pop up 창이 사라질 때까지 기다리게 해 줌
    driver.find_element(By.CSS_SELECTOR, css_sel).click()
    time.sleep(2)

    return


if __name__ == '__main__':
    # open browser
    main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'
    # 개별종목 시세추이 data-menu-id: MDC0201020103
    driver = open_browser()
    driver.get(main_url)

    set_current_unit(driver, 1)

    # test function
    com_name = '005930/삼성전자'  # '000660/SK하이닉스'
    open_window_historical_data(driver, com_name)

    time.sleep(5)  # wait before close
    driver.close()
