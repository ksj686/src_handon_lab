from flask import render_template
from webapp import app

@app.route('/map')
def draw_map():
    locations = [
    {'lat': 37.5665, 'lng': 126.9780, 'name': '서울시청'},  # 서울시청
    {'lat': 35.1796, 'lng': 129.0756, 'name': '부산광역시'},  # 부산광역시
    {'lat': 37.4563, 'lng': 126.7053, 'name': '인천광역시'},  # 인천광역시
]
    return render_template('map.html', locations=locations)

# 기본 페이지
@app.route('/index')
def index():
    return render_template('index.html')

from flask import request

# 크롤링 결과 페이지
@app.route('/crawl', methods=['POST'])
def crawl():
    url = request.form['url']  # 사용자로부터 URL 입력 받기
    id_text, class_text = crawl_website(url)  # 웹 크롤링 실행
    return render_template('result.html', id_text=id_text, class_text=class_text, url=url)

# 공공 데이터 받아서 맵에 표시하기
@app.route('/generate_map')
def generate_map():
    return render_template('map.html')




@app.route('/weather_home')
def weather_home():
    return render_template('weather.html')

# app.py
from flask import jsonify

@app.route('/weather-data')
def weather_data():
    cities = [
    {"name": "Seoul", "lat": 37.5665, "lon": 126.9780},
    {"name": "Busan", "lat": 35.1796, "lon": 129.0756},
    {"name": "Incheon", "lat": 37.4563, "lon": 126.7052},
    {"name": "Daegu", "lat": 35.8714, "lon": 128.6014},
    {"name": "Daejeon", "lat": 36.3510, "lon": 127.3850},
    # 다른 도시들도 추가할 수 있습니다
    ]

    weather_data = []
    for city in cities:
        url = f"http://www.7timer.info/bin/api.pl?lon={city['lon']}&lat={city['lat']}&product=civil&output=json"
        response = requests.get(url)
        data = response.json()
        reconstruct_place = {
            "name": city["name"],
            "lat": city["lat"],
            "lon": city["lon"],
            "weather": data["dataseries"][0]
        }
        weather_data.append(reconstruct_place)
    return jsonify(weather_data)

import pandas as pd

@app.route('/reconstruct_map')
def reconstruct_map():
    return render_template('reconstruct.html')

@app.route('/reconstruct-data')
def reconstruct_data():
    # places = pd.read_csv('./webapp/reconstruction/d_none.csv')
    places = pd.read_csv('./webapp/reconstruction/df_latlong_cate_added.csv')
    '''
    places = [
    {"name": "Seoul", "lat": 37.5665, "lon": 126.9780},
    {"name": "Busan", "lat": 35.1796, "lon": 129.0756},
    {"name": "Incheon", "lat": 37.4563, "lon": 126.7052},
    {"name": "Daegu", "lat": 35.8714, "lon": 128.6014},
    {"name": "Daejeon", "lat": 36.3510, "lon": 127.3850},
    # 다른 도시들도 추가할 수 있습니다
    ]
    '''

    # df_filtered = places[['위도', '경도', 'cate_code']]

    # DataFrame을 리스트로 변환 
    reconstruct_data = places.to_dict(orient='records')
    # app.logger.debug(reconstruct_data)
    return jsonify(reconstruct_data)

@app.route('/react_index')
def react_index():
    return render_template('react.html')

# 번역테스트 페이지
@app.route('/translate_index')
def translate_index():
    return render_template('translate_index.html')

# ============================여기부터는 함수들===========================



# pip install playwright
# python -m playwright install
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# TO-DO 크롤링 함수. 댓글을 통한 감정 분석 시도도 해보기
def crawl_website(url):
    try:
        with sync_playwright() as p:
            # 브라우저 시작 (Headless 모드)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 페이지 열기
            page.goto(url)

            # JavaScript가 완전히 로드될 때까지 기다리기
            page.wait_for_load_state('networkidle')  # 모든 네트워크 요청이 끝날 때까지 기다림

            # 페이지 소스 가져오기
            html = page.content()

            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(html, 'html.parser')

            # 특정 id를 가진 div 요소 크롤링
            id_content = soup.find('div', id='container')
            if id_content:
                app.logger.debug(id_content)
            else:
                app.logger.debug('no id')
            id_text = id_content.get_text() if id_content else "No element with the given id"

            # 특정 class를 가진 div 요소 크롤링
            class_content = soup.find_all('div', class_='comment_text')
            class_text = [item.get_text() for item in class_content] if class_content else ["No elements with the given class"]

            crawl_prev_page(url)

            # 브라우저 닫기
            browser.close()

            return id_text, class_text

    except Exception as e:
        return f"Error: {e}", []
    

import requests

