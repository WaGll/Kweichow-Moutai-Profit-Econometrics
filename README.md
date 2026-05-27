# 贵州茅台净利润模型及实证分析

> 基于课程论文《贵州茅台净利润模型及实证分析》重构的可复现计量经济学项目。项目以贵州茅台 2000-2023 年年度数据为样本，围绕净利润、营业收入、营业成本、GDP 增长率和 CPI 建立对数长期均衡模型，并通过 ADF 单位根检验、Engle-Granger 协整检验和误差修正模型（ECM）解释长期均衡与短期调整机制。

本仓库不是简单保存课程作业，而是将原始 Word 报告、数据、Python 代码和 Stata 脚本整理为一个可以在 GitHub 展示、复现和扩展的计量经济学工程。

## 1. 研究问题

贵州茅台净利润的变化主要受哪些因素影响？营业收入、营业成本、宏观经济增长和价格水平变量是否与净利润之间存在长期均衡关系？当短期利润偏离长期均衡时，系统是否会通过误差修正机制回到均衡路径？

## 2. 数据与变量

样本区间为 2000-2023 年，共 24 个年度观测值。原始数据文件为：

```text
data/raw/moutai_profit_2000_2023.csv
```

| 原始变量 | 代码变量 | 含义 | 单位或口径 |
|---|---:|---|---|
| `net_profit_y_billion_cny` | `Y` | 净利润 | 亿元 |
| `operating_revenue_x2_billion_cny` | `X2` | 营业收入 | 亿元 |
| `operating_cost_x3_billion_cny` | `X3` | 营业成本 | 亿元 |
| `gdp_growth_index_x4_prev_year_100` | `X4` | GDP 增长率指数 | 上年 = 100 |
| `cpi_x5_1978_100` | `X5` | 居民消费价格指数 | 1978 = 100 |

建模变量为自然对数形式：`LNY`、`LNX2`、`LNX3`、`LNX4`、`LNX5`。一阶差分变量为：`DLNY`、`DLNX2`、`DLNX3`、`DLNX4`、`DLNX5`。

## 3. 方法路线

项目方法与原报告保持一致，并补充了可复现代码：

```text
数据整理
  -> 对数变换
  -> 描述性统计与相关性分析
  -> ADF 单位根检验
  -> 长期均衡 OLS 回归
  -> Engle-Granger 残差协整检验
  -> ECM 误差修正模型
  -> VIF / White / Breusch-Godfrey 诊断
  -> 图表与结果导出
```

核心模型包括长期对数模型：

```math
\ln Y_t = C + \beta_1 \ln X_{2t} + \beta_2 \ln X_{3t} + \beta_3 \ln X_{4t} + \beta_4 \ln X_{5t} + u_t
```

以及误差修正模型：

```math
\Delta \ln Y_t = \alpha_0 + \alpha_1 \Delta \ln X_{2t} + \alpha_2 \Delta \ln X_{3t} + \alpha_3 \Delta \ln X_{4t} + \alpha_4 \Delta \ln X_{5t} + \lambda ECM_{t-1} + \varepsilon_t
```

原报告最终 ECM 估计式为：

```math
\Delta \ln Y_t = -0.031873 + 1.677150\Delta\ln X_{2t} - 0.481618\Delta\ln X_{3t} + 0.592824\Delta\ln X_{4t} + 0.532925\Delta\ln X_{5t} - 0.619758ECM_{t-1}
```

其中 `ECM_{t-1}` 系数为负，表示当净利润短期偏离长期均衡水平时，下一期会出现向长期均衡回归的调整机制。

## 4. 主要结论

- 营业收入 `DLNX2` 对净利润增速具有显著正向影响，是解释贵州茅台利润增长的核心变量。
- 营业成本 `DLNX3` 对净利润增速具有显著影响，系数为负，符合利润形成机制。
- `ECM(-1)` 系数约为 `-0.6198`，且通过显著性检验，说明短期偏离会被修正，存在长期均衡关系。
- GDP 增长率和 CPI 在 ECM 中的短期显著性较弱，说明公司利润更多由自身经营变量解释，而不是由年度宏观变量直接解释。
- White 检验和 Breusch-Godfrey LM 检验结果显示，最终 ECM 未发现明显异方差和自相关问题。

