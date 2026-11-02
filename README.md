# 논문 키워드 워드클라우드 · GitHub Actions

Colab용 `author_keyword_wordcloud_v8.4_citations_fixed.ipynb`의 분석 모듈을 Python 파일로 추출했습니다. 원본의 한국어 Okt·영어 spaCy 분석, 필드별 DF/IDF, 피인용 가중치, Excel 시트, 4종 PNG, 클릭형 HTML과 분리 자산을 유지합니다. Colab 업로드 창과 자동 다운로드 대신 **저장소의 Excel 파일 → 수동 Actions 실행 → 결과 다운로드 + GitHub Pages HTML 보기** 방식입니다. 별도 API 키는 필요하지 않습니다.

## 1. 예제로 먼저 실행하기

1. 이 저장소의 **Actions** 탭을 엽니다. 비활성 상태라면 Actions를 활성화합니다.
2. 왼쪽 **Analyze Excel** → **Run workflow**를 누릅니다.
3. 브랜치 `main`, `input_path`는 `data/example.xlsx`, `mode`는 `sample`, `config_path`는 `config.json` 그대로 실행합니다.
4. `publish_pages`를 켜면 실행마다 새 결과 주소가 생깁니다. 완료된 실행의 **Summary → deploy → 이용자에게 전달할 결과 링크**에서 주소를 복사하세요. `github-pages` 배포 링크에서도 해당 결과를 열 수 있습니다.
5. 실행 완료 후 **Artifacts**의 `wordcloud-sample-실행번호`를 다운로드합니다.
6. 한 번 압축을 풀면 `analysis.xlsx`, `paper_explorer.html`, 이미지와 자산 폴더가 바로 나옵니다. 중복된 내부 ZIP은 없습니다. 비밀번호나 7-Zip은 필요하지 않습니다.


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

## 여러 이용자에게 서로 다른 결과 링크 전달하기

분석 코드는 `main`에 하나만 둡니다. 관리자에게 신청한 이용자마다 다음 작업을 반복하세요.

1. 이용자별 Excel을 다른 파일명으로 저장소에 업로드합니다. 예: `data/request-a.xlsx`, `data/request-b.xlsx`.
2. **Actions → Analyze Excel → Run workflow**에서 해당 `input_path`, `sample`/`full`, 필요하면 별도의 `config_path`를 지정합니다. `publish_pages`를 켭니다.
3. 실행 완료 후 **Summary**에서 `deploy` 작업의 **이용자에게 전달할 결과 링크**를 복사합니다.
4. 해당 이용자에게 이 링크를 직접 전달합니다. 메일·문자 자동 발송이나 신청 접수 웹폼은 포함하지 않습니다.

주소 예시: `https://kdh2110.github.io/wordcloud_github/results/32자리임의ID/`

- 실행마다 새 ID가 생깁니다. 같은 파일을 다시 실행해도 새 주소가 생성됩니다.
- 결과 A를 만든 뒤 B를 만들어도 A의 URL·HTML·데이터를 유지합니다. 최초 전환 시 기존 루트 주소의 화면도 보존합니다.
- 공개 홈페이지에 다른 이용자의 결과 목록을 만들지 않습니다. 하지만 Pages와 `pages-data` 브랜치는 공개되므로 **고유 링크는 접근 권한이나 비공개 보장이 아닙니다.** 화면 데이터도 공개입니다.
- ZIP·Excel은 Pages에 게시하지 않습니다. 기존 선택 논문 CSV·워드클라우드 이미지 저장 기능은 유지합니다.
- `publish_pages`를 끄면 다운로드용 결과만 만들고, 기존 링크를 변경하지 않습니다.
- Pages 최초 설정은 **Settings → Pages → Source: GitHub Actions**입니다.

웹 결과는 `pages-data` 보관 브랜치의 `results/<ID>/`에 누적됩니다. 분석 코드 사본은 이 브랜치에 저장하지 않습니다. Actions Artifacts 보관 기간이 끝나도 결과 링크는 남습니다. 이 브랜치를 삭제하거나 강제로 덮어쓰지 마세요. Pages의 사이트 용량 제한(1GB)을 고려해 오래된 결과의 보관 정책을 별도로 정해야 합니다.

동시 실행은 Git 업로드 충돌 시 최신 보관 브랜치를 다시 읽어 병합합니다. 배포는 누적된 최신 전체 사이트를 읽습니다. 많은 실행이 겹치면 GitHub의 배포 대기 작업 교체 때문에 일부 실행의 `deploy`가 취소될 수 있지만, 이미 보관된 결과는 다음 성공한 전체 배포에 포함됩니다. 배포 실패/취소 시 `pages-data`에 보관된 결과는 삭제되지 않습니다. 필요하면 배포 작업을 다시 실행하세요.

`Publish Pages example`은 예제 파일/해당 워크플로 변경 시와 수동 실행 시 새 예제 링크를 만듭니다. 실제 이용자의 기존 링크는 교체하지 않습니다.

## ZIP·Excel 받기

**Actions → Analyze Excel → 완료된 실행 → Artifacts**에서 `wordcloud-모드-실행번호`를 다운로드하세요. 일반 압축 풀기로 열 수 있으며 비밀번호는 필요하지 않습니다. 보관 기간은 14일입니다.

`github-pages`와 `new-result-site`는 배포 과정에서만 사용하는 임시 파일입니다. 성공한 실행이 끝나면 자동 삭제합니다. 다운로드 목록에는 분석 결과 `wordcloud-…`를 남깁니다. 실행 중이거나 실패한 작업의 임시 파일은 완료/재시도를 위해 보존합니다. 게시된 사이트와 기존 이용자 링크는 삭제하지 않습니다.

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
- `v8_4_<mode>_results.zip`: 로컬 실행용 묶음. Actions 다운로드에는 중복을 피하려고 포함하지 않습니다.

Actions 다운로드는 결과 파일만 담습니다. 한 번 압축을 풀고 `paper_explorer.html`을 열면 됩니다. 로컬 실행에서는 결과가 `output/sample/` 또는 `output/full/`에 저장되고 별도 ZIP도 생성됩니다. 분석 오류가 기록되거나 필수 이미지가 없으면 Actions는 실패로 표시됩니다. 생성된 진단 결과는 실패한 실행에서도 업로드합니다(설치 단계 실패 등으로 결과가 없으면 업로드 없음).

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
