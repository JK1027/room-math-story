# 수학 방탈출 게임 스토리 제작 및 빌드 엔진 (room-math-story)

이 프로젝트는 수학 방탈출 게임의 대본(Script), 스토리보드(Storyboard)를 관리하고 정적 분석(Validation) 및 HTML/PDF 형식의 클라이언트 빌드를 통합 통제하는 스토리 제작 파이프라인 엔진입니다.

---

## 🛠️ 주요 기능
1. **정적 분석기 (`validate_story.py`)**: 씬/퍼즐 번호 순차 검사, 금지어 필터링, 이미지 누락 검증뿐만 아니라 `metadata.yaml` 기반의 캐릭터 매핑 검사 및 `--json` 구조화 리포팅 지원.
2. **파이프라인 오케스트레이터 (`build_story.py`)**: 정적 검사부터 대본 컴파일, HTML 클라이언트 빌드, PDF 스토리북 컴파일까지 E2E 자동 실행.
3. **통합 배포기 (`deploy_gas.py`)**: 단일 타겟/일괄 배포 및 대화형 CLI 모드를 지원하여 HTML5 클라이언트를 구글 앱스 스크립트(gas)로 동기화.

---

## 🧭 프로젝트 구조 및 아키텍처
디렉토리 구조 및 레이어별(Build/Deploy/Tools/Config) 역할, 입출력 데이터 계약(Data Contract)에 관한 상세한 아키텍처 내용은 **[PROJECT_STRUCTURE.md](file:///c:/Coding/Projects/School/room-math-story/docs/architecture/PROJECT_STRUCTURE.md)**를 참조하십시오.

---

## 🚀 사용법 및 가이드

### 1. 개발 환경 요구사항
- Python 3.8 이상
- Google Chrome 또는 Microsoft Edge (Headless PDF 인쇄용)

### 2. 전체 E2E 빌드 실행 (Orchestration)
```bash
python scripts/build/build_story.py
```
*이 명령 하나로 검증(Validation) 및 HTML, PDF 빌드가 일괄 수행됩니다.*

### 3. 클라이언트 웹 앱 GAS 동기화 배포
```bash
# 특정 학년만 배포 (grade1, grade2, grade3)
python scripts/deploy/deploy_gas.py --target grade1

# 전체 학년 일괄 배포
python scripts/deploy/deploy_gas.py --target all

# 대화형 CLI 선택 배포 모드 실행
python scripts/deploy/deploy_gas.py
```

### 4. 새로운 스토리(Story) 추가 절차
1. **메타데이터 등록**: `stories/gradeX/metadata.yaml`에 유닛명과 캐릭터(조력자, 빌런) 이름을 등록합니다.
2. **대본 작성**: `stories/gradeX/` 하위에 `mX_XX_script.md` 파일을 마크다운 형식으로 작성합니다.
3. **스토리보드 템플릿 생성**:
   ```bash
   python scripts/tools/story/story_builder.py
   ```
   *이 실행을 통해 `storyboards/gradeX/mX_XX_storyboard.md` 템플릿이 자동 생성됩니다.*
4. **스토리보드 상세 채우기**: 템플릿 내의 문제 질문, 힌트, 정답 체크 수식 등을 수동 조율합니다.
5. **정적 검사 실행**:
   ```bash
   python scripts/tools/story/validate_story.py
   # 구조화 JSON 리포트 확인 시
   python scripts/tools/story/validate_story.py --json
   ```
6. **E2E 통합 빌드 및 검증 완료**:
   `python scripts/build/build_story.py` 실행 후 최종 빌드 성공 및 렌더링을 확인합니다.
