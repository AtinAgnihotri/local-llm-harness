from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentTask:
    task: str
    repo_path: str


def build_agent_prompt(task: AgentTask, root_dir: Path) -> str:
    repo = Path(task.repo_path).resolve()
    return (
        "You are operating as a local offline coding agent.\n"
        "Work in planning-first mode and be explicit about assumptions.\n"
        "Do not execute shell commands automatically.\n"
        "Prefer concise output grouped into Summary, Proposed File Changes, and Suggested Commands.\n"
        "When shell commands are needed, emit a section titled 'Suggested Commands'.\n"
        "When file edits are needed, emit a section titled 'Proposed File Changes'.\n"
        f"Harness root: {root_dir}\n"
        f"Target repository: {repo}\n"
        f"Task: {task.task}\n"
    )
