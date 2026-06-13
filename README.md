<p align="center">
  <img src="images/favicon.svg" width="64" alt="LLM Deep Learning">
</p>

<h1 align="center">LLM Deep Learning</h1>

<p align="center">
  <strong>Starting from code, 11 chapters to build a complete large language model engineering system</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/chapters-11-orange" alt="11 chapters">
  <img src="https://img.shields.io/badge/exercises-programming_+_written-blue" alt="programming and written exercises">
  <img src="https://img.shields.io/badge/sections-127-yellow" alt="127 sections">
  <img src="https://img.shields.io/badge/frontier-architecture_cases-green" alt="frontier architecture cases">
  <img src="https://img.shields.io/badge/iPad_Pro-optimized-purple" alt="iPad Pro">
  <img src="https://img.shields.io/badge/db-IndexedDB-red" alt="IndexedDB">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="license">
</p>

---

## About This Course

This is a **code-first** hands-on LLM course. Instead of browsing concepts, it implements every core component of a large language model line by line using Python and PyTorch. Necessary foundations in math, PyTorch, ML, and systems are not separated into side tracks but are integrated into the prerequisites at the beginning of each chapter, the implementations within the chapter, and the validation signals.

**Learning loop for each chapter:**
> Deep theory → Understand the "why" → Programming exercises (you write code) → Compare with reference solutions → Consolidate with conceptual exercises

Incorporates industrial-grade architecture cases such as MLA, MoE, GRPO/DAPO/GSPO, FP8, sparse/compressed attention, learnable residual connections, using them to understand the engineering bottlenecks behind each component, rather than chasing the specifications of individual model versions.

## How Beginners Should Learn

This course covers the complete pipeline from basic components to industrial frontiers. When learning for the first time, don't treat all advanced topics as mandatory. Follow a three-pass reading rhythm:

| Phase | Chapters | Goal | Suggestion |
|------|----------|------|------------|
| First Pass: Main Line Required | Ch01-Ch06 | Turn text into tokens, build a GPT that can forward propagate | Must write code exercises; for DeepSeek extensions, just understand the motivation |
| Second Pass: Make it Run | Ch07-Ch08 | Train a small model and make it generate text | Focus on the input/output shapes of loss, optimizer, sampling |
| Third Pass: Advanced Selective Reading | Ch09-Ch10 | Fine-tuning, alignment, RAG, inference optimization, and frontier architectures | First grasp the concept map, then go back to fill in formulas and engineering details |

**Minimum Prerequisites:** Know Python functions, lists/dictionaries, basic matrix multiplication, and the `shape` of PyTorch tensors. If math derivations are difficult initially, first grasp "what is the input, what is the output, how does the shape change" for each section. Math, PyTorch, statistics, and system knowledge are only expanded upon when needed by the chapter tasks; the appendix is for reference and does not require prior study.

## LLM Knowledge System

This course is organized around "how large models are represented, computed, trained, generated, aligned, and deployed," not around scattered tools:

| Module | Corresponding Chapters | Core Question |
|--------|------------------------|---------------|
| Representation Layer | Ch01-Ch02 | How text becomes tokens, how tokens become vectors, how the model obtains positional information |
| Transformer Core | Ch03-Ch06 | How attention, mask, multi-head, GQA/MLA, Norm, FFN, MoE, and GPT forward propagation combine |
| Training Loop | Ch07 | Why next-token prediction is equivalent to maximum likelihood, how loss, PPL, optimizer, checkpoint/resume integrity, and distributed training gates work |
| Generation & Inference | Ch08-Ch10 | How prefill/decode, sampling, speculative decoding, KV Cache, FlashAttention, RAG, multimodal serving, and inference services trade off |
| Fine-tuning & Alignment | Ch09 | How SFT chat template/mask/packing gates, preference data gates, LoRA, preference modeling, DPO, GRPO/DAPO/GSPO, RLVR/RFT change model behavior |
| Classic NLP & Evaluation | Week 8 Topic / Ch11 Assignments | How RNN/LSTM, dependency parsing, seq2seq, BERT/MLM, BLEU/ROUGE/F1/EM connect to modern LLMs |
| Frontier Engineering Cases | Ch04-Ch10 | What engineering bottlenecks designs like MLA, MoE, FP8, GRPO/DAPO/GSPO, sparse/compressed attention, dynamic-resolution vision, and multimodal serving solve |

The key to university-level course quality is not the quantity of materials, but that every knowledge point can answer three things:

- Mathematically, what problem does it solve, and what is each quantity in the formula.
- In code, how does it translate to PyTorch tensors, shapes, masks, dtypes, and gradients.
- In engineering, what cost, speed, quality, or stability trade-offs does it introduce.

