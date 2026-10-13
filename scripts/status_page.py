#!/usr/bin/env python3
"""Render a live status page for a GitHub profile as a single SVG.

Every live number on the page (contributions, CI state, ship dates) is fetched
from the GitHub API on each run. The one-line proof per service is static text
from status.json, copied from that repo's own README.

Usage:
  GITHUB_TOKEN=... python3 scripts/status_page.py --out assets/status.svg
  python3 scripts/status_page.py --snapshot scripts/seed_snapshot.json --out assets/status.svg

Standard library only, so the workflow needs no install step.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"
HERE = Path(__file__).resolve().parent

# Workflow runs GitHub creates on its own (dependency graph, Dependabot) are not CI.
NON_CI_EVENTS = {"dynamic", "dependabot"}
NON_CI_NAME_PREFIXES = ("Graph Update", "Dependabot", "Automatic Dependency Submission")

# ---------------------------------------------------------------- fetch


def _request(url: str, token: str, body: dict | None = None) -> dict | list:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "profile-status-page")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def _is_ci(run: dict) -> bool:
    if run.get("event") in NON_CI_EVENTS:
        return False
    return not str(run.get("name", "")).startswith(NON_CI_NAME_PREFIXES)


def latest_ci(runs: list[dict]) -> dict | None:
    """Most recent completed CI run, ignoring GitHub's own housekeeping runs."""
    for run in runs:
        if _is_ci(run) and run.get("status") == "completed":
            return {"conclusion": run.get("conclusion"), "workflow": run.get("name"),
                    "event": run.get("event")}
    return None


