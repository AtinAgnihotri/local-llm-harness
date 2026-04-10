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
7. Run `runner.sh prompt --profile qwen-coder-7b --text "Write a Python function..."`.
8. Run `runner.sh chat --profile qwen-coder-7b` for interactive chat.
9. Run `runner.sh agent --profile qwen-coder-7b --repo . --task "Summarize this repository and propose the next three improvements."`.

## Recommended initial models

- `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF`
  - recommended file: `qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- `ggml-org/gemma-4-E4B-it-GGUF`
  - recommended file: `gemma-4-e4b-it-Q4_K_M.gguf`

## Practical notes for this machine

- RTX 3060 Mobile with 6 GB VRAM is a good fit for 7B Q4/Q5 coding models with partial GPU offload.
- `Qwen2.5-Coder 7B Instruct` is the primary coding model because the official Qwen model card positions it for code generation, code reasoning, code fixing, and agent-style usage.
- `Gemma 4 E4B IT` is the secondary general-purpose profile because Google positions it as laptop-friendly and improved for coding and agentic tasks.
- I could not verify an official `Qwen3-Coder-7B-Instruct-GGUF` release from Qwen. The official Qwen3-Coder announcement centers on `Qwen3-Coder-480B-A35B-Instruct`, which is not viable on this hardware.
- If Gemma access is blocked on Hugging Face, make sure you have accepted the Gemma license in the browser first.

## Suggested local paths

- `third_party/llama.cpp/`
- `models/qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- `models/gemma-4-e4b-it-Q4_K_M.gguf`

## Verified local behavior on the current machine

- `Qwen2.5-Coder 7B Instruct Q4_K_M` loads successfully with CUDA offload at `-ngl 35`.
- Observed generation speed is about `57 tokens/sec` on the RTX 3060 Laptop GPU.
- Interactive conversation works with `-cnv`.
- The one-shot prompt path works correctly for Qwen and the harness generates a valid `llama-cli` command.

## Notes

- Do not commit GGUF model files.
- Do not commit `llama.cpp` build artifacts.
- Keep experimental uncensored weights in a separate local profile.
- Current `llama.cpp` uses `-cnv` for conversation mode. Do not rely on older `-i` examples.
- `runner.sh chat` should generate a pure conversation-mode command, while `runner.sh prompt` should generate a one-shot `-p` command.

## Sources

- `llama.cpp` official repository: <https://github.com/ggml-org/llama.cpp>
- Qwen official GGUF model card: <https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF>
- Qwen3-Coder official announcement: <https://qwenlm.github.io/blog/qwen3-coder/>
- Gemma 4 overview: <https://huggingface.co/google/gemma-4-E4B>
- Gemma 4 E4B GGUF artifact: <https://huggingface.co/ggml-org/gemma-4-E4B-it-GGUF>
