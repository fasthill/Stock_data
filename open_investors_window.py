# KRX 정보데이터 시스템에서 취득 대상 회사 시세 추이 (개벌종목 시세 추이) 화면으로 이동하기 위한 function
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

import time

from open_browser import open_browser
from set_current_unit import set_current_unit

def open_investors_window(driver):

    time.sleep(1)
    # jsOpenView_1 element 까지 스크롤
    stop_tag = driver.find_element(By.ID, 'jsOpenView_1')
    action = ActionChains(driver)
    action.move_to_element(stop_tag).perform()

    # Message: element not interactable Error 방지용. 클릭하기 위하여는 그 위치가 클릭할 수 있게 노출되어 있어야 함
    # 투자자별 거래실적 버튼이 위치한 곳으로 화면 scroll
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, 'jsOpenView_1')))
    # id가 jsOpenView_1 인 element 를 찾음
    stop_tag = driver.find_element(By.ID, 'jsOpenView_1')

    # 투자자별 거래 실적 버튼 클릭
    driver.find_element(By.ID, 'jsOpenView_1').click()
    time.sleep(2)

    return


if __name__ == '__main__':
    # open browser
    main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020203'
    # 개별종목 시세추이 data-menu-id: MDC0201020103
    driver = open_browser()
    driver.get(main_url)

    open_investors_window(driver)
    #
    set_current_unit(driver, 2)

    driver.close()
