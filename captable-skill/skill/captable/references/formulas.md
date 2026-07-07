# Cap Table Formula Reference

## Calculation Basis

State the basis before calculating:

```text
注册资本口径: denominator = issued registered capital
股份数口径: denominator = issued shares
完全稀释口径: denominator = issued shares/capital + reserved ESOP + options + warrants + convertible instruments + other potential dilution items included by the legal documents
```

If the legal documents are ambiguous, calculate the registered-capital schedule first and add a fully diluted scenario sheet.

## Final Cap Table Roll-Forward

Every shareholder row should follow:

```text
投后注册资本 =
  投前注册资本
  - 老股转让减少
  + 老股受让增加
  + 新增注册资本

投后持股比例 =
  该股东投后注册资本 / 投后注册资本合计
```

## Pure New-Money Financing

```text
新股单价 = 投前估值 / 投前注册资本
投资人新增注册资本 = 投资金额 / 新股单价
投后注册资本 = 投前注册资本 + 投资人新增注册资本合计 + ESOP新增注册资本
投资人投后股比 = 投资人新增注册资本 / 投后注册资本
```

Example:

```text
投前注册资本 = 100
投前估值 = 1,000
投资额 = 200
新股单价 = 1,000 / 100 = 10
新增注册资本 = 200 / 10 = 20
投后注册资本 = 120
投资人股比 = 20 / 120 = 16.67%
```

## Mixed New Share + Old Share Transfer

Use when one investment amount buys both newly issued registered capital and transferred old shares.

```text
新股单价 = 新股投前估值 / 投前注册资本
老股单价 = 老股估值 / 投前注册资本
合计取得注册资本 = 投资额 * 投前注册资本 / 新老股综合估值
受让老股注册资本 =
  (新股单价 * 合计取得注册资本 - 投资额)
  / (新股单价 - 老股单价)
取得新增注册资本 = 合计取得注册资本 - 受让老股注册资本
新股投资金额 = 取得新增注册资本 * 新股单价
老股投资金额 = 投资额 - 新股投资金额
```

## ESOP

Clarify the legal convention before calculating.

Pre-money ESOP:

```text
投前ESOP新增注册资本 =
  目标比例 / (1 - 目标比例) * 现有完全稀释注册资本或股份数
```

Post-money ESOP:

```text
投后ESOP新增注册资本 =
  目标比例 / (1 - 目标比例)
  * (投前注册资本 + 投资人新增注册资本)
```

## Fully Diluted Ownership

Use a separate helper block or `完全稀释后` sheet:

```text
完全稀释后数量 =
  投后注册资本或股份数
  + 既有ESOP/期权
  + 新增ESOP/期权
  + 可转债或SAFE折算数量
  + 认股权证/其他潜在稀释数量

完全稀释后持股比例 =
  该持有人完全稀释后数量 / 完全稀释后数量合计
```

If conversion price, valuation cap, discount, warrant exercise price, or anti-dilution formula is missing, leave the relevant quantity as an editable assumption and flag the output as scenario-based.

## Legal Drafting Tie-Outs

For each investor, tie:

- 投资总额;
- 新股认购价 and 新增注册资本;
- 老股转让价 and 受让老股注册资本, if any;
- 投后注册资本;
- 投后持股比例.

For each transferor, tie:

- 转让前注册资本;
- 转让注册资本;
- 转让价款;
- 转让后注册资本.

Additional legal tie-outs:

- stated pre-money valuation equals price per registered capital/share times pre-money denominator;
- stated investment amount equals each investor subscription amount plus secondary purchase amount;
- stated investor post-round percentage ties to the cap table;
- ESOP percentage ties to the drafting convention selected in the workbook;
- fully diluted ownership ties to the listed dilution instruments and assumptions.
