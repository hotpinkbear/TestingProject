import pytest

from web.signup import SignupPage

ID_CASES = [
    pytest.param("test1", "test1는 사용 가능한 아이디입니다.", id = "TC001"),
    pytest.param("test", "test는 이미 사용중인 아이디입니다.", id = "TC002"),
    pytest.param("testabcdefghijkl", "testabcdefghijkl는 사용 가능한 아이디입니다.", id = "TC003"),
    pytest.param("testab1234567890", "testab1234567890는 사용 가능한 아이디입니다.", id = "TC004"),
    pytest.param("1234", "대문자/공백/특수문자가 포함되었거나, 숫자로 시작 또는 숫자로만 이루어진 아이디는 사용할 수 없습니다.", id = "TC005"),
    pytest.param("Tes1", "대문자/공백/특수문자가 포함되었거나, 숫자로 시작 또는 숫자로만 이루어진 아이디는 사용할 수 없습니다.", id = "TC006"),
    pytest.param("test123@", "대문자/공백/특수문자가 포함되었거나, 숫자로 시작 또는 숫자로만 이루어진 아이디는 사용할 수 없습니다.", id = "TC007"),
    pytest.param("te1", "아이디는 영문소문자 또는 숫자 4~16자로 입력해 주세요.", id = "TC008"),
    pytest.param("testab12345678900", "아이디는 영문소문자 또는 숫자 4~16자로 입력해 주세요.", id = "TC009"),
    pytest.param("", "아이디를 입력해 주세요.", id = "TC010")
]

PW_CASES = [
    # pytest.param("Test12#$", "Test12#$", "회원가입이 완료 되었습니다.", id = "TC011"),
    pytest.param("TESTPW0123456789", "TESTPW0123456789", "비밀번호 입력 조건을 다시 한번 확인해주세요.", id = "TC012"),
    pytest.param("testpw12&-", "testpw12&-", "비밀번호 입력 조건을 다시 한번 확인해주세요.", id = "TC013"),
    pytest.param("test01@", "test01@", "비밀번호 입력 조건을 다시 한번 확인해주세요.", id = "TC014"),
    pytest.param("aaaaaaaa", "aaaaaaaa", "비밀번호 입력 조건을 다시 한번 확인해주세요.", id = "TC016"),
    pytest.param("test12#$", "Test12#$", "비밀번호가 일치하지 않습니다.", id = "TC017"),
    pytest.param("", "", "비밀번호 항목은 필수 입력값입니다.", id = "TC018"),
    pytest.param("testpw12#", "", "비밀번호가 일치하지 않습니다.", id = "TC019")
]

# ID 입력값 유효성 검사
@pytest.mark.parametrize("userid, expected", ID_CASES)
def test_id_chk_val(driver_session, userid, expected):
    page = SignupPage(driver_session)
    page.open()
    msg = page.input_id(userid)
    print(f"\n입력값: {userid} / 예상: {expected} / 실제: {msg}")

    assert expected == msg

# PW 입력값 유효성 검사
@pytest.mark.parametrize("userpw, userpwcfm, expected", PW_CASES)
def test_pw_chk_val(driver, userpw, userpwcfm, expected):
    page = SignupPage(driver)
    page.open()
    msg = page.input_all(userpw, userpwcfm)
    print(f"\n입력값: {userpw}, {userpwcfm} / 예상: {expected} / 실제: {msg}")
    
    assert expected == msg

# PW 최대 입력가능 글자수 제한 확인 (TC015)
def test_pw_chk_maxlen(driver):
    userpw = "testpw0123456789#"
    expected = 16
    
    page = SignupPage(driver)
    page.open()
    pw_len, pwcfm_len = page.input_pw_max(userpw)
    print(f"\n입력글자수: {len(userpw)} / 예상: {expected} / 실제: {pw_len}, {pwcfm_len}")

    assert pw_len == expected and pwcfm_len == expected

