from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SignupPage:
    URL = "https://www.bronn.kr/"
    LOGIN = (By.CSS_SELECTOR, '#wrap_nav > ul > li.xans-element-.xans-layout.xans-layout-statelogoff.btn_login.eF_ > a')
    SIGNUP = (By.XPATH, '//*[@id="member_login_module_id"]/div/fieldset/div[1]/a[2]')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN)).click()
        self.wait.until(EC.element_to_be_clickable(self.SIGNUP)).click()

    def input_id(self, id):
        # 아이디 입력 후 메시지 반환
        id_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'member_id')))
        id_field.clear()
        id_field.send_keys(id)

        # 포커스 이동
        self.driver.switch_to.active_element.send_keys(Keys.TAB)

        idmsg = self.wait.until(EC.visibility_of_element_located((By.ID, 'idMsg'))).text.strip()
        return idmsg
    
    def input_all(self, pw, pwcfm):
        # 비밀번호, 비밀번호 확인 입력
        pw_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'passwd')))
        pw_field.clear()
        pw_field.send_keys(pw)

        pwcfm_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'user_passwd_confirm')))
        pwcfm_field.clear()
        pwcfm_field.send_keys(pwcfm)

        # 포커스 이동
        self.driver.switch_to.active_element.send_keys(Keys.TAB)

        # 비밀번호 확인 메시지 체크
        try:
            element = self.driver.find_element(By.ID, "pwConfirmMsg")
            pwcfmmsg = element.text.strip()
        except:
            pwcfmmsg = ""

        if pwcfmmsg:
            return pwcfmmsg 

        # 나머지 필드 입력
        inputs = {
            'member_id': "test0",
            'name': "김영희",
            'mobile2': "1234",
            'mobile3': "5678",
            'email1': "abc0@naver.com",
        }
        for field_id, val in inputs.items():
            self.wait.until(EC.visibility_of_element_located((By.ID, field_id))).send_keys(val)

        # 주소 검색 (iframe 여러 번 전환)
        post_btn = self.wait.until(EC.presence_of_element_located((By.ID, 'postBtn')))
        self.driver.execute_script("arguments[0].click();", post_btn)
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'iframeZipcode')))
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="__daum__layer_1"]/iframe')))
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, '__daum__viewerFrame_1')))
        region_field = self.wait.until(EC.presence_of_element_located((By.ID, 'region_name')))
        region_field.send_keys("당곡로", Keys.RETURN)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.link_post span.txt_addr'))).click()
        self.driver.switch_to.default_content()

        # 상세주소, 약관동의, 회원가입 버튼
        self.wait.until(EC.visibility_of_element_located((By.ID, 'addr2'))).send_keys("1")
        self.wait.until(EC.element_to_be_clickable((By.ID, 'sAgreeAllChecked'))).click()
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "회원가입"))).click()

        # alert 노출시 메시지 확인
        try:
            alert = self.wait.until(EC.alert_is_present())
            msg = alert.text.strip()
            if "※" in msg:
                msg = alert.text.split("※")[0].strip()
            return msg
        # 가입완료 화면 메시지 확인
        except:
            try:
                msg = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#contents .xans-member-joincomplete .joinComplete .desc'))).text
                return msg
            except:
                return "test fail"


    def input_pw_max(self, pw):
        # 비밀번호, 비밀번호 확인 입력
        pw_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'passwd')))
        pw_field.clear()
        pw_field.send_keys(pw)

        pwcfm_field = self.wait.until(EC.visibility_of_element_located((By.ID, 'user_passwd_confirm')))
        pwcfm_field.clear()
        pwcfm_field.send_keys(pw)

        # 입력된 글자수 반환
        pw_len = len(pw_field.get_attribute('value'))
        pwcfm_len = len(pwcfm_field.get_attribute('value'))

        return pw_len, pwcfm_len

# 함수 확인용
# if __name__ == "__main__":
#     driver = webdriver.Chrome()
#     try :
#         page = SignupPage(driver)
#         page.open()
#         idmsg = page.input_id("slnp779")
#         print(f"flash message : {idmsg}")

#     finally :
#         driver.quit()
