# 코레일 × Cursor — 60분 실습 패키지

**목표**: ChatGPT 등에서 개발 설계서를 `.md`로 작성 → Cursor가 설계서를 읽고 코딩 → Streamlit 대시보드 실행 → 데이터와 결과를 검증.

## 1. 폴더 구성

```text
korail/
├─ README_시작하기.md
├─ 01_Passenger/
│  ├─ 개발설계서.md
│  ├─ 최소기능_백업설계서.md
│  └─ passenger.csv                  
└─ 02_PowerQuality/
   ├─ 개발설계서.md
   ├─ 최소기능_백업설계서.md
   └─ power_quality.csv              
```

## 2. 실습 전에

- Python 3.13 이상, Cursor 설치. Streamlit 앱은 로컬 브라우저에서 실행됩니다.
- Windows PowerShell / CMD 터미널에서 다음 명령 실행:

```powershell
python -m pip install streamlit pandas plotly
python -c "import streamlit, pandas, plotly; print('Ready')"
```

- 압축파일 전체를 압축 해제하고, **Cursor에서 `01_Passenger` 폴더 하나만 먼저 열어 시작**합니다.
- Internet 연결은 필요한 Python 패키지 설치 시에만 필요하며, **데이터 분석 앱 자체는 외부 API를 쓰지 않습니다.**
- Cursor 무료 AI 요청 한도는 시기/계정에 따라 달라질 수 있는 점 참고하세요.

## 3. 실습 1 

1. Cursor의 **File → Open Folder**로 `01_Passenger` 선택.
2. Agent 대화에 아래 문구 입력 (파일 첨부 메뉴 또는 `@` 입력 후 해당 파일을 선택해도 됨):

```text
@개발설계서.md 파일을 먼저 읽어줘. 같은 폴더의 passenger.csv로 app.py와
requirements.txt를 작성해줘. 요구사항 중 핵심 기능부터 개발하고,
검증값(전체 합계)이 일치하는지 확인한 후 실행 방법을 알려줘.
```

3. 코드 생성이 끝나면 터미널에서:

```powershell
python -m streamlit run app.py
```

4. 브라우저에서 필터를 바꾸며 KPI/그래프 변화를 확인.
5. 예상보다 오래 걸리면 `@최소기능_백업설계서.md`를 대신 지정.

## 4. 실습 2 

1. Cursor에서 `02_PowerQuality` 폴더 열기.
2. Agent에 아래 문구 입력:

```text
@개발설계서.md 내용을 읽어줘. power_quality.csv를 이용하여
전차선 전류·전압 시계열을 시각화하고 500A를 초과하는 지점을
붉게 표시하는 Streamlit app.py를 작성해줘.
```

3. 실행 명령은 동일합니다. **20:31, 20:41 관측값**이 그래프에 나타나는지 확인하세요.

## 5. 정확성 확인 기준

- **승하차**: CSV **1,326행**, 월별 열차 조합 **102개**. 전체 승차 **75,150**, 하차 **75,372**, 합계 **150,522**.
- **전력품질**: CSV **60행**, 500 A 초과 **2개**, 최대 전류 **10,903.695 A**.
- CSV는 UTF-8 BOM 인코딩으로 저장했습니다. Excel에서 한글 깨짐을 줄이고, `pandas.read_csv(..., encoding='utf-8-sig')`로 읽을 수 있습니다.

