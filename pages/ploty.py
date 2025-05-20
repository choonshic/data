import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울 인구 피라미드", layout="wide")
st.title("📊 서울특별시 연령별 인구 피라미드 (2025년 4월 기준)")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202504_202504_연령별인구현황_남녀구분.csv", encoding="cp949")
    return df

df = load_data()

# 서울특별시 전체만 필터링
df_seoul = df[df['행정구역'].str.contains('서울특별시\s+\\(')]

# 연령대 컬럼
male_cols = [col for col in df_seoul.columns if '2025년04월_남_' in col]
female_cols = [col for col in df_seoul.columns if '2025년04월_여_' in col]
ages = [col.split('_')[-1] for col in male_cols]

# 남성, 여성 인구 데이터 처리
male_counts = df_seoul.iloc[0][male_cols].astype(str).str.replace(',', '').str.replace('.', '').fillna(0).astype(int) * -1
female_counts = df_seoul.iloc[0][female_cols].astype(str).str.replace(',', '').str.replace('.', '').fillna(0).astype(int)

# Plotly 피라미드 그래프 생성
fig = go.Figure()

fig.add_trace(go.Bar(
    y=ages,
    x=male_counts,
    name='남성',
    orientation='h',
    marker=dict(color='blue')
))

fig.add_trace(go.Bar(
    y=ages,
    x=female_counts,
    name='여성',
    orientation='h',
    marker=dict(color='pink')
))

fig.update_layout(
    title='서울특별시 연령별 인구 피라미드',
    barmode='relative',
    xaxis_title='인구수',
    yaxis_title='연령',
    template='plotly_white',
    height=1000
)

st.plotly_chart(fig, use_container_width=True)
