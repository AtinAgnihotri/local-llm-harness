from __future__ import annotations

import argparse
from pathlib import Path

from .agent import AgentTask, build_agent_prompt
from .config import load_app_config, resolve_profile
from .doctor import doctor_report
from .llamacpp import build_invocation
from .prompts import build_chat_prompt, load_prompt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="local-harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Inspect local harness configuration.")
    subparsers.add_parser("list-models", help="List configured model profiles.")

    prompt_parser = subparsers.add_parser("prompt", help="Build a one-shot llama.cpp command.")
    prompt_parser.add_argument("--text", required=True, help="User prompt text.")
    prompt_parser.add_argument("--profile", help="Model profile to use.")

    chat_parser = subparsers.add_parser("chat", help="Build an interactive llama.cpp command.")
    chat_parser.add_argument("--profile", help="Model profile to use.")

    agent_parser = subparsers.add_parser("agent", help="Build a coding-agent llama.cpp command.")
    agent_parser.add_argument("--task", required=True, help="Coding task to hand to the model.")
    agent_parser.add_argument("--repo", default=".", help="Repository path for the task.")
    agent_parser.add_argument("--profile", help="Model profile to use.")

    setup_parser = subparsers.add_parser("setup-model", help="Show profile details for local model setup.")
    setup_parser.add_argument("--profile", required=True, help="Profile to inspect.")
    return parser


def _root_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def cmd_list_models() -> str:
    config = load_app_config(_root_dir())
    lines = []
    for profile_name, profile in sorted(config.profiles.items()):
        marker = " [experimental]" if profile.experimental else ""
        lines.append(f"{profile_name}{marker}: {profile.description}")
        lines.append(f"  model_path={profile.model_path}")
        lines.append(f"  prompt_template={profile.prompt_template}")
    return "\n".join(lines)


def _build_prompt_command(user_text: str, profile_name: str | None) -> str:
    config = load_app_config(_root_dir())
    profile = resolve_profile(config, profile_name)
    system_prompt = load_prompt(config.root_dir, profile.prompt_template)
    prompt = build_chat_prompt(system_prompt, user_text, profile.family)
    invocation = build_invocation(config, profile, prompt)
    return invocation.shell_command()


def _build_chat_command(profile_name: str | None) -> str:
    config = load_app_config(_root_dir())
    profile = resolve_profile(config, profile_name)
    invocation = build_invocation(config, profile, None, conversation_mode=True)
    return invocation.shell_command()


def cmd_setup_model(profile_name: str) -> str:
    config = load_app_config(_root_dir())
    profile = resolve_profile(config, profile_name)
    lines = [
        f"profile={profile.name}",
        f"description={profile.description}",
        f"family={profile.family}",
        f"expected_model_path={config.root_dir / profile.model_path}",
        f"prompt_template={config.root_dir / profile.prompt_template}",
        "This repository does not download models automatically.",
        "Download the GGUF file separately and update config/models.local.json if needed."
    ]
    return "\n".join(lines)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "doctor":
        print(doctor_report(load_app_config(_root_dir())))
        return

    if args.command == "list-models":
        print(cmd_list_models())
        return

    if args.command == "prompt":
        print(_build_prompt_command(args.text, args.profile))
        return

    if args.command == "chat":
        print(_build_chat_command(args.profile))
        return

    if args.command == "agent":
        agent_prompt = build_agent_prompt(AgentTask(task=args.task, repo_path=args.repo), _root_dir())
        print(_build_prompt_command(agent_prompt, args.profile))
        return

    if args.command == "setup-model":
        print(cmd_setup_model(args.profile))
        return

    raise SystemExit(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()
