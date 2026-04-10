from __future__ import annotations

from pathlib import Path


def load_prompt(root_dir: Path, relative_path: str) -> str:
    prompt_path = root_dir / relative_path
    return prompt_path.read_text(encoding="utf-8").strip()


def build_chat_prompt(system_prompt: str, user_text: str, family: str) -> str:
    family_name = family.lower()
    if family_name == "gemma":
        return (
            "<start_of_turn>system\n"
            f"{system_prompt}\n"
            "<end_of_turn>\n"
            "<start_of_turn>user\n"
            f"{user_text}\n"
            "<end_of_turn>\n"
            "<start_of_turn>model\n"
        )

    return (
        "<|im_start|>system\n"
        f"{system_prompt}\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{user_text}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )


def conversation_template_flag(family: str) -> str | None:
    family_name = family.lower()
    if family_name in {"qwen", "gemma"}:
        return None
    return None