## In-Chapter Foundations

Foundational knowledge appears in place according to chapter tasks. Each chapter begins with "Prerequisites, In-Chapter Internalization, Validation Signal," and assignments and written questions ground these foundations in runnable code or reproducible derivations.

| Chapter | In-Chapter Foundations | Directly Served Engineering Judgments |
|---------|------------------------|----------------------------------------|
| Ch01-Ch02 | Python data structures, matrix lookup, vector dot product, positional rotation, and shape trace | Token cost, embedding parameters, context utilization, and prefix cache prerequisites |
| Ch03-Ch05 | Softmax, mask, broadcasting, matrix multiplication, normalization, residual paths, and resource estimation | Attention correctness, GQA/MLA memory benefits, block stability, and FLOPs budget |
| Ch06-Ch07 | Autoregressive probability decomposition, cross entropy, optimizer state, randomness, and experimental statistics | GPT assembly, training curve interpretation, checkpoint/resume integrity, data gates, and scaling decisions |
| Ch08-Ch09 | Logits distribution, sampling variance, KL/reference model, chat template, assistant mask, preference data, and reward assumptions | Generation strategy deployment, reasoning budget, SFT/DPO/GRPO quality and safety boundaries |
| Ch10 | Queuing, memory/bandwidth, KV cache, quantization calibration/regression, stress test metrics, RAG retrieval metrics, context engineering, model routing, admission control, release gates, and overload response | TTFT/TPOT/P95, quantization release gate, context engineering gate, model routing gate, continuous batching admission, P/D decoupling, capacity planning, canary/control, load shedding, and fallback |
| Ch11 | Sequence modeling, structured prediction, encoder-only, traditional metrics, judge reliability, and agent/workflow evaluation | Choosing generation/extraction/ranking/structured decoding, determining if final answer, trajectory, state, safety, and cost evidence support deployment conclusions |

Supplementary learning materials:

- [Weekly Reading Handout](docs/reading-list.html): Paper reading, key questions, and chapter connections.
- [Written Derivation & Concept Problem Set](docs/written-problem-set.html): Formula derivation, complexity analysis, and concept differentiation.
- [Worked Example Pack](docs/worked-example-pack.html): Reproducible small examples for BPE, RoPE, attention, GQA, Norm, AdamW, SFT mask/packing, DPO, KV cache, etc.
- [Classic NLP Topic Handout](docs/classic-nlp-handout.html): Relationship between RNN/LSTM, dependency parsing, seq2seq/NMT, BERT, BLEU/ROUGE/F1/EM and modern LLMs.

Chapter assignment entry points: [assignments/ch01_bpe/](assignments/ch01_bpe/) · [assignments/ch02_embeddings/](assignments/ch02_embeddings/) · [assignments/ch03_attention/](assignments/ch03_attention/) · [assignments/ch04_multihead/](assignments/ch04_multihead/) · [assignments/ch05_block/](assignments/ch05_block/) · [assignments/ch06_gpt/](assignments/ch06_gpt/) · [assignments/ch07_training/](assignments/ch07_training/) · [assignments/ch08_generation/](assignments/ch08_generation/) · [assignments/ch09_alignment/](assignments/ch09_alignment/) · [assignments/ch10_inference/](assignments/ch10_inference/) · [assignments/ch11_classic_nlp/](assignments/ch11_classic_nlp/).

## Capability Path for LLM Inference Engineers

If your goal is to become an LLM inference engineer, the learning objective is not just "understanding Transformers," but being able to serve the model stably, cost-effectively, and observably to real users. The course is organized by the following capabilities:

| Capability | Corresponding Chapters | What You Need to Be Able to Do |
|------------|------------------------|--------------------------------|
| Model Architecture Understanding | Ch01-Ch06 | Understand tokenizer, attention, KV Cache origin, logits output, and parameter scale |
| Generation & Latency Decomposition | Ch08 | Distinguish prefill/decode, explain TTFT, TPOT, TPS, throughput, sampling quality, and reasoning budget |
| Memory & Bandwidth Optimization | Ch04, Ch10 | Calculate KV Cache, understand MQA/GQA/MLA, weight-only/W8A8/KV cache quantization, FlashAttention, and memory bottlenecks |
| Inference Service Architecture | Ch10 | Choose vLLM/SGLang/TensorRT-LLM/llama.cpp, understand MoE expert parallelism, model routing/cascade, continuous batching admission, prefix cache, concurrent scheduling, load shedding, observability trace, speculative decoding, multimodal serving, tool-call, MCP runtime security, agent trace, and context engineering |
| Retrieval & Tool Calling | Ch08-Ch10 | Design structured output, RAG, Agent toolchain, context compression/memory, and failure fallback |
| Evaluation & Deployment | Ch09-Ch11 | Design quality/safety/latency/cost metrics, perform agent/workflow eval, stress testing, regression evaluation, canary/control release, and rollback checks |

