# Chapter Markdown Schema Specification (chapter_schema.md)

이 문서는 수학 방탈출 게임 스토리의 단일 원천(Single Source of Truth)인 `chapterXX.md` 파일의 공식 마크다운 Heading 기반 DSL 규격을 정의합니다.

---

## 🧭 설계 철학
- ** Heading 기반 구조**: YAML 형태의 하위 리스트 파싱 난해함을 없애기 위해, 마크다운 표준 `#` 헤더 체계를 기반으로 데이터를 분할합니다.
- **인간과 AI 모두에게 친화적**: 에디터에서 볼 때 문서 구조가 명확히 분리되며, 파서가 정규식 또는 마크다운 토큰 분석기(ex: mistune, markdown-it 등)를 통해 100% 견고하게 추출할 수 있게 만듭니다.

---

## 📝 파일 구조 및 스펙 명세

### 1. Frontmatter (공통 메타데이터)
파일 최상단에는 `---` 로 둘러싸인 YAML Frontmatter가 위치합니다.
```yaml
---
title: "소인수분해 - 아라비아의 비밀 방"
template: "escape_room"
hero: "수학 조사관"
helper: "알콰리즈미"
villain: "검은 모래 도적단"
intro_image: "intro.png"
outro_image: "outro.png"
---
```

### 2. Opening & Intro Section
오프닝 시나리오 대사를 수록합니다.
```markdown
## 🎬 [오프닝 & 인트로]

아라비아의 오래된 공방 문을 열자, 모래 냄새와 오래된 종이 향기가 섞여 풍겨왔다.
```

### 3. Quiz Section (Q1 ~ Q20)
각 퀴즈는 `## Q[번호]` 헤더로 시작하며, 하위 헤더들로 구조화됩니다. 헤더의 순서는 보장되거나 혹은 파서가 파악할 수 있도록 고정됩니다.

```markdown
## Q1

### Title
공방 서갑 열기

### Image
q1.png

### Question
10 이하의 자연수 중 소수는 모두 몇 개인가?

### Choices
- 4
- 6
- 2
- 8

### Answer
ans === '4' || ans === '4개'

### Placeholder
숫자 또는 개수 입력

### Error Message
자물쇠가 굳게 닫혀 있습니다! 숫자를 다시 세어 보십시오.

### Hint
10 이하의 소수(1보다 크고 1과 자기 자신만을 약수로 가지는 수)를 나열해 보세요. (예: 2, 3...)

### Story
- **조력자**: "수학 조사관, 서갑 주변에 쓰인 숫자를 분석해 보게."
수학 조사관은 서갑 밑의 작은 서랍을 당겼다.
```

- **선택적 필드 (`Extra Class` 등)**: 필요한 경우 `### Extra Class` 헤더를 추가하여 특정 단원에만 적용되는 레이아웃 보조 클래스를 전달할 수 있습니다.

### 4. Event Section (Event 1 ~ 4)
돌발 및 진행도 이벤트를 수록합니다.

```markdown
## EVENT1

### Title
비밀의 방 탈출

### Image
event1.png

### Button Text
결계 통과

### Next Stage
panel_q6

### Progress
25

### Story
결계가 푸른 빛을 발산하며 공간을 가르기 시작했다.
```

### 5. Outro Section
엔딩 시나리오 대사를 수록합니다.

```markdown
## 🎬 [엔딩 & 아웃트로]

모든 결계가 해제되고, 수학 조사관과 알콰리즈미는 아라비아 공방을 빠져나왔다.
```

---

## 🚨 제약 및 규칙
1. **헤더의 규격 준수**: `## Q1`, `### Story` 등의 이름은 정확하게 일치해야 합니다. (대소문자 구분)
2. **리스트 포맷**: `### Choices` 하위는 반드시 마크다운 리스트 (`- 보기텍스트`) 형태여야 합니다.
3. **정답 형식**: `### Answer` 아래의 텍스트는 유효한 자바스크립트 수식 문자열이어야 합니다.
