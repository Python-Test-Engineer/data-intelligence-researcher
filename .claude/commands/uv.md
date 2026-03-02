---
description: "Run uv sync and activate the virtual environment"
allowed-tools: Bash(uv sync), Bash(.\.venv\Scripts\activate)
---

Run the following commands in order:

1. Run `uv sync` to install/update dependencies from the lockfile.
2. Remind the user to activate the virtual environment by running `.\.venv\Scripts\activate` in their terminal (note: Claude cannot persist shell state, so the user must run activation themselves).

Use the Bash tool to run `uv sync`. Then tell the user to run `.\.venv\Scripts\activate` in their own terminal to activate the environment, since shell environment changes (like activating a venv) don't persist between tool calls.
