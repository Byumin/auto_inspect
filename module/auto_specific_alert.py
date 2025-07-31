from selenium.webdriver.common.by import By
import time
import streamlit as st

def run(context):
    try:
        print("특정 알럿창 닫기 모듈 실행")
        driver = context["driver"]
        specific_alert_xpath = context["specific_alert_xpath"]
        print("특정 알럿 XPath:", specific_alert_xpath)  # Debugging line

        # 검사 실시 화면 통제 전환
        window = driver.window_handles
        print("현재 창 핸들:", window)  # Debugging line
        window_handle = window[-1]  # 마지막 창 핸들
        driver.switch_to.window(window_handle)
        print("현재 창 핸들로 전환:", window_handle)  # Debugging line

        try:
            time.sleep(1)  # 모듈 실행 간 잠시 대기
            alert_element = driver.find_element(By.XPATH, specific_alert_xpath)
            alert_element.click()
            print(f"특정 알럿창 닫기 완료: {specific_alert_xpath}")
        except Exception as e:
            print(f"특정 알럿창 닫기 오류: {e}")
    except Exception as e:
        print(f"특정 알럿창 닫기 모듈 실행 중 오류: {e}")
        st.error(f"특정 알럿창 닫기 모듈 실행 중 오류: {e}")
        st.stop()