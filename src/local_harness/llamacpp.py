from __future__ import annotations

import shlex
from dataclasses import dataclass
from pathlib import Path

from .config import AppConfig, ModelProfile


@dataclass(frozen=True)
class LlamaInvocation:
    binary_path: str
    command: list[str]

    def shell_command(self) -> str:
        return " ".join(shlex.quote(part) for part in self.command)


def resolve_binary(root_dir: Path) -> Path:
    candidates = [
        root_dir / "third_party" / "llama.cpp" / "build" / "bin" / "llama-cli",
        root_dir / "third_party" / "llama.cpp" / "bin" / "llama-cli",
        root_dir / "third_party" / "llama.cpp" / "llama-cli",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def build_invocation(
    config: AppConfig,
    profile: ModelProfile,
    prompt: str,
    *,
    ctx_size: int | None = None,
    threads: int | None = None,
    temperature: float | None = None,
    top_p: float | None = None,
    n_gpu_layers: int | None = None,
) -> LlamaInvocation:
    binary_path = resolve_binary(config.root_dir)
    defaults = config.defaults
    model_path = config.root_dir / profile.model_path

    command = [
        str(binary_path),
        "-m",
        str(model_path),
        "-c",
        str(ctx_size or defaults.ctx_size),
        "--threads",
        str(threads or defaults.threads),
        "--temp",
        str(temperature if temperature is not None else defaults.temperature),
        "--top-p",
        str(top_p if top_p is not None else defaults.top_p),
        "-ngl",
        str(n_gpu_layers if n_gpu_layers is not None else defaults.n_gpu_layers),
        "-p",
        prompt,
    ]
    return LlamaInvocation(binary_path=str(binary_path), command=command)

