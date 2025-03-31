# 주소로 위도 경도 가져오기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 웹 드라이버 설정

chrome_options = Options() 
chrome_options.add_argument("--headless") # 헤드리스 모드 활성화 
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--in-process-gpu")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get('https://deveapp.com/map.php')
    # #address 구역에 입력값 넣기
    address_input = driver.find_element(By.ID, 'search_area')
    '''
    address_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#search_area"))
    )
    '''
    address = '서울특별시 송파구 가락동 138'
    # address_input.send_keys(address)  # 여기에 입력값을 넣으세요
    driver.execute_script("arguments[0].value = arguments[1];", address_input, address)
    # address_input.send_keys(Keys.RETURN)

    # #btnGetGpsByAddress 버튼 클릭하기
    button = driver.find_element(By.CSS_SELECTOR, "#search_address")
    button.click()
    time.sleep(1)
    
    lat_value, lng_value = [WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, id)))
                   .get_attribute('value') for id in ['lat', 'lng']]

    # lat_value = driver.find_element(By.CSS_SELECTOR, "#lat").get_attribute('value')
    # lng_value = driver.find_element(By.CSS_SELECTOR, "#lng").get_attribute('value')

    # #lat과 #lng 값이 비어 있지 않은지 확인 
    if lat_value and lng_value: 
        print(f"Latitude: {lat_value}, Longitude: {lng_value}") 
    else: 
        print("Latitude와 Longitude 값을 가져오는 데 실패했습니다.")

except Exception as e: 
    print(f"오류가 발생했습니다: {e}")

finally:
    driver.quit()