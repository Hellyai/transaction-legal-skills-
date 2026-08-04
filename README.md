# Transaction Legal Skills

面向交易文件审阅和法律实务工作的 Codex Skills 仓库。

当前包含：

- `vc-investment-review`：VC/PE 投资文件审阅助手，用于审阅 TS / Term Sheet、投资协议、股东协议、交割文件及 Cap Table 相关条款。

## 目录结构

```text
transaction-legal-skills/
├── README.md
├── LICENSE
├── .gitignore
└── skills/
    └── vc-investment-review/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        │   ├── review-routing.md
        │   ├── ts-review.md
        │   ├── investment-agreement-review.md
        │   ├── shareholder-agreement-review.md
        │   ├── new-investor-review.md
        │   ├── existing-investor-review.md
        │   ├── economic-rights-review.md
        │   ├── governance-review.md
        │   ├── closing-final-check.md
        │   ├── output-templates.md
        │   ├── quality-control.md
        │   └── sop-guides/
        └── scripts/
            └── rights_math.py
```

## 安装方式

将目标 skill 文件夹复制到本地 Codex skills 目录：

```text
%USERPROFILE%\.codex\skills\vc-investment-review
```

复制后目录应为：

```text
.codex/
└── skills/
    └── vc-investment-review/
        ├── SKILL.md
        ├── agents/
        ├── references/
        └── scripts/
```

重启 Codex 后即可识别。

## 使用示例

```text
请使用 vc-investment-review 审阅这份股东协议。我方是本轮新进投资人。
```

```text
请按既有投资人视角审阅本轮增资协议，并重点核查前轮回购权、反稀释、优先认购权是否被削弱。
```

## vc-investment-review 功能

- 按文件类型自动区分 TS、投资协议、股东协议、交割文件。
- 按我方身份区分新进投资人、既有投资人、政府引导基金或地方产业基金、其他产业投资人。
- 对回购权、反稀释、优先清算、MFN、共同出售、拖售、董事席位、保护性条款等进行结构化审阅。
- 输出 P0 / P1 / P2 风险分级、处理标签、修改建议和待核实清单。
- 对涉及估值、注册资本、投资单价、股比、ESOP、反稀释等事项，提示进行专项 Cap Table 核验。

## 脱敏说明

本仓库仅保留通用审阅 SOP、模板、规则和计算脚本，不应上传客户原始文件、聊天记录、合同原件、身份证明、签署页、工商内档、尽调资料或其他涉密资料。

上传前建议执行敏感信息检查，重点排查：

```text
身份信息、联系方式、邮箱、客户名称、项目名称、账号口令、访问密钥、本地绝对路径
```

## 免责声明

本 skill 输出内容用于辅助交易文件审阅，不构成正式法律意见。具体交易决策应结合完整文件、尽职调查、最新法律法规和执业律师判断。
