# manuscript-audit：检查、修复、复查的完整教学案例

**合成材料；检查实际执行；报告在本次实现过程中编写；没有独立模型评测。**

此例用 48 个生成样本、12 个生成患者和纯 Python 1-NN 分类器，展示如何将质疑转为可检查的证据。没有医学数据、GPU、依赖安装或模型服务调用。

## 从这里读

1. [原稿](original/manuscript.md)及[配置](original/config.json)。
2. [具体审查与检查依据](audit.md)：两项确认问题、一项证据不足、一项被排除的质疑。
3. [修改差异](repair.diff)与[修复后稿件](revised/manuscript.md)。
4. [复查结果](recheck.md)。

| 检查 | 原版本 | 修复后版本 |
|---|---|---|
| 训练／测试患者交集 | 12 个患者 | 空集 |
| 实际准确率 | 12/12 = 1.0 | 4/16 = 0.25 |
| 稿件表格 | 0.93，不匹配 | 0.25，匹配 |
| 归一化仅拟合训练集 | 检查通过；质疑排除 | 检查通过 |
| 组件因果归因 | 缺乏消融依据 | 撤回强主张，保留限制 |

两版本测试集合不同，这个成绩变化不构成泄漏影响的受控因果估计。低成绩被如实保留；修复让实验与表述一致，并不把模型变成好模型。

## 本地重跑

在本目录执行；将 `python` 换为项目现有解释器亦可。输出采用新文件名，避免覆盖归档结果：

```text
python experiment.py --data data.csv --config original/config.json --output original-result-rerun.json
python verify.py --data data.csv --config original/config.json --manuscript original/manuscript.md --result original-result-rerun.json --output original-check-rerun.json
python experiment.py --data data.csv --config revised/config.json --output revised-result-rerun.json
python verify.py --data data.csv --config revised/config.json --manuscript revised/manuscript.md --result revised-result-rerun.json --output revised-check-rerun.json
```

预期退出码依次为 **0、1、0、0**。原版本的 1 表示检查确实检出预设问题；不是程序异常。重复执行时换一个新输出文件名。

## 原始证据与边界

- [原始预测](original/result.json)、[检查失败](original/check.json)、[执行日志](original/execution.json)。
- [修复后预测](revised/result.json)、[检查通过](revised/check.json)、修复后[实验日志](revised/experiment-execution.json)和[检查日志](revised/check-execution.json)。
- 程序结果包含输入哈希；检查器记录逐项结果并标注 `semantic_quality: not_evaluated`。
- 回归测试包含伪造拟合范围、篡改预测和缺失报告值的负向检查。

这套公开案例用于展示流程。之后的三组对照使用另行封存的材料；教学报告不能记作某一条件的模型输出。
