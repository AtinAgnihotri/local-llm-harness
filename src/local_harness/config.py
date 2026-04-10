from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Defaults:
    model_profile: str
    ctx_size: int
    threads: int
    temperature: float
    top_p: float
    n_gpu_layers: int
    log_dir: str
    session_dir: str


@dataclass(frozen=True)
class ModelProfile:
    name: str
    family: str
    description: str
    model_path: str
    prompt_template: str
    experimental: bool = False


@dataclass(frozen=True)
class AppConfig:
    root_dir: Path
    defaults: Defaults
    profiles: dict[str, ModelProfile]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_app_config(root_dir: Path) -> AppConfig:
    local_path = root_dir / "config" / "models.local.json"
    example_path = root_dir / "config" / "models.example.json"
    source = local_path if local_path.exists() else example_path
    raw = _read_json(source)

    defaults = Defaults(**raw["defaults"])
    profiles = {
        name: ModelProfile(name=name, **profile_data)
        for name, profile_data in raw["profiles"].items()
    }
    return AppConfig(root_dir=root_dir, defaults=defaults, profiles=profiles)


def resolve_profile(config: AppConfig, profile_name: str | None) -> ModelProfile:
    selected = profile_name or config.defaults.model_profile
    if selected not in config.profiles:
        available = ", ".join(sorted(config.profiles))
        raise SystemExit(f"Unknown model profile '{selected}'. Available: {available}")
    return config.profiles[selected]

