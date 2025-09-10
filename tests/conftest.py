import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# test 실행할 브라우저 설정
@pytest.fixture (scope="session")
def driver():
    opts = Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        opts.add_argument("--headless=new") # GUI 없이 Chrome 실행
    opts.add_argument("--window-size=1280,900") # 브라우저 창 크기 설정

    driver = webdriver.Chrome(options=opts)
    yield driver
    driver.quit()

# 브라우저가 모든 test 실행 후 종료되도록 설정
@pytest.fixture(autouse=True)
def reset_state(driver):
    driver.delete_all_cookies()
    driver.get("about:blank")
    yield
