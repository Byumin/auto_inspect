from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

CHROMIUM_PATH = "/usr/bin/chromium-browser"  # 서버에 설치된 chromium-browser의 경로

# 웹 드라이버 최신화
def start_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = CHROMIUM_PATH  # 서버에 설치된 chromium-browser 경로 설정
    options.add_experimental_option("detach", True)  # 브라우저 자동 종료 방지
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# 웹 제어 브라우저
def control_browser(driver, url) : 
    driver.get(url)

def launch_browser(url):
    options = webdriver.ChromeOptions()
    options.binary_location = CHROMIUM_PATH  # 서버에 설치된 chromium-browser 경로 설정
    options.add_experimental_option("detach", True)  # 브라우저 자동 종료 방지
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    return driver