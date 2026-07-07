---
name: captable
description: Build, explain, audit, or template financing capitalization tables for equity investments. Use when the user provides or asks for cap table inputs such as valuation, investment amount, registered capital/share capital, existing shareholders, new-money subscriptions, secondary share transfers, ESOP pools, option pool shuffle, fully diluted ownership, dilution, post-financing ownership percentages, transaction agreement schedules, or Excel cap tables with formulas.
---

# Cap Table

Use this skill for financing cap tables, especially PRC-style registered-capital based investment agreement schedules. Default to a generic transaction-schedule presentation. Do not use matter-specific labels unless the user asks for them.

## Core Workflow

1. Identify the calculation basis:
   - `registered capital basis`: default for PRC companies and investment agreement schedules.
   - `share count basis`: use when the source table is ordinary shares/preferred shares instead of registered capital.
   - `fully diluted basis`: use when options, reserved ESOP, warrants, convertible instruments, SAFE notes, or anti-dilution adjustments may affect ownership.
2. Separate source inputs, formulas, and final legal schedule output.
3. Ask only for missing terms that materially change the result. If common alternatives exist, calculate both scenarios and label them clearly.
4. Keep every material derived number formula-driven in Excel.
5. Include visible checks that reconcile source shareholder list, investment amounts, new registered capital/shares, secondary transfers, ESOP, and final ownership.

## Default Naming

- File name: `<ProjectName>_CapTable.xlsx` or `<ProjectName>_CapTable_<date>.xlsx` when versioning is useful.
- Sheet 1: `计算逻辑`
- Sheet 2: `投后股权结构`
- Sheet 3: `检查`
- Optional sheet: `完全稀释后` when fully diluted output is relevant.

## Workbook Shape

1. `计算逻辑` - assumptions, calculation basis, financing terms, investor allocation, ESOP and fully diluted scenario blocks.
2. `投后股权结构` - agreement-ready final cap table with one row per shareholder.
3. `完全稀释后` - optional view including ESOP reserve, options, convertible securities, warrants, SAFE, or anti-dilution shares.
4. `检查` - tie-outs and model status.

## Calculation Basis

Always state the basis used in `计算逻辑`.

- Registered capital basis:
  - Use amounts in 万元人民币 unless the user supplies another unit.
  - Price per registered capital = pre-money valuation / pre-money registered capital.
- Share count basis:
  - Use shares as the denominator.
  - Price per share = pre-money valuation / pre-money shares.
- Fully diluted basis:
  - Start from issued registered capital/shares.
  - Add reserved but unissued ESOP, granted options, warrants, convertible instruments, and other potential dilution items where the legal term sheet says they are included.
  - If conversion terms are missing, create an input block and mark the affected output as scenario-based.

## ESOP / Option Pool

Never assume ESOP treatment silently. Show the convention:

- `post-money ESOP`: ESOP target percentage is measured after investor subscription and ESOP issuance.
- `pre-money ESOP / option pool shuffle`: ESOP is created or topped up before investor money, economically diluting existing shareholders before the financing.
- `existing ESOP only`: existing pool is included in fully diluted denominator, no new issuance unless specified.

If the agreement only says "3% after this financing" or similar, default to post-money ESOP and add a note. If drafting or negotiation context matters, output both pre-money and post-money ESOP scenarios.

## Final Cap Table Columns

Use these columns unless the user requests otherwise:

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

Keep old-share transfer columns even when there is no old-share transfer; fill them with zero. This keeps the schedule reusable and agreement-friendly.

## Formula Patterns

Read `references/formulas.md` when explaining formulas step by step, auditing an existing workbook, or creating a template.

Common registered-capital formulas:

```text
新股单价 = 投前估值 / 投前注册资本
投资人新增注册资本 = 投资金额 / 新股单价
投后注册资本 = 投前注册资本 - 老股转让减少 + 老股受让增加 + 新增注册资本
投后持股比例 = 该股东投后注册资本 / 投后注册资本合计
```

Post-money ESOP formula:

```text
ESOP新增注册资本 =
  ESOP目标比例 / (1 - ESOP目标比例)
  * (投前注册资本 + 投资人新增注册资本)
```

## Required Checks

Always include:

- 投前注册资本合计 ties to source shareholder list.
- 投前持股比例合计 equals 100%.
- 老股转让减少合计 equals 老股受让增加合计.
- 投资人投资金额合计 ties to stated financing amount.
- 投资金额 equals 新股投资金额 plus 老股投资金额.
- 新增注册资本合计 ties to investor subscription plus ESOP/new pool issuance.
- 投后注册资本 equals 投前注册资本 plus 新增注册资本净额.
- 投后持股比例合计 equals 100%.
- 完全稀释后持股比例合计 equals 100%, when a fully diluted sheet is included.
- No shareholder has negative post-round registered capital/share count.
- Round ownership and valuation implied by the schedule tie to the financing terms.

## Transaction Lawyer Output Modes

Default to `dual-use`:

- Agreement schedule view: concise, clean, suitable for annexing to transaction documents.
- Internal calculation view: formula-rich, with assumptions, scenario toggles, and checks.

For legal drafting, surface these review notes when applicable:

- Whether ESOP dilutes only existing shareholders or all shareholders.
- Whether investors are subscribing new shares only or also buying old shares.
- Whether stated investment amount includes premium/capital reserve accounting.
- Whether foreign shareholders, nominee platforms, or employee platforms need separate display.
- Whether convertible securities, warrants, anti-dilution, or MFN rights can change the fully diluted cap table.

## Formatting

- Hide gridlines.
- Use dark blue merged title rows with white bold text.
- Use light blue table headers.
- Use yellow fill and blue font for editable inputs.
- Use black font for formulas.
- Use green font for links to other sheets.
- Use `#,##0.000000` for registered capital when source precision is six decimals.
- Use `0.0000%` for legal schedule ownership percentages.
- Put totals in a clearly bordered final row.
- Freeze header rows on long tables.

## References

Read `references/transaction-layout.md` for the default transaction-schedule layout.

Read `references/formulas.md` when explaining formulas step by step or auditing an existing cap table.

Use `scripts/build_template.mjs` only as a starter example. Adapt row counts, labels, and formulas to the actual transaction.
