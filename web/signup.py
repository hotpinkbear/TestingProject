from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SignupPage:
    URL = "https://www.bronn.kr/"
    LOGIN = (By.CSS_SELECTOR, '#wrap_nav > ul > li.xans-element-.xans-layout.xans-layout-statelogoff.btn_login.eF_ > a')
    SIGNUP = (By.XPATH, '//*[@id="member_login_module_id"]/div/fieldset/div[1]/a[2]')
    INPUTID = (By.ID, 'member_id')
    IDMSG = (By.ID, "idMsg")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN)).click()
        self.wait.until(EC.element_to_be_clickable(self.SIGNUP)).click()

    def input_id(self, id):
        id_field = self.wait.until(EC.visibility_of_element_located(self.INPUTID))
        id_field.clear()
        id_field.send_keys(id)

        self.driver.find_element(By.TAG_NAME, "body").click()

        idmsg = self.wait.until(EC.visibility_of_element_located(self.IDMSG)).text
        return idmsg.strip()
    
    def input_pw(self, pw):
        pass # 코드 입력 예정

    def input_all(self):
        pass # 코드 입력 예정

    def submit(self):
        pass # 코드 입력 예정

# 함수 실행 확인용
if __name__ == "__main__":
    driver = webdriver.Chrome()
    try :
        page = SignupPage(driver)
        page.open()
        idmsg = page.input_id("slnp779")
        print(f"flash message : {idmsg}")

    finally :
        driver.quit()
