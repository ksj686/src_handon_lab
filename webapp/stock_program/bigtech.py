import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# 임의의 날짜 설정 (예: 2024년 11월 7일)
input_date = datetime.datetime(2024, 11, 7)

# 3개월 전 날짜 계산
three_months_ago = input_date - datetime.timedelta(days=90)

# 오늘 날짜
today = datetime.datetime.today()

# 빅 테크 기업들의 주식 티커 (Apple, Microsoft, Google, Amazon, Meta, Tesla)
big_tech_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA']

# 주식 데이터 다운로드
big_tech_data = yf.download(big_tech_tickers, start=three_months_ago, end=today)['Close']

# 특정 날짜를 그래프에 표시 (예: input_date)
highlight_date = input_date  # datetime.datetime 형식으로 그대로 사용

# 그래프 그리기
plt.figure(figsize=(10, 6))

# 각 빅 테크 기업의 종가를 그래프에 표시
for ticker in big_tech_tickers:
    plt.plot(big_tech_data.index, big_tech_data[ticker], label=f'{ticker} Closing Price')

# highlight_date가 데이터 인덱스에 있는지 확인하고, 없으면 가장 가까운 날짜 선택
for ticker in big_tech_tickers:
    if highlight_date in big_tech_data.index:
        highlight_price = big_tech_data.loc[highlight_date, ticker]
        plt.scatter(highlight_date, highlight_price, zorder=5, label=f'{ticker} on {highlight_date.date()}')
    else:
        # 가까운 날짜를 찾기 위해 가장 가까운 날짜를 찾음
        closest_date = min(big_tech_data.index, key=lambda x: abs(x - highlight_date))
        closest_price = big_tech_data.loc[closest_date, ticker]
        plt.scatter(closest_date, closest_price, zorder=5, label=f'{ticker} on {closest_date.date()}')

# 그래프 제목 및 레이블 설정
plt.title('Big Tech Companies & Tesla Closing Prices (Last 3 Months)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.xticks(rotation=45)
plt.legend(loc='upper left')

# 그래프 이미지 파일로 저장
plt.tight_layout()
plt.savefig('big_tech_tesla_trend.png')

# 그래프 보여주기
plt.show()