## Capability Path for LLM Training Engineers

If your goal is to become an LLM training engineer, the learning objective should advance from "being able to run a loss" to "being able to deliver a reproducible, recoverable, observable, and cost-explainable training system." The course is organized by the following capabilities:

| Capability | Corresponding Chapters | What You Need to Be Able to Do |
|------------|------------------------|--------------------------------|
| Data & Token Budget | Ch01, Ch07 | Analyze samples, duplication, quality filtering, eval contamination, domain mixing, length distribution, and token scale; estimate training steps |
| Training Loop Engineering | Ch06-Ch07 | Organize PyTorch Dataset/DataLoader, forward, loss, backward, optimizer, scheduler |
| Stability & Recovery | Ch07 | Use seed, grad clipping, checkpoint integrity, distributed resume, and anomaly troubleshooting to protect training |
| Monitoring & Evaluation | Ch07-Ch09 | Record train_loss, val_loss, ppl, lr, grad_norm, tokens/s, and interpret curves |
| Fine-tuning & Alignment | Ch09 | Distinguish data formats, losses, rollout logs, and applicable scenarios for SFT/preference data gates, LoRA, DPO, GRPO/DAPO/GSPO, RLVR/RFT |
| Distribution & Cost | Ch07, Ch10 | Understand AMP, FSDP/ZeRO, global batch tokens, MFU, GPU hours, distributed checkpoint, checkpoint storage, and scale rehearsal |

## Quick Start

### Local Development

```bash
git clone https://github.com/garry-x/llm-course.git && cd llm-course

./serve.sh                    # Default 0.0.0.0:8080
./serve.sh serve -p 3000      # Specify port
```

### Running Assignment Tests

This repository recommends using `.venv` in the root directory to run local code; if you have already activated an equivalent virtual environment, you can also replace `.venv/bin/python` with `python`. First confirm PyTorch is importable:

```bash
.venv/bin/python -c "import sys, torch; print(sys.version.split()[0], torch.__version__)"
.venv/bin/python run_assignment_tests.py
```

### CLI Command Overview

| Command | Description | Supports `-p` |
|---------|-------------|:-------------:|
| `serve` | Local Python HTTP server | ✓ |

**Environment Requirements:** Python 3.10+ / Modern browser (Safari / Chrome / Edge); iPad Pro or desktop reading recommended.

## Course Outline

| # | Chapter | Programming Output | Exercises |
|---|---------|--------------------|:---------:|
| 1 | **Environment Setup & Tokenization** — Implement BPE Tokenizer | `BPETokenizer` ~80 lines | 5+5 |
| 2 | **Embedding Layer & Positional Encoding** — TokenEmbedding + RoPE + Introduction to In-Context Learning | `TokenEmbedding` + `RoPE` ~60 lines | 4+5 |
| 3 | **Single-Head Self-Attention** — Scaled Dot-Product Attention | `ScaledDotProductAttention` ~40 lines | 5+5 |
| 4 | **Multi-Head Attention & MLA** — MHA → GQA → DeepSeek MLA | `MultiHeadAttention` ~60 lines | 5+5 |
| 5 | **Transformer Block** — RMSNorm + FFN/SwiGLU + mHC | `TransformerBlock` ~50 lines | 5+5 |
| 6 | **Assemble GPT + DeepSeekMoE** — GPT-2 124M Complete Model | `GPTModel` ~100 lines | 5+5 |
| 7 | **Training Loop** — AdamW/Muon + FP8/MXFP8 + Distributed Strategy Ledger | Complete training script + strategy/gate report | 7+5 |
| 8 | **Text Generation** — Sampling strategies + reasoning budget + MTP speculative decoding + constrained generation | Text generator + test-time compute gate | 7+5 |
| 9 | **Fine-tuning & Alignment** — SFT/preference data/synthetic distillation/LoRA/DPO/GRPO/DAPO/GSPO/RLVR + R1 reasoning | SFT protocol, post-training data audit, LoRA, DPO/GRPO/RLVR, reasoning RL logs, and distillation data quality analysis | 8+5 |
| 10 | **Inference Optimization & Frontiers** — KV Cache/quantization release gate/RAG/Context Engineering/Structured Output/Tool/MCP Gate/vLLM/Triton/MoE serving/Model routing/Production release/Long context/Multimodal | KV Cache + quantization calibration/regression + RAG + context engineering gate + structured output gate + Tool/MCP Gate + MoE serving gate + model routing gate + rollout gate + overload response + continuous batching admission + P/D pool plan + speculative gate + long-context gate + LSH + service blueprint | 11+5 |
| Topic | **Classic NLP & Evaluation** — RNN/LSTM / dependency parsing / seq2seq / BERT / metrics / agent workflow eval | RNN gradient path + UAS/LAS + BLEU/ROUGE/EM/F1 + judge audit + agent eval protocol + MLM mask | Ch11 |