def calendar_days(graphql_response: dict) -> tuple[int, list[list]]:
    cal = graphql_response["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [[d["date"], d["contributionCount"]] for w in cal["weeks"] for d in w["contributionDays"]]
    return cal["totalContributions"], days


def fetch(config: dict, token: str) -> dict:
    owner = config["owner"]
    repos = []
    for svc in config["services"]:
        name = svc["repo"]
        meta = _request(f"{API}/repos/{owner}/{name}", token)
        branch = meta.get("default_branch", "main")
        runs = _request(f"{API}/repos/{owner}/{name}/actions/runs?branch={branch}&per_page=20", token)
        repos.append({
            "name": name,
            "stars": meta.get("stargazers_count", 0),
            "pushed_at": meta.get("pushed_at"),
            "ci": latest_ci(runs.get("workflow_runs", [])),
        })
    query = """query($login:String!){user(login:$login){contributionsCollection{
      contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
    gql = _request(f"{API}/graphql", token, {"query": query, "variables": {"login": owner}})
    if "errors" in gql:
        raise RuntimeError(f"GraphQL error: {gql['errors']}")
    total, days = calendar_days(gql)
    return {
        "fetched_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "GitHub REST + GraphQL",
        "contributions": {"total": total, "days": days},
        "repos": repos,
    }

# ---------------------------------------------------------------- derive


def parse_ts(s: str) -> dt.datetime:
    return dt.datetime.strptime(s.replace(".000", ""), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def ago(then: dt.datetime, now: dt.datetime) -> str:
    days = (now - then).days
    if days <= 0:
        return "today"
    if days == 1:
        return "1 day ago"
    return f"{days} days ago"


def ci_state(repo: dict) -> str:
    ci = repo.get("ci")
    if not ci or not _is_ci({"name": ci.get("workflow", ""), "event": ci.get("event")}):
        return "none"
    return "pass" if ci.get("conclusion") == "success" else "fail"


def summarize(snap: dict, config: dict) -> dict:
    now = parse_ts(snap["fetched_at"])
    proofs = {s["repo"]: s["proof"] for s in config["services"]}
    rows = []
    for r in snap["repos"]:
        pushed = parse_ts(r["pushed_at"])
        rows.append({"name": r["name"], "proof": proofs.get(r["name"], ""), "ci": ci_state(r),
                     "pushed": pushed, "ago": ago(pushed, now)})
    rows.sort(key=lambda x: x["pushed"], reverse=True)
    days = snap["contributions"]["days"]
    with_ci = [x for x in rows if x["ci"] != "none"]
    return {
        "now": now,
        "rows": rows,
        "days": days,
        "total": snap["contributions"]["total"],
        "active_days": sum(1 for _, c in days if c > 0),
        "ci_pass": sum(1 for x in with_ci if x["ci"] == "pass"),
        "ci_total": len(with_ci),
        "no_ci": len(rows) - len(with_ci),
        "last": rows[0] if rows else None,
    }

# ---------------------------------------------------------------- render

W = 1000
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
SURFACE, TILE, LINE = "#0B0E14", "#11161F", "#1F2633"
INK, INK2, MUTED = "#E6EDF3", "#A8B3C7", "#6B7689"
HEAT = ["#161B26", "#3B2F7A", "#5A48C2", "#7C6CF2", "#B7ACFF"]  # one hue, light = more
STATUS = {"pass": "#3FB950", "fail": "#F85149", "none": "#6B7689"}


def heat_level(c: int) -> int:
    return 0 if c == 0 else 1 if c <= 2 else 2 if c <= 6 else 3 if c <= 15 else 4


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def status_icon(state: str, x: float, y: float) -> str:
    col = STATUS[state]
    if state == "pass":
        mark = f'<path d="M{x-3.5} {y} l2.5 2.5 l4.5 -5" stroke="{SURFACE}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    elif state == "fail":
        mark = f'<path d="M{x-3} {y-3} l6 6 M{x+3} {y-3} l-6 6" stroke="{SURFACE}" stroke-width="1.8" stroke-linecap="round"/>'
    else:
        mark = f'<path d="M{x-3} {y} h6" stroke="{SURFACE}" stroke-width="1.8" stroke-linecap="round"/>'
    return f'<circle cx="{x}" cy="{y}" r="7" fill="{col}"/>{mark}'


def render(s: dict, config: dict) -> str:
    out: list[str] = []
    a = out.append
    pad = 40

    # heatmap geometry: weeks as columns, Sunday on top, like GitHub
    days = s["days"]
    first = dt.date.fromisoformat(days[0][0])
    first_sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    n_weeks = (dt.date.fromisoformat(days[-1][0]) - first_sunday).days // 7 + 1
    step = (W - 2 * pad) / n_weeks
    cell = round(step - 3, 1)
    hm_y = 214

    tiles_y = hm_y + 7 * step + 34
    tiles_h = 86
    table_y = tiles_y + tiles_h + 44
    row_h = 30
    H = int(table_y + 26 + row_h * len(s["rows"]) + 54)

    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
      f'aria-label="Live status page for {esc(config["owner"])}: {s["total"]} contributions in the last year, '
      f'{s["ci_pass"]} of {s["ci_total"]} CI pipelines passing.">')
    a(f'''<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  <radialGradient id="glow" cx="88%" cy="0%" r="65%"><stop offset="0%" stop-color="#7C6CF2" stop-opacity=".30"/><stop offset="100%" stop-color="#7C6CF2" stop-opacity="0"/></radialGradient>
  <linearGradient id="nm" x1="0" x2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#C4BBFF"/></linearGradient>
  <style>
    .m{{font-family:{MONO}}} .s{{font-family:{SANS}}}
    .in{{opacity:0;animation:in .5s ease-out forwards}}
    @keyframes in{{to{{opacity:1}}}}
  </style>
</defs>''')
    a(f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{SURFACE}"/><rect width="{W}" height="{H}" fill="url(#glow)"/>')

    # header
    a(f'''<circle cx="{pad+6}" cy="36" r="4" fill="{STATUS["pass"]}"><animate attributeName="opacity" values="1;.35;1" dur="1.8s" repeatCount="indefinite"/></circle>
<circle cx="{pad+6}" cy="36" r="4" fill="none" stroke="{STATUS["pass"]}" stroke-width="1.5"><animate attributeName="r" values="4;11" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="1.8s" repeatCount="indefinite"/></circle>
<text x="{pad+20}" y="40" class="m" font-size="13" fill="{MUTED}">LIVE  ·  status / {esc(config["owner"])}</text>
<text x="{W-pad}" y="40" class="m" font-size="13" fill="{MUTED}" text-anchor="end">refreshed {s["now"].strftime("%Y-%m-%d %H:%M")} UTC</text>
<text x="{pad}" y="104" class="s in" font-size="46" font-weight="800" letter-spacing="-1" fill="url(#nm)">{esc(config["name"])}</text>
<text x="{pad+2}" y="140" class="s in" font-size="18" fill="{INK2}" style="animation-delay:.15s">{esc(config["tagline"])}</text>
<line x1="{pad}" y1="166" x2="{W-pad}" y2="166" stroke="{LINE}"/>''')

    # contributions heatmap
    a(f'<text x="{pad}" y="198" class="m" font-size="11" letter-spacing="1.5" fill="{MUTED}">CONTRIBUTIONS · LAST 12 MONTHS</text>')
    legend_x = W - pad - 5 * 14 - 70
    a(f'<text x="{legend_x}" y="198" class="m" font-size="11" fill="{MUTED}">less</text>')
    for i, col in enumerate(HEAT):
        a(f'<rect x="{legend_x + 34 + i*14}" y="189" width="10" height="10" rx="2" fill="{col}"/>')
    a(f'<text x="{legend_x + 34 + 5*14 + 4}" y="198" class="m" font-size="11" fill="{MUTED}">more</text>')
    last_month = None
    for date_s, c in days:
        d = dt.date.fromisoformat(date_s)
        off = (d - first_sunday).days
        col_i, row_i = off // 7, off % 7
        x = pad + col_i * step
        y = hm_y + row_i * step
        delay = 0.3 + col_i * 0.012
        a(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2.5" fill="{HEAT[heat_level(c)]}" class="in" style="animation-delay:{delay:.2f}s"/>')
        if row_i == 0 and d.month != last_month and d.day <= 7:
            a(f'<text x="{x:.1f}" y="{hm_y + 7*step + 12:.1f}" class="m" font-size="10.5" fill="{MUTED}">{d.strftime("%b")}</text>')
            last_month = d.month

    # stat tiles
    last = s["last"]
    tiles = [
        (f'{s["total"]:,}', "contributions", "in the last 12 months"),
        (f'{s["active_days"]}', "active days", f'of the last {len(days)} days'),
        (f'{s["ci_pass"]}/{s["ci_total"]}', "CI pipelines green", f'{s["no_ci"]} repos have no CI yet' if s["no_ci"] else "every repo has CI"),
        (last["ago"] if last else "n/a", "last ship", last["name"] if last else ""),
    ]
    gap = 16
    tw = (W - 2 * pad - 3 * gap) / 4
    for i, (big, label, sub) in enumerate(tiles):
        x = pad + i * (tw + gap)
        a(f'<g class="in" style="animation-delay:{0.9 + i*0.1:.2f}s"><rect x="{x:.1f}" y="{tiles_y:.1f}" width="{tw:.1f}" height="{tiles_h}" rx="10" fill="{TILE}" stroke="{LINE}"/>'
          f'<text x="{x+16:.1f}" y="{tiles_y+34:.1f}" class="s" font-size="26" font-weight="700" fill="{INK}">{esc(big)}</text>'
          f'<text x="{x+16:.1f}" y="{tiles_y+55:.1f}" class="m" font-size="11.5" fill="{INK2}">{esc(label)}</text>'
          f'<text x="{x+16:.1f}" y="{tiles_y+71:.1f}" class="m" font-size="11" fill="{MUTED}">{esc(sub)}</text></g>')

    # services table
    cx_proof, cx_ci, cx_ship = pad + 230, pad + 640, W - pad
    a(f'<text x="{pad}" y="{table_y:.1f}" class="m" font-size="11" letter-spacing="1.5" fill="{MUTED}">SERVICE</text>'
      f'<text x="{cx_proof}" y="{table_y:.1f}" class="m" font-size="11" letter-spacing="1.5" fill="{MUTED}">PROOF</text>'
      f'<text x="{cx_ci}" y="{table_y:.1f}" class="m" font-size="11" letter-spacing="1.5" fill="{MUTED}">CI</text>'
      f'<text x="{cx_ship}" y="{table_y:.1f}" class="m" font-size="11" letter-spacing="1.5" fill="{MUTED}" text-anchor="end">LAST SHIP</text>'
      f'<line x1="{pad}" y1="{table_y+10:.1f}" x2="{W-pad}" y2="{table_y+10:.1f}" stroke="{LINE}"/>')
    labels = {"pass": "passing", "fail": "failing", "none": "no CI"}
    for i, r in enumerate(s["rows"]):
        y = table_y + 34 + i * row_h
        a(f'<g class="in" style="animation-delay:{1.3 + i*0.07:.2f}s">'
          + (f'<rect x="{pad-8}" y="{y-19:.1f}" width="{W-2*pad+16}" height="{row_h}" rx="6" fill="{TILE}"/>' if i % 2 == 0 else "")
          + f'<text x="{pad}" y="{y:.1f}" class="m" font-size="14" fill="{INK}">{esc(r["name"])}</text>'
          f'<text x="{cx_proof}" y="{y:.1f}" class="m" font-size="12.5" fill="{INK2}">{esc(r["proof"])}</text>'
          + status_icon(r["ci"], cx_ci + 7, y - 4.5)
          + f'<text x="{cx_ci+20}" y="{y:.1f}" class="m" font-size="12.5" fill="{INK2}">{labels[r["ci"]]}</text>'
          f'<text x="{cx_ship}" y="{y:.1f}" class="m" font-size="12.5" fill="{INK2}" text-anchor="end">{esc(r["ago"])}</text></g>')

    foot_y = H - 22
    a(f'<text x="{pad}" y="{foot_y}" class="m" font-size="11" fill="{MUTED}">Contributions, CI state and ship dates come from the GitHub API on every run. '
      f'Proof lines are copied from each repo&apos;s README.</text>')
    a(f'</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="15.5" fill="none" stroke="{LINE}"/></svg>')
    return "\n".join(out)

# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--config", default=str(HERE / "status.json"))
    ap.add_argument("--snapshot", help="render from a saved snapshot instead of calling the API")
    ap.add_argument("--save-snapshot", help="write the fetched data here")
    ap.add_argument("--out", default="assets/status.svg")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    if args.snapshot:
        snap = json.loads(Path(args.snapshot).read_text())
    else:
        # STATUS_TOKEN (optional personal token) lets the calendar match what you see when
        # signed in; the default Actions token sees public contributions only.
        token = os.environ.get("STATUS_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
        if not token:
            print("Set GITHUB_TOKEN (or STATUS_TOKEN); the GraphQL calendar needs one.", file=sys.stderr)
            return 2
        try:
            snap = fetch(config, token)
        except urllib.error.HTTPError as e:
            print(f"GitHub API error {e.code} on {e.url}: {e.read()[:300]!r}", file=sys.stderr)
            return 1
    if args.save_snapshot:
        Path(args.save_snapshot).write_text(json.dumps(snap, indent=1))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(render(summarize(snap, config), config))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
