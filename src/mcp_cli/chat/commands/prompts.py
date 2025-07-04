# mcp_cli/chat/commands/prompts.py
"""
Chat-mode `/prompts` command for MCP-CLI
========================================

This module connects the **/prompts** slash-command to the shared
:meth:`mcp_cli.commands.prompts.prompts_action_cmd` coroutine so users can
list every prompt template stored on the connected MCP servers straight from
the interactive chat session.

Features
--------
* **Cross-platform Rich console** - relies on
  :pyfunc:`mcp_cli.utils.rich_helpers.get_console`, which transparently
  falls back to plain text when ANSI colours aren't available (e.g. Windows
  *cmd.exe*, PowerShell without VT, or when piping to a file).
* **Read-only & stateless** - the handler simply renders a Rich table and
  never mutates the chat context, so it's safe to hot-reload.
* **One-liner behaviour** - a single `await` to the shared helper keeps the
  code footprint minimal.

Example
-------
>>> /prompts
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Name      ┃ Description                                   ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ greet     │ Friendly greeting prompt                      │
│ sql_query │ Extract SQL table info                        │
└───────────┴───────────────────────────────────────────────┘
"""

from __future__ import annotations

from typing import Any, Dict, List

# Cross-platform Rich console helper (handles Windows quirks, piping, etc.)
from mcp_cli.utils.rich_helpers import get_console

# Shared implementation
from mcp_cli.commands.prompts import prompts_action_cmd
from mcp_cli.tools.manager import ToolManager
from mcp_cli.chat.commands import register_command


async def cmd_prompts(_parts: List[str], ctx: Dict[str, Any]) -> bool:  # noqa: D401
    """List stored prompt templates from all connected servers."""
    console = get_console()

    tm: ToolManager | None = ctx.get("tool_manager")
    if tm is None:
        console.print("[red]Error:[/red] ToolManager not available.")
        return True  # command handled (nothing further to do)

    # Delegate to the shared async helper
    await prompts_action_cmd(tm)
    return True


# ────────────────────────────────────────────────────────────────
# Registration (no extra alias - keep namespace clean)
# ────────────────────────────────────────────────────────────────
register_command("/prompts", cmd_prompts)
