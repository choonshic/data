import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/source-data/big-mac-source-data.csv"
    df = pd.read_csv(url)
    return df

df = load_data()
df['dollar_price'] = df['local_price'] / df['dollar_ex']
df = df[df['dollar_price'] < 20]
st.title("🍔 Big Mac Index 물가 비교기")

# ---------------------------------------
# 1️⃣ 한국의 가격 변화 추이 (현지통화 기준)
# ---------------------------------------
south_korea = df[df['name'] == "South Korea"].copy()
south_korea = south_korea[['date', 'local_price']].dropna().sort_values('date')

st.subheader("📈 한국의 Big Mac 가격 변화 추이 (현지 통화 기준)")
fig_kor = px.line(
    south_korea,
    x='date',
    y='local_price',
    markers=True,
    title="South Korea Big Mac 가격 추이 (Local Currency)",
    labels={'date': '연도', 'local_price': '가격 (현지 통화)'}
)
fig_kor.update_layout(height=500)
st.plotly_chart(fig_kor, use_container_width=True)

# ---------------------------------------
# 2️⃣ 연도 및 기준국가 선택
# ---------------------------------------
st.subheader("📅 연도 및 기준 국가 선택")
year = st.selectbox("연도 선택", sorted(df['date'].unique(), reverse=True))
default_country = "South Korea" if "South Korea" in df['name'].unique() else sorted(df['name'].unique())[0]
base_country = st.selectbox("기준 국가 선택", sorted(df['name'].unique()), index=sorted(df['name'].unique()).index(default_country))

# 해당 연도 데이터만 추출
df_year = df[df['date'] == year].copy()
df_year = df_year[['name', 'dollar_price']].dropna()

# 기준국가 비교 시각화
df_base = df_year[df_year['name'] == base_country]
if not df_base.empty:
    base_price = df_base['dollar_price'].values[0]
    df_year['price_ratio'] = df_year['dollar_price'] / base_price
    df_year['valuation'] = (df_year['price_ratio'] - 1) * 100

    st.subheader(f"🌍 {year}년 Big Mac 가격 비교 (기준: {base_country})")
    fig = px.bar(
        df_year.sort_values('valuation'),
        x='name',
        y='valuation',
        color='valuation',
        color_continuous_scale='RdBu',
        labels={'name': '국가', 'valuation': '기준 대비 가격 차이 (%)'},
        height=700
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"{base_country}에 대한 데이터가 없습니다.")

# ---------------------------------------
# 3️⃣ 상위 10개 / 하위 10개 표
# ---------------------------------------
top10_expensive = df_year.sort_values(by='dollar_price', ascending=False).head(10)
top10_cheap = df_year.sort_values(by='dollar_price').head(10)

st.subheader(f"💸 {year}년 가장 비싼 국가 TOP 10")
st.dataframe(top10_expensive.set_index('name').rename(columns={'dollar_price': 'Big Mac (USD)'}))

st.subheader(f"🪙 {year}년 가장 저렴한 국가 TOP 10")
st.dataframe(top10_cheap.set_index('name').rename(columns={'dollar_price': 'Big Mac (USD)'}))
