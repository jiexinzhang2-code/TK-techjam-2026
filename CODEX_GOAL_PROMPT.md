# Codex Goal Prompt - Track 2 Autonomous ML Research Agent（Git + 本机适配版）

将下面代码块中的完整内容粘贴为 Codex Goal。该目标已按当前 GitHub 工作树、macOS/Apple Silicon、Python 3.9 和本地已有数据调整。

它授权 Codex 在已有 Git 仓库的 `feature/bpr-fm` 分支内实现、测试、创建本地 commits，并在全部验收通过后 push 到同名 `origin` 分支。它不授权直接修改或 push `main`、force-push、合并 PR、提交 Devpost、访问比赛 hidden-test 标签、调用付费 API、使用未提供的密钥，或修改允许范围外的文件。

## 可行性审计结论

结论：按下方 P0/P1 边界执行时可行，并与 Track 2 的核心目标一致。已验证公开 GitHub remote、`main` 同步状态、现有 `feature/bpr-fm`、外部数据读取，以及 random/pop/FM 的本机 CPU 运行路径。当前云端 feature 分支只包含 `.gitignore` 更新，Agent、BPR、tests、logs 和 submission 流程仍是待实现内容；本结论不把计划误报为已完成产品。主要剩余风险是真实 LLM planner 凭证未提供，因此 deterministic planner 是必备 fallback，真实 LLM 自动写 plugin 属于有凭证/有时间时的增强项。