> **Total: Covers 11 chapters of programming assignments, written derivation problems, and classic NLP topic assignments.**

## DeepSeek Technology Integration

The table below is for establishing a technology map. Please open and read the original papers and model cards when studying the corresponding chapters.

| Technology | Corresponding Chapter | Learning Focus |
|------------|-----------------------|----------------|
| MLA (Multi-head Latent Attention) | Ch04 | KV Cache compression, latent vector RoPE decoupling |
| GRPO (Group Relative Policy Optimization) | Ch09 | No Critic needed, intra-group whitening advantage, RL incentivizes reasoning ability |
| DAPO / GSPO | Ch09 | Dynamic sampling, length control, sequence-level ratio, and MoE RL stability diagnosis |
| RLVR / RFT | Ch09 | Train reasoning with verifiable graders, and check reward signal, cost, and hacking risks |
| DeepSeekMoE + Aux-Loss-Free | Ch06 | Sparse activation, expert routing, and dynamic bias load balancing |
| FP8 Mixed Precision + DualPipe | Ch07 | Low-precision training, scaling strategy, communication computation overlap |
| MTP (Multi-Token Prediction) | Ch08 | Training auxiliary objective and speculative decoding draft signal || DSA / CSA / HCA | Ch10 | Long-context sparse attention and KV/computation cost compression |
| Engram external memory | Ch10 | Differences between model external memory, LSH retrieval, and RAG |
| mHC (Manifold-Constrained Hyper-Connections) | Ch05 | Birkhoff constraint, Sinkhorn-Knopp, and residual connection extension |
| Muon Optimizer | Ch07 | Momentum matrix orthogonalization and large-scale optimizer design |

## Repository Structure

```
llm-course/
├── index.html                # Course homepage: Hero + Dashboard + Chapter directory
├── css/style.css              # Warm editorial style, dark/light dual theme
├── js/
│   ├── db.js                  # IndexedDB persistent storage layer
│   └── app.js                 # Search/theme/font size/progress/notes/TOC/keyboard navigation
├── chapters/                  # 11 chapters, pure HTML
│   └── ch01.html ~ ch11.html
├── docs/
│   ├── reading-list.md          # Weekly paper and technical report reading
│   ├── written-problem-set.md   # Written derivations and conceptual problems
│   ├── worked-example-pack.md   # Reproducible small examples
│   ├── math-prerequisites.md    # Mathematical prerequisites
│   └── classic-nlp-handout.md   # Classic NLP topics
├── images/                    # 11 SVG concept diagrams + favicon (supports dark mode)
│   ├── bpe-pipeline.svg       # BPE training and encoding/decoding pipeline
│   ├── rope-rotation.svg      # RoPE rotary position encoding principle
│   ├── attention-flow.svg     # Scaled Dot-Product Attention data flow
│   ├── transformer-arch.svg   # GPT architecture overview
│   ├── mha-gqa-mla.svg        # MHA / GQA / MLA KV Cache compression comparison
│   ├── transformer-block.svg  # Transformer Block internal structure
│   ├── gpt-params.svg         # GPT-2 124M parameter breakdown
│   ├── training-loop.svg      # Training loop + optimizer evolution
│   ├── sampling-strategies.svg# Comparison of 4 sampling strategies
│   ├── rlhf-dpo-grpo.svg      # RLHF / DPO / GRPO alignment method comparison
│   ├── gpu-memory.svg         # GPU memory hierarchy — A100 architecture
│   └── favicon.svg/.png/.ico  # Generated by ComfyUI + FLUX.1-dev
├── serve.sh                   # CLI: local static server
└── README.md
```

## Content Maintenance Principles

The homepage and README only retain the course main line, chapter entry points, and how to run. Papers, technical reports, and tool documentation are not listed on the homepage; instead, they enter the corresponding chapters and the [weekly reading material handout](docs/reading-list.html), requiring students to map reading conclusions back to formulas, code, system metrics, or chapter judgments.

When extending course content in the future, prioritize following three rules:

- New concepts must enter the objective function, tensor shape, system metric, or evaluation protocol of the relevant chapter; no isolated remedial paths are added.
- Cutting-edge cases must explain the engineering bottleneck they solve, the prerequisite knowledge they depend on, the applicable boundary, and reported evidence.
- The homepage only answers "How does this course systematically train training/inference engineers?" and does not serve as a resource navigation station or product feature description.