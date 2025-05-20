import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("📊 서울특별시 연령별 인구 피라미드")

# 루트 기준으로 정확한 경로 지정
df = pd.read_csv("pages/202504_202504_연령별인구현황_남녀구분.csv", encoding="cp949")

df_seoul = df[df['행정구역'].str.contains('서울특별시\\s+\\(')]
male_cols = [col for col in df_seoul.columns if '2025년04월_남_' in col]
female_cols = [col for col in df_seoul.columns if '2025년04월_여_' in col]
ages = [col.split('_')[-1] for col in male_cols]

male_counts = df_seoul.iloc[0][male_cols].astype(str).str.replace(',', '').str.replace('.', '').fillna(0).astype(int) * -1
female_counts = df_seoul.iloc[0][female_cols].astype(str).str.replace(',', '').str.replace('.', '').fillna(0).astype(int)

fig = go.Figure()
fig.add_trace(go.Bar(y=ages, x=male_counts, name='남성', orientation='h', marker=dict(color='blue')))
fig.add_trace(go.Bar(y=ages, x=female_counts, name='여성', orientation='h', marker=dict(color='pink')))
fig.update_layout(
    title='서울특별시 연령별 인구 피라미드',
    barmode='relative',
    xaxis_title='인구수',
    yaxis_title='연령',
    height=1000,
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)