```text
## Goal

在以下本机 Git 工作树中实现一个用于 TikTok TechJam 2026 Track 2 的最小可用 Autonomous ML Research Agent（MVP）：

`/Users/mr.handsome/Documents/GitHub/bytedance-techjam-2026-kuairand`

所有实现、测试和运行命令都必须从该目录执行。路径包含空格，首次进入目录时必须使用：

cd "/Users/mr.handsome/Documents/GitHub/bytedance-techjam-2026-kuairand"

该 Agent 必须把 KuaiRand-Pure 推荐模型研究变成受控、可复现、可审计的实验闭环：

`提出假设 -> 校验计划 -> 执行受控模型工具 -> 固定验证评估 -> 选择/回滚 -> 记录证据 -> 下一轮或停止`

目标不是只训练一个高分模型，也不是制作聊天 UI、Web 服务或容器平台；目标是让 Agent 以尽量少的人工干预，自动驱动推荐模型改进，并产出合法提交文件和完整运行证据。

“自主”必须体现在：planner 根据前序 validation 指标和失败记录选择下一项单一变化，形成 code/config diff，运行后自主 accept/reject/recover，而不是固定顺序播放三个脚本。规则型 planner 是无密钥时的可靠 fallback；若团队提供可用 LLM 凭证，正式 demo 应优先展示同一受控接口下的 LLM planner。没有凭证时必须如实披露限制，不能把静态菜单包装成完全自主研究。

## 72 小时可行性优先级

- P0（必须完成）：Git 可审计闭环、官方 baseline、规则/LLM 统一 planner 接口、至少一轮受控 code/plugin diff、安全 runner、validation-only 选择、失败恢复、JSONL、3 轮 demo、submission check、README/架构/结果摘要。
- P1（核心竞争力）：NumPy pairwise FM/BPR，至少一次由历史结果驱动的 accept/reject，并报告相对 FM 的 validation delta。
- P2（有余力再做）：真实 LLM 自动写新 plugin、更多模型/特征、bonus datasets。不得为 P2 牺牲 P0/P1 的完整性和演示证据。

## 已核验的本机环境

以下事实已经在 2026-08-30 的本机上核验，实施时不要重新猜测：

- 主机：macOS 26.3.1、Darwin arm64、Apple Silicon、16 GB 内存；默认按 CPU-only 运行。
- 可用解释器：`/usr/bin/python3`，Python 3.9.6，NumPy 2.0.2。
- 统一使用 `python3` 或绝对路径 `/usr/bin/python3`；不要使用裸 `python`，它指向另一个缺少 NumPy 的环境。
- Desktop 副本自带的 `.venv` 已失效：其 pip shebang 指向旧目录 `/Users/mr.handsome/Downloads/kuairand-starter-kit/.venv`，而且没有 NumPy。不得激活、修补、覆盖或删除它。
- 核心 baseline 只需要标准库和 NumPy。默认直接使用 `/usr/bin/python3`；只有新增依赖确有必要且用户允许安装时，才新建 `.venv-local`，不要复用 `.venv`。
- 编写 Python 3.9 兼容代码：使用 `typing.Optional` 等兼容写法，不使用 `match`、`tomllib` 或 `X | None` 等较新版本专属语法。
- 当前没有 pytest、Pydantic、PyTorch、pandas、scikit-learn 或 psutil；MVP 不得默认依赖这些包。schema 使用 `dataclasses`/标准库，测试使用 `unittest`，模型优先保持 NumPy-only。
- macOS 没有 GNU `timeout`/`gtimeout`。超时必须由 Python `subprocess` 实现，禁止在命令中假定存在 `timeout`。
- 当前没有 Docker/Podman、数据库、后台服务或端口需求；不要把它们加入 MVP。
- 权威代码工作树是上述 `Documents/GitHub/...` 仓库；Desktop 下的 starter kit 只是同源副本和数据位置，不得在那里实施代码。
- 本地数据位于 `/Users/mr.handsome/Desktop/TK Hackathon/kuairand-starter-kit/KuaiRand-Pure/data`，约 194 MB；压缩包也已存在。Git 工作树不包含数据，所有命令必须显式传入该只读 data directory，不得复制、下载或解压到仓库。
- 已核验 split 行数：train 1,141,112；valid 124,909；local test 170,588。
- 已核验 `python3 baseline.py --model random --seed 0`、`--model pop` 和完整 FM 都能在 CPU 上运行。FM 的发布参考值见 `baseline_scores.json`；随机单 seed 会有正常波动。
- GitHub 仓库：`https://github.com/OwenWen00/bytedance-techjam-2026-kuairand`，公开，默认分支 `main`。
- 本地 `main` 当前干净，commit `e4ac2b1` 与 `origin/main` 一致。
- 远端已有 `feature/bpr-fm`，commit `b1c3d0f`；它目前仅更新 `.gitignore`。实施必须基于这个已有分支，不另造含义重叠的分支。
- `origin/main` 是受保护基线：不直接开发、不 push、不 rebase、不 merge。代码版本 ID 以 Git commit SHA 为主，SHA-256 manifest 作为固定文件和配置完整性证据。

如果当前沙箱对上述精确 Git 工作树没有写权限，先请求该目录的写入授权；不要把项目复制到 Desktop 副本后静默实现。不要修改 Desktop 上的赛事 PDF、教学手册、本 `CODEX_GOAL_PROMPT.md` 或数据文件。

## 启动前强制 preflight

在写代码前完成并记录以下只读检查：

1. 确认 `pwd` 正好是上述 `Documents/GitHub/bytedance-techjam-2026-kuairand` 根目录。
2. 用 `/usr/bin/python3` 打印 `sys.version`、`sys.executable` 和 `numpy.__version__`。
3. 检查 `git remote -v`、`git status --short --branch`、当前分支和 `origin/main`；若存在未知 dirty changes，停止并报告，不 reset/restore/stash。
4. 运行 `git fetch --prune origin`，确认 `origin/main` 与预期基线一致，然后切换并跟踪已有 `origin/feature/bpr-fm`。所有实现都在 `feature/bpr-fm` 完成。
5. 确认外部 data directory 中以下 6 个 CSV 均存在：两个 standard log、一个 random log、user features、video basic features、video statistic features。
6. 调用官方 `data.load()` 核对 split 行数为 1,141,112 / 124,909 / 170,588；不一致时停止真实实验并报告。
7. 计算并保存 `data.py`、`evaluate.py`、`baseline.py`、`submit.py`、`baseline_scores.json` 的初始 SHA-256，并记录起始 Git SHA。
8. 检查 `.gitignore` 至少覆盖 data/tar/zip、`.venv*`、缓存、`.DS_Store`、checkpoint、prediction、submission 和其他大生成物；轻量 configs、JSONL logs、结果摘要、tests、docs 必须可跟踪。
9. 检查是否已有用户文件或同名输出。保留未知文件，不删除、不覆盖，不使用 `git clean`。

