# KuaiRand 推荐模型迭代试验室

这套文件不会修改官方 baseline.py、data.py 或 evaluate.py。它们从官方目录只读加载数据与评分规则，把每次实验结果写到本目录下的 runs 文件夹。

## 1. 先看懂：这四个版本分别在验证什么

### Iteration 00：官方 Pointwise FM

文件：iteration_00_official_pointwise.py

它回答：我们能否公平复现官方五个特征的 FM？

与官方相比，模型逻辑不变，只增加：

- 最佳模型保存
- 每轮 JSON 日志
- 验证集预测文件
- test 默认不可见

这是所有实验的对照组。

### Iteration 01：Pairwise BPR FM

文件：iteration_01_pairwise_bpr.py

它保留同一个 FM 打分公式，只改变学习方式：

- Pointwise 问：这一行是不是 long_view？
- Pairwise 问：同一用户的正例是否比负例分数高？

每一轮会为同一用户自动组成正负曝光对。全正或全负用户无法组成 pair，不进入这一项 pairwise loss，但仍按官方规则参加验证评分。

这是 README 最建议优先探索的方向。

### Iteration 02：难负例 Pairwise BPR

文件：iteration_02_hard_negative_bpr.py

普通 BPR 随机挑选负例。难负例版本先用随机负例热身；模型有基本判断能力后，再从几个负例候选中挑当前分数最高、最容易误判的负例，并与普通负例混合训练。

类比：普通练习随机做错题；难负例练习专门做最容易混淆的错题。

它只相对 Iteration 01 改变负例选择方式。

### Iteration 03：历史/时间特征 + Pairwise

文件：iteration_03_history_pairwise.py

在 Iteration 01 的随机负例 BPR 基础上，增加：

- 小时桶
- 星期
- 用户过去曝光次数桶
- 用户过去 long_view 比例桶
- 视频过去曝光次数桶
- 视频过去 long_view 比例桶

严格防泄漏规则：

- 训练行只使用更早日期的统计
- 同一天的 label 不反哺同一天特征
- valid/test 只使用 train 结束时冻结的统计
- valid/test 的点击、观看和 long_view 不进入特征

## 2. 截图七个方向的零基础解释

### 方向 1：换损失函数

模型是打分机器，Loss 是老师怎样批改作业。官方老师逐题判断 0/1，但比赛考的是排序。Pairwise 把练习方式改成正例与负例比较，使练习题更像正式考试。

本试验室已实现随机负例 BPR 和难负例 BPR。

### 方向 2：用户历史序列

官方只知道用户是谁，没有直接告诉模型这个用户刚刚连续看过哪些内容。完整 DIN/SIM 会读取按时间排列的视频序列，再判断当前视频与近期兴趣是否匹配。

本试验室先实现低风险历史统计版，不直接实现 DIN/SIM。原因是 DIN/SIM 需要新的深度学习框架、序列 padding、attention 和更大资源，适合第二阶段。

### 方向 3：多目标

除了 long_view，日志还有点击、点赞、关注、评论、转发和观看时长。多目标模型让同一个底层表示同时学习这些行为，但最终提交仍输出 long_view score。

当前版本没有把本次点击或观看时长直接当输入，因为那会偷看推荐发生后的答案。第二阶段可以把这些行为作为辅助训练标签，并让 Agent 调整不同任务的 Loss 权重。

### 方向 4：观看时长建模

视频总长 20 秒，用户看完 20 秒，不表示他只愿意看 20 秒；真实兴趣被视频结束截断。CWM 用删失回归处理这个问题。

这是有研究价值但实现和验证成本较高的第二阶段方向。

### 方向 5：DeepFM/DCN/xDeepFM

它们是更复杂的打分机器，不保证自动更好。官方已经证明单纯扩大 FM 容量几乎无收益，因此先验证 Loss 和历史信息，再换复杂模型。

### 方向 6：时间与分布漂移

用户兴趣和内容流量会随日期与小时变化。Iteration 03 加入小时和星期；更进一步可以比较 train、valid、test 的分布变化。

### 方向 7：随机曝光无偏验证

标准日志来自旧推荐系统挑选过的流量，数据本身带有偏好。random 日志像随机抽查，可检查模型是否只适合旧系统选择过的内容。

它应作为额外验证，不应该混进官方训练/验证主分，也不能代替 evaluate.py。

## 3. 对官方 baseline.py 的问题分析

### 问题 A：训练目标与评分目标不完全一致

官方使用 Pointwise Logloss，最终评分是 GAUC 和 nDCG@5。Iteration 01/02 改为直接比较同一用户的正负曝光。

### 问题 B：只使用五个静态域

官方使用 user_id、video_id、author_id、tab、dur_bucket，没有历史行为和时间变化。Iteration 03 增加严格只看过去的统计。

### 问题 C：每次训练都输出 test 分数

如果 Agent 每轮看到 test，就会逐渐针对 test 调参。本试验室默认只看 valid；只有最终选定版本显式加 --score-test 才读取 test 指标。

### 问题 D：训练完成不保存模型

官方 run_fm 只返回指标，进程结束后模型消失。本试验室保存 best_model.npz。

