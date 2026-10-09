# Intel Arc Pro B65: local LLM inference on 1-4 cards (raw data)

Date: 2026-09-16 to 2026-10-05 (measured).

Verdict: Raw results and GPU/host telemetry behind https://b65.thekaiser.us. Four Arc Pro B65s run Qwen3.8-27B INT4 at up to 105.9 tok/s for one user (TP=4, MTP-2) and about 830 tok/s total at 32 users (four replicas); this folder holds every measured value and sensor trace those figures come from.

## Environment

4 x Intel Arc Pro B65 32 GB (ASRock), 200 W power cap each; AMD EPYC 7343 (16 cores), Supermicro H12SSL-NT, 499 GiB RAM; bare metal; Ubuntu 26.04.1, kernel 7.0.0-31-generic. Each card sits behind its own PCIe switch at 16 GT/s x16. Engines: Intel `llm-scaler-vllm` 0.26.0-b1 and 0.26.0-b2, upstream `vllm/vllm-openai-xpu` v0.31.0, llama.cpp SYCL and Vulkan; image digests are in `results/cells.csv`. Current retail price $1,199.99 per card; no sponsorship.

## Measurements

Speed tests send 1,024 random tokens and force 512 output tokens, at 1 to 32 concurrent users, thinking off, 3-5 repetitions after a discarded warm-up. `results/` holds every value with its aggregation, `n` and status; `telemetry/` holds the sensor traces sampled during each run. See README.md for every file.

## Reproduction

Benchmark: `vllm bench serve --dataset-name random --random-input-len 1024 --random-output-len 512 --ignore-eos --temperature 0 --seed 42` against each server configuration described in `results/cells.csv`. Verify this folder with `sha256sum -c SHA256SUMS`.

## Limitations

Power is GPU-reported (no wall meter); temperatures are absolute sensor readings (no ambient sensor). Logs, per-request records and prompts are not published. Results apply to this host, these engine versions and these models; quality was measured at task level only.

## Evidence

[README.md](README.md) links every file in `results/` and `telemetry/`.