如果外部数据意外缺失，只报告缺失文件和以下 macOS 备用命令，不要自动联网下载或写入 Git 工作树：

`curl -L https://zenodo.org/records/10439422/files/KuaiRand-Pure.tar.gz -o "/Users/mr.handsome/Desktop/TK Hackathon/kuairand-starter-kit/KuaiRand-Pure.tar.gz"`

## 事实来源和口径优先级

实现口径以本机可运行 Starter Kit 为准：

1. `evaluate.py` 和 `submit.py`：评分与提交校验的最终执行口径。
2. `data.py`、`baseline_scores.json` 和 Starter Kit `README.md`：split、标签、baseline 与数据流。
3. Track 2 信息文档中的详细 Starter Kit、deliverables 和 judging criteria 段落。
4. 教学手册仅作流程参考；其中示例路径、虚拟环境和 Git 命令不能覆盖本机事实。

赛事 PDF 有一处摘要行残留了 `NDCG@10 / Recall@50, click=positive`，但同一份文档的详细 Starter Kit、benchmark、deliverables、judging criteria，以及本机 `evaluate.py`/`baseline_scores.json` 均固定为：

- 标签：`long_view`
- 任务：用户内 logged impressions 排序
- 指标：GAUC、nDCG@5
- primary：两者平均

因此本项目实施必须使用后者，不得擅自改成 click、NDCG@10 或 Recall@50。若发现新的组委会文件与本地 evaluator 冲突，停止并报告，不自行重写评分器。

## 先参考并适配开源实现，不从头造轮子

实施前阅读并在 `docs/open_source_adaptation.md` 中记录可复用的设计边界：

1. `https://github.com/karpathy/autoresearch`
   - 参考：冻结评估器、限制可编辑范围、change -> evaluate -> keep/revert、结果台账。
2. `https://github.com/VectorInstitute/helix`
   - 参考：声明式实验配置、可编辑文件 scope、评估命令、append-only ledger、可复现研究轨迹。
3. 可选：`https://github.com/WecoAI/weco-cli`
   - 参考：评估驱动的探索策略；不要把外部云服务作为运行前提。

要求：

- 优先只读查看公开文档、源码和许可证，不 clone 大型仓库，不复制完整平台。
- 不引入网页 UI、后台服务、复杂 multi-agent 平台或与本题无关的依赖。
- 记录借鉴了什么、为何适配、哪些部分自行实现、为何未直接引入完整框架。
- 保留实际复用代码所需的许可证和归属。
- 如果网络不可用，继续实现本地 MVP；只记录“未能在线核验”，不得虚构源码细节或许可证结论。

## 固定底座：绝对不可修改或绕过

以下文件和规则是评测公平性边界：

- `data.py`：冻结其官方日期 split、行序、标签与默认数据流。新增特征读取放在 `features/`，不要改此文件。
- `evaluate.py`：唯一合法的 GAUC、nDCG@5、primary 实现。
- `submit.py`：唯一合法的 submission 对齐/格式校验逻辑。
- `baseline.py`：官方 baseline 参考，保持原样可运行。
- `baseline_scores.json`：只读参考。
- Desktop 外部 `KuaiRand-Pure/`、`KuaiRand-Pure.tar.gz`：只读数据资产；不改、不移动、不复制进 Git，也不纳入 commit。

完成后重新计算上述官方文件 SHA-256，并与 preflight 清单逐项比较；任何变化都视为验收失败。

## 本地 test 与比赛 hidden test 的边界

