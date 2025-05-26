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

# -------------------------------
# 1️⃣ 가장 비싼/싼 나라 10개 출력
# -------------------------------
df_year = df[df['date'] == year].copy()
df_year = df_year[['name', 'dollar_price']].dropna()

top10_expensive = df_year.sort_values(by='dollar_price', ascending=False).head(10)
top10_cheap = df_year.sort_values(by='dollar_price').head(10)

st.subheader(f"💸 {year}년 가장 비싼 국가 TOP 10")
st.dataframe(top10_expensive.set_index('name').rename(columns={'dollar_price': 'Big Mac (USD)'}))

st.subheader(f"🪙 {year}년 가장 저렴한 국가 TOP 10")
st.dataframe(top10_cheap.set_index('name').rename(columns={'dollar_price': 'Big Mac (USD)'}))

# -------------------------------
# 2️⃣ 한국의 가격 추이 시각화
# -------------------------------
# 2️⃣ 한국의 가격 추이 시각화 (local_price로 변경)
south_korea = df[df['name'] == "South Korea"].copy()
south_korea = south_korea[['date', 'local_price']].dropna()
south_korea = south_korea.sort_values('date')

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


# -------------------------------
# 기준 국가 대비 다른 국가 비교
# -------------------------------
df_base = df_year[df_year['name'] == base_country]

if not df_base.empty:
    base_price = df_base['dollar_price'].values[0]
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
        height=700
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.subheader(f"🌍 {year}년 Big Mac 가격 비교")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"{base_country}에 대한 데이터가 없습니다.")
