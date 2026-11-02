# 논문 키워드 워드클라우드 · GitHub Actions

Colab용 `author_keyword_wordcloud_v8.4_citations_fixed.ipynb`의 분석 모듈을 Python 파일로 추출했습니다. 원본의 한국어 Okt·영어 spaCy 분석, 필드별 DF/IDF, 피인용 가중치, Excel 시트, 4종 PNG, 클릭형 HTML과 분리 자산을 유지합니다. Colab 업로드 창과 자동 다운로드 대신 **저장소의 Excel 파일 → 수동 Actions 실행 → 결과 다운로드 + GitHub Pages HTML 보기** 방식입니다. 별도 API 키는 필요하지 않습니다.

## 1. 예제로 먼저 실행하기

1. 이 저장소의 **Actions** 탭을 엽니다. 비활성 상태라면 Actions를 활성화합니다.
2. 왼쪽 **Analyze Excel** → **Run workflow**를 누릅니다.
3. 브랜치 `main`, `input_path`는 `data/example.xlsx`, `mode`는 `sample`, `config_path`는 `config.json` 그대로 실행합니다.
4. `publish_pages`를 켜면 [Pages에서 결과 보기](https://kdh2110.github.io/wordcloud_github/)로 게시됩니다. 실행 페이지의 `deploy` 작업 링크에서도 열 수 있습니다.
5. 실행 완료 후 **Artifacts**의 `wordcloud-sample-실행번호`를 다운로드합니다.
6. 일반 압축 풀기로 열면 `sample/analysis.xlsx`와 `v8_4_sample_results.zip` 등이 있습니다. 비밀번호나 7-Zip은 필요하지 않습니다.


`data/example.xlsx`는 실제 논문이 아닌 한·영문 가상 데이터 6건입니다.

## 2. 내 Excel로 분석하기

1. 저장소의 **Add file → Upload files**에서 `.xlsx` 파일을 올려 커밋합니다. 예를 들어 `data` 폴더에서 `papers.xlsx`를 업로드하면 경로는 `data/papers.xlsx`입니다.
2. 첫 행에 아래 컬럼이 있어야 합니다. 컬럼명을 다르게 쓴 경우 `config.json`의 대응 항목을 수정하세요.

| 컬럼 | 내용 |
| --- | --- |
| `Title` | 제목 |
| `Abstract` | 초록 |
| `Author Keywords` | 저자 키워드, 세미콜론(`;`)으로 구분 |
| `Cited by` | 0 이상의 피인용 횟수. 빈 값은 기본적으로 가중치 1 적용 및 경고 |

선택 컬럼은 `Authors`, `Year`, `Source title`, `DOI`, `Link`, `EID`, `Source`입니다. 기본값은 첫 번째 시트를 읽습니다.

3. **Analyze Excel → Run workflow**에서 `input_path`를 실제 파일 경로로 바꿉니다. 먼저 `sample`로 확인한 뒤 `full`로 실행하세요. sample은 고정 시드로 최대 100건을 고릅니다.
4. 결과는 Artifacts에서 받습니다. 보관 기간은 14일입니다. 실행은 최대 120분이며, 큰 파일은 GitHub 러너의 메모리·시간 및 계정 사용량 제한을 받습니다.

**데이터 공개 범위:** 공개 저장소에 올린 입력 Excel은 저장소에서 공개됩니다. Pages의 HTML/JS에도 화면을 표시하는 데 필요한 제목·초록·키워드 데이터가 담깁니다. ZIP·Excel 파일을 Pages에서 제거해도 화면 데이터 자체가 비공개로 바뀌지는 않습니다. 비공개 자료는 공개 저장소에 올리거나 Pages에 게시하지 마세요.

## GitHub Pages에서 HTML 보기

처음 한 번 저장소 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 선택합니다.

**Actions → Analyze Excel → Run workflow**에서 `publish_pages`를 켜고 실행합니다(기본값: 켬).

- 웹 주소: **https://kdh2110.github.io/wordcloud_github/**
- 클릭형 워드클라우드·검색·정렬 화면과 필요한 JS 자산만 게시합니다.
- Pages에는 ZIP·Excel 파일이나 해당 다운로드 링크를 넣지 않습니다. `/results.zip`, `/analysis.xlsx` 직접 URL로도 받을 수 없습니다.
- 최근 배포에 성공한 화면이 사이트를 교체합니다. `publish_pages`를 끄면 기존 사이트를 변경하지 않습니다.
- 기존 화면의 선택 논문 CSV·워드클라우드 이미지 저장 기능은 유지합니다.
- 분석 실패 시 새 사이트를 게시하지 않습니다. Pages 배포와 결과 다운로드은 분리되어 있습니다.

`Publish Pages example`은 `data/example.xlsx` 변경 시 예제를 게시합니다. 실제 결과를 게시한 뒤 이를 수동 실행하면 예제로 교체되므로 주의하세요.

## ZIP·Excel 받기

**Actions → Analyze Excel → 완료된 실행 → Artifacts**에서 `wordcloud-모드-실행번호`를 다운로드하세요. 일반 압축 풀기로 열 수 있으며 비밀번호는 필요하지 않습니다. 보관 기간은 14일입니다.

공개 저장소에서는 일반 열람자도 Actions Artifacts를 다운로드할 수 있습니다. Pages에는 계속 HTML과 필요한 JS만 게시하며 ZIP·Excel은 올리지 않습니다.

`RESULTS_PASSWORD` Secret은 더 이상 사용하지 않으므로 삭제해도 됩니다. 기존 암호화 파일은 자동 변환되지 않습니다. 새 방식으로 받으려면 **새 Run workflow**로 분석을 실행하세요(이전 실행 재시도는 예전 코드를 사용합니다).

## 3. 분석 설정 바꾸기

GitHub에서 `config.json`을 편집하고 커밋한 후 다시 실행합니다. JSON 문법을 사용하세요(`true`/`false`, 문자열은 큰따옴표).

| 설정 | 기본값 / 용도 |
| --- | --- |
| `CITATION_ALPHA` | `0.5`, 0이면 피인용 가중치 미반영 |
| `MISSING_CITATIONS` | `neutral`, `error`이면 피인용 누락 시 실패 |
| `CITATION_AS_OF` | 피인용 데이터 수집일, 기본 공란 |
| `TITLE_WEIGHT` / `ABSTRACT_WEIGHT` / `KEYWORD_WEIGHT` | `5` / `1` / `5` |
| `WORDCLOUD_MIN_DF` | `2`, 최소 문서 빈도 |
| `WORDCLOUD_MAX_WORDS` | `50` |
| `HTML_INCLUDE_ABSTRACT` | `true`, false이면 HTML 데이터에서 초록만 제외 |
| `WORDCLOUD_WIDTH` / `WORDCLOUD_HEIGHT` | `1200` / `800` |
| `WORDCLOUD_DEFAULT_DIRECTION` | `horizontal`, 또는 `diverse`, `orthogonal` |
| `RANKING_VERSION` | `citation`, 또는 `no_idf`, `idf`, `citation_idf` |

코드의 다른 대문자 설정도 JSON에 추가할 수 있습니다. 집합형 설정은 문자열 배열로 씁니다. 원본 3번 셀의 기본 설정을 `config.json`에 옮겼으며 분석 알고리즘은 변경하지 않았습니다. 원본 최종 Excel에서 누락되던 `오류`·`실행정보` 시트는 자동 실행의 성공 여부 확인을 위해 포함했습니다. 원본 실행 당시 패키지 버전이 제공되지 않아 과거 결과와 바이트 단위 동일성은 보장하지 않습니다.

## 결과 파일

- `analysis.xlsx`: 빈도·DF·IDF·피인용 비교, 오류 및 실행정보 시트
- `wordcloud_no_idf.png`, `wordcloud_idf.png`, `wordcloud_citation.png`, `wordcloud_citation_idf.png`
- `paper_explorer.html` + `paper_explorer_assets/data.js`, `images.js`: 검색·정렬·표현 클릭·논문 연결·이미지 다운로드
- `v8_4_<mode>_results.zip`: 위 파일의 묶음

다운로드한 결과 안에는 `sample/` 또는 `full/` 원본 결과 폴더도 있습니다. `sample/`만 따로 받았다면 그 안의 HTML을 열어도 됩니다. 분석 오류가 기록되거나 필수 이미지가 없으면 Actions는 실패로 표시됩니다. 생성된 진단 결과는 실패한 실행에서도 업로드합니다(설치 단계 실패 등으로 결과가 없으면 업로드 없음).

## 로컬 실행 / 개발

Python 3.12와 Java 17 이상, 나눔고딕이 필요합니다. Ubuntu에서는:

```bash
sudo apt-get update
sudo apt-get install -y default-jre-headless fonts-nanum
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run_analysis.py data/example.xlsx --mode sample
python -m unittest discover -s tests -v
```

다른 시스템에서는 `--font-path /path/to/korean-font.ttf`로 폰트를 지정하세요. 테스트는 `TEST_FONT_PATH` 환경변수로 폰트 경로를 지정할 수 있습니다.

```bash
python run_analysis.py data/papers.xlsx --mode full --config config.json \
  --output-dir output/run2 --cache-dir nlp_cache
```

기존 결과 혼합을 방지하려고 비어 있지 않은 출력 모드 폴더는 거부합니다. 재실행은 `--output-dir`을 새 경로로 지정하세요. 로컬 `nlp_cache`는 재사용됩니다. Actions 실행 간에는 원문이 담긴 형태소 캐시를 따로 업로드/공유하지 않습니다.

`Tests` 워크플로는 push/PR마다 가상 Excel로 실제 영어·한국어 NLP, sample/full, 피인용 점수, 캐시 재사용, 4종 점수 × 3방향 이미지, Excel/HTML/ZIP과 프로젝트 하위 경로에서 Pages 자산의 HTTP 200, ZIP·Excel의 HTTP 404, 기존 화면을 보존하는 마이그레이션를 검사합니다. 수동 분석에는 `google.colab`, 브라우저 입력창, 노트북 실행기가 필요하지 않습니다.

문제 발생 시 Actions의 `Analyze` 로그와 Excel의 `오류` 시트를 확인하세요. 컬럼 오류는 Excel 헤더/설정, 이미지 누락은 `WORDCLOUD_MIN_DF`와 필터를 확인하세요. 원본의 기본 최소 DF=2에서는 여러 논문에 반복되는 용어가 필요합니다. 입력이 한 건뿐이라면 해당 값을 1로 낮춰 테스트할 수 있습니다.
