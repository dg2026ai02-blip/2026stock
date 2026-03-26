import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="주식 비교 분석", layout="wide")

st.title("📈 한국 vs 미국 주식 비교 분석")

# 기본 종목
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
selected_names = st.multiselect(
    "비교할 종목 선택",
    list(default_tickers.keys()),
    default=["삼성전자", "애플"]
)

period = st.selectbox(
    "기간 선택",
    ["1mo", "3mo", "6mo", "1y", "3y", "5y"],
    index=3
)

if len(selected_names) > 0:
    tickers = [default_tickers[name] for name in selected_names]

    try:
        # 데이터 다운로드
        raw_data = yf.download(
            tickers,
            period=period,
            group_by='ticker',
            auto_adjust=True,
            progress=False
        )

        price_df = pd.DataFrame()

        # 여러 종목 처리 안정화
        if len(tickers) == 1:
            ticker = tickers[0]
            price_df[selected_names[0]] = raw_data["Close"]
        else:
            for name, ticker in zip(selected_names, tickers):
                if ticker in raw_data:
                    price_df[name] = raw_data[ticker]["Close"]

        # 데이터 없을 경우
        if price_df.empty:
            st.error("데이터를 불러오지 못했습니다. 티커를 확인하세요.")
        else:
            st.subheader("📊 가격 차트")
            st.line_chart(price_df)

            # 수익률 계산
            returns = (price_df.iloc[-1] / price_df.iloc[0] - 1) * 100

            st.subheader("📈 수익률 (%)")
            st.dataframe(returns.sort_values(ascending=False).round(2))

            # 누적 수익률
            st.subheader("📉 누적 수익률 비교")
            normalized = price_df / price_df.iloc[0]

            fig, ax = plt.subplots()
            normalized.plot(ax=ax)
            ax.set_title("누적 수익률 비교")
            ax.grid()

            st.pyplot(fig)

    except Exception as e:
        st.error(f"오류 발생: {e}")

else:
    st.warning("종목을 선택해주세요.")
