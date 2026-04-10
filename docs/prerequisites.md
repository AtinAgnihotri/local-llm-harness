# Prerequisites and Bootstrap Commands

This file records the command-line setup needed to get this repository into a usable state on a fresh Ubuntu machine similar to the current laptop.

## 1. System packages

Install the basic build toolchain and utilities:

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake ninja-build git curl pkg-config
```

## 2. Python environment

Create a local virtual environment and install the repo in editable mode:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## 3. Working directories

Create the local machine-only directories used by the harness:

```bash
mkdir -p third_party models logs sessions
```

## 4. Fetch llama.cpp

Clone the official `llama.cpp` repository into the local third-party directory:

```bash
git clone https://github.com/ggml-org/llama.cpp third_party/llama.cpp
```

## 5. CUDA toolkit validation

The NVIDIA driver alone is not enough; `llama.cpp` CUDA builds require the CUDA toolkit and `nvcc`.

Useful validation commands:

```bash
which nvcc
nvcc --version
```

If `nvcc` is missing, install the toolkit:

```bash
sudo apt-get update
sudo apt-get install -y nvidia-cuda-toolkit
```

## 6. Build llama.cpp with CUDA

Configure and build `llama.cpp` with CUDA enabled:

```bash
cmake -S third_party/llama.cpp -B third_party/llama.cpp/build -G Ninja -DGGML_CUDA=ON -DCUDAToolkit_ROOT=/usr -DGGML_NATIVE=ON
cmake --build third_party/llama.cpp/build --config Release -j
```

Successful builds should produce `third_party/llama.cpp/build/bin/llama-cli`.

Verify with:

```bash
third_party/llama.cpp/build/bin/llama-cli --version
```

## 7. Harness config bootstrap

Copy the example model config into a local machine-specific file:

```bash
cp config/models.example.json config/models.local.json
chmod +x runner.sh
```

## 8. Optional: Hugging Face CLI for model downloads

Install the Hugging Face Hub package inside the venv. Use the `hf` command, not the deprecated `huggingface-cli` command:

```bash
. .venv/bin/activate
pip install -U huggingface_hub
```

## Notes

- Do not commit model files, build artifacts, logs, or sessions.
- NCCL warnings are safe to ignore on a single-GPU laptop.
- OpenSSL warnings during `llama.cpp` configure do not block local `llama-cli` usage.
- Models are downloaded separately per machine and configured through `config/models.local.json`.
- `huggingface-cli` is deprecated; use `hf` instead.
