from __future__ import annotations

from pathlib import Path

from .config import AppConfig
from .llamacpp import resolve_binary


def doctor_report(config: AppConfig) -> str:
    lines: list[str] = []
    binary_path = resolve_binary(config.root_dir)
    lines.append(f"root_dir={config.root_dir}")
    lines.append(f"llama_cli={binary_path}")
    lines.append(f"llama_cli_exists={binary_path.exists()}")

    for profile_name, profile in sorted(config.profiles.items()):
        model_path = config.root_dir / profile.model_path
        prompt_path = config.root_dir / profile.prompt_template
        lines.append(
            f"profile={profile_name} experimental={profile.experimental} "
            f"model_exists={model_path.exists()} prompt_exists={prompt_path.exists()}"
        )

    logs_dir = config.root_dir / config.defaults.log_dir
    sessions_dir = config.root_dir / config.defaults.session_dir
    lines.append(f"log_dir={logs_dir}")
    lines.append(f"session_dir={sessions_dir}")
    return "\n".join(lines)

