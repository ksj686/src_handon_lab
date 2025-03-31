import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from geopy.geocoders import Nominatim

df = pd.read_csv('./webapp/reconstruction/Current_Status.csv', encoding='euc-kr')
df1 = df[['진행단계','정비구역명칭','정비구역위치', '정비구역면적(㎡)', '사업구분',]]
df_cleaned = df1.dropna(subset=['정비구역위치', '진행단계', '정비구역면적(㎡)','사업구분','정비구역명칭'])
df_cleaned['서울시_정비구역위치'] = '서울시 ' + df_cleaned['정비구역위치']
# '정비구역위치' 열 삭제 
df_cleaned = df_cleaned.drop(columns=['정비구역위치'])
# print(df_cleaned)

# To-Do : category로 숫자 지정, sort할 필요있을지? 주소 다시 geopy로 가져오기

# 진행단계를 3개 범주로 매핑
stage_mapping = {
    '안전진단': '조합 설립 전',
    '정비계획 수립': '조합 설립 전',
    '정비구역지정': '조합 설립 전',
    '조합설립추진위원회승인': '조합 설립 전',
    '조합설립인가': '조합 설립 전',
    '사업시행인가': '재건축 시행',
    '관리처분인가': '재건축 시행',
    '철거신고': '재건축 시행',
    '착공신고': '재건축 시행',
    '일반분양승인': '재건축 시행',
    '이전고시': '재건축 완료',
    '준공인가': '재건축 완료',
    '조합청산': '재건축 완료',
    '조합해산': '재건축 완료'
}

# 새로운 열 생성
df_cleaned['재건축단계'] = df_cleaned['진행단계'].map(stage_mapping)


category_order = ['조합 설립 전','재건축 시행','재건축 완료']
# CategoricalDtype을 사용하여 범주형 데이터 타입 지정
cat_type = CategoricalDtype(categories=category_order, ordered=True)
df_cleaned['재건축단계'] = df_cleaned['재건축단계'].astype(cat_type)
df_cleaned = df_cleaned.sort_values(by='재건축단계')

# 인덱스 재설정 
df_cleaned.reset_index(drop=True, inplace=True)

print(df_cleaned['재건축단계'])
# print(df_cleaned.info())
print(df_cleaned)
df_cleaned.to_csv('./df_cleaned.csv', index=False)


'''
# Geopy를 사용한 Geocoding 함수 정의
geolocator = Nominatim(user_agent="myGeocoder")

def geocode(address):
    try:
        location = geolocator.geocode(address)
        return location.latitude, location.longitude
    except:
        return None, None

# DataFrame에 위도와 경도 값을 추가
lats = []
lngs = []

for address in df['서울시_정비구역위치']:
    lat, lng = geocode(address)
    lats.append(lat)
    lngs.append(lng)

df1['위도'] = lats
df1['경도'] = lngs

# 결과를 새로운 CSV 파일로 저장
df1.to_csv('./Geocoded_Current_Status.csv', index=False)

print(df1)
'''




'''
df_cleaned.to_csv('./d_none.csv', index=False)

df1 = pd.concat([df['대표지번'],df['진행단계']], axis=1)
# df1 = df['대표지번'].join(df['진행단계']) -> series는 join 안됨
# df1

# df1['진행단계'].value_counts()

# 진행단계의 순서 지정
category_order = ['안전진단', '정비계획 수립', '정비구역지정', '조합설립추진위원회승인', '조합설립인가', '사업시행인가', '관리처분인가', '이전고시', '철거신고', '착공신고', '일반분양승인', '준공인가', '조합청산', '조합해산']
category_order = ['조합 설립 전','재건축 시행','재건축 완료']
# CategoricalDtype을 사용하여 범주형 데이터 타입 지정
cat_type = CategoricalDtype(categories=category_order, ordered=True)
df1['진행단계'] = df1['진행단계'].astype(cat_type)

df1['cate_code'] = df1['진행단계'].cat.codes
# 데이터프레임 확인
print(df1)


'''