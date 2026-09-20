# 도시 날씨 웹앱

Open-Meteo 공개 API를 사용하는 Streamlit 웹앱입니다. API 키 없이 실행할 수 있습니다.

## 실행 (PowerShell)

```powershell
cd C:\Users\user\Documents\public_weather_app
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

브라우저에서 http://localhost:8501 에 접속합니다.

## 기능

- 국내외 10개 도시 선택
- 현재 기온, 체감 온도, 습도, 풍속
- 7일 최고·최저 기온 그래프 및 강수 확률 표
- CSV 다운로드와 원본 JSON 확인
- 10분 캐시, 수동 새로고침, 네트워크·응답 오류 처리

도시를 추가하려면 app.py의 CITIES에 도시 이름과 위도·경도를 추가하세요.
API 호출에는 인터넷 연결이 필요합니다. 현재 날씨는 모델 기반 데이터입니다.

API 문서: https://open-meteo.com/en/docs
Streamlit 문서: https://docs.streamlit.io/
무료 API의 상업적 사용과 호출 한도는 공급자의 최신 이용약관을 확인하세요.