> 复现说明：原 Word 报告中的部分结果来自 EViews 截图。本项目的 Python 与 Stata 代码均以 `data/raw/moutai_profit_2000_2023.csv` 为统一数据源自动计算，保证结果可追踪、可复现。

## 5. 仓库结构

```text
kweichow-moutai-profit-econometrics/
├─ data/
│  ├─ raw/                         # 原始年度数据
│  └─ processed/                   # 清洗、对数化、差分后的数据
├─ docs/
│  ├─ econometric_model_guide.md    # 模型公式、经济含义与原文结果对应
│  ├─ research_framework.md         # 研究框架与方法论逻辑
│  ├─ model_assumptions.md          # 建模假设与适用边界
│  ├─ reproducibility_notes.md      # 复现说明与数据核验记录
│  ├─ stata_guide.md                # Stata 脚本说明
│  └─ model_formula_guide.pdf       # 公式与方法说明 PDF
├─ notebooks/                       # 原始 Python 教学笔记本
├─ src/
│  ├─ config.py                     # 路径配置
│  ├─ data_process.py               # 数据清洗与变量生成
│  ├─ model.py                      # 长期模型、协整、ECM
│  ├─ diagnostics.py                # ADF、VIF、White、BG 检验
│  ├─ visualize.py                  # 图表导出
│  └─ run_all.py                    # Python 一键复现入口
├─ stata/
│  ├─ master.do                     # Stata 一键运行入口
│  ├─ 00_setup.do                   # 路径与日志设置
│  ├─ 01_data_preparation.do        # 数据导入、对数与差分
│  ├─ 02_descriptive_analysis.do    # 描述统计与相关性分析
│  ├─ 03_stationarity_cointegration.do
│  ├─ 04_ecm_diagnostics.do
│  ├─ 05_export_results.do
│  └─ moutai_ecm_analysis.do        # 兼容原单文件脚本入口
├─ outputs/
│  ├─ figures/                      # 自动导出的图片
│  ├─ tables/                       # 自动导出的表格
│  └─ models/                       # 模型摘要文本
├─ report/
│  └─ 计量经济学.docx               # 原始课程论文
├─ CITATION.cff
├─ README.md
├─ README_EN.md
├─ requirements.txt
├─ .gitignore
└─ LICENSE
```

## 6. 快速开始：Python 复现

```bash
# 1. 克隆仓库后进入项目目录
cd kweichow-moutai-profit-econometrics

# 2. 安装依赖
pip install -r requirements.txt

# 3. 一键运行完整流程
python -m src.run_all
```

运行后会自动生成：

```text
data/processed/moutai_profit_processed.csv
outputs/tables/descriptive_statistics.csv
outputs/tables/correlation_matrix.csv
outputs/tables/adf_tests.csv
outputs/tables/long_run_coefficients.csv
outputs/tables/ecm_coefficients.csv
outputs/tables/vif.csv
outputs/tables/diagnostic_tests.csv
outputs/figures/*.png
outputs/models/*.txt
```

也可以分步运行：

```bash
python -m src.data_process
python -m src.model
python -m src.diagnostics
python -m src.visualize
```

## 7. Stata 复现

在 Stata 中进入项目根目录后执行：

```stata
do stata/master.do
```

如果只想运行兼容原始版本的单脚本，也可以执行：

```stata
do stata/moutai_ecm_analysis.do
```

## 8. 文档阅读顺序

建议按以下顺序阅读：

1. `report/计量经济学.docx`：原始课程论文。
2. `docs/research_framework.md`：研究设计与方法流程。
3. `docs/econometric_model_guide.md`：模型公式、经济含义、结果解释。
4. `docs/model_assumptions.md`：建模假设、局限与稳健性说明。
5. `docs/reproducibility_notes.md`：复现逻辑、数据核验与原报告对应关系。
6. `docs/stata_guide.md`：Stata 工程运行说明。

## 9. 数据来源

- 国家统计局数据库：GDP 增长率、CPI。
- 东方财富数据中心：贵州茅台财务数据。
- 巨潮资讯：贵州茅台 2000-2023 年利润表。

本仓库保留原报告中的数据来源说明，并将样本数据整理为 CSV 文件以便复现。

## 10. 引用

如果你在课程展示、论文复现或项目说明中引用本仓库，可参考 `CITATION.cff`。

## 11. License

MIT License. 仅供课程学习、方法复现和展示使用，不构成投资建议。
