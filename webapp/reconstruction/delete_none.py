import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import os

# print(os.listdir('.'))  # 현재 디렉토리의 파일 목록을 출력하여 확인


df = pd.read_csv('./webapp/reconstruction/Current_Status.csv', encoding='euc-kr')
df1 = df[[]]
df_cleaned = df.dropna(subset=['정비구역위치', '진행단계', '정비구역면적(㎡)'])
print(df_cleaned)
df_cleaned.to_csv('./d_none.csv', index=False)

# df = pd.read_csv('./webapp/reconstruction/d_none.csv')
# 진행단계의 순서 지정
category_order = ['안전진단', '정비계획 수립', '정비구역지정', '조합설립추진위원회승인', '조합설립인가', '사업시행인가', '관리처분인가', '이전고시', '철거신고', '착공신고', '일반분양승인', '준공인가', '조합청산', '조합해산']

# CategoricalDtype을 사용하여 범주형 데이터 타입 지정
cat_type = CategoricalDtype(categories=category_order, ordered=True)

df['진행단계'] = df['진행단계'].astype(cat_type)

df['cate_code'] = df['진행단계'].cat.codes
print(df)
df.to_csv('./d_none.csv', index=False)