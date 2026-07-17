# 프로젝트 아키텍처 및 설계 가이드라인 (PROJECT_STRUCTURE.md)

이 문서는 수학 방탈출 게임 스토리 빌드/배포 프로젝트의 전체 디렉토리 구조, 데이터 흐름 계약, 그리고 개발팀 온보딩 가이드라인을 정의합니다.

---

## 🧭 데이터 파이프라인 흐름 (E2E Data Flow)

```mermaid
graph TD
    M["단일 메타데이터 (stories/gradeX/metadata.yaml)"]
    A["대본 원본 (stories/gradeX/*_script.md)"]
    M -.->|캐릭터/유닛 매핑 참조| A
    
    A -->|1. story_builder.py| B["스토리보드 원본 (storyboards/gradeX/*_storyboard.md)"]
    B -->|2. build_pdf.py| C["배포용 PDF 스토리북 (storyboards/gradeX/*.pdf)"]
    B -->|3. update_app_*.py (Builders)| D["클라이언트용 HTML (apps/*.html)"]
    D -->|4. deploy_gas.py| E["Google Apps Script (gas/*)"]
    E -->|5. QA 확인| F["Web Browser (게임 구동)"]
    
    B -.->|검증 도구: validate_story.py| B
    M -.->|교차 검증 규칙| B
```

---

## 📝 데이터 계약 (Data Contract)

| 산출물 종류 | 위치 | 포맷 스펙 (Format Contract) | 필수 포함 요소 및 스키마 |
| :--- | :--- | :--- | :--- |
| **Grade Metadata** | `stories/gradeX/metadata.yaml` | `YAML` | **[Source of Truth]** 학년, 타이틀, 빌더, 캐릭터(영웅, 조력자, 빌런) 정보 중앙 통제 |
| **Story Script** | `stories/gradeX/` | `Markdown (.md)` | 캐릭터 대사, 지문, 퀴즈 정보, 이벤트 지시어 |
| **Storyboard** | `storyboards/gradeX/` | `Markdown + YAML (.md)` | 이미지 매핑 정보, 질문/선택지/정답 조건, EVENT 진행 데이터 |
| **Generated HTML** | `apps/` | `HTML5 (CSS/JS Embedded)` | 퀴즈 풀이용 가상 콘솔 화면, 상태 감지 락다운, 수식 렌더링 |
| **PDF Storybook** | `storyboards/gradeX/` | `Landscape A4 PDF` | A4 가로 인쇄 스펙, HUD 헤더 및 상태 패널 테마 적용 |

---

## 📂 디렉토리 구조 및 레이어 (Directory Layers)

```text
room-math-story/
├── apps/                         # 빌드 완료된 HTML5 클라이언트 게임 배포본
│   └── assets/                   # 단원별 이미지/사운드 에셋 리소스 폴더
├── gas/                          # [MOVE] GAS 서버 배포용 폴더 (Index_*.html로 동기화)
├── storyboards/                  # [MOVE] data/에서 독립된 스토리보드 및 컴파일된 PDF
│   ├── grade1/
│   ├── grade2/
│   └── grade3/
├── stories/                      # 원본 대본집 및 단일 메타데이터
│   ├── grade1/
│   │   ├── metadata.yaml         # 학년별 유일 메타데이터 중앙 관리
│   │   └── *.md
│   ├── grade2/
│   └── grade3/
├── archive/                      # 보존용 보관소
│   ├── releases/                 # 과거 릴리즈 완료 스토리 아카이브 (영구 보관용)
│   └── drafts/                   # [MOVE] 예전 기획 드래프트 (.txt) 보존 폴더
├── docs/
│   └── architecture/             # 시스템 설계도 및 아키텍처 가이드 문서
│       └── PROJECT_STRUCTURE.md  # 본 가이드라인 파일
├── scripts/
│   ├── build/                    # 빌드 및 E2E 오케스트레이션 레이어
│   │   ├── build_pdf.py          # HTML/MD 기반 PDF 가로 스토리북 렌더러
│   │   └── build_story.py        # [Orchestrator] 정적 검사 -> 스토리보드 -> HTML -> PDF 통합 파이프라인
│   ├── deploy/                   # 배포 전담 레이어
│   │   └── deploy_gas.py         # 구글 앱스 스크립트(GAS) 싱크용 통합 배포 스크립트
│   ├── builders/                 # 학년별 클라이언트 HTML 템플릿 컴파일러 소스 (update_app_*.py)
│   ├── tools/                    # 보조 도구 레이어
│   │   ├── clean/                # 프로젝트 청소 및 중복 제거 도구
│   │   ├── image/                # 이미지 리소스 크기 및 포맷 최적화 도구
│   │   └── story/                # 스토리 정적 분석 및 파싱 도구
│   │       ├── validate_story.py # [Static Analyzer] 메타데이터 캐릭터 크로스 매핑 및 JSON 리포팅 지원
│   │       ├── storyboard_parser.py
│   │       └── patch_storyboard_events.py
│   └── config/                   # [NEW] 전역 경로 및 상수 설정 패키지
│       ├── paths.py              # 프로젝트 절대 경로 상수 및 경로 생성 헬퍼 함수 제공
│       ├── constants.py          # 학년 한글명 매핑 및 지원 학년 등 전역 상수 정의
│       └── settings.py           # 경로/상수 통합 래퍼 클래스
└── scratch/                      # 임시 테스트 폴더
```

---

## 🚀 개발자 진입 가이드 (Onboarding Guide)

### 1. 새로운 스토리(Story) 추가 및 컴파일 절차
1. `stories/gradeX/` 폴더 하위에 `mX_XX_script.md` 명칭으로 신규 대본 마크다운 파일을 작성합니다.
2. `scripts/tools/story/story_builder.py`를 실행하여 뼈대가 되는 `data/storyboards/gradeX/mX_XX_storyboard.md` 템플릿을 생성합니다.
3. 템플릿 내의 `제목`, `질문`, `정답 체크` 등의 YAML 메타데이터를 기획 수식에 맞추어 보정하고, 수식 표기 기호(`\times` 등)의 유효성을 검증합니다.
4. `python scripts/tools/story/validate_story.py`를 가동하여 정적 에러가 없는지 1차 확인합니다.

### 2. 전체 프로젝트 빌드 및 배포 방법
*   **전체 빌드 파이프라인 통합 가동 (E2E)**
    ```bash
    python scripts/build/build_story.py
    ```
    이 명령을 실행하면 `정적 검사 -> 스토리보드 검출 -> 이벤트 씬 패치 -> HTML 배포본 생성 -> PDF 가로 스토리북 렌더링`까지 전 단계가 자동으로 순차 수행됩니다.
*   **GAS 서버에 클라이언트 동기화 배포**
    ```bash
    # 특정 학년만 배포 (grade1, grade2, grade3)
    python scripts/deploy/deploy_gas.py --target grade1
    
    # 전체 학년 배포
    python scripts/deploy/deploy_gas.py --target all
    
    # 인자 생략 시 대화형 콘솔 모드로 배포
    python scripts/deploy/deploy_gas.py
    ```
