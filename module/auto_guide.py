from selenium.webdriver.common.by import By
import time

def run(context):
    print("검사안내 모듈 실행")
    driver = context["driver"]

    # 검사 실시 화면 통제 전환 
    window = driver.window_handles
    print("현재 창 핸들:", window)  # Debugging line
    window_handle = window[-1]  # 마지막 창 핸들
    driver.switch_to.window(window_handle)
    print("현재 창 핸들로 전환:", window_handle)  # Debugging line

    time.sleep(1)  # 잠시 대기하여 화면 로드
    next_button_xpath = driver.find_element(By.ID, 'submitBtn')
    next_button_xpath.click()