import os
import platform
import time
import streamlit as st
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


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
    system_platform = platform.system()
    if system_platform == "Darwin":  # macOS
        options.add_experimental_option("detach", True)  # 창 유지 (사용자 확인용)
        print("📍 Mac 환경에서 브라우저 실행")
    
    elif system_platform == "Linux":  # Linux
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--remote-debugging-port=9222")
        print("📍 Linux 서버 환경에서 Headless 브라우저 실행")

    else:
        raise EnvironmentError(f"Unsupported platform: {system_platform}.")
    
    # 드라이버 설치 및 브라우저 실행
    service = Service(ChromeDriverManager(driver_version="138.0.7204.157").install())
    driver = webdriver.Chrome(service=service, options=options)

    # 페이지 접속
    driver.get(url)
    print("Browser launched and navigated to:", url)
    screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved at:", screenshot_path)
    image = Image.open(screenshot_path)
    st.image(image, caption="Initial Page Screenshot", width=600)
    return driver

# 로그인 -> 검사 실시 시작 화면 진입
def login_and_start_inspection(driver, id, pw, psy_name):
    id_element = driver.find_element(By.XPATH, '//*[@id="loginId"]') # 로그인 아이디 입력 필드
    pw_element = driver.find_element(By.XPATH, '//*[@id="password"]') # 비밀번호 입력 필드
    id_element.send_keys(id) # 로그인 아이디 입력
    pw_element.send_keys(pw) # 비밀번호 입력
    login_button = driver.find_element(By.XPATH, '//*[@id="processBtn"]') # 로그인 버튼
    login_button.click() # 로그인 버튼 클릭
    time.sleep(1)  # 로그인 처리 대기
    driver.find_element(By.XPATH, '//*[@id="showimage_sign_first"]/div[2]/div/p[2]/a').click() # 담당자 인증 패스
    driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[3]/div[2]/ul/li[1]/a').click() # 심리검사 목록 탭
    psy_name_element = driver.find_element(By.XPATH, '//*[@id="psyItemNm"]') # 심리 검사 이름 클릭
    psy_name_element.send_keys(psy_name) # 심리 검사 이름 입력
    psy_name_element.send_keys("\n") # 엔터키 입력
    time.sleep(1)  # 검사 목록 로딩 대기
    psy_start_button = driver.find_element(By.XPATH, '//*[@id="table-data"]/li[1]/div[3]/a[2]') # 검사 시작 버튼
    actions = ActionChains(driver)
    actions.move_to_element(psy_start_button).perform()
    psy_start_button.click() # 검사 시작 버튼 클릭
    driver.switch_to.alert.accept()
    time.sleep(1)  # 검사 시작 대기
    # 검사 실시 화면 통제 전환 
    window = driver.window_handles
    print("현재 창 핸들:", window)  # Debugging line
    window_handle = window[-1]  # 마지막 창 핸들
    driver.switch_to.window(window_handle)
    print("현재 창 핸들로 전환:", window_handle)  # Debugging line
    screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
    driver.save_screenshot(screenshot_path)
    print("Screenshot saved at:", screenshot_path)
    image = Image.open(screenshot_path)
    st.image(image, caption="Initial Page Screenshot", width=600)
    print("Login successful, navigating to inspection start page.")
    return driver