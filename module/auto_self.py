from selenium.webdriver.common.by import By
import streamlit as st
from selenium.webdriver.common.action_chains import ActionChains
# from module.error_with_screenshot import error_with_screenshot
# from itertools import islice

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

def run(context):
    try:
        # context에서 필요한 값 가져오기
        print("자기보고 입력 모듈 실행")
        driver = context["driver"]
        self_df = context["self_df_row"]
        self_response_xpath_raw = context["self_response_xpath_raw"]
        item_start_index = int(context["item_start_index"])
        item_index_step = int(context["item_index_step"])
        value_offset = int(context["value_offset"])
        self_page_dict = context["self_page_dict"]
        print("asdfasdfsadf", self_response_xpath_raw)

        # 검사 실시 화면 통제 전환
        window = driver.window_handles
        print("현재 창 핸들:", window)  # Debugging line
        window_handle = window[-1]  # 마지막 창 핸들
        driver.switch_to.window(window_handle)
        print("현재 창 핸들로 전환:", window_handle)  # Debugging line

        print("자기보고 입력 데이터프레임:", self_df)  # Debugging line


        row_list = self_df.iloc[0].to_list()
        # row의 각 원소값에 value_offset을 적용
        row_list = [str(int(value) + value_offset) for value in row_list]
        # item_start_index, item_index_step을 적용해 item_idx 생성
        item_index_list = [item_start_index + i * item_index_step for i in range(len(row_list))]
        print("자기보고 항목 인덱스:", item_index_list)  # Debugging line
        print("자기보고 항목 값:", row_list)  # Debugging line
        print("자기보고 dict:", self_page_dict)  # Debugging line

        for key_index, _ in enumerate(list(self_page_dict.keys())):
            print(f"처리 중인 페이지 인덱스: {key_index}")
            start_page_index = list(self_page_dict.keys())[key_index]
            end_page_index = list(self_page_dict.keys())[key_index + 1] if key_index + 1 < len(self_page_dict) else len(item_index_list)
            item_index_list_slice = item_index_list[start_page_index:end_page_index]
            row_list_slice = row_list[start_page_index:end_page_index]
            print(f"페이지 {start_page_index}에서 {end_page_index}까지의 항목 인덱스: {item_index_list_slice}, 값: {row_list_slice}")

            for item_index, value in zip(item_index_list_slice, row_list_slice):
                print(f"자기보고 항목 {item_index}: {value}")
                print(f"자기보고 row_XPath: {self_response_xpath_raw}")
                try:
                    self_response_xpath = self_response_xpath_raw.format(item_index, value)
                    print(f"자기보고 XPath: {self_response_xpath}")  # Debugging line
                    actions = ActionChains(driver)
                    self_element = driver.find_element(By.XPATH, self_response_xpath)
                    actions.move_to_element(self_element).perform()
                    self_element.click()  # 클릭하여 입력 필드 활성화
                except Exception as e:
                    print(f"XPath 오류: {self_response_xpath} - {e}")
                    st.error(f"XPath 오류: {self_response_xpath} - {e}")
                    st.stop()
            print(f"{key_index+1} 페이지에서 항목 입력 완료")
            # 페이지 다음 버튼 클릭
            try:
                next_button_xpath = self_page_dict[start_page_index]
                next_button = driver.find_element(By.XPATH, next_button_xpath)
                next_button.click()  # 다음 버튼 클릭
                print(f"{key_index+1} 페이지 다음 버튼 클릭 완료")
            except Exception as e:
                print(f"다음 버튼 클릭 오류: {e}")
                st.error(f"다음 버튼 클릭 오류: {e}")
                st.stop()

    except Exception as e:
        print(f"자기보고 입력 모듈 실행 중 오류 발생: {e}")
        st.error(f"자기보고 입력 모듈 실행 중 오류 발생: {e}")
        error_with_screenshot(driver, e)
        st.stop()