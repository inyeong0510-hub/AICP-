# AICP — FOMC 어조 지수 카드 이미지 (Qualtrics 설문 자극물)

Qualtrics 설문에 삽입할 실험 자극물 이미지 저장소입니다.

## 파일 구성

| 파일 | Fed 어조 지수 (종합) | 성명문 (z) | 기자회견 (z) | 배지 |
|---|---|---|---|---|
| `stim_01` | **+0.47** (낙관) | −0.18 | +1.12 | 정합 |
| `stim_02` | **+0.30** (낙관) | −0.15 | +0.75 | 정합 |
| `stim_03` | **−0.32** (비관) | −0.12 | −0.53 | 정합 |
| `stim_04` | **−0.35** (비관) | −0.18 | −0.53 | 정합 |

- 모든 이미지는 2000 × 1500 px (4:3)
- 모든 카드에 "의사록 반영 전 잠정치" 배지 및 신뢰도 "보통" 표기 포함

## 포맷

동일한 이미지를 두 가지 포맷으로 제공합니다.

- `images/png/` — PNG. Qualtrics 그래픽 라이브러리 업로드용 (호환성 최우선)
- `images/webp/` — WebP. 용량이 약 1/5 수준, `<img>` 직접 삽입용

## Qualtrics에서 사용하는 법

### 방법 1 — 그래픽 라이브러리 업로드 (권장)
`images/png/` 의 PNG 파일을 내려받아 Qualtrics **Library → Graphics Library** 에 업로드한 뒤,
질문 편집기의 이미지 삽입 버튼으로 불러옵니다. 외부 호스팅에 의존하지 않아 가장 안정적입니다.

### 방법 2 — 외부 URL 직접 삽입
질문 편집기를 HTML 보기로 전환한 뒤 아래 형식으로 삽입합니다.

```html
<img src="RAW_URL/images/png/stim_01.png" alt="FOMC 어조 지수 카드" style="width:100%;max-width:640px;height:auto;" />
```

`RAW_URL` 기본형:

```
https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/
```

> 주의: 방법 2는 저장소가 **public** 일 때만 동작합니다. private 저장소의 raw 링크는
> 만료되는 토큰이 붙어 설문 응답 중 이미지가 깨질 수 있으므로 방법 1을 사용하세요.
