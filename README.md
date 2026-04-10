# localLLM

Private, offline-first local LLM harness and CLI coding agent built around `llama.cpp`.

## Goals

- Keep inference local and reproducible.
- Support multiple model profiles without committing model weights.
- Prefer privacy/offline operation over convenience.
- Provide a shell-first interface for chat, prompts, system checks, and coding-agent workflows.

## Planned Model Profiles

- `qwen-coder-7b`: default coding profile
- `gemma-small-it`: secondary general-purpose profile
- `qwen-coder-7b-exp`: optional future experimental profile for uncensored/abliterated weights

Recommended starting artifacts:

- `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF` with `qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- `ggml-org/gemma-4-E4B-it-GGUF` with `gemma-4-e4b-it-Q4_K_M.gguf`

Why this split:

- `Qwen2.5-Coder-7B-Instruct-GGUF` remains the default coding model because it is an official code-specialized GGUF release from Qwen and is explicitly positioned for code generation, code reasoning, code fixing, and code-agent workflows.
- `Gemma 4 E4B` is the better secondary general-purpose profile than the earlier Gemma 3 1B placeholder because Google positions Gemma 4 E4B as a stronger laptop-friendly model with improved coding and agentic capabilities.

## Repository Layout

- `runner.sh`: shell-first entrypoint
- `pyproject.toml`: Python package metadata
- `src/local_harness/`: Python CLI, config, adapter, and agent code
- `config/models.example.json`: portable model profile template
- `prompts/`: reusable prompt templates
- `docs/`: setup, architecture, and workflow notes

Useful docs:

- setup: [docs/setup.md](/home/atinagnihotri/work_repos/localLLM/docs/setup.md)
- prerequisites: [docs/prerequisites.md](/home/atinagnihotri/work_repos/localLLM/docs/prerequisites.md)
- upgrade path: [docs/model-upgrade-path.md](/home/atinagnihotri/work_repos/localLLM/docs/model-upgrade-path.md)

## What Stays Out Of Git

- model weights
- downloaded `llama.cpp` source/build outputs
- logs and local transcripts
- caches and virtual environments
- machine-specific config overrides

## Next Steps

1. Create a virtual environment and install the local package.
2. Build `llama.cpp` locally with CUDA support.
3. Copy `config/models.example.json` to `config/models.local.json` and fill in your local model paths.
4. Download the selected GGUF models separately into a local `models/` directory.
5. Use `runner.sh doctor` and `runner.sh list-models` to verify the local install.
6. Use `runner.sh prompt` for one-shot prompts.
7. Use `runner.sh chat --profile qwen-coder-7b` for interactive conversation mode.
8. Use `runner.sh agent` to generate a coding-agent prompt command.
6. For current `llama.cpp`, interactive chat uses conversation mode (`-cnv`).

Detailed command-by-command setup lives in [docs/setup.md](/home/atinagnihotri/work_repos/localLLM/docs/setup.md).
