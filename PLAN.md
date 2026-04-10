# localLLM Plan and Implementation Handoff

This file is the project handoff and resume point for future work in this repository, including continuation in a different chat or with a different AI tool.

## Project goal

Build a private, offline-first local LLM harness and local coding agent around `llama.cpp`, with:

- `Qwen2.5-Coder 7B Instruct` as the primary coding model
- `Gemma 4 E4B` as the secondary general-purpose model
- a portable Git repository that can be cloned across machines
- model files and third-party binaries kept out of Git
- a path for future experimental uncensored / Heretic-derived profiles

## Hardware baseline

Current validated machine:

- Ubuntu `25.10`
- AMD Ryzen `7 5800H`
- `27 GiB` RAM
- NVIDIA RTX `3060 Laptop GPU` with `6 GiB` VRAM
- `500+ GiB` free storage

Observed local inference behavior:

- `llama.cpp` built successfully with CUDA
- `Qwen2.5-Coder 7B Instruct Q4_K_M` loads successfully
- `Gemma 4 E4B Q4_K_M` is downloaded and configured
- Qwen interactive conversation works with `-cnv`
- Observed Qwen generation speed is about `57 tokens/sec`
- Qwen worked with `-ngl 35` on this GPU

## Core decisions

### Runtime

- Use `llama.cpp` directly as the primary inference backend.
- Do not use Ollama in the baseline architecture.
- Keep compatibility with possible future adapters, but stay `llama.cpp`-first.

### Models

- Primary coding model:
  - `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF`
  - file: `qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- Secondary general model:
  - `ggml-org/gemma-4-E4B-it-GGUF`
  - file: `gemma-4-e4b-it-Q4_K_M.gguf`
- Experimental placeholder:
  - `qwen-coder-7b-exp`

### Privacy and portability

- The repo stores code, prompts, docs, and config templates.
- The repo does not store:
  - GGUF models
  - `llama.cpp` build artifacts
  - logs
  - transcripts
  - caches
  - virtual environments

### Unsloth

- Not part of the baseline implementation.
- Worth considering later for fine-tuning, custom quantization workflows, or export pipelines.
- Not needed for current local inference and initial agent setup.

## What is already implemented

### Repo structure

- `.gitignore`
- `README.md`
- `PLAN.md`
- `pyproject.toml`
- `runner.sh`
- `config/models.example.json`
- `config/models.local.json`
- `prompts/coder_system.txt`
- `prompts/general_system.txt`
- `docs/setup.md`
- `docs/prerequisites.md`
- `docs/architecture.md`
- `docs/model-upgrade-path.md`

### Python harness

Under `src/local_harness/`:

- `config.py`
  - loads defaults and model profiles
- `prompts.py`
  - builds one-shot prompts
- `llamacpp.py`
  - constructs `llama-cli` commands
- `agent.py`
  - builds a first-pass coding-agent prompt
- `doctor.py`
  - checks binary/model/prompt presence
- `cli.py`
  - command surface for `doctor`, `list-models`, `prompt`, `chat`, `agent`, `setup-model`

### Current command behavior

- `./runner.sh doctor`
  - validates local config and presence of binary/models/prompts
- `./runner.sh list-models`
  - lists configured profiles
- `./runner.sh prompt --profile ... --text "..."`
  - prints a one-shot `llama-cli` command using `-p`
- `./runner.sh chat --profile ...`
  - prints a conversation-mode `llama-cli` command using `-cnv`
- `./runner.sh agent --profile ... --repo ... --task "..."`
  - prints a one-shot coding-agent prompt command

These commands currently print the command to run; they do not execute it automatically.

## What has been validated manually

- CUDA toolkit installed and `nvcc` available
- `llama.cpp` cloned and built locally
- `llama-cli` exists and runs
- Qwen model downloaded locally
- Gemma model downloaded locally
- Qwen one-shot prompt works
- Qwen interactive chat works with `-cnv`

## Important lessons already learned

- Current `llama.cpp` conversation mode uses `-cnv`, not `-i`
- `huggingface-cli` is deprecated; use `hf`
- `LLAMA_CURL` warning can be ignored in current builds
- NCCL warning can be ignored on a single-GPU laptop
- OpenSSL warning during configure does not block local `llama-cli` inference

## Current known limitations

- `prompt`, `chat`, and `agent` only print commands; they do not execute them
- no session logging or transcript persistence yet
- no benchmark/tuning command yet
- agent mode does not yet gather repository context automatically
- no tool execution layer yet
- no structured approval workflow for proposed commands yet
- no actual file-editing agent loop yet
- experimental uncensored profile is only a placeholder

## Next recommended implementation steps

### 1. Add execution mode

Extend the CLI so `prompt`, `chat`, and `agent` can optionally execute the generated command.

Suggested behavior:

- default: print command only
- optional flag: `--execute`
- keep manual/print-only mode for safety and reproducibility

### 2. Add session and transcript logging

Add machine-local logging under:

- `logs/`
- `sessions/`

Suggested scope:

- generated command
- timestamp
- selected profile
- task or prompt text
- optional captured output path

### 3. Improve agent context ingestion

Upgrade `agent` from a prompt wrapper into a repo-aware helper.

Suggested additions:

- include top-level repo file listing
- include a small set of relevant file contents
- include git status if available
- include an option to point at specific files

### 4. Add benchmark and tuning command

Add a command to help tune:

- `-ngl`
- context size
- thread count
- approximate prompt/gen speed

Suggested command:

- `./runner.sh benchmark --profile qwen-coder-7b`

### 5. Add controlled command proposal workflow

The coding agent should eventually:

- inspect repo context
- propose file changes
- propose shell commands
- wait for user approval before running anything

This is especially important because the intended workflow is:

- the repo can be edited by the harness
- terminal commands are handed to the user unless explicit execution is enabled

### 6. Add optional experimental profile workflow

Later work:

- define how Heretic or other abliterated models are registered
- keep them opt-in
- benchmark them separately
- do not replace the stable coding default automatically

## Suggested future architecture direction

Near-term target:

- local harness
- stable profile management
- command execution toggle
- logging
- repo-aware agent prompts

Medium-term target:

- lightweight local coding agent with:
  - repo context ingestion
  - shell command proposal
  - editable plans
  - transcript persistence

Longer-term target:

- optional local API layer
- optional editor integration
- optional Unsloth-based fine-tuning workflow
- optional uncensored experimental profile path

## Recommended next commands for a future operator

These are expected to work on the current machine:

```bash
./runner.sh doctor
./runner.sh list-models
./runner.sh prompt --profile qwen-coder-7b --text "Write a Python function that returns the factorial of n."
./runner.sh chat --profile qwen-coder-7b
./runner.sh agent --profile qwen-coder-7b --repo . --task "Summarize this repository and propose the next three improvements."
```

## Related docs

- [README.md](/home/atinagnihotri/work_repos/localLLM/README.md)
- [docs/setup.md](/home/atinagnihotri/work_repos/localLLM/docs/setup.md)
- [docs/prerequisites.md](/home/atinagnihotri/work_repos/localLLM/docs/prerequisites.md)
- [docs/architecture.md](/home/atinagnihotri/work_repos/localLLM/docs/architecture.md)
- [docs/model-upgrade-path.md](/home/atinagnihotri/work_repos/localLLM/docs/model-upgrade-path.md)
