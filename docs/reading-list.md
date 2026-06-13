# Weekly Reading Handout

This handout organizes the reading materials for the 10-week course by chapter and task. It is not an independent remedial path; each reading must be tied back to chapter code, written assignments, or chapter judgments. Readings are divided into three categories:

- Required: Default dependencies for class discussions and assignments.
- Optional: For projects, reports, or deeper understanding.
- Course Connections: Used to map objective functions, architectural details, or experimental designs from the readings to the code in this course.

After each reading, focus on answering three questions: What technical problem does this material address, how is the core method expressed as a formula or algorithmic step, and which chapter's code, written assignments, or system design in this course is it directly related to.

## Reading Method: From Papers to Course Competencies

This course does not require students to memorize a list of papers, but rather to transform the technical choices in the papers into derivable, implementable, and evaluable competencies. When reading each piece of material, you should complete at least four steps:

1.  Problem Setting: Write down the input, output, training data, model assumptions, and target task.
2.  Mathematical Object: Identify an objective function, probability decomposition, matrix operation, mask rule, complexity formula, or evaluation metric, and explain each variable.
3.  Code Landing Point: Point out which function, tensor shape, test case, or system design judgment in this course it corresponds to.
4.  Conclusion Boundaries: Explain the data, scale, metrics, hardware, prompt, decoding strategy, or human annotation assumptions on which the experimental conclusions depend.

Reading depth progresses through three levels:

| Level | What Students Should Be Able to Do | Example |
|-------|------------------------------------|---------|
| Conceptual Level | Rephrase the problem, method, results, and limitations in their own words | Why BPE alleviates OOV; why DPO requires a reference model |
| Mathematical Level | Expand key formulas and complete a small numerical example | SGNS loss, attention scaling, next-token CE, DPO log-ratio |
| Systems Level | Connect the paper's method to resource, latency, quality, or safety trade-offs | GQA's KV cache, PagedAttention's memory paging, RAG's retrieval/generation dual metrics |

## Week 0: Built-in Prerequisite Diagnosis in Chapter

Corresponding Materials: Prerequisite Diagnostic, [Math and PyTorch Prerequisite Review](math-prerequisites.md), [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md).

This week's reading goal: Ensure students can translate basic ML language into objects repeatedly used in the LLM course, including loss, gradient, generalization, held-out evaluation, tensor shape, and PyTorch module. If the diagnosis reveals weaknesses, directly return to the "Prerequisite Skills/Internalization within Chapter/Acceptance Signal" of the relevant chapter to reinforce, rather than taking a separate independent course.

Required:

