import pytest

from web.signup import SignupPage

ID_CASES = [
    pytest.param("test1", "test1는 사용 가능한 아이디입니다.", id = "사용가능"),
    pytest.param("test", "test는 이미 사용중인 아이디입니다.", id = "중복")
]

@pytest.mark.parametrize("userid, expected", ID_CASES)
def test_idchk_cases(driver, userid, expected):

    page = SignupPage(driver)
    page.open()
    msg = page.input_id(userid)
    print(f"\n입력값: {userid}, 예상: {expected}, 실제: {msg}")

    assert expected in msg
