# Transaction-Schedule Cap Table Layout

Use this layout for cap tables intended as investment agreement schedules or internal legal calculations.

## Sheet Names

- `计算逻辑`
- `投后股权结构`
- `检查`
- Optional: `完全稀释后`

Avoid matter-specific labels in sheet names unless the user asks for a round-specific label.

## 计算逻辑

Recommended sections:

1. `核心数据`
   - 计算口径: 注册资本口径 / 股份数口径 / 完全稀释口径
   - 本轮投前注册资本或股份数
   - 本轮投前估值
   - 本轮融资金额
   - 新股单价
   - ESOP口径: 无 / 投前ESOP / 投后ESOP / 仅列示既有ESOP
   - ESOP目标比例和新增注册资本, if relevant
   - 本轮投后注册资本

2. `本轮投资人新老股分配`
   - 投资人
   - 投资总额
   - 合计取得注册资本
   - 受让老股注册资本
   - 取得新增注册资本
   - 新股投资金额
   - 老股投资金额
   - 投后持股比例

3. `老股转让`
   - 转让方
   - 受让方
   - 老股对价
   - 转让注册资本

4. `ESOP计算`
   - 持股平台/对象
   - ESOP口径
   - 目标比例
   - 新增注册资本
   - 投后股比
   - 稀释承担方
   - 备注

5. `潜在稀释事项`
   - 工具/事项
   - 持有人
   - 换股或行权条件
   - 折算注册资本/股份数
   - 是否计入完全稀释
   - 备注

## 投后股权结构

Columns:

```text
序号
简称
股东姓名/名称
本轮投前注册资本（万元）
老股转让减少（万元）
老股受让增加（万元）
新增注册资本（万元）
本轮投后注册资本（万元）
本轮投后持股比例
完全稀释后持股比例
备注
```

Row formulas:

```text
本轮投后注册资本 =
  本轮投前注册资本
  - 老股转让减少
  + 老股受让增加
  + 新增注册资本

本轮投后持股比例 =
  本轮投后注册资本 / 本轮投后注册资本合计

完全稀释后持股比例 =
  完全稀释后注册资本或股份数 / 完全稀释后总额
```

## 完全稀释后

Include this sheet when ESOP, options, warrants, convertible securities, SAFE, anti-dilution, or other potential dilution items exist or may be negotiated.

Recommended columns:

```text
持有人/股东
投后注册资本或股份数
既有ESOP/期权
新增ESOP/期权
可转债/SAFE折算
认股权证/其他
完全稀释后注册资本或股份数
完全稀释后持股比例
备注
```

## 检查

Checks:

```text
投前注册资本合计 = 来源股东名册合计
投前持股比例合计 = 100%
老股转让减少合计 = 老股受让增加合计
老股转让价款合计 = 投资人老股投资金额合计
投资人投资金额合计 = 本轮融资金额
新增注册资本合计 = 投资人新增注册资本合计 + ESOP新增注册资本
投后注册资本合计 = 投前注册资本 + 新增注册资本净额
投后持股比例合计 = 100%
完全稀释后持股比例合计 = 100%, if applicable
负数注册资本行数 = 0
```

## Style

- Dark blue merged title row.
- Light blue table headers.
- Yellow fill + blue font for user input assumptions.
- Black font for formulas.
- Green font for same-workbook links.
- Totals row with strong top border.
- Percentages shown with four decimals.
- Registered capital shown with four to six decimals, matching source precision.
