# vc-investment-review · VC/PE 投资文件审阅 Skill

一个用于 **VC/PE 私募股权融资法律文件审阅** 的 WorkBuddy / OpenAI 兼容 Agent skill。
上传 TS、投资协议、股东协议或交割文件，说明你的身份，即可按沉淀的 SOP 自动产出
结构化、可交付的中文审阅意见（P0/P1/P2 分级）。

---

## 功能特性

- **四类身份路由**：新进投资人 / 既有投资人 / 政府引导基金·地方产业基金 / 其他产业投资人
- **四类文件场景**：
  - TS / Term Sheet —— 快速完整性审核
  - 投资协议（增资 / 股转）—— 交易执行、交割、Cap Table、尽调落实、违约、解除
  - 股东协议 —— 16 类特殊权利齐备性与投资人友好度
  - 交割文件最终核验 —— 章程 / 决议 / 披露函 / 放弃函横向一致性
- **P0 红线速判**：回购权缺失价格/义务主体、Cap Table 缺失、放弃函概括豁免等一键标红
- **双视角审阅逻辑**：新进重"权利是否给足"，既有重"权利是否被削弱"
- **标准输出模板**：结论先行 + 明细表 + 既有投资人专项 + Checklist 兜底
- **附录参考手册**：`references/sop-guides/` 内含投资协议、股东协议《统一审阅指引》全文

---

## 目录结构

```
vc-investment-review-skill/
├── README.md
├── LICENSE
├── .gitignore
└── skill/
    ├── SKILL.md                       # 入口：触发条件 + 核心工作流
    ├── agents/
    │   └── openai.yaml                # OpenAI 兼容 Agent 声明
    └── references/
        ├── review-routing.md          # 场景 × 身份 路由与识别规则
        ├── ts-review.md               # TS 快速审核规则
        ├── investment-agreement-review.md   # 投资协议审核规则
        ├── shareholder-agreement-review.md   # 股东协议审核规则
        ├── closing-final-check.md     # 交割文件核验规则
        ├── output-templates.md        # 输出格式与 P0/P1/P2 定义
        └── sop-guides/                # 附录：统一审阅指引（脱敏通用版）
            ├── 投资协议统一审阅指引.md
            └── 股东协议统一审阅指引.md
```

---

## 安装方式

### 方式 A：WorkBuddy（推荐）

将本仓库 `skill/` 目录整体复制到你的用户级 skills 目录：

- **Windows**：`C:\Users\<你的用户名>\.workbuddy\skills\vc-investment-review\`
- **macOS / Linux**：`~/.workbuddy/skills/vc-investment-review/`

即：`skill/` 内的 `SKILL.md`、`agents/`、`references/` 应位于
`.../skills/vc-investment-review/` 之下。复制完成后重启 WorkBuddy 即可自动识别。

### 方式 B：OpenAI 兼容 Agents（如支持 `agents/` 声明）

`skill/agents/openai.yaml` 已声明 `display_name` 与 `default_prompt`，
可直接被兼容的 Agent 运行时加载。

---

## 使用方式

1. 上传待审文件（TS / 投资协议 / 股东协议 / 交割文件）。
2. 说明你的身份，例如：
   > "我是本轮新进投资人，按 vc-investment-review 审阅这份股东协议。"
3. Skill 会自动：
   - 识别场景与身份 → 加载对应规则 → 逐条比对 → 风险定级（P0/P1/P2）→
     套用输出模板生成《审阅意见》。

> 提示：既有投资人视角下，建议同时提供**前轮交易文件**，否则无法判断
> "既有权利是否被削弱"。缺材料时 Skill 会先列出"待补充清单"再出初稿。

---

## 脱敏说明

本 skill 的通用版已做脱敏处理：
- 移除了原内部专属的"基金"身份，统一泛化为"政府引导基金 / 地方产业基金"；
- 附录指引中的项目实例均来自公开市场范本并做匿名化处理，不含任何机构或交易主体信息。

---

## 免责声明

本 skill 生成的审阅意见基于所提供文件及公开市场惯例作出，**不构成法律意见**，
未经完整尽职调查核验。实际交易决策请结合最新事实、监管口径及执业律师意见综合判断。

---

## License

[MIT](./LICENSE)
