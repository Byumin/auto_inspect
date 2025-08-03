import os
from datetime import datetime
import streamlit as st

def error_with_screenshot(driver, error_message):
    # 1. 파일 이름에 타임스탬프 추가해 중복 방지
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(os.getcwd(), f"screenshot_{timestamp}.png")

    # 2. 스크린샷 저장
    driver.save_screenshot(screenshot_path)
    print("📸 오류 스크린샷 저장 위치:", screenshot_path)

    # 3. Streamlit에 이미지와 오류 메시지 출력
    st.error(error_message)
    st.image(screenshot_path, caption="🛑 오류 발생 시점 화면", width=700)