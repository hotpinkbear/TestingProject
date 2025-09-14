import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 함수 단위로 실행되는 드라이버
@pytest.fixture
def driver():
    opts = Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        opts.add_argument("--headless=new") # GUI 없이 Chrome 실행
    opts.add_argument("--window-size=1280,900") # 브라우저 창 크기 설정

    driver = webdriver.Chrome(options=opts)
    yield driver
    driver.quit()

# 세션 단위로 실행되는 드라이버
@pytest.fixture(scope="session")
def driver_session():
    opts = Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        opts.add_argument("--headless=new") # GUI 없이 Chrome 실행
    opts.add_argument("--window-size=1280,900") # 브라우저 창 크기 설정

    driver = webdriver.Chrome(options=opts)
    yield driver
    driver.quit()
    
# 테스트 실행 전후에 브라우저 상태 초기화
@pytest.fixture(autouse=True)
def reset_state(driver):
    driver.delete_all_cookies()
    driver.get("about:blank")
    yield
