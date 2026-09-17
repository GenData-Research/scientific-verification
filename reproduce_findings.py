"""Recompute every number reported in "What the AI scientist doesn't tell you" from data/verification.csv.

Usage: python reproduce_findings.py   (Python 3.8+, standard library only)
"""
import csv
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = list(csv.DictReader(open(os.path.join(HERE, "data", "verification.csv"), encoding="utf-8")))
MODELS = ["Claude Opus 5", "GPT 5.6 Luna", "Gemini 3.1 Pro"]
ESTABLISHED = {"stated", "stated_elsewhere"}


def pct(n, d):
    return f"{n} of {d} ({100 * n / d:.0f}%)" if d else f"{n} of {d}"


def overreached(r):
    return r["evidence_outcome"].startswith("overreached")


def disclosed(r):
    return r["evidence_outcome"] == "overreached_disclosed"


def section(title):
    print(f"\n{title}\n" + "-" * len(title))


section("Overall")
correct = [r for r in ROWS if r["verdict_correct"] == "true"]
wrong = [r for r in ROWS if r["verdict_correct"] == "false"]
established = [r for r in ROWS if r["deciding_evidence_status"] in ESTABLISHED]
print("Verdicts correct:                          ", pct(len(correct), len(ROWS)))
print("Established deciding evidence accepted:    ", pct(sum(r["evidence_outcome"] == "within_evidence" for r in established), len(established)))
print("Wrong verdicts resting on overreach:       ", pct(sum(overreached(r) for r in wrong), len(wrong)))

section("Disclosure: calculations vs assumed experimental conditions")
print(f"{'':16}{'Calculations shown':>22}{'Assumed conditions disclosed':>32}")
for name, subset in [("All three models", ROWS)] + [(m, [r for r in ROWS if r["model"] == m]) for m in MODELS]:
    calc = [r for r in subset if r["deciding_evidence_status"] == "only_calculable" and overreached(r)]
    cond = [r for r in subset if r["deciding_evidence_status"] == "not_reported" and overreached(r)]
    print(f"{name:16}{pct(sum(map(disclosed, calc)), len(calc)):>22}{pct(sum(map(disclosed, cond)), len(cond)):>32}")

section("Shared across models")
by_claim = defaultdict(list)
for r in ROWS:
    if r["deciding_evidence_status"] == "not_reported":
        by_claim[r["case_id"]].append(r)
shared = sum(sum(map(overreached, rs)) >= 2 for rs in by_claim.values())
print("Claims with an unreported deciding condition filled in by at least two models:", pct(shared, len(by_claim)))

section("Correct verdicts that did not use the deciding measurement")
for r in ROWS:
    if r["verdict_correct"] == "true" and r["evidence_outcome"] == "missed_deciding_evidence":
        print(f"{r['case_id']} | {r['model']} | {r['description']}")

section("Lead example (claim v6-B1-10)")
for r in ROWS:
    if r["case_id"] == "v6-B1-10":
        print(f"{r['model']}: verdict {r['model_verdict']}, outcome {r['evidence_outcome']}, value used '{r['model_value']}'")
