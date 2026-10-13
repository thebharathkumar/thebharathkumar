"""Tests for status_page.py. Run: python3 -m pytest scripts/ or python3 scripts/test_status_page.py"""
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import status_page as sp  # noqa: E402

UTC = dt.timezone.utc


def test_latest_ci_skips_github_housekeeping_runs():
    runs = [
        {"name": "Graph Update: pip in /.", "event": "dynamic", "status": "completed", "conclusion": "success"},
        {"name": "CI", "event": "push", "status": "in_progress", "conclusion": None},
        {"name": "CI", "event": "push", "status": "completed", "conclusion": "failure"},
    ]
    assert sp.latest_ci(runs)["conclusion"] == "failure"


def test_latest_ci_none_when_only_housekeeping():
    runs = [{"name": "Graph Update: pip", "event": "dynamic", "status": "completed", "conclusion": "success"}]
    assert sp.latest_ci(runs) is None


def test_ci_state_mapping():
    assert sp.ci_state({"ci": None}) == "none"
    assert sp.ci_state({"ci": {"workflow": "CI", "conclusion": "success"}}) == "pass"
    assert sp.ci_state({"ci": {"workflow": "ci", "conclusion": "failure"}}) == "fail"
    assert sp.ci_state({"ci": {"workflow": "Graph Update: pip", "conclusion": "success"}}) == "none"


def test_calendar_days_flattens_weeks_in_order():
    resp = {"data": {"user": {"contributionsCollection": {"contributionCalendar": {
        "totalContributions": 3,
        "weeks": [{"contributionDays": [{"date": "2026-01-04", "contributionCount": 1},
                                        {"date": "2026-01-05", "contributionCount": 0}]},
                  {"contributionDays": [{"date": "2026-01-11", "contributionCount": 2}]}]}}}}}
    total, days = sp.calendar_days(resp)
    assert total == 3
    assert days == [["2026-01-04", 1], ["2026-01-05", 0], ["2026-01-11", 2]]


def test_ago():
    now = dt.datetime(2026, 10, 13, 8, tzinfo=UTC)
    assert sp.ago(now, now) == "today"
    assert sp.ago(now - dt.timedelta(days=1, hours=1), now) == "1 day ago"
    assert sp.ago(now - dt.timedelta(days=4), now) == "4 days ago"


def test_heat_levels_are_monotonic():
    levels = [sp.heat_level(c) for c in [0, 1, 2, 3, 6, 7, 15, 16, 100]]
    assert levels == sorted(levels) and levels[0] == 0 and levels[-1] == 4


def test_seed_snapshot_renders_and_matches_its_own_totals():
    here = Path(__file__).resolve().parent
    config = json.loads((here / "status.json").read_text())
    snap = json.loads((here / "seed_snapshot.json").read_text())
    s = sp.summarize(snap, config)
    assert s["total"] == sum(c for _, c in snap["contributions"]["days"])
    svg = sp.render(s, config)
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    for svc in config["services"]:
        assert svc["repo"] in svg


if __name__ == "__main__":
    fns = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for fn in fns:
        fn()
    print(f"{len(fns)} passed")
