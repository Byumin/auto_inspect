from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 웹 드라이버 최신화
def start_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"  # 서버에 설치된 chromium-browser 경로 설정
    options.add_argument("--headless=new") # 헤드리스 모드로 실행
    options.add_argument("--no-sandbox") # 샌드박스 모드 비활성화
    options.add_argument("--disable-dev-shm-usage") # 공유 메모리 사용 비활성화
    options.add_experimental_option("detach", True)  # 브라우저 자동 종료 방지
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# 웹 제어 브라우저
def control_browser(driver, url) : 
    driver.get(url)

def launch_browser(url):
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    #options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager(version="138.0.7204.157").install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    print("Browser launched and navigated to:", url)
    return driver