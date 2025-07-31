from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# 웹 드라이버 최신화
def start_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # 브라우저 자동 종료 방지
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# 웹 제어 브라우저
def control_browser(driver, url) : 
    driver.get(url)

def launch_browser(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # 브라우저 자동 종료 방지
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    return driver