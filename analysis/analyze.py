# -*- coding: utf-8 -*-
import numpy as np, pandas as pd
from scipy import stats
pd.set_option("display.width", 220)

w = pd.read_csv("wide.csv"); l = pd.read_csv("long.csv")
IDX = {1:-0.35, 2:+0.30, 3:-0.32, 4:+0.47}
LBL = {1:"A 2021(비관)", 2:"C 2024(낙관)", 3:"B 2023(비관)", 4:"D 2025(낙관)"}

def cohen_d(a, b):
    na, nb = len(a), len(b)
    s = np.sqrt(((na-1)*np.var(a, ddof=1) + (nb-1)*np.var(b, ddof=1)) / (na+nb-2))
    return (np.mean(a)-np.mean(b))/s if s else np.nan

def report(df, ld, tag):
    print("\n" + "#"*78)
    print(f"#  {tag}   (기사 n={sum(df.group=='기사')}, 도표 n={sum(df.group=='도표')})")
    print("#"*78)

    # ---------- 시행별 정답률 ----------
    print("\n[시행별 정답률]")
    tab = ld.pivot_table(index="trial", columns="group", values="correct", aggfunc="mean")
    tab.index = [LBL[i] for i in tab.index]
    print((tab*100).round(1).to_string())

    # ---------- H1 ----------
    a = df[df.group=="기사"]["n_correct"].values
    b = df[df.group=="도표"]["n_correct"].values
    t, p = stats.ttest_ind(b, a, equal_var=False)
    print(f"\n[H1] 4시행 정답 수(0-4)")
    print(f"  기사 M={a.mean():.2f} SD={a.std(ddof=1):.2f}  |  도표 M={b.mean():.2f} SD={b.std(ddof=1):.2f}")
    print(f"  Welch t={t:.3f}, p={p:.5f}, Cohen's d={cohen_d(b,a):.2f}")
    print("  각 군 정답률의 우연 수준(50%) 이항검정:")
    for g in ("기사","도표"):
        s = ld[ld.group==g]["correct"]
        k, n = int(s.sum()), len(s)
        pb = stats.binomtest(k, n, 0.5).pvalue
        print(f"    {g}: {k}/{n} = {k/n*100:.1f}%  p={pb:.2e}")

    # ---------- H2 ----------
    print(f"\n[H2] 강도 평정(문항2)이 실제 지수를 따라가는가 — 개인별 기울기")
    sl = {}
    for g in ("기사","도표"):
        ss = []
        for rid, d in ld[ld.group==g].groupby("rid"):
            x = d["index"].values; y = d["q2"].values
            if len(x) >= 3 and np.std(x) > 0:
                ss.append(np.polyfit(x, y, 1)[0])
        sl[g] = np.array(ss)
        print(f"  {g}: 평균 기울기 {ss and np.mean(ss):.2f} (SD {np.std(ss, ddof=1):.2f}, n={len(ss)})")
    t2, p2 = stats.ttest_ind(sl["도표"], sl["기사"], equal_var=False)
    print(f"  Welch t={t2:.3f}, p={p2:.5f}, d={cohen_d(sl['도표'], sl['기사']):.2f}")
    print("  시행 단위 상관(문항2 × 지수):")
    for g in ("기사","도표"):
        d = ld[ld.group==g]
        r, pr = stats.pearsonr(d["index"], d["q2"])
        print(f"    {g}: r={r:.3f}, p={pr:.2e}")

    # ---------- H3 ----------
    ca = df[df.group=="기사"]["congruence"].values
    cb = df[df.group=="도표"]["congruence"].values
    t3, p3 = stats.ttest_ind(cb, ca, equal_var=False)
    print(f"\n[H3] 어조 정합 조정 지수 (문항3, 부호 정렬 평균)")
    print(f"  기사 M={ca.mean():+.2f} SD={ca.std(ddof=1):.2f}  |  도표 M={cb.mean():+.2f} SD={cb.std(ddof=1):.2f}")
    print(f"  Welch t={t3:.3f}, p={p3:.5f}, d={cohen_d(cb,ca):.2f}")
    for g, v in (("기사",ca), ("도표",cb)):
        t0, p0 = stats.ttest_1samp(v, 0)
        print(f"    {g}: 0과 차이 t={t0:.3f}, p={p0:.4f}")

    # ---------- H4 ----------
    print(f"\n[H4] 확신도(문항4)와 정확도의 대응")
    for g in ("기사","도표"):
        d = ld[ld.group==g]
        cor = d[d.correct==1]["q4"]; inc = d[d.correct==0]["q4"]
        gap = cor.mean() - inc.mean() if len(inc) else np.nan
        acc = d["correct"].mean()*100
        conf = d["q4"].mean()
        print(f"  {g}: 평균 확신도 {conf:.2f}/10  정답률 {acc:.1f}%")
        print(f"       정답 시 {cor.mean():.2f} (n={len(cor)}) | 오답 시 {inc.mean() if len(inc) else float('nan'):.2f} (n={len(inc)}) | 차이 {gap:+.2f}")
        print(f"       과신 지표(확신도×10 − 정답률) = {conf*10-acc:+.1f}%p")
    ka = df[df.group=="기사"]["confidence"].values
    kb = df[df.group=="도표"]["confidence"].values
    t4, p4 = stats.ttest_ind(kb, ka, equal_var=False)
    print(f"  군간 평균 확신도: Welch t={t4:.3f}, p={p4:.4f}, d={cohen_d(kb,ka):.2f}")

report(w, l, "A. 전체 표본 (제외 기준 적용 전)")
wx = w[~w.excluded]; lx = l[~l.excluded]
report(wx, lx, "B. 사전 등록 9절 제외 기준 적용 후")
