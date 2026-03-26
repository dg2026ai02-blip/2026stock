import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 페이지 기본 설정
st.set_page_config(page_title="한/미 주식 수익률 비교기", layout="wide", page_icon="📈")

st.title("📈 한/미 주요 주식 수익률 비교 분석기")
st.markdown("한국(KOSPI/KOSDAQ) 및 미국 시장의 주요 주식 종가를 가져와 수익률을 비교합니다.")

# --- 사이드바 (사용자 설정) ---
st.sidebar.header("⚙️ 검색 설정")

# 기본 티커 설정 (삼성전자, SK하이닉스, 애플, 테슬라, 엔비디아)
default_tickers = "005930.KS, 000660.KS, AAPL, TSLA, NVDA"
tickers_input = st.sidebar.text_input("티커 입력 (쉼표로 구분)", value=default_tickers)
tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]

# 날짜 설정
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("시작일", datetime.now() - timedelta(days=365))
end_date = col2.date_input("종료일", datetime.now())

# --- 데이터 불러오기 및 시각화 ---
if st.sidebar.button("데이터 조회하기"):
    if not tickers:
        st.warning("최소 한 개 이상의 티커를 입력해 주세요.")
    else:
        with st.spinner("주식 데이터를 불러오는 중입니다..."):
            try:
                # yfinance에서 데이터 다운로드 (종가 기준)
                data = yf.download(tickers, start=start_date, end=end_date)['Close']
                
                # 티커가 하나일 경우 Series로 반환되므로 DataFrame으로 변환
                if isinstance(data, pd.Series):
                    data = data.to_frame()

                if data.empty:
                    st.error("데이터를 불러오지 못했습니다. 티커 명칭과 날짜를 확인해 주세요.")
                else:
                    # 1. 누적 수익률 차트 (가장 중요)
                    st.subheader("🚀 누적 수익률 비교 (기준 시점 = 100)")
                    st.markdown("시작일의 주가를 100으로 환산하여, 어떤 주식이 가장 많이 올랐는지 직관적으로 보여줍니다.")
                    
                    # 결측치(NaN)가 있는 경우, 해당 주식의 첫 거래일을 기준으로 계산되도록 앞방향 채우기 적용
                    normalized_data = (data / data.bfill().iloc[0]) * 100
                    st.line_chart(normalized_data)

                    # 2. 원본 주가 차트
                    st.subheader("📊 종가 추이 (Closing Price)")
                    st.line_chart(data)

                    # 3. 요약 통계 테이블
                    st.subheader("📑 기간 내 요약 통계")
                    
                    # 통계 데이터프레임 생성
                    stats_df = pd.DataFrame({
                        "시작일 종가": data.bfill().iloc[0],
                        "최근 종가": data.ffill().iloc[-1],
                        "최고가": data.max(),
                        "최저가": data.min(),
                        "기간 수익률 (%)": ((data.ffill().iloc[-1] / data.bfill().iloc[0]) - 1) * 100
                    })
                    
                    # 테이블 출력 (소수점 둘째 자리까지 표시)
                    st.dataframe(stats_df.style.format("{:.2f}"))

            except Exception as e:
                st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")
else:
    st.info("👈 왼쪽 사이드바에서 티커와 날짜를 설정한 후 '데이터 조회하기' 버튼을 눌러주세요.")
    st.markdown("""
    **💡 한국 주식 검색 팁:**
    * KOSPI (코스피): 종목코드 뒤에 `.KS`를 붙이세요. (예: 삼성전자 `005930.KS`)
    * KOSDAQ (코스닥): 종목코드 뒤에 `.KQ`를 붙이세요. (예: 에코프로 `086520.KQ`)
    """)
