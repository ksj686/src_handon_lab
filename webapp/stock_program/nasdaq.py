import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# 임의의 날짜 설정 (예: 2024년 11월 7일)
input_date = datetime.datetime(2024, 11, 7)

# 3개월 전 날짜 계산
three_months_ago = input_date - datetime.timedelta(days=90)

# 오늘 날짜
today = datetime.datetime.today()

# 'NASDAQ' 주식 데이터 다운로드 (이 예에서는 ^IXIC로 사용)
nasdaq = yf.download('^IXIC', start=three_months_ago, end=today)

# 특정 날짜를 그래프에 표시 (예: input_date)
highlight_date = input_date  # datetime.datetime 형식으로 그대로 사용

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(nasdaq.index, nasdaq['Close'], label='NASDAQ Closing Price', color='blue')

# highlight_date가 데이터 인덱스에 있는지 확인하고, 없으면 가장 가까운 날짜 선택
if highlight_date in nasdaq.index:
    highlight_price = nasdaq.loc[highlight_date, 'Close']
    plt.scatter(highlight_date, highlight_price, color='red', zorder=5, label=f'Highlighted Date: {highlight_date.date()}')
else:
    # 가까운 날짜를 찾기 위해 가장 가까운 날짜를 찾음
    closest_date = min(nasdaq.index, key=lambda x: abs(x - highlight_date))
    closest_price = nasdaq.loc[closest_date, 'Close']
    plt.scatter(closest_date, closest_price, color='red', zorder=5, label=f'Closest Date: {closest_date.date()}')

# 그래프 제목 및 레이블 설정
plt.title('NASDAQ Closing Price (Last 3 Months)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 그래프 이미지 파일로 저장
plt.tight_layout()
plt.savefig('nasdaq_trend.png')

# 그래프 보여주기
plt.show()
