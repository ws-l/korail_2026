"""실행: python -m streamlit run app.py"""
import json
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd
import streamlit as st

st.set_page_config(page_title="도시 날씨", page_icon="🌤️", layout="wide")

CITIES = {
    "서울": (37.5665, 126.9780), "부산": (35.1796, 129.0756),
    "인천": (37.4563, 126.7052), "대구": (35.8714, 128.6014),
    "대전": (36.3504, 127.3845), "광주": (35.1595, 126.8526),
    "제주": (33.4996, 126.5312), "도쿄": (35.6762, 139.6503),
    "런던": (51.5074, -0.1278), "뉴욕": (40.7128, -74.0060),
}


@st.cache_data(ttl=600, show_spinner=False)
def fetch_weather(latitude, longitude):
    params = {
        "latitude": latitude, "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto", "forecast_days": 7, "wind_speed_unit": "ms",
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)
    with urlopen(url, timeout=15) as response:
        data = json.load(response)
    if data.get("error"):
        raise ValueError(data.get("reason", "API 응답 오류"))
    if not data.get("current") or not data.get("daily", {}).get("time"):
        raise ValueError("날씨 데이터가 비어 있습니다.")
    return data, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def metric_value(value, unit):
    return "정보 없음" if value is None else f"{value} {unit}"


st.title("🌤️ 도시 날씨")
st.write("오늘의 날씨와 앞으로 7일의 예보를 확인하세요.")
with st.sidebar:
    st.header("조회 설정")
    city = st.selectbox("도시", list(CITIES))
    if st.button("새로고침", width="stretch"):
        fetch_weather.clear()
    st.caption("조회 결과는 10분간 캐시됩니다. 새로고침하면 다시 조회합니다.")

try:
    with st.spinner("날씨를 가져오는 중입니다…"):
        data, fetched_at = fetch_weather(*CITIES[city])
    current = data["current"]
    daily = data["daily"]
    forecast = pd.DataFrame({
        "날짜": pd.to_datetime(daily["time"]),
        "최고 기온 (°C)": daily["temperature_2m_max"],
        "최저 기온 (°C)": daily["temperature_2m_min"],
        "강수 확률 (%)": daily["precipitation_probability_max"],
    })
except HTTPError as exc:
    st.error(f"날씨 서버가 요청을 처리하지 못했습니다 (HTTP {exc.code}). 잠시 후 새로고침해 주세요.")
    st.stop()
except (URLError, TimeoutError, OSError):
    st.error("날씨 서버에 연결할 수 없습니다. 인터넷 연결을 확인하고 새로고침해 주세요.")
    st.stop()
except (ValueError, KeyError, TypeError):
    st.error("날씨 응답 형식이 올바르지 않거나 데이터가 없습니다. 잠시 후 다시 시도해 주세요.")
    st.stop()

st.subheader(f"{city} · 현재 날씨")
st.caption(f"기준 시각: {current['time'].replace('T', ' ')} · {data.get('timezone', '현지 시간')} | 조회 시각: {fetched_at}")
for column, label, key, unit in zip(
    st.columns(4), ["기온", "체감 온도", "습도", "풍속"],
    ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "wind_speed_10m"],
    ["°C", "°C", "%", "m/s"],
):
    column.metric(label, metric_value(current.get(key), unit))

st.subheader("7일 예보")
st.line_chart(forecast.set_index("날짜")[["최고 기온 (°C)", "최저 기온 (°C)"]])
st.caption("기온 단위: °C · 날짜는 선택한 도시의 현지 시간 기준입니다.")
table = forecast.copy()
table["날짜"] = table["날짜"].dt.strftime("%Y-%m-%d")
st.dataframe(table, hide_index=True, width="stretch")
st.download_button("예보 CSV 다운로드", table.to_csv(index=False).encode("utf-8-sig"),
                   file_name=f"{city}_7일_예보.csv", mime="text/csv")
with st.expander("API 원본 데이터 보기"):
    st.json(data)
st.caption("출처: [Open-Meteo](https://open-meteo.com/) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · 날씨 모델 기반 데이터")