本地 KuaiRand-Pure chronological `test` CSV 带有 `long_view`，官方 baseline 和 `data.load()` 会解析它；它不是比赛平台最终隐藏标签。必须按以下规则使用：

- 训练、调参、accept/reject、停止条件和 planner 的下一轮输入只允许使用 train + valid。
- 本地 test 指标不得进入实验 ledger 中供 planner 决策，不得选择 checkpoint，不得改变下一轮计划。
- baseline 自检可以运行官方脚本并看到它固有打印的 local-test 参考分数，但 Agent 不得据此调参。
- 研究冻结后，可以对唯一的 validation-best checkpoint 做至多一次本地 holdout 报告；将其明确标为 `local_test_holdout`，不能写成 hidden-test 成绩。
- 比赛 hidden test 只由最终 submission 在组委会侧评估，本地不可访问。
- 禁止把任何 test 标签作为训练特征、目标、采样依据、早停依据或特征统计输入。
- Agent 研究循环中允许 `submit.py --score --split valid`；最终格式检查允许 `submit.py --check --split test`；禁止研究循环调用 `submit.py --score --split test`。

不得把密钥、token、数据内容、隐藏标签、绝对个人路径写入 Git、实验日志、生成 README 或提交物。data directory 在运行时通过 CLI/env 注入；命令日志把它规范化为 `<DATA_DIR>`，其他路径使用从项目根开始的相对 argv 和脱敏 cwd。

## 可写范围

只允许新增或修改：

- `agent/`
- `models/`
- `features/`
- `experiments/configs/`
- `experiments/logs/`
- `experiments/checkpoints/`
- `experiments/predictions/`
- `experiments/submissions/`
- `scripts/`
- `docs/`
- `tests/`
- 根目录 `README.md`、`.gitignore`、`requirements.txt`、`.env.example`、`THIRD_PARTY_NOTICES.md`（仅在确有需要时）

禁止笼统写“配置文件”或写入其他路径。不要修改本计划文件和上级目录文档。生成物不得覆盖已有未知文件；输出存在时使用 run-id 子目录或明确失败。

## 所需功能模块

实现轻量 Python Agent，不要求 Web UI。建议目录：

agent/
  __init__.py
  orchestrator.py       # 有限状态机，协调实验循环和 CLI
  schemas.py            # ExperimentPlan / ExperimentResult 校验与 JSON
  planner.py            # 基于历史结果的规则 planner + 可选 LLM adapter
  patcher.py            # 受控模板/LLM patch，只能写允许的 plugin/config 路径
  policy.py             # 固定文件、参数、预算、split、路径和命令检查
  registry.py           # 模型工具注册表及合法参数范围
  tools.py              # 受控训练、评估、提交和检查入口
  runner.py             # subprocess timeout、输出、退出码和进程组清理
  selector.py           # validation best、accept/reject、checkpoint 指针回滚
  recovery.py           # 错误分类、至多一次重试、降级建议
  state.py              # 持久化 run 状态、停止条件和最佳产物
  audit.py              # append-only JSONL、Git SHA/diff、资源统计、SHA-256
models/
  __init__.py
  fm_adapter.py         # 封装官方 FM 行为，不改 baseline.py
  pairwise_fm.py        # 首个替代模型：用户内 BPR/pairwise 排序损失
features/
  __init__.py
experiments/
  configs/
  logs/
  checkpoints/
  predictions/
  submissions/
scripts/
  summarize_runs.py
docs/
tests/

可根据实现微调名称，但职责和边界必须清楚。

## 1. Orchestrator

实现并持久化状态机：

`INIT -> BASELINE_VERIFIED -> PLAN -> VALIDATE -> RUN -> EVALUATE -> SELECT -> LOG -> PLAN/STOP`

