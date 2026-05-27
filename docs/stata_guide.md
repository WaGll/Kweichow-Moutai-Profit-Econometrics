# Stata 使用指南

## 1. 一键运行

在 Stata 中将工作目录切换到项目根目录，然后执行：

```stata
do stata/master.do
```

`master.do` 会按顺序运行以下脚本：

```text
00_setup.do
01_data_preparation.do
02_descriptive_analysis.do
03_stationarity_cointegration.do
04_ecm_diagnostics.do
05_export_results.do
```

## 2. 文件说明

| 文件 | 功能 |
|---|---|
| `00_setup.do` | 设置路径、创建输出目录、开启日志 |
| `01_data_preparation.do` | 导入 CSV，生成对数变量和一阶差分变量 |
| `02_descriptive_analysis.do` | 描述性统计、相关性矩阵、趋势图 |
| `03_stationarity_cointegration.do` | ADF 单位根检验、长期方程、残差协整检验 |
| `04_ecm_diagnostics.do` | ECM 回归、VIF、White 检验、BG-LM 检验 |
| `05_export_results.do` | 导出处理后数据与保存日志 |
| `moutai_ecm_analysis.do` | 兼容原始仓库的单文件入口，内部调用 `master.do` |

## 3. Stata 输出

运行后将生成：

```text
data/processed/moutai_profit_processed_stata.csv
outputs/models/stata_master.log
outputs/figures/stata_lny_trend.png
```

## 4. 滞后阶数说明

原报告中的 EViews 截图采用了固定或默认的滞后设定。本项目 Stata 脚本为了保持课程报告可读性，ADF 检验默认采用 `lags(1)` 或注释中指定的简单设定。正式研究中建议依据 AIC、SIC、HQ 等信息准则选择滞后阶数，并对趋势项和截距项设定进行稳健性比较。

## 5. 与 Python 结果的差异

不同软件在 ADF 检验的默认滞后阶数、趋势项和临界值计算上可能存在差异。因此：

- ECM 回归系数应高度一致。
- ADF 检验结果可能因设定不同略有差异。
- README 中的核心经济解释以原报告与 ECM 结果为主。
