from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import streamlit as st
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains

def run(context):
    print("인적정보 입력 모듈 실행")
    driver = context["driver"]
    info_df = context["info_df_row"]
    info_dict = context["info_dict"]
    info_submit_xpath = context["info_submit_xpath"]

    # 검사 실시 화면 통제 전환 
    window = driver.window_handles
    print("현재 창 핸들:", window)  # Debugging line
    window_handle = window[-1]  # 마지막 창 핸들
    driver.switch_to.window(window_handle)
    print("현재 창 핸들로 전환:", window_handle)  # Debugging line

    print("info_df_row:", info_df.head())  # Debugging line
    print("info_dict:", info_dict) # Debugging line 인자 잘 받는지

    for field, xpath in info_dict.items():
        try:
            if field == 'SEX' :
                print(f"성별 입력: {field}, XPath: {xpath}")
                sex_xpath = xpath.format(info_df[field].values[0])
                sex_element = driver.find_element(By.XPATH, sex_xpath)
                sex_element.click()
            elif field == 'BIRTHDAY' :
                print(f"생년월일 입력: {field}, XPath: {xpath}")
                birth_xpath = xpath
                birth_box = driver.find_element(By.XPATH, birth_xpath)
                birth_box.click()  # 클릭하여 입력 필드 활성화
                time.sleep(1)  # 잠시 대기하여 달력 로드
                birth_day = info_df[field].iloc[0]
                birth_day = pd.to_datetime(birth_day, errors='coerce')
                print(f"입력할 생년월일: {birth_day}")
                # 년 요소 선택
                dropdown_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-year')
                dropdown_year = Select(dropdown_year)
                year = birth_day.strftime('%Y')
                dropdown_year.select_by_visible_text("{}".format(year))
                # 월 요소 선택
                dropdown_month = driver.find_element(By.CLASS_NAME, 'ui-datepicker-month')
                dropdown_month = Select(dropdown_month)
                month = birth_day.strftime('%m')
                month = str(int(month)) + '월'  # 월을 숫자로 변환
                dropdown_month.select_by_visible_text("{}".format(month))
                # 일 요소 선택
                day = birth_day.strftime('%d')
                day = str(int(day))
                day_element = driver.find_element(By.XPATH, "//a[@class='ui-state-default' and text()='{}']".format(day))
                day_element.click()
            elif field == 'REGION' :
                print(f"지역 입력: {field}, XPath: {xpath}")
                region = info_df[field].iloc[0]
                dropdown_element = driver.find_element(By.XPATH, xpath)
                dropdown_element = Select(dropdown_element)
                dropdown_element.select_by_visible_text(region)
            elif field == 'AFFILIATION' : 
                print(f"소속 입력: {field}, XPath: {xpath}")
                affiliation = info_df[field].iloc[0]
                affiliation_element = driver.find_element(By.XPATH, xpath)
                affiliation_element = Select(affiliation_element)
                affiliation_element.select_by_visible_text(affiliation)
            elif field == 'GRADE' : # 여기서 오류가 발생함
                time.sleep(1)  # 페이지 로드 대기
                print(f"학년 입력: {field}, XPath: {xpath}")
                grade = info_df[field].iloc[0]
                grade_element = driver.find_element(By.XPATH, xpath)
                grade_element = Select(grade_element)
                grade_element.select_by_visible_text(grade)
            else :
                print(f"입력할 필드: {field}, XPath: {xpath}")
                if '{' in xpath:
                    try:
                        print("넘어 왔는지 확인")
                        addition_xpath = xpath.format(info_df[field].values[0])
                        print(f"추가 입력 필드 XPath: {addition_xpath}")  # Debugging line
                        actions = ActionChains(driver)
                        addition_element = driver.find_element(By.XPATH, addition_xpath)
                        actions.move_to_element(addition_element).perform()
                        addition_element.click()  # 클릭하여 입력 필드 활성화
                    except Exception as e:
                        print(f"클릭 입력 실패 - 필드: {field} - {e}")
                        st.error(f"클릭 입력 실패 - 필드: {field} - {e}")
                        st.stop()
                        continue
                else:
                    try:
                        element = driver.find_element(By.XPATH, xpath)
                        value = info_df[field].values[0]
                        element.send_keys(value)
                    except Exception as e:
                        print(f"텍스트 입력 실패 - 필드: {field} - {e}")
                        continue
        except Exception as e:
            print(f"입력 실패: {field} - {e}")
            st.stop()
    # 확인 버튼 클릭
    print("인적사항 입력 완료, 제출 버튼 클릭")
    print(f"인적사항 제출 버튼 XPath: {info_submit_xpath}")  # Debugging line
    try:
        info_submit_button = driver.find_element(By.XPATH, info_submit_xpath)
        actions = ActionChains(driver)
        actions.move_to_element(info_submit_button).perform()
        info_submit_button.click()  # 클릭하여 제출
    except Exception as e:
        print(f"인적사항 제출 버튼 클릭 오류: {e}")
        st.error(f"인적사항 제출 버튼 클릭 오류: {e}")
        st.stop()
    time.sleep(1)