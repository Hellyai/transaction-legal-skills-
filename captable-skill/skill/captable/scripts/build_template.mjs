import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = path.join(process.cwd(), "outputs");
await fs.mkdir(outputDir, { recursive: true });

const workbook = Workbook.create();
const calc = workbook.worksheets.add("计算逻辑");
const post = workbook.worksheets.add("投后股权结构");
const checks = workbook.worksheets.add("检查");

const dark = "#1F4E78";
const light = "#D9EAF7";
const inputFill = "#FFF2CC";
const border = "#D9E2EA";

for (const sheet of [calc, post, checks]) sheet.showGridLines = false;

function title(sheet, range, text) {
  const r = sheet.getRange(range);
  r.merge();
  r.values = [[text]];
  r.format = {
    fill: dark,
    font: { bold: true, color: "#FFFFFF", size: 14 },
    horizontalAlignment: "left",
  };
}

function header(range) {
  range.format = {
    fill: light,
    font: { bold: true },
    borders: { preset: "all", style: "thin", color: border },
    wrapText: true,
  };
}

function body(range) {
  range.format = {
    borders: { preset: "all", style: "thin", color: border },
    wrapText: true,
  };
}

function input(range) {
  range.format = {
    fill: inputFill,
    font: { color: "#0000FF" },
    borders: { preset: "all", style: "thin", color: border },
  };
}

title(calc, "A1:D1", "计算逻辑");
calc.getRange("A3:D3").values = [["项目", "数值", "单位", "说明"]];
header(calc.getRange("A3:D3"));
calc.getRange("A4:D11").values = [
  ["本轮投前注册资本", 1000, "万元", "示例输入"],
  ["本轮投前估值", 90000, "万元", "示例输入"],
  ["本轮投资总额", 5000, "万元", "示例输入"],
  ["新股单价", null, "万元投资款/万元注册资本", "投前估值 / 投前注册资本"],
  ["ESOP目标比例", 0.03, "%", "示例输入"],
  ["投资人新增注册资本合计", null, "万元", "投资总额 / 新股单价"],
  ["ESOP新增注册资本", null, "万元", "投后ESOP公式"],
  ["本轮投后注册资本", null, "万元", "投前注册资本 + 投资人新增 + ESOP新增"],
];
body(calc.getRange("A4:D11"));
input(calc.getRange("B4:B6"));
input(calc.getRange("B8"));
calc.getRange("B7").formulas = [["=B5/B4"]];
calc.getRange("B9").formulas = [["=B6/B7"]];
calc.getRange("B10").formulas = [["=B8/(1-B8)*(B4+B9)"]];
calc.getRange("B11").formulas = [["=B4+B9+B10"]];
calc.getRange("B4:B7").format.numberFormat = "#,##0.000000";
calc.getRange("B8").format.numberFormat = "0.0000%";
calc.getRange("B9:B11").format.numberFormat = "#,##0.000000";

title(post, "A1:I1", "投后股权结构");
post.getRange("A3:I3").values = [[
  "序号",
  "股东姓名/名称",
  "投前注册资本",
  "老股转让减少",
  "老股受让增加",
  "新增注册资本",
  "投后注册资本",
  "投后持股比例",
  "备注",
]];
header(post.getRange("A3:I3"));
post.getRange("A4:I8").values = [
  [1, "创始人A", 500, 0, 0, 0, null, null, ""],
  [2, "员工平台B", 300, 0, 0, 0, null, null, ""],
  [3, "投资人C", 200, 0, 0, 0, null, null, ""],
  [4, "本轮投资人", 0, 0, 0, null, null, null, "示例"],
  [5, "ESOP", 0, 0, 0, null, null, null, "示例"],
];
body(post.getRange("A4:I8"));
post.getRange("F7").formulas = [["='计算逻辑'!B9"]];
post.getRange("F8").formulas = [["='计算逻辑'!B10"]];
for (let row = 4; row <= 8; row += 1) {
  post.getRange(`G${row}`).formulas = [[`=C${row}-D${row}+E${row}+F${row}`]];
  post.getRange(`H${row}`).formulas = [[`=G${row}/$G$9`]];
}
post.getRange("A9:I9").values = [["合计", "", null, null, null, null, null, null, ""]];
for (const col of ["C", "D", "E", "F", "G", "H"]) {
  post.getRange(`${col}9`).formulas = [[`=SUM(${col}4:${col}8)`]];
}
post.getRange("C4:G9").format.numberFormat = "#,##0.000000";
post.getRange("H4:H9").format.numberFormat = "0.0000%";

title(checks, "A1:E1", "检查");
checks.getRange("A3:E3").values = [["检查项", "实际值", "应等于", "差异", "状态"]];
header(checks.getRange("A3:E3"));
checks.getRange("A4:E7").values = [
  ["投前注册资本合计", null, null, null, null],
  ["投后注册资本合计", null, null, null, null],
  ["投后持股比例合计", null, 1, null, null],
  ["负数注册资本行数", null, 0, null, null],
];
body(checks.getRange("A4:E7"));
checks.getRange("B4").formulas = [["='投后股权结构'!C9"]];
checks.getRange("C4").formulas = [["='计算逻辑'!B4"]];
checks.getRange("B5").formulas = [["='投后股权结构'!G9"]];
checks.getRange("C5").formulas = [["='计算逻辑'!B11"]];
checks.getRange("B6").formulas = [["='投后股权结构'!H9"]];
checks.getRange("B7").formulas = [["=COUNTIF('投后股权结构'!G4:G8,\"<0\")"]];
for (let row = 4; row <= 7; row += 1) {
  checks.getRange(`D${row}`).formulas = [[`=B${row}-C${row}`]];
  checks.getRange(`E${row}`).formulas = [[`=IF(ABS(D${row})<0.000001,"OK","需检查")`]];
}

for (const sheet of [calc, post, checks]) {
  sheet.getUsedRange().format.autofitColumns();
  sheet.getUsedRange().format.autofitRows();
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outputDir, "示例项目_CapTable.xlsx"));
