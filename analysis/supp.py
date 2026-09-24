# -*- coding: utf-8 -*-
import numpy as np, pandas as pd
from scipy import stats
w = pd.read_csv("wide.csv"); l = pd.read_csv("long.csv")
LBL = {1:"A 2021(정답 비관)", 2:"C 2024(정답 낙관)", 3:"B 2023(정답 비관)", 4:"D 2025(정답 낙관)"}

print("="*78); print("기사군의 오답 방향 — 무엇으로 답했나 (1=낙관, 2=비관)")
d = l[l.group=="기사"]
tb = d.pivot_table(index="trial", columns="q1", values="rid", aggfunc="count").fillna(0).astype(int)
tb.columns = ["낙관이라 답함" if c==1 else "비관이라 답함" for c in tb.columns]
tb.index = [LBL[i] for i in tb.index]
print(tb.to_string())

print("\n"+"="*78); print("문항2 평균 강도 평정 (실제 지수와 비교)")
p = l.pivot_table(index="trial", columns="group", values="q2", aggfunc="mean").round(2)
p["실제 지수"] = [-0.35, .30, -0.32, .47]
p.index = [LBL[i] for i in p.index]
print(p.to_string())

print("\n"+"="*78); print("참가자번호 '11' 2건 제외 시 (형식 위반 → 테스트 응답 추정)")
w2 = w[~((w.group=="기사") & (w.pid.astype(str)=="11"))]
l2 = l[l.rid.isin(w2.rid)]
print("  표본:", w2.groupby("group").size().to_dict())
a = w2[w2.group=="기사"]["n_correct"].values; b = w2[w2.group=="도표"]["n_correct"].values
t,pv = stats.ttest_ind(b,a,equal_var=False)
sp = np.sqrt(((len(a)-1)*np.var(a,ddof=1)+(len(b)-1)*np.var(b,ddof=1))/(len(a)+len(b)-2))
print(f"  H1 기사 M={a.mean():.2f} vs 도표 M={b.mean():.2f} | t={t:.2f}, p={pv:.2e}, d={(b.mean()-a.mean())/sp:.2f}")
for g in ("기사","도표"):
    s = l2[l2.group==g]["correct"]; k,n = int(s.sum()), len(s)
    print(f"  {g} 정답률 {k}/{n}={k/n*100:.1f}%  vs 50% p={stats.binomtest(k,n,0.5).pvalue:.3f}")

print("\n"+"="*78); print("공변량 — 투자 경험별 정답 수 (기사군만; 도표군은 천장)")
for g in ("기사","도표"):
    sub = w[w.group==g]
    print(f"  {g}:", sub.groupby("invest")["n_correct"].agg(["count","mean"]).round(2).to_dict("index"))

print("\n"+"="*78); print("소요 시간 군간 비교")
a = w[w.group=="기사"]["duration"]; b = w[w.group=="도표"]["duration"]
u,pu = stats.mannwhitneyu(a,b)
print(f"  중앙값 기사 {a.median():.0f}초 vs 도표 {b.median():.0f}초 | Mann-Whitney U={u:.0f}, p={pu:.4f}")

print("\n"+"="*78); print("자유응답 (기사군)")
for _,r in w[w.group=="기사"].iterrows():
    if isinstance(r.freetext,str) and r.freetext.strip():
        print(f"  [{r.pid}] {r.freetext}")
print("\n자유응답 (도표군)")
for _,r in w[w.group=="도표"].iterrows():
    if isinstance(r.freetext,str) and r.freetext.strip():
        print(f"  [{r.pid}] {r.freetext}")
