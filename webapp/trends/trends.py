from pytrends.request import TrendReq
from datetime import datetime, timedelta

pytrends = TrendReq(hl='en-US', tz=360, retries=3)
start_date = datetime(2024, 11, 1).date()
end_date = datetime(2024, 11, 1).date()
pytrends.build_payload(kw_list=['Python'], timeframe=f'{start_date} {end_date}', geo='US', gprop='news')
data = pytrends.interest_over_time()
print(data.head())

related_queries = pytrends.related_queries()
print(related_queries)

data.to_csv('google_trends_data.csv')



'''
from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

# Google Trends와 연결
pytrends = TrendReq(hl='en-US', tz=360)

# 정치 카테고리에서 검색한 키워드 (예: 정치 관련 인기 키워드들)
political_keywords = ['politics']

# 요청 기간을 나누기 위한 함수
def split_dates(start_date, end_date, delta_days=1):
    """
    날짜를 delta_days 단위로 나누어서 시작 날짜부터 끝 날짜까지 반환하는 함수
    """
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=delta_days)
        date_list.append((current_date, next_date if next_date <= end_date else end_date))
        current_date = next_date
    return date_list

# 데이터를 요청하는 함수
def get_trend_data(keywords, start_date, end_date):
    try:
        # 요청 기간 설정
        pytrends.build_payload(kw_list=keywords, timeframe=f'{start_date} {end_date}')
        return pytrends.interest_over_time()
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# 시작 날짜와 끝 날짜 설정
start_date = datetime(2024, 11, 1).date()
end_date = datetime(2024, 11, 1).date()

# 날짜를 나누어 요청하기
date_ranges = split_dates(start_date, end_date, delta_days=1)

# 결과를 저장할 빈 DataFrame
all_data = pd.DataFrame()

# 날짜별로 데이터를 요청하여 결합
for start, end in date_ranges:
    print(f"Fetching data from {start} to {end}")
    
    # 최대 3번 재시도
    retries = 3
    while retries > 0:
        df = get_trend_data(political_keywords, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        
        if df is not None:
            all_data = pd.concat([all_data, df])
            break
        else:
            print(f"Retrying... ({retries} retries left)")
            retries -= 1
            time.sleep(5)  # 에러가 발생하면 잠시 대기 후 재시도
    
    # 요청 후 잠시 대기 (일반적으로 1초 이상의 대기)
    time.sleep(1)

# 'isPartial' 컬럼이 있을 경우 제거
if 'isPartial' in all_data.columns:
    all_data = all_data[all_data['isPartial'] == False]
    all_data = all_data.drop(columns=['isPartial'])

# 각 날짜의 평균 검색량 계산
all_data['average_search'] = all_data.mean(axis=1)

# 이상치 탐지: 평균 + 2*표준편차를 초과하는 날짜를 찾음
std_dev = all_data['average_search'].std()
mean_search = all_data['average_search'].mean()

# 유난히 검색이 많은 날짜 찾기 (평균 + 2*표준편차를 넘는 값)
threshold = mean_search + 2 * std_dev
outlier_dates = all_data[all_data['average_search'] > threshold]

# 결과 출력
print(f"Threshold for unusual search activity: {threshold}")
print("Dates with unusually high search activity:")
print(outlier_dates[['average_search']])

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(all_data.index, all_data['average_search'], label='Average Search Volume', color='blue')

# 이상치 날짜에 대해 빨간색으로 표시
plt.scatter(outlier_dates.index, outlier_dates['average_search'], color='red', label='Unusual Search Activity')

plt.title('Unusual Search Activity in Politics (Last 3 Days)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Average Search Volume', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 그래프 이미지 파일로 저장
plt.tight_layout()
plt.savefig('unusual_political_search_activity.png')

# 그래프 보여주기
plt.show()
'''