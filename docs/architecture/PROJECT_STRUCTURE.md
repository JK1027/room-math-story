# 프로젝트 아키텍처 및 설계 가이드라인 (PROJECT_STRUCTURE.md)

이 문서는 수학 방탈출 게임 스토리 빌드/배포 프로젝트의 전체 디렉토리 구조, 데이터 흐름 계약, 그리고 개발팀 온보딩 가이드라인을 정의합니다.

---

## 빌드 파이프라인 원칙

이 프로젝트는 다음 단일 책임 원칙(SRP)을 따릅니다.

1. **`build_story.py` 가 유일한 오케스트레이터** — 모든 빌드는 이 파일 하나를 통해서만 시작됩니다.
2. **각 하위 스크립트는 자신의 역할만 수행** — `build_pdf.py`는 PDF만 생성하고, 생성기 호출 등 다른 역할을 겸하지 않습니다.
3. **Validation Gate** — 검증(Validate) 단계가 실패하면 HTML/PDF 빌드는 실행되지 않습니다.

---

## 데이터 파이프라인 흐름 (E2E Data Flow)

```text
[Authoring Sources]
  stories/gradeX/*_script.md      ← 스토리 대본 (유일 원본)
  quiz_data/gradeX/*.yaml          ← 퀴즈 문항/이벤트 데이터 (유일 원본)
         │
         ▼
  [1] storyboard_generator.py      ← 두 원본을 결합하여 Markdown 합성
         │
         ▼
  storyboards/generated/gradeX/*.md
         │
         ▼
  [2] validate_story.py            ← YAML 스키마 + 스토리보드 정적 심사
         │
         ├── FAIL → 빌드 중단 (HTML/PDF 생성 안 함)
         │
         ▼
  [3] update_app_*.py              ← HTML 클라이언트 컴파일
         │
         ▼
  [4] build_pdf.py                 ← PDF 대본집 컴파일
         │
         ▼
  .build/build_report.yaml         ← 빌드 통계 자동 기록
```

---

## 작성 원본 (Canonical Authoring Sources)

스토리 데이터의 원본(Source of Truth)은 딱 두 가지입니다.

| 원본 | 경로 | 역할 |
| :--- | :--- | :--- |
| 스토리 대본 | `stories/gradeX/*_script.md` | 인트로/아웃트로, 각 문제별 지문 대사 |
| 퀴즈 데이터 | `quiz_data/gradeX/*.yaml` | 이미지 매핑, 정답 조건식, 이벤트 메타데이터 |

> **주의**: `storyboards/generated/` 내의 파일은 파생 데이터입니다. 직접 편집하지 마세요.
> 대본이나 YAML을 수정한 뒤 빌드를 실행하면 자동으로 재생성됩니다.

---

## 빌드 명령어

### 특정 단원만 빌드

```bash
python scripts/build/build_story.py --unit m1_02
```

→ `Generate → Validate → HTML → PDF` 4단계를 해당 단원에 대해서만 실행합니다.

### 전체 23개 단원 빌드

```bash
python scripts/build/build_story.py
```

→ 사전 전체 검증 후, 23개 단원을 순차 E2E 빌드합니다.

### 실시간 감시 (대본 수정 시 자동 빌드)

```bash
python scripts/build/watch_story.py
```

→ `stories/` 또는 `quiz_data/` 파일 저장을 감지하면 해당 단원을 즉시 자동 빌드합니다.

---

## 데이터 계약 (Data Contract)