- This course [ML Foundations Prerequisite Bridge](ml-foundations-prerequisite-bridge.md): Focus on how calculus, probability/statistics, ML objectives, generalization, and evaluation enter the training, evaluation, and deployment conclusions in Ch07-Ch11.
- Goodfellow, Bengio, Courville. [Deep Learning](https://www.deeplearningbook.org/), relevant chapters on optimization and ML basics.
- This course [Math and PyTorch Prerequisite Review](math-prerequisites.md): Focus on confirming how Python, PyTorch, calculus, linear algebra, probability/statistics, and ML foundations appear in the shape, mask, loss, and gradient implementations in Ch01-Ch06.

Questions to consider:

- What is the relationship between training objectives, validation metrics, and engineering conclusions?
- Under what conditions can a benchmark or hidden test result not generalize?
- Why can cross entropy serve as the negative log-likelihood for a probabilistic model? What is its relationship with accuracy/F1?
- Where do implementations with correct shapes but semantic errors in PyTorch typically occur?

## Reading Focus

- Core conclusion: Describe in your own words the problem, method, and conclusion addressed by the paper or document.
- Technical details: Explain at least one formula, structural diagram, algorithm step, or experimental setup.
- Code connection: Clearly point out the corresponding chapter code, assignment function, or system design judgment.
- Boundary conditions: Write down one failure mode, counterexample, or scope of application.
- Extended question: Pose a question that can be further explored in class discussion or assignments.

## Week 1: Tokenization and Word Vectors

Corresponding chapters: Ch01-Ch02.

Reading goal for this week: Understand two approaches from discrete text to continuous vectors: subword tokenization addresses symbol coverage and compression issues, while word vectors use distributed semantics to project co-occurrence relationships into vector space.

Required reading:

- Sennrich, Haddow, Birch. [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909). Focus on how BPE alleviates OOV.
- Mikolov et al. [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781). Focus on the skip-gram objective.
- Pennington, Socher, Manning. [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf). Focus on the co-occurrence matrix and weighted least squares objective.

Optional reading:

- Sections related to word vectors and embeddings in Chapter 02 of this course.
- Chapters on word embeddings in Jurafsky and Martin, Speech and Language Processing.

Questions to consider:

- Why are BPE merge rules greedy? On which corpora do they produce tokens that are semantically unintuitive?
- How do skip-gram window co-occurrence samples become positive/negative binary classification targets?
- Is the analogy phenomenon in word2vec directly guaranteed by the training objective, or is it an empirical phenomenon in the spatial structure?
- SGNS, PMI, and GloVe all utilize co-occurrence statistics. What are the differences in their normalization and weighting approaches?
- How does token granularity affect context length, embedding parameter count, training token budget, and inference cost?

## Week 2: Attention and Tensor Derivatives

Corresponding chapters: Chapter 03 and math prerequisite review.

Reading goal for this week: Write the Transformer's attention as a complete tensor computation, and be able to explain every dimension in scaling, masking, softmax, weighted sum, and backpropagation.

Required reading:

- Vaswani et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Focus on scaled dot-product attention, masking, and multi-head structure.
- Chapter 03 attention assignments and written problems from this course: Focus on neural network foundations, tensor derivatives, and masked attention.

Optional reading:

- Goodfellow, Bengio, Courville. [Deep Learning](https://www.deeplearningbook.org/), chapters on optimization and backpropagation.
- Entries on softmax/cross entropy and matrix derivatives from The Matrix Cookbook.

Questions to consider:
- Why should the attention score be divided by `sqrt(d_k)`?
- Why does the additive implementation of the causal mask typically use a very large negative number instead of multiplying by 0 directly?
- Do the padding mask and the causal mask constrain the query or the key respectively? How should the shapes be broadcast after combination?
- Can attention weights be directly used as model explanations? What type of diagnostic conclusions do they support at most?

## Week 3: Multi-Head Attention, GQA, MLA, and the Block

Corresponding chapters: Ch04-Ch05.

Reading goal for this week: Extend from standard multi-head attention to GQA, MLA, norm, FFN, and the complete block, understanding how modern LLM architectures make trade-offs regarding memory, throughput, training stability, and expressiveness.

Required reading:

- Vaswani et al. [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Re-read multi-head attention and positional encoding.
- Ainslie et al. [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245). Focus on the number of KV heads and inference efficiency.
- DeepSeek-AI. [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](https://arxiv.org/abs/2405.04434). Focus on the motivation for KV cache compression in MLA.

Optional reading:

- Zhang and Sennrich. [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467).
- Shazeer. [GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202).
- Geva et al. [Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913). Focus on the key-value storage interpretation of FFN neurons.
- Meng et al. [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262). Focus on causal tracing, activation patching, and the boundaries of model editing.

Questions for thought:

- What expressive power is lost when GQA saves KV cache?
- Why does the decoupling of MLA's latent cache and RoPE change the engineering implementation?
- What conclusions can Probing, activation patching, and ablation support, and what conclusions can they not support?
- What numerical or optimization problems during training do Pre-Norm, RMSNorm, SwiGLU, and the residual path solve respectively?
- Why is parameter count alone insufficient to predict training memory and inference memory?

## Week 4: GPT Assembly, Pre-training Objectives, and MoE

Corresponding chapter: Ch06.

Reading goal for this week: Organize the probabilistic decomposition of a decoder-only LM, PyTorch forward pass, label shift, LM head, and MoE sparse activation into a complete model.

Required reading:

- Radford et al. [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf). Focus on the decoder-only pre-training paradigm of GPT-2.
- Fedus, Zoph, Shazeer. [Switch Transformers](https://arxiv.org/abs/2101.03961). Focus on top-1 routing, capacity, and load balancing.
- DeepSeek-AI. [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437). Focus on DeepSeekMoE and auxiliary-loss-free load balancing.

Optional reading:

- Brown et al. [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165).
- Hugging Face Transformers GPT-2 model documentation.

Questions for thought:

- Why is the training label for a decoder-only LM shifted right by one position?
- What problems arise if the MoE capacity factor is too low or too high?
- Where do tied embedding, final norm, position encoding, and causal mask reside in the GPT forward pass?
- Why must the "total parameter count" and "activated parameters per token" for MoE be reported separately?

## Week 5: Training Loop, Scaling, and Distributed Training

Corresponding chapter: Ch07.

Reading goal for this week: Move from single-step loss into the training system, understanding how data curation, optimizer, scheduler, mixed precision, checkpoint, scaling law, and distributed memory sharding collectively determine the feasible training scale.

Required reading:

- Loshchilov and Hutter. [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101). Focus on the difference between AdamW and L2 regularization.
- Hoffmann et al. [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556). Focus on the data/parameter trade-off in the Chinchilla scaling law.
- Li et al. [DataComp-LM: In search of the next generation of training sets for language models](https://arxiv.org/abs/2406.11794). Focus on data curation strategies: deduplication, filtering, data mixing, and multi-scale evaluation.
- Penedo et al. [The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale](https://arxiv.org/abs/2406.17557). Focus on filtering, deduplication, ablation of pretraining data, and the educational text filtering of FineWeb-Edu.
- Soldaini et al. [Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research](https://arxiv.org/abs/2402.00159). Focus on corpus composition, documented curation steps, intermediate corpus analysis, and reproducible data tooling.
- Rajbhandari et al. [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054). Focus on optimizer/gradient/parameter state sharding.
- Shoeybi et al. [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](https://arxiv.org/abs/1909.08053). Focus on how tensor parallelism partitions matrices within Transformer layers.
- Jiang et al. [MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs](https://arxiv.org/abs/2402.15627). Focus on full-stack observability, straggler diagnosis, fault tolerance, and MFU in large-scale training, rather than just memorizing the GPU count.

Optional reading:

- Huang et al. [GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism](https://arxiv.org/abs/1811.06965). Focus on micro-batch, pipeline bubble, and activation rematerialization.
- PyTorch documentation: `torch.amp`, `DistributedDataParallel`, [FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html), [DTensor](https://docs.pytorch.org/docs/stable/distributed.tensor.html), and [Distributed Checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html). Focus on how FSDP2 uses DTensor-style sharding for parameters, gradients, and optimizer state, how DCP performs multi-rank checkpointing and load-time resharding, and how resume parity is verified.
- PyTorch [TorchTitan checkpoint guide](https://github.com/pytorch/torchtitan/blob/main/docs/checkpoint.md). Focus on the difference between model-only save and full training state save, and how engineering parameters like checkpoint interval/async/keep-latest affect training reliability.
- NVIDIA Transformer Engine documentation on [FP8/MXFP8/NVFP4](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/index.html). Focus on low-precision training not only as a dtype choice, but also including scaling, amax history, kernel support, and checkpoint state.
- NVIDIA Megatron Core parallelism guide. Focus on which dimensions DP, TP, PP, CP, EP, and sequence parallelism respectively shard, and when to combine them.
- DeepSeek-V3 Technical Report on FP8 mixed precision, DualPipe, MLA/MoE, and MTP. Focus on how these designs collectively serve training efficiency and stability.
- Meta. [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783). Focus on how pre-training data cleaning, deduplication, PII/adult-content filtering, and contamination analysis affect evaluation interpretation.
- Jordan et al. [Muon is Scalable for LLM Training](https://arxiv.org/abs/2502.16982). Focus on the need for weight decay and update scale when scaling Muon from small model experiments to LLMs; do not just memorize the "orthogonalization" slogan.
- NVIDIA / PyTorch profiler documentation: diagnostic methods for GPU utilization, kernel timeline, communication overlap, and dataloader bottleneck.

Questions to consider:

- Why can AdamW's weight decay not simply be equated to L2 penalty in Adam?
- Given fixed compute, why is a "larger model" not necessarily more reasonable than a "smaller model + more training tokens"?
- Which types of erroneous training conclusions do the size, dedup, quality, eval contamination, domain mixture, and privacy diagnostics of the `training_data_curation_report` respectively prevent?
- When training loss decreases but the development set worsens, which outputs should be checked first?
- How do parameters, gradients, optimizer state, activations, and communication buffers respectively enter the GPU memory budget?
- Which bottlenecks (capacity, communication, or throughput) do DDP, ZeRO/FSDP, tensor parallel, and pipeline parallel respectively address?
- Which risks to the training system do the per-GPU model state, global batch tokens, MFU, and action item in the `distributed_training_strategy_report` respectively correspond to?
- Which types of recovery failures do the state completeness, write integrity, distributed reshard, interval, and overhead check in the `checkpoint_resume_integrity_report` respectively prevent?
- When MFU is low, how to distinguish between batch size too small, communication waiting, insufficient data loading, checkpoint writing to disk, and unfused kernels?
- When FP8/MXFP8 brings throughput gains, why is it still necessary to separately check loss spikes, scale/amax history, gradient ranges, and checkpoint resume?
- What minimum evidence is required for the optimization, throughput, state/checkpoint, and evaluation claims of a single training run?
- Which simplified problem in the course's tiny train do tools like FSDP2 / Distributed Checkpoint / Megatron Core solve?
- Why can a model-only export not replace a recoverable training checkpoint? Under FSDP/ZeRO, why is it still necessary to check the sharded/DCP format and shard metadata?
- What are the boundaries of the Chinchilla scaling law's conclusions when data quality, token repetition rate, or domain shift changes?

## Week 6: Generation, Search, and Speculative Decoding

Corresponding chapter: Ch08.

This week's reading goal: Transform the same next-token distribution into different decoding behaviors, understanding the quality/cost trade-offs of greedy, sampling, beam, self-consistency, constrained decoding, and speculative decoding.

Required reading:

- Holtzman et al. [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751). Focus on nucleus sampling.
- Leviathan, Kalman, Matias. [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192). Focus on the draft/target acceptance mechanism.
- Stern et al. [Blockwise Parallel Decoding for Deep Autoregressive Models](https://arxiv.org/abs/1811.03115). Focus on the motivation for predicting multiple tokens at once.
- Wei et al. [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903). Focus on how intermediate reasoning tokens change task success rates.
- Wang et al. [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171). Focus on multi-path sampling and voting.
- Snell et al. [Scaling LLM Test-Time Compute Optimally Can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314). Focus on verifier search, test-time compute, and marginal returns; do not equate multiple sampling with a free improvement.

Optional reading:

- Hugging Face Transformers generation strategies documentation.
- DeepSeek-V3 Technical Report on multi-token prediction.
- OpenAI. [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/). Focus on the difference between train-time compute and test-time compute, and why system metrics for reasoning models should be reported separately.

Questions to consider:

- Which properties of the distribution do top-k, top-p, and temperature respectively control?
- Under what circumstances does speculative decoding not yield significant speedup?
- When reporting accuracy improvements from self-consistency or best-of-N, how should token cost and latency be reported simultaneously?
- Which types of erroneous deployment conclusions do the quality, token, latency, cost, and efficiency diagnostics of the `test_time_compute_budget_report` respectively prevent?
- Does constrained decoding modify model parameters, logits, token masks, or post-processing? What are the failure modes of different implementations?
- When test-time compute improves accuracy, which system metrics should be reported simultaneously?

## Week 7: SFT, LoRA, DPO, GRPO, and RLVR/RFT

Corresponding chapter: Ch09.

This week's reading goal: Distinguish the training signals of SFT, parameter-efficient fine-tuning, synthetic data/distillation, reward modeling, DPO, GRPO, and RLVR/RFT. Understand how preference data, AI/human feedback, safety slices, rejection sampling, and verifiable rewards enter the objective function.

Required reading:

- Hugging Face. [Chat templates](https://huggingface.co/docs/transformers/chat_templating). Focus on how roles/messages are serialized into the model's actual input, and why training and inference must use a consistent template.
- Hugging Face TRL. [SFT Trainer](https://huggingface.co/docs/trl/sft_trainer). Focus on how assistant/completion-only loss, packing, and training data format affect the SFT label mask.
- OpenAI. [Fine-tuning guide](https://platform.openai.com/docs/guides/fine-tuning). Focus on chat-format training samples, training/validation splits, and production fine-tuning data protocols.
- Hu et al. [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685). Focus on low-rank increments and the proportion of trainable parameters.
- Bai et al. [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2204.05862). Focus on chosen/rejected preference data, helpful/harmless objectives, and online feedback data iteration.
- Rafailov et al. [Direct Preference Optimization](https://arxiv.org/abs/2305.18290). Focus on the derivation from KL-constrained RL to a classification-style loss.
- DeepSeek-AI. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948). Focus on GRPO, cold-start data, rejection sampling, distilled models, and method boundaries.
- Kimi Team. [Kimi k1.5: Scaling Reinforcement Learning with LLMs](https://arxiv.org/abs/2501.12599). Focus on long-context RL, long2short, length control, sampling strategies, and engineering trade-offs for multimodal reasoning.
- Yu et al. [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476). Focus on Clip-Higher, dynamic sampling, token-level policy gradient loss, overlong reward shaping, and how open-source RL recipes serve reproducible training.
- Zheng et al. [Group Sequence Policy Optimization](https://arxiv.org/abs/2507.18071). Focus on sequence-level importance ratio, length normalization, MoE RL stability, and why token-level ratio noise affects long training runs.
- verl [documentation](https://verl.readthedocs.io/), OpenRLHF [documentation](https://openrlhf.readthedocs.io/), SGLang [Post-Training Integration](https://sgl-project.github.io/references/post_training_integration.html), slime [documentation](https://thudm.github.io/slime/), and AReaL [paper](https://arxiv.org/abs/2505.24298). Focus on rollout engines, Ray/vLLM/SGLang integration, weight synchronization, colocated versus decoupled rollout, asynchronous RL, sample staleness, and production run ledgers.

Optional reading:

- Ouyang et al. [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155).
- Bai et al. [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073). Focus on how AI feedback generates harmlessness preference data, and why auditing data mixture and safety boundaries is still necessary.
- Meta. [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783). Focus on how post-training data, rejection sampling, reward models, human annotation, safety data, and evaluation slices collectively support the release conclusions.
- OpenAI. [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/) and [Reinforcement fine-tuning guide](https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning). Focus on train-time/test-time compute, programmable graders, validation splits, and grader applicability conditions.
- Qwen Team. [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388). Focus on unified thinking/non-thinking modes, thinking budget, model routing, and how inference-time compute should be reported together with latency and task success.

Questions to consider:

- Why does DPO need a reference model? What happens when `beta` is increased or decreased?
- After SFT data is converted from messages to token sequences, what information must be retained to check assistant-only loss, truncation, and packing boundaries?
- Before synthetic/distilled data enters SFT or preference optimization, why must the teacher version, sampling parameters, verifier accuracy, human spot-checking, deduplication, and eval overlap be recorded?
- How do length bias, style bias, or annotator disagreement in preference data enter the DPO/RLHF objective function?
- Which types of failed post-training conclusions do the coverage, label quality, leakage, and safety checks of the `post_training_data_audit` respectively correspond to?
- If the task coverage of SFT/preference data is insufficient or the eval overlap is non-zero, why can a decrease in DPO/GRPO training loss not be used as evidence for deployment?
- What sampling assumption does the intra-group advantage whitening in GRPO rely on?
- Why must a DAPO/GSPO-style reasoning RL report simultaneously examine rollout hit rate, completion length, entropy, clip fraction, sequence ratio, and held-out prompt slices?
- Why does the grader for RLVR/RFT require four types of checks: pass-rate, reward variance, completion length, and hacking signal?
- Which update directions are constrained by LoRA's low-rank increments? Does it save training parameters, optimizer states, or forward activations?
- When model quality improves after alignment but capability regresses, how should one distinguish between issues related to data distribution, KL constraint, and evaluation metrics?

## Week 8: Inference Engineering, RAG, Quantization, and Serving

Corresponding chapter: Ch10.

This week's reading goal: Integrate model outputs into real services, understanding how KV cache, continuous batching, paged memory, FlashAttention, quantization, RAG, speculative decoding, and multimodal inputs jointly affect latency, throughput, cost, and quality.

Required reading:

- Kwon et al. [Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180). Focus on KV cache paging.
- Dao et al. [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135). Focus on IO-aware attention.
- Gu and Dao. [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752). Focus on why selective state updates make compact recurrent memory more viable for language than earlier subquadratic models.
- Dao and Gu. [Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality](https://arxiv.org/abs/2405.21060). Focus on how attention and SSM-style layers can be placed into a shared structured-matrix view, and why Mamba-2 changes the systems/kernel discussion.
- Kimi Team. [Kimi Linear: An Expressive, Efficient Attention Architecture](https://arxiv.org/abs/2510.26692). Focus on hybrid linear attention plus MLA as an example of reducing long-context KV/decode cost while retaining attention-like capability.
- Lewis et al. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401). Focus on the retriever/generator combination.
- Dettmers et al. [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314). Focus on combining 4-bit quantization with LoRA.
- Yu et al. [Orca: A Distributed Serving System for Transformer-Based Generative Models](https://www.usenix.org/conference/osdi22/presentation/yu). Focus on why iteration-level scheduling and continuous batching reduce queue waste.
- vLLM documentation: [Optimization and Tuning](https://docs.vllm.ai/en/stable/configuration/optimization/) and [serve scheduler arguments](https://docs.vllm.ai/en/stable/cli/serve/). Focus on the relationship between `max_num_seqs`, `max_num_batched_tokens`, chunked prefill, KV cache capacity, and queue/SLO.
- vLLM documentation: [Disaggregated Prefilling](https://docs.vllm.ai/en/latest/features/disagg_prefill/). Focus on why separating prefill/decode allows tuning TTFT and ITL independently, and why this feature should still be evaluated alongside chunked prefill, KV transfer, and failure recovery.
- PyTorch and vLLM. [Disaggregated Inference at Scale with PyTorch & vLLM](https://pytorch.org/blog/disaggregated-inference-at-scale-with-pytorch-vllm/). Focus on how separating prefill/decode simultaneously affects TTFT, TPOT, throughput, and KV transfer.
- OpenAI. [Function calling](https://developers.openai.com/api/docs/guides/function-calling) and [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs). Focus on how function tools, JSON schema, strict structured output, and tool call output form the server-side protocol.
- vLLM. [Structured Outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/) and SGLang. [Structured Outputs](https://docs.sglang.ai/advanced_features/structured_outputs.html). Focus on JSON schema, choice, regex, grammar/EBNF constrained decoding in OpenAI-compatible serving, and why parse/schema/retry/safety regression testing is still necessary.
- vLLM. [Quantization](https://docs.vllm.ai/en/latest/features/quantization/) and [Quantized KV Cache](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/). Focus on which resources FP8/INT8/INT4, weight-only, and KV cache quantization respectively act upon, and why KV cache quantization requires long-context quality validation.
- NVIDIA TensorRT-LLM. [Quantization](https://nvidia.github.io/TensorRT-LLM/latest/features/quantization.html) and Transformer Engine [FP8/FP4 primer](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/fp8_primer.html). Focus on how SmoothQuant, AWQ, FP8 KV cache, FP8/FP4 scale metadata, hardware generations, and kernel support determine actual gains.
- Xiao et al. [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](https://arxiv.org/abs/2211.10438), Frantar et al. [GPTQ](https://arxiv.org/abs/2210.17323), Lin et al. [AWQ](https://arxiv.org/abs/2306.00978). Focus on the different assumptions of W8A8 activation outliers, approximate second-order weight quantization, and activation-aware weight-only quantization.
- Model Context Protocol. [Specification](https://modelcontextprotocol.io/specification/2025-06-18) / [Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) and [What is MCP?](https://modelcontextprotocol.io/docs/getting-started/intro). Focus on host/client/server, resources/prompts/tools, sampling/roots/elicitation, authorization, user consent, data privacy, and tool safety.
- Anthropic. [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp). Focus on how tool definitions and intermediate results consume context, and why large agent systems require lazy loading of tools, execution environment handling, and result summarization.
- Anthropic. [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and Claude Cookbook [Context engineering: memory, compaction, and tool clearing](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools). Focus on active context, context rot, compaction, tool-result clearing, memory, and why agent/RAG cannot rely solely on expanding the context window.
- OWASP. [Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) and [LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/). Focus on prompt injection, insecure output handling, insecure plugin design, excessive agency, and external content isolation.

Optional deep dive:

- Sun et al. [Retentive Network: A Successor to Transformer for Large Language Models](https://arxiv.org/abs/2307.08621). Focus on the three execution modes: parallel training, recurrent inference, and chunkwise recurrent long-sequence modeling.
- Moonshot AI. [Kimi-Linear implementation](https://github.com/MoonshotAI/Kimi-Linear). Focus on what must exist beyond the paper claim: kernels, vLLM integration, checkpoints, and reproducible serving path.
- OpenAI. [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices) and [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Focus on how reliability, monitoring, evaluation, and cost control during the transition from prototype to production factor into go-live decisions.
- Google SRE. [Canarying Releases](https://sre.google/workbook/canarying-releases/) and [Implementing SLOs](https://sre.google/workbook/implementing-slos/). Focus on how canary/control, phased traffic shifting, SLO/SLI, and error budget translate into release decisions.
- Google SRE. [Handling Overload](https://sre.google/sre-book/handling-overload/) and [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/). Focus on degraded responses, load shedding, dynamic timeouts, and preventing overload cascades.
- OpenTelemetry. [Generative AI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) and [GenAI attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/). Focus on how model, operation, token usage, finish reason, prompt/completion/tool event, and trace span become cross-platform telemetry fields.
- OpenAI Agents SDK [Tracing](https://openai.github.io/openai-agents-python/tracing/). Focus on how LLM generation, tool calls, handoffs, guardrails, and custom spans within an agent run help debug production workflows.
- Chen, Zaharia, Zou. [FrugalGPT](https://arxiv.org/abs/2305.05176) and Ong et al. [RouteLLM](https://arxiv.org/abs/2406.18665). Focus on LLM cascade, strong/weak model query routing, cost-quality frontier, and why the router needs preference/quality data for validation.
- LiteLLM [Router / Load Balancing](https://docs.litellm.ai/docs/routing) and [Fallbacks](https://docs.litellm.ai/docs/proxy/reliability). Focus on how load balancing, cooldowns, timeouts, retries, fallbacks, and provider/model group management factor into reliability controls.
- vLLM documentation: [Production Metrics](https://docs.vllm.ai/en/latest/usage/metrics/) and [V1 Metrics design](https://docs.vllm.ai/en/latest/design/v1/metrics.html). Focus on how the inference engine's request/engine metrics serve production monitoring, capacity planning, and incident triage.
- vLLM. [Expert Parallel Deployment](https://docs.vllm.ai/en/latest/serving/expert_parallel_deployment/) and [Parallelism and Scaling](https://docs.vllm.ai/en/stable/serving/parallelism_scaling/). Focus on why MoE layers require Expert Parallelism, DP+EP, `--enable-expert-parallel`, EPLB, and the KV cache/AllToAll trade-off.
- SGLang Team. [Deploying DeepSeek with PD Disaggregation and Large-Scale Expert Parallelism](https://lmsys.org/blog/2025-05-05-large-scale-ep/) and DeepSeek-AI [EPLB](https://github.com/deepseek-ai/eplb). Focus on how prefill/decode decoupling, large-scale EP, expert replication/placement, and load balancing in DeepSeek-style MoE serving collectively impact throughput and cost.
- vLLM [Disaggregated Prefilling](https://docs.vllm.ai/en/latest/features/disagg_prefill/), SGLang [PD Disaggregation](https://github.com/sgl-project/sglang/blob/main/docs/advanced_features/pd_disaggregation.md), NVIDIA [Dynamo](https://developer.nvidia.com/dynamo), and [llm-d](https://github.com/llm-d/llm-d). Focus on prefill/decode instances, KV transfer connectors, KV-aware routing, multi-tier cache management, SLO planning, and Kubernetes-native distributed inference.
- Google Gemini API [Long context](https://ai.google.dev/gemini-api/docs/long-context) and Anthropic Claude API [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows). Focus on the product implications of 1M+ context, context rot, context management, token counting, and the fact that long context does not automatically equate to stable recall.
- OpenAI. [Introducing GPT-4.1 in the API](https://openai.com/index/gpt-4-1/). Focus on 1M-token context, multi-needle/coreference and graph-style long-context evals, prompt caching, and the latency/cost trade-off of large input contexts.
- vLLM [Automatic Prefix Caching](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/) and [serve scheduler arguments](https://docs.vllm.ai/en/stable/cli/serve/). Focus on long document repeated queries, prefix cache, chunked prefill, long-prefill scheduling, and full input sequence length KV admission.

Optional Reading:

- vLLM documentation on PagedAttention, continuous batching, prefix caching, and disaggregated prefilling.
- TensorRT-LLM documentation on [in-flight batching and request scheduling](https://nvidia.github.io/TensorRT-LLM/). Focus on how in-flight batching dynamically adds/removes requests in the generation loop.
- vLLM [Speculative Decoding](https://docs.vllm.ai/en/latest/features/speculative_decoding/) documentation. Focus on medium-to-low QPS, memory-bound workload, draft/EAGLE/MTP/n-gram/suffix method selection, and lossless validation boundaries.
- SGLang [Speculative Decoding](https://docs.sglang.ai/advanced_features/speculative_decoding.html) documentation. Focus on EAGLE-2/EAGLE-3, MTP, standalone draft model, NGRAM, and OOM/benchmark considerations.
- SGLang v0.4 release note. Focus on how the zero-overhead batch scheduler, cache-aware load balancer, RadixAttention, and structured outputs integrate CPU scheduling, prefix caching, and format constraints into the serving engine.
- TensorRT-LLM disaggregated serving documentation. Focus on KV cache exchange, layout conversion, UCX/NIXL, and KV transfer overlap with computation.
- NVIDIA Dynamo. [Datacenter-scale inference stack](https://github.com/ai-dynamo/dynamo) and TensorRT-LLM. [Disaggregated Serving in TensorRT-LLM](https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog5_Disaggregated_Serving_in_TensorRT-LLM.html). Focus on why single-engine serving evolves into cluster orchestration with KV-aware routing, SLA planning, multi-tier KV cache, prefill/decode pool ratios, and failure recovery.
- Model Context Protocol tools specification. Focus on how tool names, metadata, input schema, tool results, and cross-service tool discovery are standardized; also examine the impact of tool list bloat on TTFT, context window, and tool selection accuracy.
- OpenAI Agents SDK guardrails and tracing. Focus on the different positions where input/output/tool guardrails run within the agent workflow, and how tracing records LLM generation, tool calls, handoffs, guardrail events, and custom spans.
- Google SRE Book. [Release Engineering](https://sre.google/sre-book/release-engineering/) and [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/). Focus on the connection between release engineering, rollback, SLOs, and business risk.
- llama.cpp official documentation on quantization, CPU/GPU offload, and local deployment boundaries.
- Sarathi-Serve or chunked prefill related papers/documentation: Focus on how long prompt prefill affects short request TTFT.
- Liu et al. [Visual Instruction Tuning](https://arxiv.org/abs/2304.08485). Focus on the two-stage process of vision encoder, projection, and LLM instruction tuning.
- OpenAI. [GPT-4o System Card](https://cdn.openai.com/gpt-4o-system-card.pdf). Focus on the unified text/audio/image/video model, safety assessment, voice/vision risks, refusal on sensitive attributes, and the fact that multimodal capabilities cannot be explained by text benchmarks alone.
- OpenAI. [Realtime and audio guide](https://developers.openai.com/api/docs/guides/realtime) and Google Gemini API [Live API](https://ai.google.dev/gemini-api/docs/live-api). Focus on low-latency voice/video sessions, streaming input, session state, interruption handling, and why realtime multimodal serving differs from batch audio transcription or ordinary chat completion.
- Gemini Team. [Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context](https://arxiv.org/abs/2403.05530). Focus on how long documents, video, audio, and multimodal long-context recall simultaneously impact quality, latency, context budget, and task boundaries.
- Qwen Team. [Qwen2.5-VL Technical Report](https://arxiv.org/abs/2502.13923). Focus on how dynamic resolution, window attention, document parsing, chart/layout, object localization, video event localization, and GUI/agent tasks change visual token representation and inference paths.
- Wang et al. [InternVL3.5: Advancing Open-Source Multimodal Models in Versatility, Reasoning, and Efficiency](https://arxiv.org/abs/2508.18265). Focus on how open-source multimodal models report trade-offs on general, reasoning, text, agentic benchmarks, and inference efficiency.
- OpenAI, Anthropic, or Google DeepMind multimodal model card / system card: Focus on how input resolution, task settings, latency, and safety boundaries are described.

Questions for Thought:

- Which system bottlenecks affect TTFT, TPOT, and TPS respectively?
- Why must RAG evaluation simultaneously consider both retrieval quality and generation quality?
- Why should multimodal evaluation separately examine VQA, OCR, chart understanding, and visual grounding?
- Why must multimodal serving simultaneously understand resolution/crop, vision/audio token, preprocess/encoder/prefill/decode latency, active KV tokens, cache isolation, and safety failures?
- Which costs and failure modes do dynamic resolution, OCR-first, query resampler, and video frame sampling respectively reduce or amplify?
- How should a benchmark summary limit the scope of its conclusions?
- Why are the compute/memory bottlenecks different for the prefill and decode phases?
- Which tasks, layers, or token distributions are preferentially affected by quantization errors?
- Why can't serving admission control be based solely on the number of concurrent requests, but must consider active KV tokens, prompt/output token distribution, and SLO queues?
- When a long prompt enters continuous batching, which TTFT issues do chunked prefill and prefix cache respectively mitigate?
- Why can't tool/function calling rely solely on prompt constraints? Which failures do schema, permissions, and loop budget respectively intercept?
- When deploying structured outputs, why must one simultaneously report JSON parse rate, schema valid rate, repair retry, fallback/refusal, P95 latency, and safety violation, rather than just looking at a single example output?
- After integrating MCP/remote tools, why must one separately audit server trust, user consent, roots/elicitation, sensitive data egress, observation isolation, and recursive sampling?
- Why must agent traces record guardrail events, tool spans, context budget, and side-effect logs? Which types of production incidents do these fields respectively help locate?
- Why must the context engineering report simultaneously include token proportion, citation retention, summary fidelity, permissions, and P95 TTFT for active context, retrieved context, summary, memory, tool observation, and cleared results?
- During production release, even if a candidate model has a higher offline pass rate, why must it still pass through canary/control, per-version quality/safety/SLO/cost monitoring, and rollback readiness checks?
- When model routing or cascading goes online, why can't average cost reduction replace regression testing on route branch quality, safety, schema, RAG, and high-risk task slices?
- During service operation, what different overload responses do queue backlog, KV cache nearing full, swapped requests, worsening TPOT, rising timeout, and single-tenant over-quota each point to?
- After prefill/decode decoupling, why must KV transfer, decode queue, and active KV tokens be reported separately?
- For the MoE serving report, why must TP baseline, EP/DP+EP, expert token skew, AllToAll/dispatch/combine time, KV cache per rank, EPLB, and P95 TPOT all be monitored simultaneously?
- What layer of bottleneck do SGLang's cache-aware load balancing, vLLM's disaggregated prefilling, and TensorRT-LLM's KV transfer overlap each solve?
- How do speculative decoding's acceptance rate, draft overhead, QPS, and quality regression collectively determine whether to enable it, rather than just looking at `num_speculative_tokens`?
- When deploying long contexts, why can't you only report max context length? What types of failures do context fit, quality, position robustness, and serving cost in `long_context_serving_gate_report` each prevent?

## Week 9: RNN, Classic NLP, Encoder-only, Evaluation & Ethics

Corresponding Materials: Classic NLP Topic Handout, Classic NLP Deep-Dive Teaching Module, Written Derivation and Conceptual Question Bank.

Reading Goals for This Week: Place modern LLMs back into the NLP curriculum context, understanding why RNN/LSTM, dependency parsing, seq2seq, BERT, and traditional metrics remain fundamental for understanding structural prediction, representation learning, and evaluation limitations.

Required Reading:

- Elman. [Finding Structure in Time](https://crl.ucsd.edu/~elman/Papers/fsit.pdf). Focus on how the recurrent hidden state represents prefixes.
- Hochreiter and Schmidhuber. [Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf). Focus on how gates and cell state mitigate the long-range gradient problem.
- Chen and Manning. [A Fast and Accurate Dependency Parser using Neural Networks](https://aclanthology.org/D14-1082/). Focus on transition-based parsing.
- Sutskever, Vinyals, Le. [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215). Focus on encoder-decoder and teacher forcing.
- Devlin et al. [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805). Focus on MLM/NSP and encoder-only representations.
- Bommasani et al. [On the Opportunities and Risks of Foundation Models](https://arxiv.org/abs/2108.07258). Focus on risk classification.

Optional Reading:

- Papineni et al. [BLEU: a Method for Automatic Evaluation of Machine Translation](https://aclanthology.org/P02-1040/).
- Lin. [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/).
- Zheng et al. [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html). Focus on position, verbosity, self-enhancement bias, and consistency verification with human preferences.
- OpenAI. [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Focus on model graders needing to verify consistency with human labels first before being used for optimization.
- Jimenez et al. [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770), [SWE-bench official leaderboard](https://www.swebench.com/index.html), and OpenAI [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/). Focus on how real-world codebase issues, patches, hidden tests, PASS_TO_PASS regression tests, human task filtering, costs, and scaffolds transform code agent evaluation from "generating code snippets" into task-level workflow eval.
- Yao et al. [tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045), Sierra [tau2-bench](https://sierra.ai/resources/research/tau-squared-bench), and [tau2-bench repository](https://github.com/sierra-research/tau2-bench). Focus on how multi-turn users, domain policies, API tools, user simulation, final database state, repeated-trial reliability, task fixes, and voice/dual-control variants enter the agent eval protocol.
- OpenAI. [BrowseComp: a benchmark for browsing agents](https://openai.com/index/browsecomp/). Focus on hard-to-find but verifiable short answers, browsing depth, search strategy, answer verifiability, and why short-answer benchmarks cannot represent all open-ended research tasks.

Questions for Thought:

- Why does the multiplicative chain of gradients in RNN BPTT cause difficulty with long-range dependencies? Which path does LSTM change?
- What are the differences in structural inductive bias between dependency parsing and decoder-only LLMs?
- How do the K/V sources differ between encoder-decoder cross-attention and decoder-only causal self-attention?
- In BERT MLM labels, why is an ignore index used for non-masked tokens?
- Why can't BLEU/ROUGE/F1/EM alone serve as quality metrics for LLMs?
- When is encoder-only token classification or span extraction more appropriate than open-ended generation?
- What commonality exists between legal action constraints in transition-based parsing and token masks in structured decoding?
- What conclusions do position bias, verbosity bias, swapped-order inconsistency, and human-label disagreement in LLM-as-judge each distort?
- Why must agent/workflow eval simultaneously report final task success, tool trajectory, state delta, side effects, latency/cost, and environment version?
- Which parts of agent capability do SWE-bench, tau-bench, and BrowseComp each cover? What real-world production risks does each fail to cover?

## Week 10: Frontier Methods, Benchmark Boundaries & Chapter Connections

Corresponding Materials: Ch10 Frontier Reasoning Section, Worked-Example-Pack, and Frontier Topic Readings.

Reading Goals for This Week: Synthesize knowledge from the previous nine weeks on representation, architecture, training, generation, alignment, evaluation, and serving to analyze which layer of the technology stack a frontier method actually changes, and what experiments are needed to support its claims.

Required Reading:

- Official paper, course handout, or model card for the target direction: interpretability, multimodality, social impact, agents, or reasoning.
- This course's worked-example-pack: Focus on checking the computable definitions and common misconceptions for each module.

Optional Reading:

- Official model card / technical report / API documentation for the target model, framework, or dataset.
- Related work and evaluation sections of papers on the same topic from the past year.
- Official papers, course handouts, or model cards for interpretability, multimodality, agents, reasoning, or safety governance directions.

Frontier Paper Reading Task:

Each student needs to select 2 materials closest to the current chapter's problem: one methods or systems paper, and one model card, benchmark paper, or official technical report. The reading goal is not to pile up citations, but to place the training, inference, or evaluation judgments from the course into a clear technical coordinate system:

| Paper Section | What You Need to Extract | How to Map to Chapter Content |
|----------|----------------|---------------------|
| Problem setup | Input, output, constraints, target user or system workload | Clearly state the current problem and what is not being studied |
| Method | Core algorithm, model structure, training objective, or system mechanism | Correspond to baseline, modification points, and implementation boundaries |
| Experiments | Dataset, sample size, metrics, baseline, ablation, and hardware | Correspond to evaluation set, stress test, ablation, and cost estimation |
| Analysis | Failure examples, error classification, resource bottlenecks, or safety boundaries | Correspond to error analysis and deployment risks |
| Limitations | Limitations acknowledged by the authors and uncovered scenarios | Correspond to conclusion boundary |

Reading notes should include a short related work paragraph, explaining what ideas the current judgment inherits, what conditions it simplifies, and which experimental scopes from the paper it does not cover. Training directions typically relate to optimizer, scaling, LoRA/alignment, or data quality; inference directions typically relate to serving, RAG, quantization, structured output, or evaluation.

Questions for Thought:

- What capability does the benchmark for the target direction measure? What capability does it not measure?
- Which claim in the paper or model card depends on a specific dataset, inference setting, or evaluator?
- If this method were integrated into this course's training or inference system, would memory, latency, quality, safety, or cost be affected first?
- If a new method is only effective on a single benchmark, a single model scale, or a single prompt template, how should the conclusion be stated?
- How can claims from papers on interpretability, multimodality, agents, reasoning, or safety be mapped to the formulas, code, and system metrics already present in this course?
- What questions should the method, experiments, analysis, and limitations sections of a technical conclusion each answer?
