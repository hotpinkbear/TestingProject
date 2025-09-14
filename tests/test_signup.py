import csv
import pytest

from web.signup import SignupPage

# 해당 경로의 csv파일에서 테스트케이스 수집
def load_cases(path):
    cases = []
    ids = []

    # 파일을 읽기모드로 열고 자동으로 닫음
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        # 컬럼명 추출
        input_keys = [key for key in reader.fieldnames if key.startswith("input")]
        expected_key = "expected_result"
        id_key = "id" if "id" in reader.fieldnames else None

        for idx, row in enumerate(reader):
            inputs = tuple(row[key] for key in input_keys) # input들을 튜플로 묶음
            expected = row[expected_key]
            case_id = row[id_key] if id_key and row[id_key] else f"case{idx+1}"

            cases.append((inputs, expected)) #튜플형태로 리스트에 추가
            ids.append(case_id)
    return cases, ids

ID_CASES, ID_IDS = load_cases("tests/data/id.csv")
PW_CASES, PW_IDS = load_cases("tests/data/pw.csv")

# ID 입력값 유효성 검사
@pytest.mark.parametrize("inputs, expected", ID_CASES, ids=ID_IDS)
def test_id_chk_val(driver_session, inputs, expected):
    page = SignupPage(driver_session)
    page.open()

    (userid,) = inputs
    msg = page.input_id(userid)
    print(f"\n입력값: {userid} / 예상: {expected} / 실제: {msg}")

    assert expected == msg

# PW 입력값 유효성 검사
@pytest.mark.parametrize("inputs, expected", PW_CASES, ids=PW_IDS)
def test_pw_chk_val(driver, inputs, expected):
    page = SignupPage(driver)
    page.open()

    userpw, userpwcfm = inputs
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