- 只接受合法 `ExperimentPlan`；不要让 LLM 直接执行任意命令。
- 首版必须有确定性的规则型 planner，无 API key、无网络时仍能完整运行和测试；它必须基于历史结果选择下一步，不能只是固定顺序菜单。
- LLM planner 只做可选协议适配器；没有 SDK/key 时使用 fake adapter 测试，`token_usage=0`。
- planner 输出必须同时包含 hypothesis、单一变化、expected signal、fallback 和允许修改路径；每轮把 decision rationale 写入日志。
- 至少一轮非 baseline 实验必须由 planner 触发受控 code/plugin diff，并完成 validate -> run -> evaluate -> Git accept/reject。无 LLM key 时可使用预审计的 deterministic patch template；日志必须明确其来源，不能声称是 LLM 生成。
- 默认 demo 为 CPU 上最多 3 轮；正式 run 最多 50 轮、6 小时，且收敛规则可更早停止。
- resume 必须从持久化状态继续，不能重复已完成 iteration 或覆盖 append-only 日志。

## 2. Plan / Result 合同

使用 Python 3.9 兼容的 `dataclasses` 和标准库验证/保存 JSON。

`ExperimentPlan` 必填：

- `run_id`, `iteration`, `parent_run_id`
- `hypothesis`, `rationale`, `single_primary_change`
- `experiment_type`, `model_name`, `feature_flags`, `params`, `seed`
- `timeout_minutes`, `expected_cost`, `validation_protocol`
- `acceptance_rule`, `editable_paths`, `requested_tool`

`ExperimentResult` 必填：

- `run_id`, `status`（`accepted` / `rejected` / `failed`）
- `code_version_id`, `parent_git_sha`, `result_git_sha`, `config_path`, `code_diff_summary`, `command`
- `GAUC`, `nDCG@5`, `primary`：成功实验为数字；failed 时必须允许为 `null`
- `elapsed_seconds`, `token_usage`, `gpu_hours`
- `stdout_summary`, `stderr_summary`, `error_class`, `recovery_action`
- `human_intervention`, `human_intervention_reason`
- `artifacts`（checkpoint、prediction、日志等相对路径）

规则型 planner 的 token usage 记录 0；CPU 运行的 GPU-hours 记录 0.0；未知值记录 `null` 并解释，不得伪造。

## 3. Policy / Guardrails

至少实现：

- 禁止写入或改名官方固定文件和数据目录；运行前后比对 SHA-256。
- 精确检查允许写入的目录和文件；拒绝 `..`、符号链接逃逸、绝对输出路径和未声明路径。
- 参数 allowlist 和范围校验，例如 learning rate、embedding dimension、epochs、batch size、seed、loss、pairs-per-user。
- 只允许 train/valid 驱动开发评估；拒绝 test label 输入和 `--score --split test`。
- 每轮只允许一个主要实验变化；拒绝模糊或混合大改动计划。
- 每次训练必须有 timeout；全 run 最多 50 轮、6 小时。
- 检查 prediction score 的长度、dtype、NaN/Inf 和 row order。
- 记录人工介入；不要把人类决定伪装成 Agent 决定。
- 命令必须是 argv allowlist，不接受自由 shell 字符串。

## 4. Runner

- 使用 `subprocess.Popen(..., shell=False, start_new_session=True)` 和 Python timeout。
- timeout 时终止整个 POSIX 进程组，等待回收，并记录退出状态；不得遗留训练进程。
- 限制 stdout/stderr 大小，保存可审计摘要和完整日志的相对路径，脱敏绝对个人路径和 secret-like 值。
- 捕获 command、cwd、退出码、开始/结束时间和 elapsed seconds。
- 不依赖 GNU `timeout`、Docker、GPU 或 shell 激活虚拟环境。

## 5. 模型工具层

所有模型工具遵守统一接口：

`run_experiment(plan: ExperimentPlan, context: RunContext) -> ExperimentResult`

第一版至少支持：

1. `fm`：封装官方 FM，作为 baseline tool，不复制或改写官方评估逻辑。
2. `pairwise_fm`：用户内 BPR/pairwise 排序损失，作为与 GAUC/nDCG 更对齐的首个方向。
3. `submission`：由指定 accepted checkpoint 生成 `row_id,user_id,video_id,score`。
4. `validate_submission`：调用官方 `submit.py --check`。

