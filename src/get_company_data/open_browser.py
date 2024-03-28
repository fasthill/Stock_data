import time
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# set driver
def open_browser():
    service = Service(r"../../chromedriver/chromedriver.exe")
    options = wd.ChromeOptions()
    options.add_experimental_option("detach", True)  # let windows stay open, this prevents windows from disappearing

    return wd.Chrome(service=service, options=options)


if __name__ == '__main__':
    url = 'https://www.google.com/'
    driver = open_browser()
    driver.get(url)

    time.sleep(5)  # wait before close
    driver.close()
