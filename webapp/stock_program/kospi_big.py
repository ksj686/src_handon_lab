import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# 임의의 날짜 설정 (예: 2024년 11월 7일)
# input_date = datetime.datetime(2024, 11, 7)
input_date = datetime.datetime(2024, 12, 3)

# 3개월 전 날짜 계산
three_months_ago = input_date - datetime.timedelta(days=90)

# 오늘 날짜
today = datetime.datetime.today()

# 특정 기업들의 티커 (삼성전자, LG전자, 현대자동차, SK)
stocks = ['005930.KS', '066570.KS', '005380.KS', '034730.KS']
company_names = ['Samsung Electronics', 'LG Electronics', 'Hyundai Motors', 'SK Group']

# 주식 데이터 다운로드
stock_data = yf.download(stocks, start=three_months_ago, end=today)['Close']

# 특정 날짜를 그래프에 표시 (예: input_date)
highlight_date = input_date  # datetime.datetime 형식으로 그대로 사용

# 그래프 그리기
plt.figure(figsize=(10, 6))

# 각 기업의 종가를 그래프에 표시
for i, stock in enumerate(stocks):
    plt.plot(stock_data.index, stock_data[stock], label=company_names[i])

# highlight_date가 데이터 인덱스에 있는지 확인하고, 없으면 가장 가까운 날짜 선택
for i, stock in enumerate(stocks):
    if highlight_date in stock_data.index:
        highlight_price = stock_data.loc[highlight_date, stock]
        plt.scatter(highlight_date, highlight_price, zorder=5, label=f'{company_names[i]} on {highlight_date.date()}')
    else:
        # 가장 가까운 날짜를 찾기 위해 가장 가까운 날짜를 찾음
        closest_date = min(stock_data.index, key=lambda x: abs(x - highlight_date))
        closest_price = stock_data.loc[closest_date, stock]
        plt.scatter(closest_date, closest_price, zorder=5, label=f'{company_names[i]} on {closest_date.date()}')

# 그래프 제목 및 레이블 설정
plt.title('Selected KOSPI Stocks Closing Prices (Last 3 Months)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (KRW)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 그래프 이미지 파일로 저장
plt.tight_layout()
plt.savefig('kospi_selected_stocks_trend_with_names.png')

# 그래프 보여주기
plt.show()