接口必须允许后续独立添加 deepfm、多任务、历史序列、时间特征或 ensemble，而不修改 Orchestrator。MVP 不因这些未来方向引入 PyTorch。

## 6. 固定评估、选择、收敛与回滚

- 所有开发实验均通过原始 `evaluate.py` 在 validation 上评分。
- baseline 复现顺序：random、pop、FM。CLI 名称是 `pop`，不是 `popularity`。
- random 的单 seed 只做约 0.475 test primary 的宽容 sanity check；发布值是多 seed 均值，不要求逐位相等。
- FM validation 发布参考 primary 约 0.6016；保存真实命令、seed 和输出。
- 初版 accept 条件：`primary > best_primary + 0.002`。
- 收敛：连续 3 轮 validation primary 提升不超过 0.002，或达到 50 轮/6 小时上限，以先到者为准。
- 记录所有 rejected/failed 实验；只有 accepted checkpoint 能更新 best 指针。
- rollback 同时恢复 validation-best checkpoint/config 指针和已知 best Git SHA。只允许恢复本轮由 Agent 创建或修改、且列在 plan 中的路径；禁止 `git reset --hard`、`git clean` 或覆盖 preflight 前已有的用户改动。
- 训练报错、超时、NaN/Inf 时最多自动重试一次；重试必须是预先允许的确定性降级。再次失败则记录 failed，并继续或安全停止。
- 只有收敛时的 validation-best checkpoint 可以生成最终 test submission；不得用 local test 或 hidden test 分数决定下一步。

## 7. Git、日志、版本和可复现性

- 追加式 `experiments/logs/experiments.jsonl`：每轮一个完整 `ExperimentResult`。
- 保存 config snapshot、随机种子、相对命令、指标、耗时、token、GPU-hours、错误、恢复、人工介入、parent/result Git SHA。
- Git 是代码版本主证据：`code_version_id` 使用 commit SHA，`code_diff_summary` 来自实际 `git diff --stat` 和允许路径的语义摘要。
- 每个 accepted 实验必须形成一个原子 commit，包含实现、config、测试和轻量结果记录；commit message 使用 `exp(E###): <single change>`。
- rejected/failed 实验仍必须保留 config 和 append-only 结果记录。回滚本轮受控代码后，用独立 `log(E###): rejected|failed <summary>` commit 保存证据。
- 不把 checkpoint、完整 prediction、submission 或数据反复 commit。Git 跟踪源码、tests、docs、轻量 JSON/JSONL/CSV 摘要；大产物通过相对路径、SHA-256、大小和再生成命令引用。
- 使用标准库 `hashlib` 补充生成 config/artifact SHA-256，并记录 Python 3.9.6、NumPy 2.0.2、平台和固定官方文件哈希。
- 不允许 Agent 自动 merge/rebase/force-push `main`。通过全部 gates 后，只 push `feature/bpr-fm`；合并由团队通过 PR 完成。
- push 前再次 fetch，确认 `origin/main` 未被本任务改动；若远端 feature 分支出现非快进更新，停止并报告，不强推。
- `scripts/summarize_runs.py` 生成可读结果表：baseline、best validation、每轮增量、失败数、人工介入数、迭代数、总 wall-clock、token/GPU 使用。

## 8. 提交路径

- submission 统一写到 `experiments/submissions/<run-id>/submission.csv`。
- 生成前确认 checkpoint 是当前 validation-best accepted checkpoint。
- 生成后必须调用官方 `submit.py --check --split test`。
- 不用 Excel 或 pandas 重排 CSV；严格保持 `data.load()[split]` 行序。
- 不在本地声称得到比赛 hidden-test 分数，不自动上传 Devpost。最终 submission/checkpoint 是否作为 GitHub Release 或 Devpost artifact 上传，由团队另行决定，不直接塞入普通 Git 历史。

## 9. 本机命令与 CLI 验收

所有命令先执行：

