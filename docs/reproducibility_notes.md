# 复现说明与数据核验记录

## 1. 本项目基于哪些上传文件修改

本项目直接基于用户上传的 ZIP 工程 `kweichow-moutai-profit-econometrics.zip` 重构，保留并增强以下原始内容：

- `report/计量经济学.docx`：原始课程报告。
- `data/raw/moutai_profit_2000_2023.csv`：原始样本数据。
- `src/`：原 Python 脚本框架。
- `stata/moutai_ecm_analysis.do`：原 Stata 单文件脚本。
- `README.md`、`README_EN.md`、`requirements.txt`、`.gitignore`、`LICENSE`。

## 2. 已做的工程化修改

| 类型 | 修改内容 |
|---|---|
| README | 重写中文与英文 README，加入研究问题、方法路线、公式、结果解释与运行指南 |
| docs | 新增模型说明、研究框架、建模假设、复现说明、Stata 指南和 PDF 说明 |
| Python | 修复原脚本字符串断行导致的语法问题，并拆分为可复用模块 |
| Stata | 将原单文件脚本拆分为分章节 `.do` 文件，并新增 `master.do` 一键入口 |
| 输出 | 新增自动导出的表格、模型摘要和图形目录 |
| 工程化 | 新增 `CITATION.cff`、`Makefile`、更完整的 `.gitignore` 和目录说明 |

## 3. 原报告与脚本结果的关系

原报告中的 ECM 结果来自 EViews 截图。本项目使用 CSV 数据通过 Python / Stata 自动复现。ECM 主要系数可与原报告图 3 对应：

| 变量 | 原报告图 3 系数 |
|---|---:|
| C | -0.031873 |
| DLNX2 | 1.677150 |
| DLNX3 | -0.481618 |
| DLNX4 | 0.592824 |
| DLNX5 | 0.532925 |
| ECM(-1) | -0.619758 |

Python 代码采用与上述一致的建模逻辑：先估计长期方程，保存残差，再将滞后一阶残差作为 `ECM_L1` 加入差分回归。

## 4. 数据核验提示

在原 Word 报告中，表 3 相关系数显示 `LNY` 与 `LNX4` 为正相关；但若直接使用 `data/raw/moutai_profit_2000_2023.csv` 中的 GDP 增长率指数重新计算，`LNX4` 与 `LNY` 的相关性方向可能与报告表格存在差异。为保证复现一致性，本项目以 CSV 文件为唯一可执行数据源，并在输出表格中自动生成相关性矩阵。

这不影响 ECM 公式与原报告图 3 的主要对应关系，但提示读者在写作或展示时说明“脚本输出以 CSV 复算结果为准”。

## 5. 一键复现

Python：

```bash
python -m src.run_all
```

Stata：

```stata
do stata/master.do
```

## 6. 可复现输出

完整运行后应生成：

- `data/processed/moutai_profit_processed.csv`
- `outputs/tables/descriptive_statistics.csv`
- `outputs/tables/correlation_matrix.csv`
- `outputs/tables/adf_tests.csv`
- `outputs/tables/cointegration_residual_adf.csv`
- `outputs/tables/long_run_coefficients.csv`
- `outputs/tables/ecm_coefficients.csv`
- `outputs/tables/vif.csv`
- `outputs/tables/diagnostic_tests.csv`
- `outputs/models/long_run_summary.txt`
- `outputs/models/ecm_summary.txt`
- `outputs/figures/01_level_trends.png`
- `outputs/figures/02_log_scatter_matrix.png`
- `outputs/figures/03_actual_fitted_ecm.png`
- `outputs/figures/04_ecm_residuals.png`

## 7. 展示建议

GitHub 展示时建议在仓库首页突出三点：

1. 本项目将 Word 课程论文升级为可复现工程。
2. 同时提供 Python 与 Stata 实现，适合计量经济学课程和金融实证展示。
3. ECM 结果能够解释贵州茅台净利润的长期均衡与短期修正机制。
