"""
gps.aply.biz 사이트에서 위도, 경도 가져오기
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # GPU 하드웨어 가속 비활성화
chrome_options.add_argument("--no-sandbox")   # 샌드박스 모드 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")  # 리소스 제한 문제 해결

# WebDriver 생성 시 옵션 추가
driver = webdriver.Chrome(options=chrome_options)
try:
    # 구글 지도 URL 생성
    SEARCH_LOC_URL = 'https://gps.aply.biz/'
    address = '서울특별시 동대문구 이문로12길 3-7'

    driver.get(SEARCH_LOC_URL)

    # 검색창 찾기
    search_box = driver.find_element(By.NAME, 'address')
    
    # 검색어 입력
    search_box.send_keys(address)
    search_box.send_keys(Keys.RETURN)
    
    # 알림창 처리
    try:
        # 최대 3초 동안 알림창 대기
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.dismiss()  # 알림창 닫기
    except (TimeoutException, NoAlertPresentException):
        # 알림창 없으면 무시
        pass
    
    # 검색 결과 추출 (예: 첫 번째 검색 결과)
    try:
        # 검색 결과 요소 대기 및 찾기
        lat, lng = [WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, name)))
                   .get_attribute('value') for name in ['lat', 'lng']]
        
        # 결과 텍스트 추출
        print(lat, lng)

    
    except Exception as e:
        print(f"결과 추출 중 오류 발생: {e}")

except Exception as e:
    print(f"검색 중 오류 발생: {e}")


finally:
    # 브라우저 닫기
    driver.quit()