cd "/Users/mr.handsome/Documents/GitHub/bytedance-techjam-2026-kuairand"

Git preflight（当前本地尚未创建 tracking branch，因此首次使用第二条）：

git fetch --prune origin
git switch --track -c feature/bpr-fm origin/feature/bpr-fm
git status --short --branch

如果本地 `feature/bpr-fm` 已存在，则使用 `git switch feature/bpr-fm`，不要重复 `-c`。

设置只在本机 shell 使用、不得写入 tracked 文件的 data directory：

export KUAI_DATA_DIR="/Users/mr.handsome/Desktop/TK Hackathon/kuairand-starter-kit/KuaiRand-Pure/data"

使用以下本机兼容命令：

/usr/bin/python3 baseline.py --model random --seed 0 --data_dir "$KUAI_DATA_DIR"
/usr/bin/python3 baseline.py --model pop --data_dir "$KUAI_DATA_DIR"
/usr/bin/python3 baseline.py --model fm --seed 0 --data_dir "$KUAI_DATA_DIR"
/usr/bin/python3 -m unittest discover -s tests -v
/usr/bin/python3 -m agent.orchestrator --data-dir "$KUAI_DATA_DIR" --verify-baseline
/usr/bin/python3 -m agent.orchestrator --data-dir "$KUAI_DATA_DIR" --run --max-iterations 3
/usr/bin/python3 -m agent.orchestrator --data-dir "$KUAI_DATA_DIR" --resume <run-id>
/usr/bin/python3 -m agent.orchestrator --data-dir "$KUAI_DATA_DIR" --generate-submission --checkpoint <path> --output experiments/submissions/<run-id>/submission.csv
/usr/bin/python3 submit.py --data_dir "$KUAI_DATA_DIR" --check --split test experiments/submissions/<run-id>/submission.csv
/usr/bin/python3 scripts/summarize_runs.py

全部 gates 通过后才允许：

git push -u origin feature/bpr-fm

不得把尚未实现的命令写成已验证；先实现，再逐条执行并记录退出码与结果。

## 10. README 与依赖

根目录 `README.md` 必须保留现有官方说明并新增清晰章节：

- public GitHub repository、clone、`feature/bpr-fm` 开发分支和团队 PR 工作流；不得要求读者使用个人绝对路径。
- 本机/通用安装方式；说明本机使用 `/usr/bin/python3`，不要复用 Desktop 副本中的失效 `.venv`。
- 最小依赖与 `requirements.txt`；除非必要，仅声明 NumPy，不引入未使用包。
- 通用 `--data-dir`/环境变量用法、数据验证步骤和缺失数据时的下载说明；README 使用 `<DATA_DIR>` 占位符，不写个人路径。
- 架构图和模块职责。
- 如何运行规则型 Agent，以及如何可选接入 LLM planner。
- 如何增加模型 adapter 或 feature plugin 而不改官方文件。
- local test 与 competition hidden test 的区别。
- autonomy、人工介入、失败恢复、资源日志、Git commit 轨迹和 artifact hash。
- 已知限制、安全边界、结果复现和最终 submission 校验。
- team contributions、三分钟 demo 路径、validation-best 结果表和相对官方 FM 的 delta。

## 验收标准

完成前必须满足：

