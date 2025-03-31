# 주소로 위도 경도 가져오기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 웹 드라이버 설정

chrome_options = Options() 
chrome_options.add_argument("--headless") # 헤드리스 모드 활성화 
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--in-process-gpu")

# chrome_options.add_argument("--disable-software-rasterizer")
# chrome_options.add_argument("--disable-gpu-driver-bug-workarounds") # GPU 드라이버 버그 우회 비활성화

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver_path = ChromeDriverManager().install() 
# service = Service(driver_path)
driver = webdriver.Chrome(options=chrome_options)
# service = Service('C:\\labs_python\\chromedriver.exe')  # 여기에 chromedriver 경로를 입력하세요
# driver = webdriver.Chrome(service=service)

try:
    driver.get('https://gps.aply.biz/')
    # #address 구역에 입력값 넣기
    address_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#address"))
    )
    address_input.send_keys('서울특별시 송파구 가락동 138')  # 여기에 입력값을 넣으세요

    # #btnGetGpsByAddress 버튼 클릭하기
    button = driver.find_element(By.CSS_SELECTOR, "#btnGetGpsByAddress")
    button.click()
    time.sleep(1)
    button = driver.find_element(By.CSS_SELECTOR, "#askModalOKButton")
    button.click()

    lat_value = driver.find_element(By.CSS_SELECTOR, "#lat").get_attribute('value')
    lng_value = driver.find_element(By.CSS_SELECTOR, "#lng").get_attribute('value')

    # #lat과 #lng 값이 비어 있지 않은지 확인 
    if lat_value and lng_value: 
        print(f"Latitude: {lat_value}, Longitude: {lng_value}") 
    else: 
        print("Latitude와 Longitude 값을 가져오는 데 실패했습니다.")

except Exception as e: 
    print(f"오류가 발생했습니다: {e}")

finally:
    driver.quit()