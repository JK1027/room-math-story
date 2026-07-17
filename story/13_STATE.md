# 13_STATE - 에이전트 협업 상태 일지 (Story State Machine Log)

이 문서는 스토리 제작 파이프라인의 에이전트들이 협업을 수행하며 각 단계의 결과를 축적하고, 수정 내역과 상태 변화를 추적하는 **공동 작업 일지(State Machine)**입니다. 수동 혹은 자동으로 파이프라인이 구동될 때마다 이 파일을 업데이트해야 합니다.

---

## 1. 현재 메타 상태 (Current Meta State)
```yaml
revision: 0               # 현재 수정 회차 번호 (최초 초고는 0)
current_step: "ready"     # [ready | architect | writer | review | score | director | fix | qa | complete]
last_updated: "2026-07-17T16:10:00+09:00"
qa_status: "PENDING"      # [PENDING | FAIL | PASS]
```

---

## 2. 단계별 마일스톤 로그 (Milestone Log)

### Rev 0: 초고 생성 단계 (Initial Build)
- **Architect 완료 여부**: false
- **Writer 완료 여부**: false
- **산출물 위치**: `None`
- **리뷰 수합 개수**: 0개
- **최종 점수**: `None`
- **조치 사항**: `초고 빌딩 대기 중`

---

## 3. 수정 히스토리 및 피드백 추적 (Fix History & Feedback Track)

수정 루프가 돌 때마다 아래 형식으로 기록을 누적하여, 이전에 반영한 수정이 다음 단계에서 되돌아가거나(Regression) 같은 문제가 무한 반복되는 루프를 미연에 방지합니다.

```yaml
# 예시 템플릿 (실제 수정 루프 발생 시 누적 기재):
# revision_history:
#   - rev: 1
#     modified_scenes: [3, 4]
#     fixed_issues:
#       - issue_id: 1 (Scene 3의 억지 퍼즐 연결부 수정)
#       - issue_id: 2 (Scene 4의 피코 대사 톤 교정)
#     reviewer_re_evaluation:
#       puzzle: "Scene 3 퍼즐이 비상 밸브 수동 개방으로 자연스럽게 결합되었음 (해결)"
#       student: "피코의 말투가 확실히 더 논리적이고 차가워졌음 (해결)"
#
#   - rev: 2
#     modified_scenes: [5]
#     fixed_issues:
#       - issue_id: 4 (Scene 5 결말부 반전 복선 추가)
#     reviewer_re_evaluation:
#       drama: "반전 결말에 대한 힌트가 Scene 2와 3에서 적절히 수집되어 개연성 상승 (해결)"
```