| 산출물 종류 | 위치 | 포맷 | 필수 포함 요소 |
| :--- | :--- | :--- | :--- |
| **Grade Metadata** | `stories/gradeX/metadata.yaml` | YAML | 학년, 타이틀, 빌더, 캐릭터(영웅/조력자/빌런) |
| **Story Script** | `stories/gradeX/*_script.md` | Markdown | 캐릭터 대사, 지문, 이벤트 씬 |
| **Quiz Data** | `quiz_data/gradeX/*.yaml` | YAML | 이미지 매핑, 정답 조건식, 이벤트 메타데이터 |
| **Generated Storyboard** | `storyboards/generated/gradeX/*.md` | Markdown | [파생 데이터] 직접 편집 금지 |
| **Generated HTML** | `apps/*.html` | HTML5 | 퀴즈 풀이 클라이언트, 수식 렌더링 |
| **PDF Storybook** | `storyboards/generated/gradeX/*.pdf` | A4 Landscape PDF | HUD 헤더 테마 적용 |
| **Build Report** | `.build/build_report.yaml` | YAML | [자동 생성] 빌드 통계 — 직접 편집 금지 |

---

## 디렉토리 구조 (Directory Layers)

```text
room-math-story/
├── .build/                       # [자동 생성] 빌드 리포트 및 캐시 (Git 미포함)
│   └── build_report.yaml
├── apps/                         # 빌드 완료된 HTML5 클라이언트 게임 배포본
│   └── assets/                   # 단원별 이미지/사운드 에셋 리소스
├── gas/                          # GAS 서버 배포용 폴더
├── storyboards/
│   └── generated/                # [파생 데이터] 직접 편집 금지
│       ├── grade1/
│       ├── grade2/
│       └── grade3/
├── stories/                      # [원본] 대본집 및 학년 메타데이터
│   ├── grade1/
│   │   ├── metadata.yaml         # 학년별 캐릭터/유닛 메타데이터
│   │   └── *_script.md
│   ├── grade2/
│   └── grade3/
├── quiz_data/                    # [원본] 퀴즈 문항/이벤트 YAML 데이터
│   ├── grade1/
│   ├── grade2/
│   └── grade3/
├── docs/
│   ├── architecture/
│   │   └── PROJECT_STRUCTURE.md  # 본 가이드라인 (사람이 작성)
│   └── schemas/
│       └── quiz_data.schema.yaml # quiz_data YAML 공식 스키마 명세
├── scripts/
│   ├── build/                    # 빌드 및 E2E 오케스트레이션
│   │   ├── build_story.py        # [유일 오케스트레이터] Programmatic API + CLI
│   │   ├── build_pdf.py          # [순수 PDF 컴파일러] PDF만 생성
│   │   └── watch_story.py        # [실시간 감시] 파일 변경 시 build_unit() 자동 호출
│   ├── builders/                 # 학년별 HTML 클라이언트 컴파일러 (update_app_*.py)
│   ├── tools/
│   │   └── story/
│   │       ├── storyboard_generator.py  # Authoring Sources → Markdown 합성기
│   │       └── validate_story.py        # YAML 스키마 + 스토리보드 정적 검증기
│   ├── migration/                # 마이그레이션 스크립트 (레거시 이주용)
│   └── config/                   # 전역 경로 및 상수 설정 패키지
│       ├── paths.py
│       ├── constants.py
│       └── settings.py
├── archive/                      # 보존용 보관소 (과거 릴리즈/기획 드래프트)
└── scratch/                      # 임시 테스트 폴더
```

---

## 개발자 진입 가이드 (Onboarding Guide)

### 스토리 수정 후 확인하는 방법

1. `stories/gradeX/*_script.md` 또는 `quiz_data/gradeX/*.yaml` 을 수정합니다.
2. 아래 명령을 실행합니다:
   ```bash
   python scripts/build/build_story.py --unit m1_02
   ```
3. `storyboards/generated/grade1/m1_02_storyboard.pdf` 를 열어 결과를 확인합니다.

> 실시간으로 확인하고 싶다면 `watch_story.py`를 백그라운드에서 켜두세요.
> 파일을 저장하는 순간 자동으로 PDF가 재생성됩니다.

### GAS 서버 배포

```bash
# 특정 학년만
python scripts/deploy/deploy_gas.py --target grade1

# 전체 학년
python scripts/deploy/deploy_gas.py --target all
```
