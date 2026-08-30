# 已验证结果

验证日期：2026-08-30

数据：KuaiRand-Pure 全量官方 train/valid 切分

评估：原始 evaluate.py；test 未用于模型选择，也未在本轮运行中评分

## 1. 代码连通性

四个版本均已通过真实 CSV 冒烟测试，能够完成：

- 数据读取与编码
- Pointwise 或 Pairwise 训练
- 官方 valid 评分
- early stopping
- 最佳 checkpoint 保存与恢复
- epoch JSONL 日志
- validation_predictions.csv 输出
- summary.json 输出

## 2. 官方 Baseline 复现

seed 0：

- GAUC 0.66713
- nDCG@5 0.53581
- Primary 0.60147

官方 valid 参考为 0.6016，差异约 -0.00013，复现通过。

## 3. 三个 seed 的公平配对结果

| 版本 | seed 0 | seed 1 | seed 2 | 平均 Primary | 相对同 seed Baseline 的平均变化 |
|---|---:|---:|---:|---:|---:|
| Pointwise Baseline | 0.601470 | 0.601761 | 0.601090 | 0.601440 | 0 |
| Pairwise BPR | 0.603396 | 0.602221 | 0.603226 | 0.602948 | +0.001507 |
| 历史/时间 + Pairwise | 0.603638 | 0.603143 | 0.604199 | 0.603660 | +0.002220 |

历史/时间 Pairwise 的三个配对提升分别为：

- seed 0：+0.002168
- seed 1：+0.001382
- seed 2：+0.003109

初步解释：

- 单纯改成 Pairwise 有正向信号，但三 seed 平均尚未达到 +0.002。
- 在 Pairwise 上加入严格只看过去的历史/时间特征，三 seed 均正向，平均超过 +0.002。
- 目前只有三个 seed，仍建议补完 seed 3、4，再决定是否作为正式 best candidate。

## 4. 难负例结果

未经热身的纯难负例曾下降到 Primary 0.57714，说明随机初始化模型产生的所谓难负例不可信。

修正后的版本：

- 前 3 轮使用随机负例
- 后续 50% 使用难负例，50% 保留随机负例
- 恶化时 early stop 并恢复最佳 checkpoint

seed 0 最终保留 Primary 0.60147，没有超过普通 Pairwise。该方向目前应标记为 rejected，不应由 Agent 重复相同配置。

## 5. 官方提交校验

以下三个完整版本的 validation_predictions.csv 已通过官方 submit.py 的格式、行数、row_id、user_id、video_id、NaN/Inf 和评分校验：

- Pointwise Baseline：124,909 行，Primary 0.6015
- Pairwise BPR：124,909 行，Primary 0.6034
- 历史/时间 Pairwise：124,909 行，Primary 0.6036

## 6. 当前可确认与不可确认

可以确认：

- 实验代码可运行并与官方评估对齐。
- Pairwise 在三个 seed 中均高于对应 Pointwise。
- 历史/时间 Pairwise 的三个 seed 平均提升约 0.00222。
- 简单难负例挖掘没有收益，系统能够拒绝并回滚。

尚不能确认：

- test 分数是否同步提升。
- 五个 seed 后平均提升是否仍超过 0.002。
- 提升主要来自时间特征还是四个历史统计特征；这需要下一轮消融。
- 真实线上用户的 long-view 是否提升；本实验只有离线验证。

## 7. 下一项最小实验

建议按以下顺序继续：

1. 补跑 seed 3、4。
2. 对 Iteration 03 做消融：只加时间、只加用户历史、只加视频历史。
3. valid 结论冻结后，最终候选只评分一次 test。
4. 再考虑多目标或 Listwise，不要立即跳到 DeepFM。

