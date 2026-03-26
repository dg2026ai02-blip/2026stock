import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="주식 비교 분석", layout="wide")

st.title("📈 한국 vs 미국 주식 비교 분석")

# 기본 종목 리스트
default_tickers = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "네이버": "035420.KS",
    "카카오": "035720.KS",
    "애플": "AAPL",
    "마이크로소프트": "MSFT",
    "엔비디아": "NVDA",
    "테슬라": "TSLA"
}

# 사용자 선택
selected = st.multiselect(
    "비교할 종목 선택",
    options=list(default_tickers.keys()),
    default=["삼성전자", "애플"]
)

period = st.selectbox(
    "기간 선택",
    ["1mo", "3mo", "6mo", "1y", "3y", "5y"],
    index=3
)

if selected:
    tickers = [default_tickers[name] for name in selected]

    st.subheader("📊 가격 데이터")

    data = yf.download(tickers, period=period)["Adj Close"]

    if len(tickers) == 1:
        data = data.to_frame()

    st.line_chart(data)

    # 수익률 계산
    returns = (data.iloc[-1] / data.iloc[0] - 1) * 100

    st.subheader("📈 수익률 (%)")
    st.dataframe(returns.sort_values(ascending=False).round(2))

    # 누적 수익률 그래프
    st.subheader("📉 누적 수익률 비교")

    normalized = data / data.iloc[0]

    fig, ax = plt.subplots(figsize=(10, 5))
    normalized.plot(ax=ax)

    ax.set_title("누적 수익률 비교")
    ax.set_ylabel("배수")
    ax.grid()

    st.pyplot(fig)

else:
    st.warning("종목을 선택해주세요.")
