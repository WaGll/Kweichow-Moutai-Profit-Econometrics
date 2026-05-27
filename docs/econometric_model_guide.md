# 计量经济模型说明：贵州茅台净利润模型及实证分析

本文档根据原始报告《计量经济学.docx》整理，重点说明每个模型的公式、经济学含义、采用原因，以及与原报告结果之间的对应关系。

## 1. 变量设定

设贵州茅台第 `t` 年净利润为 `Y_t`，营业收入为 `X_{2t}`，营业成本为 `X_{3t}`，GDP 增长率指数为 `X_{4t}`，CPI 为 `X_{5t}`。

为降低量纲差异并将系数解释为近似弹性，报告采用自然对数变换：

```math
LNY_t = \ln Y_t
```

```math
LNX_{it} = \ln X_{it}, \quad i=2,3,4,5
```

一阶差分变量表示对数增长率：

```math
DLNY_t = \Delta \ln Y_t = \ln Y_t - \ln Y_{t-1}
```

```math
DLNX_{it} = \Delta \ln X_{it} = \ln X_{it} - \ln X_{i,t-1}
```

## 2. 初始长期对数模型

原报告设定的初始模型为：

```math
\ln Y_t = C + \beta_1 \ln X_{2t} + \beta_2 \ln X_{3t} + \beta_3 \ln X_{4t} + \beta_4 \ln X_{5t} + u_t
```

### 经济学含义

- `\beta_1`：营业收入对净利润的长期弹性。预期为正，因为收入增长通常会提高利润规模。
- `\beta_2`：营业成本对净利润的长期弹性。预期为负，因为成本上升会压缩利润空间。
- `\beta_3`：宏观经济增长对企业利润的长期影响。
- `\beta_4`：价格水平变化对企业利润的长期影响，可能通过消费价格、产品价格和成本价格共同作用。
- `u_t`：长期均衡误差，表示实际净利润与长期均衡水平之间的偏离。

### 为什么采用对数模型

1. 可以缓解变量量纲差异，避免净利润、收入、成本和宏观指数在数值尺度上差异过大。
2. 系数可解释为弹性，更适合财务变量与经济变量之间的比例关系分析。
3. 对时间序列数据而言，对数变换通常能减弱异方差问题。

## 3. ADF 单位根检验

时间序列回归容易出现伪回归问题，因此需要先检验变量是否平稳。ADF 检验的一般形式为：

```math
\Delta y_t = \alpha + \rho y_{t-1} + \sum_{i=1}^{p}\gamma_i \Delta y_{t-i} + \varepsilon_t
```

带趋势项时可写为：

```math
\Delta y_t = \alpha + \delta t + \rho y_{t-1} + \sum_{i=1}^{p}\gamma_i \Delta y_{t-i} + \varepsilon_t
```

### 原假设与判断

- 原假设 `H_0`：序列存在单位根，即非平稳。
- 备择假设 `H_1`：序列不存在单位根，即平稳。
- 若 ADF 统计量小于临界值，或 P 值小于显著性水平，则拒绝原假设。

### 与原报告对应

原报告表 4 的结论为：大部分原序列非平稳，一阶差分后变为平稳序列。因此净利润、营业收入、营业成本、CPI 等变量可作为一阶单整序列处理，并进一步进行协整检验。

## 4. Engle-Granger 两步法协整检验

当多个非平稳变量均为同阶单整时，如果它们的某种线性组合是平稳序列，则变量之间存在协整关系，即存在长期均衡关系。

### 第一步：估计长期方程

```math
LNY_t = C + \beta_1 LNX2_t + \beta_2 LNX3_t + \beta_3 LNX4_t + \beta_4 LNX5_t + u_t
```

得到残差：

```math
\widehat{u}_t = LNY_t - \widehat{LNY}_t
```

### 第二步：对残差进行 ADF 检验

```math
\Delta \widehat{u}_t = \phi \widehat{u}_{t-1} + \sum_{i=1}^{p}\theta_i \Delta \widehat{u}_{t-i} + \eta_t
```

若残差序列平稳，则说明 `LNY` 与 `LNX2`、`LNX3`、`LNX4`、`LNX5` 之间存在长期均衡关系。

### 与原报告对应

原报告图 2 对长期回归残差进行单位根检验，结论为残差序列平稳，因此认为变量之间存在协整关系。该结论是进一步构建 ECM 的基础。

## 5. 误差修正模型 ECM

若变量之间存在长期均衡关系，短期波动可通过误差修正模型表示：

