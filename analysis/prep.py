# -*- coding: utf-8 -*-
"""Qualtrics 원자료 → 분석용 long/wide 테이블"""
import csv, io, glob, os, json
import pandas as pd

SRC = "/tmp/claude-0/-home-user-AICP-/99c02220-1092-5bb6-851e-24e36e963599/scratchpad/data"

# 시행 순서: A → C → B → D (사전 등록 4절)
TRIALS = [
    dict(trial=1, sid="A", year=2021, index=-0.35, answer=2),  # 비관
    dict(trial=2, sid="C", year=2024, index=+0.30, answer=1),  # 낙관
    dict(trial=3, sid="B", year=2023, index=-0.32, answer=2),  # 비관
    dict(trial=4, sid="D", year=2025, index=+0.47, answer=1),  # 낙관
]
# 각 시행의 문항1~4 컬럼
COLS = {1: ("Q8","Q9_1","Q24_1","Q12_1"),
        2: ("Q16","Q21_1","Q23_1","Q28_1"),
        3: ("Q18","Q20_1","Q25_1","Q27_1"),
        4: ("Q17","Q22_1","Q26_1","Q29_1")}

def load(path, group):
    rows = list(csv.reader(io.open(path, encoding="utf-8-sig")))
    hdr = rows[0]
    idx = {c: i for i, c in enumerate(hdr)}
    out = []
    for r in rows[3:]:
        g = lambda c: (r[idx[c]] or "").strip()
        num = lambda c: (float(g(c)) if g(c) not in ("", None) else None)
        rec = dict(group=group, rid=g("ResponseId"), pid=g("Q3"),
                   status=g("Status"), progress=num("Progress"),
                   duration=num("Duration (in seconds)"), finished=num("Finished"),
                   consent=num("Q1"), invest=num("Q4"), age=num("Q5"),
                   focus=num("Q30"), searched=num("Q31"), freetext=g("Q32"))
        for t in TRIALS:
            c1, c2, c3, c4 = COLS[t["trial"]]
            rec[f"t{t['trial']}_q1"] = num(c1)
            rec[f"t{t['trial']}_q2"] = num(c2)
            rec[f"t{t['trial']}_q3"] = num(c3)
            rec[f"t{t['trial']}_q4"] = num(c4)
        out.append(rec)
    return out

recs = []
for f in sorted(glob.glob(os.path.join(SRC, "*.csv"))):
    group = "기사" if "(기사)" in f else "도표"
    recs += load(f, group)

wide = pd.DataFrame(recs)

# ---- 파생 변수 ----
for t in TRIALS:
    n = t["trial"]
    wide[f"t{n}_correct"] = (wide[f"t{n}_q1"] == t["answer"]).astype(int)
    # 어조 정합 조정: 낙관 시행은 (문항3-5), 비관 시행은 -(문항3-5)
    sign = 1 if t["answer"] == 1 else -1
    wide[f"t{n}_congruent"] = sign * (wide[f"t{n}_q3"] - 5)

wide["n_correct"] = wide[[f"t{t['trial']}_correct" for t in TRIALS]].sum(axis=1)
wide["congruence"] = wide[[f"t{t['trial']}_congruent" for t in TRIALS]].mean(axis=1)
wide["confidence"] = wide[[f"t{t['trial']}_q4" for t in TRIALS]].mean(axis=1)

# ---- 사전 등록 9절 제외 기준 ----
q2 = wide[[f"t{t['trial']}_q2" for t in TRIALS]]
q3 = wide[[f"t{t['trial']}_q3" for t in TRIALS]]
q4 = wide[[f"t{t['trial']}_q4" for t in TRIALS]]
straight = (q2.nunique(axis=1) == 1) & (q3.nunique(axis=1) == 1) & (q4.nunique(axis=1) == 1)

wide["ex1_consent"]   = wide["consent"] != 1
wide["ex2_incomplete"]= (wide["progress"] < 100) | (wide["finished"] != 1)
wide["ex3_focus"]     = wide["focus"] == 4          # 집중하지 못했다
wide["ex4_search"]    = wide["searched"] == 3       # 여러 번 있다
wide["ex5_fast"]      = wide["duration"] < 120      # 2분 미만
wide["ex6_straight"]  = straight
EXC = ["ex1_consent","ex2_incomplete","ex3_focus","ex4_search","ex5_fast","ex6_straight"]
wide["excluded"] = wide[EXC].any(axis=1)

# ---- long 형식 ----
long_rows = []
for _, r in wide.iterrows():
    for t in TRIALS:
        n = t["trial"]
        long_rows.append(dict(
            group=r["group"], rid=r["rid"], pid=r["pid"], excluded=r["excluded"],
            trial=n, sid=t["sid"], year=t["year"], index=t["index"],
            answer=t["answer"], q1=r[f"t{n}_q1"], correct=r[f"t{n}_correct"],
            q2=r[f"t{n}_q2"], q3=r[f"t{n}_q3"], q4=r[f"t{n}_q4"],
            congruent=r[f"t{n}_congruent"],
            invest=r["invest"], age=r["age"], duration=r["duration"]))
long = pd.DataFrame(long_rows)

wide.to_csv("wide.csv", index=False)
long.to_csv("long.csv", index=False)
print("wide:", wide.shape, "| long:", long.shape)
print(wide.groupby("group").size().to_string())
