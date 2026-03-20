"""
Claude Code status line for the data-intelligence-researcher project.
Reads JSON from stdin and prints a compact status string.
"""

import json
import sys
import os
import subprocess
from pathlib import Path


def git_branch(cwd: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "--no-optional-locks", "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        branch = result.stdout.strip()
        return branch if branch else ""
    except Exception:
        return ""


def next_output_project(project_dir: str) -> str:
    """Return the highest PROJECT_XX folder that exists in output/, or empty string."""
    output_dir = Path(project_dir) / "output"
    if not output_dir.is_dir():
        return ""
    folders = sorted(
        [d.name for d in output_dir.iterdir() if d.is_dir() and d.name.startswith("PROJECT_")],
        reverse=True,
    )
    return folders[0] if folders else ""


def bar(pct: float, width: int = 8) -> str:
    filled = round(pct / 100 * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    parts = []

    # Model (shortened)
    model_name = data.get("model", {}).get("display_name", "")
    if model_name:
        # Shorten e.g. "Claude 3.5 Sonnet" -> "3.5 Sonnet"
        short = model_name.replace("Claude ", "")
        parts.append(short)

    # Git branch
    cwd = data.get("cwd", "") or data.get("workspace", {}).get("current_dir", "")
    project_dir = data.get("workspace", {}).get("project_dir", cwd)
    branch = git_branch(project_dir or cwd)
    if branch:
        parts.append(f"git:{branch}")

    # Current output project folder
    active_project = next_output_project(project_dir or cwd)
    if active_project:
        parts.append(active_project)

    # Context window usage
    ctx = data.get("context_window", {})
    used_pct = ctx.get("used_percentage")
    if used_pct is not None:
        parts.append(f"ctx:{bar(used_pct)} {used_pct:.0f}%")

    # Rate limits (Claude.ai subscribers)
    rate = data.get("rate_limits", {})
    five_h = rate.get("five_hour", {})
    if five_h and "used_percentage" in five_h:
        parts.append(f"5h:{five_h['used_percentage']:.0f}%")
    seven_d = rate.get("seven_day", {})
    if seven_d and "used_percentage" in seven_d:
        parts.append(f"7d:{seven_d['used_percentage']:.0f}%")

    print("  |  ".join(parts))


if __name__ == "__main__":
    main()