1. 权威代码工作树的 remote 是上述公开 GitHub 仓库；所有实现位于 `feature/bpr-fm`，未直接修改/push `main`。
2. 开始时工作树干净；每个 accepted 实验可从 JSONL 映射到原子 commit，每个 rejected/failed 实验有保留证据且受控代码已回滚。
3. `.gitignore` 阻止 data、压缩包、环境、缓存和大产物入库；`git ls-files` 中不存在数据、密钥、checkpoint、完整 predictions 或个人绝对路径。
4. 官方固定文件和外部数据的前后 SHA-256 完全一致；保留并报告预先存在的未知文件。
5. 代码可在 Python 3.9.6 + NumPy 2.0.2、macOS arm64、CPU-only 环境运行。
6. 不依赖失效 `.venv`、裸 `python`、pytest、Pydantic、PyTorch、Docker 或 GNU timeout。
7. 外部数据 preflight 得到 train/valid/local-test 1,141,112 / 124,909 / 170,588。
8. random、pop、FM baseline 均从 Git 工作树以显式 `--data_dir` 真实运行；结果与 `baseline_scores.json` 在合理 seed 方差/容差内一致。
9. Agent 能连续运行至少 3 个合法、不同、由历史结果驱动且可审计的计划，不需要真实 LLM API；不得只是固定脚本序列。至少一轮产生受控 plugin/code diff 并由 Git 记录 accept 或 reject。
10. 每轮产生 config snapshot、checkpoint/result artifact 和 append-only JSONL；accept/reject/failed 可由测试验证。
11. 至少一个模拟训练失败或 timeout 的测试，验证自动重试至多一次、正确清理进程、记录失败且 run 不崩溃。
12. 至少一个测试证明 policy 阻止修改 `evaluate.py`、路径逃逸、非法参数和 test-based model selection。
13. prediction/submission 校验拒绝 NaN、Inf、错行数、错行序，并允许官方 test format check。
14. failed result 的指标为 null；规则型 planner token usage=0；CPU GPU-hours=0.0。
15. `python3 -m unittest discover -s tests -v` 通过；不要声称运行不存在的 pytest。
16. 最终 submission 通过 `submit.py --check --split test`，但不在本地声称 hidden-test 得分。
17. `docs/open_source_adaptation.md`、README、架构图、运行摘要、team contributions、限制和三分钟 demo script 齐全。
18. push 前工作树干净，`feature/bpr-fm` 可快进 push 到 origin；远端 `main` 仍是任务开始时的基线。是否创建/合并 PR 由团队决定。

## 实施顺序

1. Git preflight：fetch、确认公开 remote/main、干净状态，切换已有 `feature/bpr-fm`，记录起始 SHA，不改 main。
2. 数据/环境 preflight：显式外部 data directory、split、固定文件 hash、Python/NumPy。
3. 从 Git 工作树只读复现 random/pop/FM baseline；保存证据，不根据 local test 调参。
4. 查阅开源项目并写 `docs/open_source_adaptation.md`；网络不可用时不阻塞、不虚构。
5. 搭建 dataclass schema、policy、state、Git+hash audit、JSONL 和 synthetic `unittest`。
6. 实现安全 runner、timeout 进程组清理和失败恢复测试。
7. 封装 FM tool 和 baseline verification。
8. 实现 pairwise FM adapter，保持统一结果接口，并以原子 experiment commit 记录。
9. 实现 orchestrator、result-driven planner、selector、一次重试 recovery、resume 和 submission 路径。
10. 运行三轮 CPU demo、测试与官方 submission check；检查固定文件 hash、Git history 和 ignore policy。
11. 完善 README、架构图、结果摘要、team contributions、开源适配文档和三分钟 demo script。
12. 最终 fetch/非快进检查，确认工作树干净后 push `feature/bpr-fm`；不 merge main、不提交 Devpost。

不得在无授权时安装依赖、下载数据、调用付费 API、启动无界训练、force-push、修改/合并 main、提交 Devpost 或发布大模型产物。

## 最终汇报格式

完成时汇报：

- 实现的模块和文件。
- 本机环境、解释器、依赖、数据 preflight 和固定文件 hash 结果。
- Git remote、工作分支、起始/最终/validation-best commit SHA、每轮 commit 映射和 push 状态。
- 借鉴/适配的开源项目与具体设计点；未能在线核验的内容明确标注。
- 运行的 unittest、真实 baseline、三轮 autonomous demo 和 submission check 结果。
- validation 结果与 local-test holdout（如执行）分开报告；不得冒充 hidden-test 成绩。
- 数据、网络或凭证限制导致未验证的部分。
- 如何复现三轮实验、resume、汇总和生成 submission。
- token、wall-clock、GPU-hours、人工介入、风险、限制和下一步建议。
```
