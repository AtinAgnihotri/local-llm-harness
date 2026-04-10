# Model Upgrade Path

This document records how to evolve the local harness beyond the initial stable baseline without disrupting the default working setup.

## Current stable baseline

- Primary coding model:
  - `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF`
  - recommended file: `qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- Secondary general model:
  - `ggml-org/gemma-4-E4B-it-GGUF`
  - recommended file: `gemma-4-e4b-it-Q4_K_M.gguf`

These are the default profiles because they are practical on the current hardware and align with the repo goals:

- privacy/offline first
- coding quality second
- speed/ease third

## Why upgrades should be deliberate

For this repository, model upgrades are not just “newer is better.” A candidate upgrade should be checked for:

- official availability in a usable local format such as `GGUF`
- compatibility with `llama.cpp`
- good prompt-template behavior
- realistic fit for the current machine
- improvement on coding or agent tasks that matter for this repo

## Low-risk upgrade categories

### 1. Better quantization of the same model

Safest path:

- keep the same profile name
- swap `Q4_K_M` for `Q5_K_M` or similar if memory and speed remain acceptable
- rerun local smoke tests

Use this when:

- quality is good but you want a modest improvement
- the machine still has enough RAM and VRAM headroom

### 2. Newer small general model

Good path for the secondary profile:

- replace the Gemma secondary model with a newer small or laptop-friendly general model
- keep the coding model unchanged

Use this when:

- you want better general chat, reasoning, or multilingual behavior
- the coding workflow is already stable

### 3. Newer coder-specialized 7B class model

Best candidate for a future primary-model upgrade:

- add a new profile first
- benchmark it against `qwen-coder-7b`
- only switch the default after the new model proves better for coding-agent tasks

Use this when:

- an official small coder model becomes available in `GGUF`
- the model shows clear gains in code generation, editing, and tool-use behavior

## Recommended future candidates

### Candidate: official small Qwen3-Coder release

If Qwen publishes an official small `Qwen3-Coder` model in a local-friendly form:

- add a new profile rather than replacing `qwen-coder-7b` immediately
- compare it on:
  - repo summarization
  - code editing
  - debugging
  - shell-command suggestion quality
  - repetition/refusal behavior

Recommended rollout:

1. add `qwen3-coder-7b` as a new profile
2. keep `qwen-coder-7b` as default
3. benchmark both locally
4. switch default only after validation

### Candidate: newer Gemma family release

If Google releases a stronger small local model:

- update the secondary profile first
- keep the coding baseline unchanged until side-by-side comparison is done

### Candidate: experimental uncensored profile

If later you want a Heretic or abliterated profile:

- keep it opt-in
- store it under an experimental profile name
- never replace the stable default automatically

## How to add a new model profile

1. Download the new GGUF locally into `models/`.
2. Add a new entry to `config/models.local.json`.
3. If the profile is intended to be portable, mirror it in `config/models.example.json`.
4. Set:
   - `family`
   - `description`
   - `model_path`
   - `prompt_template`
   - optional `experimental`
5. Run:
   - `./runner.sh doctor`
   - `./runner.sh list-models`
   - `./runner.sh setup-model --profile <new-profile>`
   - `./runner.sh prompt --profile <new-profile> --text "..."`

## When not to switch defaults

Do not change the default coding profile just because a model is:

- newer
- trending
- benchmarked for general reasoning
- available only in non-official or unclear quantizations

Change the default only when the new model is:

- reproducible locally
- stable with `llama.cpp`
- better on the actual coding-agent tasks this repo cares about

## Current recommendation

Keep:

- `qwen-coder-7b` as the default coding profile
- `gemma-small-it` as the secondary Gemma profile, currently backed by `Gemma 4 E4B`

Add future models as side-by-side profiles first, then promote only after local validation.
