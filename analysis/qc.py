# -*- coding: utf-8 -*-
import pandas as pd
pd.set_option("display.width", 200)
w = pd.read_csv("wide.csv")

print("="*78); print("1. 응답 수")
print(w.groupby("group").size().to_string())

print("\n"+"="*78); print("2. 참가자 번호 (중복·형식 확인)")
for g, d in w.groupby("group"):
    pids = d["pid"].astype(str).tolist()
    dup  = sorted({p for p in pids if pids.count(p) > 1})
    print(f"  {g}: {sorted(pids)}")
    print(f"       중복 {dup or '없음'} | 자릿수 {sorted({len(p) for p in pids})}")

print("\n"+"="*78); print("3. 소요 시간(초)")
print(w.groupby("group")["duration"].describe()[["count","min","25%","50%","75%","max"]].round(0).to_string())
print("\n  2분 미만:", w[w.duration < 120].groupby("group").size().to_dict())
print("  1시간 초과(탭 방치 추정):", w[w.duration > 3600][["group","pid","duration"]].to_dict("records"))

print("\n"+"="*78); print("4. 사전 등록 9절 제외 기준별 해당 건수")
EX = {"ex1_consent":"① 동의 안 함","ex2_incomplete":"② 미완료","ex3_focus":"③ 집중 못함",
      "ex4_search":"④ 검색 여러 번","ex5_fast":"⑤ 2분 미만","ex6_straight":"⑥ 직선 응답"}
for k, v in EX.items():
    s = w.groupby("group")[k].sum().to_dict()
    print(f"  {v:18s} 기사 {int(s.get('기사',0)):2d} | 도표 {int(s.get('도표',0)):2d}")
print("\n  최종 제외:", w.groupby("group")["excluded"].sum().to_dict())
print("  제외 후 잔존:", w[~w.excluded].groupby("group").size().to_dict())

print("\n"+"="*78); print("5. 사후 문항")
print("  집중도(1매우~4못함):"); print(pd.crosstab(w.group, w.focus).to_string())
print("  검색(1없다 2한두번 3여러번):"); print(pd.crosstab(w.group, w.searched).to_string())

print("\n"+"="*78); print("6. 공변량")
print("  투자경험(1있다 2없다):"); print(pd.crosstab(w.group, w.invest).to_string())
print("  연령대(1=20대 2=30대 3=40대+):"); print(pd.crosstab(w.group, w.age).to_string())
