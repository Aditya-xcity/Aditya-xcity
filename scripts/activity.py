"""Render the two headline metrics from GitHub's public contribution calendar."""
import html
import re
from pathlib import Path

calendar = Path("calendar.html").read_text()
days = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="([0-4])"', calendar)
counts = re.findall(r">\s*(No|[\d,]+) contributions? on [^<]+</tool-tip>", calendar)
if not 360 <= len(days) <= 372 or len(days) != len(counts):
    raise SystemExit("Unexpected contribution calendar format")
values = [int(count.replace(",", "")) if count != "No" else 0 for count in counts]
active = sum(level != "0" for _, level in days)
if active != sum(value > 0 for value in values):
    raise SystemExit("Contribution calendar counts disagree")
total = sum(values)
through = html.escape(max(day for day, _ in days))
Path("dist/activity.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="148" viewBox="0 0 760 148">
  <title>{total:,} GitHub contributions on {active} active days in the past year</title>
  <rect x="1" y="1" width="758" height="146" rx="16" fill="#081523" stroke="#216AA5" stroke-width="2"/>
  <g font-family="system-ui,sans-serif">
    <text x="28" y="36" fill="#BAE6FD" font-size="22">Past year through {through} · GitHub</text>
    <path d="M380 53v70" stroke="#216AA5"/>
    <g fill="#38BDF8" font-size="40" font-weight="700">
      <text x="28" y="87">{total:,}</text>
      <text x="410" y="87">{active}</text>
    </g>
    <g fill="#BAE6FD" font-size="25">
      <text x="28" y="122">Contributions</text>
      <text x="410" y="122">Active days</text>
    </g>
  </g>
</svg>
''')
