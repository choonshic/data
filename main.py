import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="미국 휴양지 지도", layout="wide")

# 제목
st.title("🇺🇸 미국 주요 휴양지 지도")
st.markdown("미국의 대표적인 휴양지를 지도에서 살펴보세요!")

# 휴양지 데이터
resorts = pd.DataFrame([
    {"name": "Maui", "state": "Hawaii", "lat": 20.7984, "lon": -156.3319, "desc": "하와이에서 가장 인기 있는 섬 중 하나"},
    {"name": "Key West", "state": "Florida", "lat": 24.5551, "lon": -81.7800, "desc": "플로리다 최남단의 휴양 도시"},
    {"name": "Lake Tahoe", "state": "California", "lat": 39.0968, "lon": -120.0324, "desc": "캘리포니아와 네바다에 걸친 산악 호수"},
    {"name": "Aspen", "state": "Colorado", "lat": 39.1911, "lon": -106.8175, "desc": "고급 스키 리조트로 유명한 도시"},
    {"name": "Myrtle Beach", "state": "South Carolina", "lat": 33.6891, "lon": -78.8867, "desc": "가족 단위 여행에 적합한 해변"},
    {"name": "Napa Valley", "state": "California", "lat": 38.5025, "lon": -122.2654, "desc": "와인으로 유명한 지역"},
])

# Folium 지도 생성
map_center = [37.0902, -95.7129]  # 미국 중심
m = folium.Map(location=map_center, zoom_start=4)

# 마커 추가
for _, row in resorts.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"<b>{row['name']}</b><br>{row['state']}<br>{row['desc']}",
        tooltip=row['name'],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Streamlit에 Folium 지도 표시
st_data = st_folium(m, width=1000, height=600)

