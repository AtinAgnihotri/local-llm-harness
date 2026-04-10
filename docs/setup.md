# Setup Guide

This project is intentionally split into:

- repo-tracked source code and config templates
- machine-local models and binaries

## Expected local directories

- `models/` for GGUF files
- `third_party/llama.cpp/` for a local `llama.cpp` checkout or build
- `logs/` for command and inference logs
- `sessions/` for saved transcripts

## High-level setup flow

1. Create a Python virtual environment and install this repo in editable mode.
2. Build `llama.cpp` with CUDA support.
3. Copy `config/models.example.json` to `config/models.local.json`.
4. Fill in the actual local model paths for Qwen and Gemma.
5. Run `runner.sh doctor`.
6. Run `runner.sh list-models`.
7. Run `runner.sh prompt --text "Write a Python function..."`.

## Recommended initial models

- `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF`
  - recommended file: `qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- `ggml-org/gemma-3-1b-it-GGUF`
  - recommended file: `gemma-3-1b-it-Q4_K_M.gguf`

## Practical notes for this machine

- RTX 3060 Mobile with 6 GB VRAM is a good fit for 7B Q4/Q5 coding models with partial GPU offload.
- `Qwen2.5-Coder 7B Instruct` is the primary coding model because the official Qwen model card positions it for code generation, code reasoning, code fixing, and agent-style usage.
- `Gemma 3 1B IT` is intentionally the lighter secondary profile; Google documents the 1B model as a text-only member of the Gemma 3 family with modest memory requirements.
- If Gemma access is blocked on Hugging Face, make sure you have accepted the Gemma license in the browser first.

## Suggested local paths

- `third_party/llama.cpp/`
- `models/qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- `models/gemma-3-1b-it-Q4_K_M.gguf`

## Notes

- Do not commit GGUF model files.
- Do not commit `llama.cpp` build artifacts.
- Keep experimental uncensored weights in a separate local profile.

## Sources

- `llama.cpp` official repository: <https://github.com/ggml-org/llama.cpp>
- Qwen official GGUF model card: <https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF>
- Gemma 3 overview: <https://ai.google.dev/gemma/docs/core>
- Gemma 3 1B GGUF artifact: <https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF>
