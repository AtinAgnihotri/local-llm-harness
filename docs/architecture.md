# Architecture

## Runtime

`llama.cpp` is the primary inference backend. This repository does not bundle the runtime; it points to a local installation or checkout.

## Layers

- `runner.sh`: user-facing shell entrypoint
- `local_harness.cli`: command parser
- `local_harness.config`: profile and settings loading
- `local_harness.llamacpp`: command generation for `llama.cpp`
- `local_harness.agent`: coding-agent prompt assembly and workflow

## Portability

The repository is portable across machines because model files and third-party binaries are configured locally rather than tracked in Git.

