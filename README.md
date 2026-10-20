<div align="center">

# 🦾 VLA Survey Companion
### *Vision-language-action models placed on four axes by written decision rules, with the evidence behind every cell*

[![Code MIT](https://img.shields.io/badge/Code-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Data CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg?style=flat-square)](DATA_LICENSE.md)
[![Systems](https://img.shields.io/badge/Systems%20placed-38-orange.svg?style=flat-square)](#-the-38-placed-systems)
[![Cutoff](https://img.shields.io/badge/Coverage%20cutoff-2026--04--30-blue.svg?style=flat-square)](#-scope-and-cutoff)
[![Contributions welcome](https://img.shields.io/badge/New%20systems-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

</div>

---

<div align="center">

Companion data for the survey &nbsp;<strong>Vision-Language-Action Models: Foundations, Architectures, Data, Efficiency, and Open Challenges</strong>&nbsp; (<em>under review</em>)

**38 systems placed · 125 verified references · 1,161 benchmark results · 75 latency records · 2,053 table-cell excerpts**

[🗺️ Axes](#️-four-axes-and-their-decision-rules) • [🤖 Systems](#-the-38-placed-systems) • [📂 Data](#-data-files) • [🔁 Rebuild](#-rebuilding-the-table) • [🤝 Contribute](CONTRIBUTING.md) • [📜 License](#-license)

</div>

---

## 📌 What this repository holds

The survey treats vision-language-action (VLA) models as a design space with four axes and gives a written test for each axis, so that two readers who apply the tests to the same paper reach the same placement. This repository releases the evidence that supports the survey. It holds a browsable copy of the model-level comparison (Table 2 of the survey), the CSV files from which the survey's tables and figures were built, and the claims files that pair each number and each table cell with a short excerpt from the source paper and its location. Every cell in the systems table is taken from the system's own paper, and the year is that of the first public version.

## 🗺️ Four axes and their decision rules

Most VLA systems combine several design choices, so category names alone do not fix a placement. Each axis below therefore comes with the test that decides it.

| Axis | What it describes | Decision rule |
| --- | --- | --- |
| **Action representation** | How perception and language become executable behavior, from language plans and code through spatial intermediates to tokenized, latent, or continuous motor commands | The lowest-level output that the learned model itself emits decides the class, not what a downstream controller executes |
| **Architectural paradigm** | Where perception, grounding, planning, and control are joined | Two tests on the structure of the system, described below |
| **Learning and adaptation** | How embodied skills are acquired, transferred, and refined | Which data enter which loss, taking the first class that applies |
| **Deployment objective** | The operational constraint that shapes the other three choices | The constraint the paper optimizes for and evaluates against in its main experiments |

**Action representation.** A planner that outputs subtask text is a language-as-action system even when a separate policy turns that text into joint commands. A model whose flow-matching head emits the action chunk directly, as in π<sub>0</sub>, is a continuous-trajectory system.

**Architectural paradigm.** The first test asks where the actions come from. A system whose actions come out of the language token stream is end-to-end (E2E), and a system whose actions come from a separate module with its own parameters and training objective is backbone plus action expert (B+E). The second test applies only to systems with two levels and asks whether the interface between them can be read by a person. A language, code, or subtask interface makes the system hierarchical (H), and a latent interface between modules that run at different rates makes it dual-system (DS). Reasoning and memory are overlays that can sit on any base class. A system is reasoning-augmented (+R) when it emits intermediate tokens before each action, and memory-augmented when it keeps state across inference calls beyond the context window. Being built on a foundation model is a property of where the backbone came from, not a class on this axis.

**Learning and adaptation.** The classes are checked in a fixed order and the first that applies is recorded. Training on action-free video or synthetic demonstrations comes first (VS), then co-training that adds non-robot data under the same objective (CT), then multi-robot corpora that precede adaptation to the target platform (XE), and last behavior cloning on target robot data alone (BC). Reward-guided refinement, which uses any signal beyond demonstrations, is recorded as an overlay (+RL).

**Deployment objective.** The class is the constraint that the paper's experiments are built around, which is usually explicit. Latency and hardware are the constraint for TinyVLA and SmolVLA, unseen homes for π<sub>0.5</sub>, and whole-body humanoid control for LeVERB. When a paper evaluates several constraints, the class follows its main experiments.

Under these rules each system maps to one position on each axis. The two Gemini Robotics reports cannot be placed, because they state that a cloud backbone and an on-robot decoder exist but not what passes between them.

## 🤖 The 38 placed systems

A system enters the table only when its own paper states the backbone, the action representation, the action decoder, the training data, and at least one benchmark together with its evaluation protocol. The sample combines the most cited systems with systems added to cover every class of the four axes and every shared benchmark, so it describes this sample and not the whole field. Each system name links to the paper.

<details>
<summary>📖 <strong>Legend for the class codes</strong> (click to expand)</summary>

- **Arch.** is the architectural class. E2E is end-to-end, B+E is backbone plus action expert, H is hierarchical, DS is dual-system, and +R marks the reasoning overlay. "Same model" marks a hierarchy in which one network produces both levels.
- **Learn.** is the learning class, the first that applies in this order. VS is action-free video or synthetic demonstrations, CT is co-training with non-robot data, XE is multi-robot corpora before target adaptation, BC is robot data from the target setting alone, and +RL marks reward-guided refinement.
- **Dep.** is the deployment class, the constraint the paper evaluates against. G is generalist transfer, E is efficient deployment, C is high-rate or dexterous control, L is long-horizon tasks and corrections, R is reasoning and interpretability, X is expanded embodiment, and V is driving.
- **Open** is yes when the paper states that weights are released, code when only code is stated, prom. when a release is promised, and n.s. when the paper does not state a release.

</details>

<!-- BEGIN SYSTEMS TABLE -->
#### End-to-end (E2E), 13 systems

| System (year) | Backbone; size | Action representation | Arch. | Decoder; passes per chunk | Training data | Learn. | Deployment objective | Dep. | Open |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [RT-1](https://doi.org/10.15607/rss.2023.xix.025) (2022) | FiLM-EfficientNet-B3 + TokenLearner + Transformer (no VLM); 35M | discrete tokens (256 uniform bins) | E2E | single Transformer pass emits all action tokens (not autoregressive); 1 | \~130k real demonstrations, 13 robots, 17 months, 700+ instructions | BC | real-time multi-task real-robot control | G | code |
| [RT-2](https://proceedings.mlr.press/v229/zitkovich23a.html) (2023) | PaLI-X (5B, 55B) or PaLM-E-12B; 5B / 12B / 55B | discrete tokens (256 uniform bins) | E2E | autoregressive tokens from the VLM head | web VL data co-fine-tuned with RT-1 robot data | CT | semantic generalization | G | n.s. |
| [ECoT](https://proceedings.mlr.press/v270/zawalski25a.html) (2024) | OpenVLA architecture (Prismatic, Llama 2 7B); 7B | reasoning text then discrete tokens | E2E+R | autoregressive reasoning then action tokens; about 350 tokens per step | Bridge V2 with synthetic reasoning labels | BC | generalization and interpretability | R | n.s. |
| [LAPA](https://openreview.net/forum?id=VYOe2eBQeh) (2024) | LWM-Chat-1M 7B; 7B | latent actions in pretraining; discrete bins after fine-tuning | E2E | action head replacing the latent head | latent pretraining on Bridge, OXE or human video without actions | VS | pretraining from action-free video | G | prom. |
| [OpenVLA](https://proceedings.mlr.press/v270/kim25c.html) (2024) | Prismatic-7B (SigLIP + DINOv2, Llama 2); 7B | discrete tokens (256 bins) | E2E | autoregressive tokens from the LLM head; 7 (one per action dimension) | 970k OXE trajectories | XE | open generalist transfer | G | yes |
| [TraceVLA](https://openreview.net/forum?id=b1CVu9l5GO) (2024) | OpenVLA 7B; Phi-3-Vision 4B variant; 7B / 4B | discrete tokens | E2E | language head on image plus visual-trace prompt | \~150K trajectories with trace annotation | XE | spatial-temporal awareness | G | n.s. |
| [CoT-VLA](https://doi.org/10.1109/cvpr52734.2025.00166) (2025) | VILA-U 7B; 7B | subgoal image then discrete tokens | E2E+R | image tokens then action tokens in one LLM | OXE subset + action-free video | VS | visual reasoning before acting | R | n.s. |
| [Magma](https://doi.org/10.1109/cvpr52734.2025.01325) (2025) | LLaMA-3-8B + ConvNeXt-XXL; 8.6B | discrete tokens (256 bins) | E2E | autoregressive LLM | 39M samples: UI, OXE, video, image-text | VS | one agent model for UI and robots | G | yes |
| [MolmoAct](https://doi.org/10.1109/icra57385.2026.11696546) (2025) | Molmo: SigLIP2 + Qwen2.5-7B; 7B | depth tokens and trace, then discrete tokens | E2E+R | autoregressive depth, trace, action tokens | 26.3M samples incl. OXE subset; MolmoAct Dataset | CT | explainable, steerable action reasoning | R | yes |
| [NORA](https://arxiv.org/abs/2504.19854) (2025) | Qwen-2.5-VL-3B; 3B | compressed tokens (FAST+) | E2E | autoregressive FAST+ tokens | 970k OXE demonstrations | XE | small VLA for consumer GPUs | E | yes |
| [OpenDriveVLA](https://doi.org/10.1609/aaai.v40i16.38386) (2025) | Qwen2.5 (0.5B/3B/7B) + 3D perception module; 0.5B / 3B / 7B | waypoint tokens (6 points, 3 s) | E2E | autoregressive text waypoints | nuScenes + driving QA sets | CT | end-to-end driving planning | V | n.s. |
| [SpatialVLA](https://doi.org/10.15607/rss.2025.xxi.011) (2025) | PaliGemma 2 + Ego3D encoding; 3.5B | spatial tokens (adaptive grids, 8,194 vocabulary) | E2E | autoregressive spatial tokens; 12 tokens per 4-action chunk | 1.1M episodes, OXE subset + RH20T | XE | 3D-aware generalist | G | code |
| [VLA-0](https://arxiv.org/abs/2510.13054) (2025) | Qwen-VL-2.5-3B, unmodified; 3B | actions as plain text integers | E2E | autoregressive text in the VLM vocabulary | LIBERO demos only; 100 demos per real task | BC | no change to the VLM | G | yes |

#### Backbone plus action expert (B+E), 10 systems

| System (year) | Backbone; size | Action representation | Arch. | Decoder; passes per chunk | Training data | Learn. | Deployment objective | Dep. | Open |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [CogACT](https://arxiv.org/abs/2411.19650) (2024) | Prismatic-7B + DiT action module; 7.6B (DiT-Base 89M) | continuous chunk | B+E | diffusion transformer, DDIM; 10 DDIM steps | 0.4M OXE trajectories (25 datasets) | XE | manipulation precision, new robots | G | yes |
| [DeeR-VLA](https://doi.org/10.52202/079017-1803) (2024) | OpenFlamingo 3B, multi-exit; 3B | continuous pose + discrete gripper | B+E | LSTM action head after a dynamic early exit; 1 (truncated LLM pass) | CALVIN language-annotated data | BC | lower compute and memory via early exit | E | yes |
| [π<sub>0</sub>](https://doi.org/10.15607/rss.2025.xxi.010) (2024) | PaliGemma 3B + 300M action expert; 3.3B | continuous chunk | B+E | flow-matching action expert, 10 steps; 1 VLM pass + 10 expert passes | 10,000+ h robot data, 7 configurations, plus OXE | XE | dexterous multi-embodiment control | C | n.s. |
| [TinyVLA](https://doi.org/10.1109/lra.2025.3544909) (2024) | Pythia-based VLM; 422M to 1.3B | continuous | B+E | diffusion policy head | no robot pretraining; 100 demos per task | BC | fast inference, data efficiency | E | n.s. |
| [DexVLA](https://proceedings.mlr.press/v305/wen25b.html) (2025) | Qwen2-VL 2B + 1B diffusion expert; 2B VLM + 1B expert | continuous | B+E+R | diffusion transformer expert with reasoning injection | \~100 h own teleoperation, 91 tasks | XE | cross-embodiment dexterous and long-horizon tasks | C | n.s. |
| [GR-3](https://arxiv.org/abs/2507.15493) (2025) | Qwen2.5-VL-3B-Instruct + flow-matching action DiT; 4B | continuous chunk | B+E | flow-matching action DiT reading the VLM KV cache | own robot teleoperation per task, web VL data, 450 VR human trajectories | CT | generalization to novel objects, environments, and instructions | G | n.s. |
| [OpenVLA-OFT](https://doi.org/10.15607/rss.2025.xxi.017) (2025) | OpenVLA (Prismatic, Llama 2 7B); 7.5B; 279M trainable | continuous chunk | B+E | parallel decoding + MLP head, L1 regression; 1 | OpenVLA base; 500 demos per LIBERO suite | XE | fast high-rate fine-tuned control | C | yes |
| [SmolVLA](https://arxiv.org/abs/2506.01844) (2025) | SmolVLM-2, first 16 layers; 450M (\~100M expert) | continuous chunk | B+E | flow-matching expert, 10 steps; 10 | 22.9k community episodes, 481 datasets | XE | affordable training and deployment | E | yes |
| [UniVLA](https://doi.org/10.15607/rss.2025.xxi.014) (2025) | Prismatic-7B; 7B; 12.6M action head | latent action tokens decoded to chunks | B+E | latent tokens + attention-pooling action head; 4 latent tokens + 1 head pass | OXE subset, navigation and human video without actions; 960 A100-h | VS | cross-embodiment from action-free video | X | code |
| [VLA-Adapter](https://doi.org/10.1609/aaai.v40i22.38931) (2025) | Prismatic on Qwen2.5-0.5B; 0.5B; 97.3M policy | continuous chunk | B+E | L1 policy with bridge attention | no robot pretraining; benchmark data | BC | low training cost, fast inference | E | n.s. |

#### Action transformer without a language model (B+E, no LLM), 4 systems

| System (year) | Backbone; size | Action representation | Arch. | Decoder; passes per chunk | Training data | Learn. | Deployment objective | Dep. | Open |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [GR-2](https://arxiv.org/abs/2410.06158) (2024) | GPT-style transformer pretrained on video generation (no VLM); 230M (95M trainable) | continuous trajectory with future images | B+E (no LLM) | cVAE action head | 38M video clips; \~40,000 robot trajectories | VS | generalist manipulation; bin picking | G | n.s. |
| [Octo](https://doi.org/10.15607/rss.2024.xx.090) (2024) | Transformer trained from scratch + t5-base encoder (no VLM); 27M / 93M | continuous chunk | B+E (no LLM) | diffusion head, 20 steps; 20 head steps after one backbone pass | 800k OXE trajectories (25 datasets) | XE | open generalist initialization | G | yes |
| [RDT-1B](https://openreview.net/forum?id=yAzN4tz7oI) (2024) | diffusion transformer + frozen SigLIP and T5-XXL encoders (no LLM); 1.2B | continuous chunk (128-dim unified space) | B+E (no LLM) | diffusion, 5 DPM-Solver++ steps; 5 | 46 datasets, 1M+ trajectories; 6K+ bimanual fine-tuning episodes | XE | bimanual manipulation foundation model | C | yes |
| [X-VLA](https://openreview.net/forum?id=kt51kZH4aG) (2025) | Florence-Large encoder + soft-prompted transformer; 0.9B | continuous chunk | B+E (no LLM) | flow matching in the transformer | 290K episodes, seven platforms | XE | cross-embodiment with per-source soft prompts | X | n.s. |

#### Hierarchical with a readable interface (H), 7 systems

| System (year) | Backbone; size | Action representation | Arch. | Decoder; passes per chunk | Training data | Learn. | Deployment objective | Dep. | Open |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [PaLM-E](https://proceedings.mlr.press/v202/driess23a.html) (2023) | PaLM 540B + ViT-22B; 12B / 84B / 562B | language plans (executed by separate low-level policies) | H | autoregressive text; low-level policies RT-1 or Lynch et al. | web VL mixture with 8.9% embodied data | CT | embodied reasoning and planning | L | n.s. |
| [RT-H](https://doi.org/10.15607/rss.2024.xx.049) (2024) | PaLI-X 55B; 55B | language motion then discrete tokens (256 bins) | H (same model) | two queries: language motion, then action; 2 queries per step | 100K demonstrations (Kitchen + Diverse) | CT | data sharing and language corrections | L | n.s. |
| [Hi Robot](https://proceedings.mlr.press/v267/shi25d.html) (2025) | PaliGemma-3B high level; pi0 low level; 3B per level | language commands, then continuous chunks | H | autoregressive commands; pi0 flow expert | teleoperated demos + VLM-generated synthetic prompts | BC | open-ended instructions and corrections | L | n.s. |
| [LoHoVLA](https://arxiv.org/abs/2506.00411) (2025) | PaliGemma-3B; 3B | discrete tokens (1,024 bins) after subtask text | H (same model) | subtask text then action tokens, closed-loop replanning | LoHoSet (Ravens sim) | BC | long-horizon planning and acting | L | n.s. |
| [OneTwoVLA](https://openreview.net/forum?id=tWMfhoP3as) (2025) | pi0 VLM (writes reasoning text) + pi0 flow-matching action expert | decision token, reasoning text when chosen, then continuous chunk | H+R (same model) | adaptive text reasoning; pi0 flow-matching action expert | 200 to 600 demos per task, 2,000 atomic-skill demos, 16,000 synthetic VL reasoning samples | CT | reasoning only at critical steps for long-horizon tasks, recovery, and interaction | L | n.s. |
| [π\*<sub>0.6</sub>](https://arxiv.org/abs/2511.14759) (2025) | Gemma 3 4B + 860M flow-matching action expert; 4B + 860M | sub-task text, then continuous chunk (FAST tokens predicted in training) | H (same model) | sub-task text at a lower rate, then flow-matching action expert | multi-robot demonstrations and web VL data; then own rollouts and expert interventions | CT+RL | throughput and success on long real-world tasks | L | n.s. |
| [π<sub>0.5</sub>](https://proceedings.mlr.press/v305/black25a.html) (2025) | PaliGemma (2B) + 300M action expert; 2B + 300M | FAST tokens in pretraining; continuous chunk after post-training | H (same model) | subtask text, then 10 flow-matching steps | mobile-manipulator data from \~100 homes + other robots, web data, subtask labels | CT | open-world generalization to unseen homes | G | n.s. |

#### Dual-system with a latent interface (DS), 4 systems

| System (year) | Backbone; size | Action representation | Arch. | Decoder; passes per chunk | Training data | Learn. | Deployment objective | Dep. | Open |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [HiRT](https://proceedings.mlr.press/v270/zhang25b.html) (2024) | InstructBLIP 7B + fast latent-conditioned policy; 7B + 35M or 150M | continuous (regression) | DS | fast policy conditioned on cached VLM latent; 1 | per-domain demos only | BC | higher control rate for dynamic tasks | C | n.s. |
| [GR00T N1](https://arxiv.org/abs/2503.14734) (2025) | Eagle-2 VLM 1.34B + flow DiT; 2.2B | continuous chunk | DS | flow-matching DiT, 4 steps; 4 | data pyramid: real robots, human video with latent actions, simulation, neural trajectories | VS | generalist humanoid control | X | yes |
| [LeVERB](https://arxiv.org/abs/2506.13751) (2025) | SigLIP encoders + CVAE transformer; RL whole-body controller | latent verbs decoded to joint targets | DS | RL-distilled whole-body controller | synthetic: retargeted human motion rendered in IsaacSim | VS | humanoid whole-body control, sim-to-real | X | n.s. |
| [ThinkAct](https://doi.org/10.52202/085713-2773) (2025) | Qwen2.5-VL 7B + DiT action model; 7B + 432M | visual plan latent, then continuous actions | DS+R | diffusion policy, 20 DDIM steps; 20 | OXE trajectories and embodied QA for reasoning; OXE for actions | CT+RL | reasoning planner with fast executor | L | n.s. |
<!-- END SYSTEMS TABLE -->

## 📂 Data files

All files are UTF-8 CSV. The `source_page` and `location` columns point to the section, table, figure, or page of the source paper, and the `key` columns hold the survey's citation keys. Each of these keys has a matched publisher, proceedings, or arXiv record in `refs_verified.csv`, except two retired keys marked `_UNUSED` in `claims_tables.csv`.

| File | Rows | Contents |
| --- | ---: | --- |
| [`systems.csv`](data/systems.csv) | 38 | The placed systems with backbone, size, action representation, architecture code, decoder, chunk length, control rate, training data, adaptation, deployment objective, class codes, weight release, and benchmarks |
| [`system_links.csv`](data/system_links.csv) | 38 | A DOI, proceedings, OpenReview, or arXiv link for each placed system |
| [`results.csv`](data/results.csv) | 1,161 | Reported benchmark results with variant, suite, metric, trial count, the paper that ran the evaluation, and protocol notes |
| [`calvin_chain.csv`](data/calvin_chain.csv) | 175 | CALVIN success at each of the five chained steps and the average chain length, by split |
| [`latency.csv`](data/latency.csv) | 75 | Reported control rates and per-action latencies, each paired with its hardware and numeric precision |
| [`longhorizon_pairs.csv`](data/longhorizon_pairs.csv) | 27 | Paired comparisons of a long-horizon mechanism against its ablated or base system, with both quotes |
| [`datasets.csv`](data/datasets.csv) | 14 | Robot datasets with source, scale, modalities, embodiments, and control rate |
| [`positioning_evidence.csv`](data/positioning_evidence.csv) | 80 | The coding of the closest earlier surveys on each comparison criterion, with the quote, its location, and the second coder's check |
| [`search_log.csv`](data/search_log.csv) | 24 | Query strings, fields, filters, run dates, and record counts of the literature search |
| [`refs_verified.csv`](data/refs_verified.csv) | 125 | Each cited reference matched against its publisher, proceedings, or arXiv record |
| [`claims.csv`](data/claims.csv) | 387 | Sentence-level claims in the survey text, each with a source excerpt, its location, and whether the source supports it |
| [`claims_tables.csv`](data/claims_tables.csv) | 2,053 | One excerpt and location for each table cell and plotted value |

Three rows of `claims.csv`, for `fan2024languagereasoningvla`, `jiang2024behavioractor`, and `zhao2025multimodal`, keep their keys and locations, but their excerpts are not redistributed here, because two were taken from library-licensed copies and one from a publisher abstract.

## 🔁 Rebuilding the table

The table above is generated from `data/systems.csv` and `data/system_links.csv` with the Python standard library only.

```bash
python scripts/build_readme_table.py
```

Run it with `--check` to confirm that the README matches the data without rewriting it. Rows are grouped by architecture class and sorted by year and name within each class, which is the order of Table 2 in the survey.

## 🕒 Scope and cutoff

The survey covers models that take visual observations and a language instruction and produce actions that a physical robot can execute, where the action-producing part is trained end-to-end on robot data or is tightly coupled to a vision-language backbone through a learned interface. The coverage cutoff is 30 April 2026, and systems released after that date are not covered.

## 🤝 Contributing

New systems are welcome when they meet the entry rule above. See [CONTRIBUTING.md](CONTRIBUTING.md) for what to send and how a proposed placement is checked.

## 📝 How to cite

Citation details will be added here once the survey completes peer review.

## 📜 License

The code in `scripts/` is released under the [MIT License](LICENSE). The CSV files in `data/` are released under [CC BY 4.0](DATA_LICENSE.md), which covers the compilation and the coding and not the short quotations from source papers.
