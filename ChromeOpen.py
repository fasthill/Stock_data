from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service

service = Service(r"chromedriver.exe")
options = wd.ChromeOptions()
options.add_experimental_option("detach", True)  # let windows stay open, this prevents windows from disappearing
driver = wd.Chrome(service=service, options=options)

url = 'https://www.google.com/'
driver.get(url)

# driver.quit()
