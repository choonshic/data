import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/source-data/big-mac-source-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# 사용자 입력
st.title("🍔 Big Mac Index 시각화")
year = st.selectbox("연도 선택", sorted(df['date'].unique(), reverse=True))
base_country = st.selectbox("기준 국가 선택", sorted(df['name'].unique()))

# 선택한 연도와 기준 국가에 해당하는 데이터 필터링
df_year = df[df['date'] == year]
df_base = df_year[df_year['name'] == base_country]

if not df_base.empty:
    base_price = df_base['dollar_price'].values[0]
    df_year = df_year.copy()
    df_year['price_ratio'] = df_year['dollar_price'] / base_price
    df_year['valuation'] = (df_year['price_ratio'] - 1) * 100

    # 시각화
    fig = px.bar(df_year.sort_values('valuation'), x='name', y='valuation',
                 labels={'name': '국가', 'valuation': '가격 차이 (%)'},
                 title=f"{year}년 Big Mac 가격 비교 (기준: {base_country})")
    st.plotly_chart(fig)
else:
    st.warning(f"{base_country}에 대한 데이터가 없습니다.")
