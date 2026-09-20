"""오프라인 화면 및 네트워크 오류 검사: python check_app.py"""
import io
import json
from unittest.mock import patch
from urllib.error import URLError

from streamlit.testing.v1 import AppTest

payload = {
    "timezone": "Asia/Seoul",
    "current": {"time": "2026-09-20T12:00", "temperature_2m": 25,
                "apparent_temperature": 26, "relative_humidity_2m": 60,
                "wind_speed_10m": 2},
    "daily": {"time": [f"2026-09-{n}" for n in range(20, 27)],
              "temperature_2m_max": [27] * 7, "temperature_2m_min": [18] * 7,
              "precipitation_probability_max": [20] * 7},
}

with patch("urllib.request.urlopen", side_effect=lambda *a, **k: io.BytesIO(json.dumps(payload).encode())):
    app = AppTest.from_file("app.py").run(timeout=30)
    assert not app.exception and not app.error
    assert len(app.metric) == 4
    assert len(app.dataframe[0].value) == 7
    app.selectbox[0].select("부산").run()
    assert not app.exception and "부산" in app.subheader[0].value

with patch("urllib.request.urlopen", side_effect=URLError("offline")):
    app.button[0].click().run()
    assert not app.exception and len(app.error) == 1
    assert len(app.metric) == 0
print("PASS: metrics, forecast, city selection, connection error")
