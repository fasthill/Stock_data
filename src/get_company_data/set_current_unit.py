import time
from selenium.webdriver.common.by import By

from src.get_company_data.open_browser import open_browser


# from open_investors_window import open_investors_window

def set_current_unit(driver, his_inv=1):
    # 백만원 단위 표시 선정
    # css_sel = '#MDCSTAT017_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) \
    #            > select.CI-MDI-UNIT-MONEY > option:nth-child(3)'
    # driver.find_element(By.CSS_SELECTOR, css_sel).click()
    # 위 코드를 아래와 같이 두 개로 분리시켜야만 동작함.
    time.sleep(1)

    if his_inv == 1:  # 1: historical current unit
        css_sel_1 = '#MDCSTAT017_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > select.CI-MDI-UNIT-MONEY'
        css_opt = 'option:nth-child(3)'
        sel_1 = driver.find_element(By.CSS_SELECTOR, css_sel_1)  # 우선
        sel_1.find_element(By.CSS_SELECTOR, css_opt).click()
    else:
        css_sel = '#MDCSTAT023_FORM > div.CI-MDI-UNIT-WRAP > div > p:nth-child(2) > select.CI-MDI-UNIT-MONEY > option:nth-child(3)'
        driver.find_element(By.CSS_SELECTOR, css_sel).click()

    time.sleep(1)

    return


if __name__ == '__main__':
    # open browser
    main_url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'  # historical data
    # 개별종목 시세추이 data-menu-id: MDC0201020103
    driver = open_browser()
    driver.get(main_url)

    set_current_unit(driver, 1)

    time.sleep(5)  # wait before close
    driver.close()
