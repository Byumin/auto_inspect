from selenium.webdriver.common.by import By
from module.error_handler import error_with_screenshot

def run(context):
    try:
        driver = context["driver"]
        # 검사 실시 화면 통제 전환 
        window = driver.window_handles
        print("현재 창 핸들:", window)  # Debugging line
        window_handle = window[-1]  # 마지막 창 핸들
        driver.switch_to.window(window_handle)
        print("현재 창 핸들로 전환:", window_handle)  # Debugging line
        version_df = context["version_df_row"]
        version_dict = context["version_dict"]
        version_next_button_xpath = context["version_next_button_xpath"]
        print("버전 선택 모듈 실행")
        print("버전 데이터프레임:", version_df)  # Debugging line
        print("버전 선택 딕셔너리:", version_dict)  # Debugging line
        version_key = version_df.iloc[0]  # 첫 번째 행의 첫 번째 열 값
        print(f"선택된 버전 키: {version_key}")  # Debugging line

        version_xpath = version_dict.get(version_key)
        version_element = driver.find_element(By.XPATH, version_xpath)
        version_element.click()  # 클릭하여 버전 선택
        print(f"버전 선택 완료: {version_key}")  # Debugging line

        # 다음 버튼 클릭
        next_button = driver.find_element(By.XPATH, version_next_button_xpath)
        next_button.click()  # 다음 버튼 클릭
        print("다음 버튼 클릭 완료")  # Debugging line

    except Exception as e:
        error_message = f"버전 선택 모듈 실행 중 오류 발생: {e}"
        print(error_message)  # Debugging line
        error_with_screenshot(driver, error_message)
        return