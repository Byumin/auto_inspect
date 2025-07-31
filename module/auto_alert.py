def run(context):
    print("알럿창 닫기 모듈 실행")
    driver = context["driver"]

    # 검사 실시 화면 통제 전환 
    window = driver.window_handles
    print("현재 창 핸들:", window)  # Debugging line
    window_handle = window[-1]  # 마지막 창 핸들
    driver.switch_to.window(window_handle)
    print("현재 창 핸들로 전환:", window_handle)  # Debugging line

    driver.switch_to.alert.accept()