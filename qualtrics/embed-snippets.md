# Qualtrics HTML 삽입 스니펫

질문 편집기에서 **리치 콘텐츠 편집기 → HTML 보기(`<>`)** 를 열고 아래 블록을 통째로 붙여넣으세요.

> - URL은 이미 퍼센트 인코딩되어 있습니다. 한글을 직접 타이핑하면 404가 납니다.
> - URL 중간에 직접 줄바꿈(Enter)을 넣지 마세요. 경로가 깨집니다.
> - `style` 값은 8문항 전부 동일하게 유지하세요. 자극물 크기 차이는 그 자체로 교란 변인이 됩니다.
> - 질문의 파란 링크 "이 질문에 사용할 그래픽 선택"은 누르지 마세요. 이미지가 두 번 표시됩니다.

---

## 언론군 — `기사`

### 시행1 · `A_2021_기사` · 정답: **비관**

```html
<p>아래 기사는 2021년 4월에 미국 FOMC 회의 직후 공공기관에서 나온 기사입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/A_2021_%EA%B8%B0%EC%82%AC.png"
     alt="2021년 FOMC 뉴스 기사"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

### 시행2 · `C_2024_기사` · 정답: **낙관**

```html
<p>아래 기사는 2024년 1월에 미국 FOMC 회의 직후 공공기관에서 나온 기사입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/C_2024_%EA%B8%B0%EC%82%AC.png"
     alt="2024년 FOMC 뉴스 기사"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

### 시행3 · `B_2023_기사` · 정답: **비관**

```html
<p>아래 기사는 2023년 6월에 미국 FOMC 회의 직후 공공기관에서 나온 기사입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/B_2023_%EA%B8%B0%EC%82%AC.png"
     alt="2023년 FOMC 뉴스 기사"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

### 시행4 · `D_2025_기사` · 정답: **낙관**

```html
<p>아래 기사는 2025년 1월에 미국 FOMC 회의 직후 공공기관에서 나온 기사입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/D_2025_%EA%B8%B0%EC%82%AC.png"
     alt="2025년 FOMC 뉴스 기사"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

---

## 대시보드군 — `대시보드`

### 시행1 · `A_2021_대시보드` · 정답: **비관**

```html
<p>아래 대시보드는 2021년 4월에 미국 FOMC 회의 직후 공공기관에서 나온 자료입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/A_2021_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C.png"
     alt="2021년 FOMC 어조 지수 대시보드"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

### 시행2 · `C_2024_대시보드` · 정답: **낙관**

```html
<p>아래 대시보드는 2024년 1월에 미국 FOMC 회의 직후 공공기관에서 나온 자료입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/C_2024_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C.png"
     alt="2024년 FOMC 어조 지수 대시보드"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

### 시행3 · `B_2023_대시보드` · 정답: **비관**

```html
<p>아래 대시보드는 2023년 6월에 미국 FOMC 회의 직후 공공기관에서 나온 자료입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/B_2023_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C.png"
     alt="2023년 FOMC 어조 지수 대시보드"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

### 시행4 · `D_2025_대시보드` · 정답: **낙관**

```html
<p>아래 대시보드는 2025년 1월에 미국 FOMC 회의 직후 공공기관에서 나온 자료입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/png/D_2025_%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C.png"
     alt="2025년 FOMC 어조 지수 대시보드"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```

---

## 용량을 줄이고 싶을 때 (WebP)

PNG는 장당 약 250~440 KB, WebP는 약 52~90 KB입니다.
URL에서 `/png/` → `/webp/`, `.png` → `.webp` 두 군데만 바꾸면 됩니다.
WebP는 Chrome·Edge·Firefox·Safari 14 이상에서 모두 표시됩니다.

```html
<p>아래 기사는 2021년 4월에 미국 FOMC 회의 직후 공공기관에서 나온 기사입니다.</p>

<img src="https://raw.githubusercontent.com/inyeong0510-hub/AICP-/claude/epic-lovelace-gc056z/images/webp/A_2021_%EA%B8%B0%EC%82%AC.webp"
     alt="2021년 FOMC 뉴스 기사"
     style="width:100%;max-width:640px;height:auto;display:block;margin:16px auto;border:1px solid #e0e0e0;border-radius:8px;" />
```
