import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/source-data/big-mac-source-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# dollar_price 계산
df['dollar_price'] = df['local_price'] / df['dollar_ex']

# 사용자 UI
st.title("🍔 Big Mac Index 물가 비교기")
st.markdown("🔍 국가별 Big Mac 가격을 USD 기준으로 비교합니다.")

# 사용자 선택
year = st.selectbox("📅 연도 선택", sorted(df['date'].unique(), reverse=True))

# 기준 국가를 South Korea로 기본 설정
default_country = "South Korea" if "South Korea" in df['name'].unique() else sorted(df['name'].unique())[0]
base_country = st.selectbox("📌 기준 국가 선택", sorted(df['name'].unique()), index=sorted(df['name'].unique()).index(default_country))

# 데이터 필터링
df_year = df[df['date'] == year]
df_base = df_year[df_year['name'] == base_country]

# 시각화
if not df_base.empty:
    base_price = df_base['dollar_price'].values[0]
    df_year = df_year.copy()
    df_year['price_ratio'] = df_year['dollar_price'] / base_price
    df_year['valuation'] = (df_year['price_ratio'] - 1) * 100

    fig = px.bar(
        df_year.sort_values('valuation'),
        x='name',
        y='valuation',
        color='valuation',
        color_continuous_scale='RdBu',
        labels={'name': '국가', 'valuation': '기준 대비 가격 차이 (%)'},
        title=f"{year}년 Big Mac USD 가격 비교 (기준: {base_country})",
        height=700  # 그래프 크기 키움
    )
    fig.update_layout(xaxis_tickangle=-45)  # 국가 이름이 겹치지 않게 회전
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("해당 국가 데이터가 없습니다.")
