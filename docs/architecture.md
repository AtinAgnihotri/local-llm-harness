# Architecture

## Runtime

`llama.cpp` is the primary inference backend. This repository does not bundle the runtime; it points to a local installation or checkout.

## Layers

- `runner.sh`: user-facing shell entrypoint
- `local_harness.cli`: command parser
- `local_harness.config`: profile and settings loading
- `local_harness.llamacpp`: command generation for `llama.cpp`
- `local_harness.agent`: coding-agent prompt assembly and workflow

## Current command model

- `prompt`: builds a one-shot `llama-cli` command using `-p`
- `chat`: builds an interactive conversation command using `-cnv`
- `agent`: builds a one-shot coding-agent prompt command that can later be evolved into a richer agent workflow

This split keeps the current harness aligned with modern `llama.cpp` behavior.

## Portability

The repository is portable across machines because model files and third-party binaries are configured locally rather than tracked in Git.