def crawl_prev_page(url):
    try:
        # 웹 페이지 요청
        response = requests.get(url)
        response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
        
        # 페이지 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 첫 번째 페이지에서 링크 추출 (예: <a> 태그)
        links = soup.find_all('a', href=True)  # href 속성이 있는 모든 <a> 태그 찾기

        # 링크들 중에서 원하는 링크만 필터링 (필터링 조건은 상황에 맞게 수정)
        next_urls = []
        for link in links:
            href = link['href']
            if "wr_id" in href:  # 원하는 조건에 맞는 링크만 추출
                # 절대 URL로 변환 (상대 URL이 있을 수 있음)
                next_urls.append(href if href.startswith('http') else f"{url}/{href}")

        # 두 번째 페이지 크롤링 (링크로 이동)
        for next_url in next_urls:
            crawl_next_page(next_url)  # 다음 링크로 재귀 호출 또는 추가 작업

    except requests.exceptions.RequestException as e:
        print(f"Error while crawling {url}: {e}")

def crawl_next_page(url):
    try:
        # 두 번째 페이지에서 데이터 추출
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 페이지에서 원하는 데이터 추출
        data = soup.find('div', {'class': 'specific-class'})  # 예시로 클래스명이 'specific-class'인 div를 찾기

        crawl_place(url)
        crawl_address(url)

        if data:
            print(f"Data from {url}: {data.get_text()}")
        else:
            print(f"No data found in {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error while crawling {url}: {e}")


# 장소 들어가는 줄 가져오기
def crawl_place(url):
    try:
        # 웹 페이지 요청
        response = requests.get(url)
        response.raise_for_status()

        # 페이지 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # "content" 클래스를 가진 div 찾기
        # content_div = soup.find('div', class_='content')

        # div에서 모든 텍스트 추출
        # text = content_div.get_text(separator='\n')  # 줄바꿈을 기준으로 텍스트 분리

        # "장소"라는 텍스트를 포함하는 줄만 추출
        # place_lines = [line for line in text.split('\n') if "장소" in line]
        place_lines = ""
        for div in soup.find_all('div'):
            if div.find(string=lambda text: "장소" in text if text else False):
                # 현재 태그의 텍스트 추출
                place_lines += div.get_text(strip=True) + '\n'
                # 다음 형제 태그의 텍스트 추출
                next_sibling = div.find_next_sibling('div')
            if next_sibling:
                place_lines += next_sibling.get_text(strip=True) + '\n'
            break

        if place_lines:
            app.logger.debug(f'장소 : {place_lines}')
        else:
            app.logger.debug("crawl_place : 찾을 수 없습니다.")

        # return place_lines

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


# 주소 규칙을 가진 값 가져오기
import re
def crawl_address(url):
    try:
        # 웹 페이지 요청
        response = requests.get(url)
        response.raise_for_status()

        # 페이지 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # "content" 클래스를 가진 div 찾기
        content_div = soup.find('div', class_='content')

        # div에서 모든 텍스트 추출
        text = content_div.get_text(separator='\n')

        # 서울시, 구, 도로명 주소 패턴을 위한 정규 표현식
        address_pattern = r"서울시\s+[가-힣]+\s+구\s+[가-힣]+로\s+\d+"
        address_pattern_new = r"""(([가-힣A-Za-z·\d~\-.]{2,}(로|길).\d+) 
                            |([가-힣A-Za-z·\d~\-.]+(읍|동|번지)\s)\d+) 
                            |([가-힣A-Za-z]+(구)+\s*[가-힣A-Za-z]+(동)) 
                            |([가-힣a-zA-Z\d]+(아파트|빌라|빌딩|마을))"""
        
        # 예: 서울시 동작구 노량진로 10

        # 정규 표현식을 사용하여 주소 추출
        address = re.findall(address_pattern_new, text)

        if address:
            app.logger.debug(f'주소규칙 : {address}')
        else:
            app.logger.debug('crawl_address : 주소가 없습니다.')

        # return address

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []








# import requests
# import time
'''
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 특정 id나 class를 가진 요소 크롤링하는 함수
def crawl_website(url):
    try:
        # WebDriver 실행
        options = webdriver.ChromeOptions()
        options.headless = True  # 브라우저 UI 없이 실행 (headless 모드)
        
        # 크롬 드라이버로 웹 페이지 로드
        driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)
        driver.get(url)

        # JavaScript가 로딩되는 시간을 기다린다 (최대 10초)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "container")))

        # 페이지 소스를 가져온 후 BeautifulSoup으로 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 특정 id를 가진 div 요소 크롤링
        id_content = soup.find('div', id='container')
        if id_content:
            app.logger.debug(id_content)
        else:
            app.logger.debug('no id')
        id_text = id_content.get_text() if id_content else "No element with the given id"

        # 특정 class를 가진 div 요소 크롤링
        class_content = soup.find_all('div', class_='comment_text')
        class_text = [item.get_text() for item in class_content] if class_content else ["No elements with the given class"]

        # 웹드라이버 종료
        driver.quit()

        return id_text, class_text

    except Exception as e:
        return f"Error: {e}", []
'''