```math
\Delta LNY_t = \alpha_0 + \alpha_1 \Delta LNX2_t + \alpha_2 \Delta LNX3_t + \alpha_3 \Delta LNX4_t + \alpha_4 \Delta LNX5_t + \lambda ECM_{t-1} + \varepsilon_t
```

其中：

```math
ECM_{t-1} = \widehat{u}_{t-1}
```

### 经济学含义

- `\Delta LNY_t` 表示净利润增长率。
- `\Delta LNX2_t` 表示营业收入增长率，解释收入短期变化对利润增长的影响。
- `\Delta LNX3_t` 表示营业成本增长率，解释成本变化对利润增长的影响。
- `\Delta LNX4_t` 和 `\Delta LNX5_t` 分别表示宏观经济增长和价格水平的短期变化。
- `ECM_{t-1}` 表示上一期偏离长期均衡的程度。
- `\lambda` 为误差修正系数。若 `\lambda < 0` 且显著，则说明系统具有向长期均衡回归的调整机制。

### 原报告最终模型

原报告图 3 给出的 ECM 估计结果为：

```math
\Delta \ln Y_t = -0.031873 + 1.677150\Delta\ln X_{2t} - 0.481618\Delta\ln X_{3t} + 0.592824\Delta\ln X_{4t} + 0.532925\Delta\ln X_{5t} - 0.619758ECM_{t-1}
```

对应 t 统计量为：

```text
C:        -1.118392
DLNX2:     7.608241
DLNX3:    -2.645002
DLNX4:     1.089809
DLNX5:     0.485431
ECM(-1):  -2.906337
```

对应解释为：

- `DLNX2` 显著为正，说明营业收入增长对净利润增长有显著正向作用。
- `DLNX3` 显著为负，说明营业成本增长会压缩净利润增长。
- `DLNX4` 与 `DLNX5` 未通过常规显著性检验，说明宏观变量对企业年度利润增长的直接短期解释力较弱。
- `ECM(-1)` 显著为负，说明上一期偏离长期均衡的误差会在下一期被修正。

## 6. 多重共线性检验：VIF

方差膨胀因子定义为：

```math
VIF_j = \frac{1}{1-R_j^2}
```

其中 `R_j^2` 是将第 `j` 个解释变量对其他解释变量回归得到的拟合优度。

### 判断标准

- `VIF < 5`：通常认为多重共线性不严重。
- `5 <= VIF < 10`：存在一定共线性，需要关注。
- `VIF >= 10`：多重共线性较严重。

原报告图 4 的结论为：模型没有严重多重共线性问题。

## 7. White 异方差检验

White 检验用于判断残差方差是否随解释变量变化。其原假设为：

```math
H_0: Var(\varepsilon_t) = \sigma^2
```

即不存在异方差。

原报告图 5 显示：F 统计量对应 P 值约为 `0.7490`，Obs*R-squared 对应 P 值约为 `0.4560`，均大于 `0.05`，因此不拒绝同方差原假设。

## 8. Breusch-Godfrey LM 自相关检验

BG-LM 检验用于判断残差是否存在高阶自相关。原假设为：

```math
H_0: \rho_1 = \rho_2 = \cdots = \rho_p = 0
```

原报告图 6 显示：F 统计量对应 P 值约为 `0.3751`，Obs*R-squared 对应 P 值约为 `0.2443`，均大于 `0.05`，因此不拒绝无自相关原假设。

## 9. 结果与论文结论的对应关系

| 原报告内容 | 本项目对应文件 |
|---|---|
| 表 1 原始变量数据 | `data/raw/moutai_profit_2000_2023.csv` |
| 表 2 描述性统计 | `outputs/tables/descriptive_statistics.csv` |
| 表 3 相关性分析 | `outputs/tables/correlation_matrix.csv` |
| 表 4 ADF 检验 | `outputs/tables/adf_tests.csv` |
| 图 1 散点图 | `outputs/figures/02_log_scatter_matrix.png` |
| 图 2 残差 ADF 检验 | `outputs/tables/cointegration_residual_adf.csv` |
| 图 3 ECM 回归 | `outputs/tables/ecm_coefficients.csv` 与 `outputs/models/ecm_summary.txt` |
| 图 4 VIF 检验 | `outputs/tables/vif.csv` |
| 图 5 White 检验 | `outputs/tables/diagnostic_tests.csv` |
| 图 6 LM 检验 | `outputs/tables/diagnostic_tests.csv` |

## 10. 小样本说明

本研究只有 24 个年度样本，单位根检验、协整检验和诊断检验均可能对滞后阶数、趋势项设定和个别年份较为敏感。因此结果应作为课程实证分析和方法展示，不宜直接作为投资或经营预测依据。