### 问题 E：缺少实验证据

官方没有逐轮 JSON、配置快照、验证预测和输出目录。本试验室每次运行都会保存。

### 问题 F：部分训练设置不能从命令行修改

官方只暴露 k、lr、epochs、seed。本试验室同时开放 l2、batch-size、patience、负例数量和难负例候选数。

### 问题 G：没有面向 Agent 的边界

官方脚本没有防止 Agent 反复读取 test、覆盖旧结果或无限运行。本试验室先把 test 设成显式开关，并把每次结果隔离到独立目录。真正接 LLM 前还应增加文件白名单、时间预算和最大迭代数。

## 4. 第一次安装

在 VS Code 打开 Terminal，依次运行：

    cd /Users/xixi/Documents/Codex/2026-08-28/referenced-chatgpt-conversation-this-is-an/outputs/kuairand_trial_lab
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

如果你的数据或 starter kit 不在默认位置，每条运行命令都可以增加 --data-dir 和 --starter-dir。

## 5. 先做两轮冒烟测试

冒烟测试只证明代码能跑，不用于判断模型好坏：

    python3 run_trial_suite.py --smoke

它会限制训练和验证行数，只跑两轮。看到四个版本都生成 summary.json 即通过。

不要拿冒烟测试分数与官方 0.6016 比，因为冒烟测试只用了部分数据。

## 6. 单独运行完整版本

官方 Pointwise：

    python3 iteration_00_official_pointwise.py

随机负例 Pairwise：

    python3 iteration_01_pairwise_bpr.py

难负例 Pairwise：

    python3 iteration_02_hard_negative_bpr.py

历史特征 Pairwise：

    python3 iteration_03_history_pairwise.py

运行全部四个版本并生成排行榜：

    python3 run_trial_suite.py --epochs 40

第一次完整试运行建议分别运行，不要一次启动四个，以便及时发现内存或耗时问题。

## 7. 每次运行会生成什么

每个 runs/iteration_xx 文件夹包含：

- config.json：本次实验设置
- epochs.jsonl：每轮 Loss、指标和耗时
- best_model.npz：验证集最好的 FM 参数
- validation_predictions.csv：验证集每行 score
- summary.json：最好轮次、最终指标、运行时间和文件位置

只在加入 --score-test 时生成：

- test_predictions.csv
- summary.json 中的 test 指标

## 8. 正式比较的规则

不要只运行一个 seed 就下结论。至少运行 seed 0 到 4：

    python3 iteration_01_pairwise_bpr.py --seed 0 --output-dir runs/bpr_seed0
    python3 iteration_01_pairwise_bpr.py --seed 1 --output-dir runs/bpr_seed1
    python3 iteration_01_pairwise_bpr.py --seed 2 --output-dir runs/bpr_seed2
    python3 iteration_01_pairwise_bpr.py --seed 3 --output-dir runs/bpr_seed3
    python3 iteration_01_pairwise_bpr.py --seed 4 --output-dir runs/bpr_seed4

官方给出的 FM seed 标准差约 0.0008。项目层面的接受标准可以沿用：提升超过 0.002，并在多个 seed 中方向基本一致。

不要为了提高平均分隐藏 GAUC 或 nDCG@5 的下降。每次都同时比较三个指标。

## 9. 负例相关参数怎样调

每个正例配两个负例：

    python3 iteration_01_pairwise_bpr.py --negative-per-positive 2

前三轮使用随机负例，之后从十个候选中选择，并让 50% 的 pair 使用难负例：

    python3 iteration_02_hard_negative_bpr.py --hard-negative-warmup 3 --hard-candidates 10 --hard-negative-ratio 0.5

限制每轮最多二十万 pair，便于低成本实验：

    python3 iteration_01_pairwise_bpr.py --max-pairs-per-epoch 200000

这些设置改变的是训练数据组织，不改变官方验证和评分规则。

## 10. 最后一次才看 test

当 valid 已经选出最终版本后，才运行：

    python3 iteration_01_pairwise_bpr.py --score-test --output-dir runs/final_candidate

不要让未来的 LLM Agent 获得 --score-test 权限。Agent 只能看到 valid；最终人工封版时才执行 test。

## 11. 怎样接到 Research Agent

这四个版本是 Agent 的工具层，还不是完整 Agent。

下一阶段由 CS 把它们包装成：

- run_baseline
- run_pairwise
- run_hard_negative
- run_history_pairwise
- read_summary
- accept_checkpoint
- rollback_checkpoint

LLM 每轮只输出结构化 ExperimentPlan。程序检查路径、预算、参数范围和是否重复后，才允许调用上述工具。

一个合格的 Agent 不是按固定顺序把四个文件全跑完，而是根据上轮 GAUC、nDCG@5、Primary、耗时和错误决定下一步。

## 12. 当前版本刻意没有做什么

- 没有修改官方 evaluate.py
- 没有把本次 click/play_time 当输入
- 没有读取 random 日志作为训练数据
- 没有默认把 test 暴露给实验循环
- 没有直接上 DeepFM
- 没有声称某个实验一定提高分数

是否真正提高，必须以完整数据、多 seed、同一 valid 协议的实际结果为准。
