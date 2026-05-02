# Analysis Depth

## Why This Module Exists

The single biggest gap between AI-generated portfolio decks and senior-designer portfolios is not visual quality — it is **analysis depth**. AI defaults to generic claims ("提升用户体验", "优化操作流程") that say nothing. Real portfolios show specific reasoning: a named user behavior, a measured friction point, a tradeoff between two real options, a principle that made one option win.

This module is a checklist + a set of forced specificity rules. Apply it to every analysis page (problem diagnosis, competitive analysis, design strategy, scheme comparison, IA, outcome, reflection). Without these rules, the deck looks well-designed but says nothing — which a recruiter spots in 30 seconds.

## When To Use

Apply on every page whose role includes one of:

- Problem diagnosis / pain point analysis
- User research summary / persona
- Competitive / benchmark analysis
- Design strategy / principles
- IA / flow / journey
- Scheme comparison / A-B iteration
- Detail proof / interaction reasoning
- Outcome / reflection

Do NOT apply to: cover, contents, section cover, gallery, thanks. Those are not analysis pages.

## The Specificity Bar

For every analysis claim, force the answer to these three questions:

```text
1. Specific to whom?         → name a user segment, not "users"
2. Specific to when?         → name a scenario / step / moment, not "in general"
3. Specific to what number?  → name a quantity / count / threshold, not "many" / "often"
```

If any answer is "users in general" / "everyday" / "many", the claim is generic. Rewrite or delete.

Examples:

| Generic AI default | Forced-specific rewrite |
|---|---|
| 用户操作不便 | 25-35 岁的店长在闭店盘点时，需要切换 4 个页面才能看完当日 3 类报表 |
| 信息架构不合理 | 一级 nav 8 个入口里，3 个使用率低于 2%，但占据黄金区位 |
| 设计了清晰的视觉层级 | 把核心指标放大到 56px，将次级指标降到 24px，KPI 卡片对比度从 1.8:1 提升到 4.5:1 |
| 优化了用户体验 | 把"新建工单"按钮从二级抽屉提到顶部固定位，预计可减少 2 次点击 |
| 提高了效率 | 闭店盘点的 7 步流程合并为 3 步，工单录入字段从 12 项减到 5 项 |

## Required Proof Elements Per Analysis Page

Every analysis page must contain at least 3 of these elements (4-5 is better):

1. **Named segment** — user role, persona name, or org type. Not "用户".
2. **Named scenario** — time of day, task step, or business moment. Not "日常使用".
3. **Counted observation** — number of clicks, count of items, percentage, time elapsed, frequency. Numbers can be designer-estimated for VISUAL_PROPOSAL mode (label as `[估算]`), but they must be present.
4. **Side-by-side comparison** — current state vs proposed, option A vs option B, competitor vs us. With one specific dimension being compared.
5. **Tradeoff acknowledgment** — what was given up to gain something else. "选择 X 是因为 Y，但代价是 Z。"
6. **Principle citation** — a named design principle (Fitts, Hick, recognition over recall, progressive disclosure, etc.) tied to one concrete decision on the page.
7. **Visual evidence** — a small screenshot crop, a flow diagram fragment, an annotated wireframe — not just text.

A page with only "principle + nice copy" but no segment / scenario / count fails the bar.

## Per-Page-Type Templates

Use these as starting structures. Customize per project.

### Problem Diagnosis Page

```text
Title: [项目名] 当前的 X 个核心问题
Layout: 3-5 numbered problem cards in a column or 2x2 grid.

Each card:
  Problem #N: [一句具体问题陈述, 12-20 字]
  Where it shows up: [具体场景 / 页面 / 步骤]
  Who hits it most: [具体用户角色]
  How often: [频率 / 占比, 可标 [估算]]
  Visual: [小截图标注 or 流程片段]
  Implication: [对业务 / 体验的具体影响]
```

### Competitive Analysis Page

```text
Title: 同类产品横向对比
Layout: rows = competitors (3-4 个), columns = comparison dimensions (4-6 个)

Comparison dimensions must be specific, not generic:
  ✘ "用户体验" (太空)
  ✓ "首页主导航深度" / "新建工单的字段数" / "首屏加载到关键指标的时间"

Conclusion block: 2-3 named opportunities found, each tied to a competitor decision.
```

### Design Strategy Page

```text
Title: 设计策略
Layout: 3-4 principle cards.

Each principle:
  Name: [4-8 字命名]
  One sentence rationale tied to a problem from the diagnosis page
  One concrete design implication (specific module / component / interaction)
  One tradeoff
```

### Scheme Comparison / A-B Page

```text
Title: 方案 A vs 方案 B
Layout: split column, A left B right, chosen option marked with a corner badge.

Each option must show:
  - The actual mockup of that option
  - 2-3 named criteria scored (cost / clarity / extensibility / dev time)
  - A one-sentence summary of strength
  - A one-sentence summary of weakness

Decision row:
  "选 [B]，因为 [criteria X]，代价是 [criteria Y]。"
```

### IA / Flow / Journey Page

```text
For IA: 3-level tree, named with real menu labels, marked with usage frequency [估算 OK].
For Flow: entry → decision → branches → success / error, with annotation on the longest path.
For Journey: 5-7 stages with action / thought / pain / opportunity rows, anchored on the named persona.
```

### Outcome / Reflection Page

```text
Title: 项目复盘
Layout: 3 columns — what shipped / what improved / what remains.

What shipped: 3-5 concrete deliverables with screenshots.
What improved: metrics if available, qualitative observations if not (label "qualitative validation, no quantitative data").
What remains: at least one honest unresolved problem. Senior portfolios always include this.
```

## Honesty Discipline (especially in VISUAL_PROPOSAL mode)

When the user did not give real data, you may include estimated numbers, but you MUST mark them and you MUST NOT pretend they are measured outcomes.

Allowed:
- `[估算] 闭店盘点平均耗时 18-22 分钟` — clearly an estimate.
- `预计可减少 2 次点击` — predictive language.
- `按行业经验，类似规模门店每日处理 30-50 单工单` — industry benchmark, labelled.

Forbidden:
- `用户满意度提升 28%` without source — fabricated outcome.
- `DAU 增长 12 万` without source — fabricated metric.
- `获得 BAT 三家投资人推荐` — fabricated endorsement.

The rule of thumb: a number inside a designed UI mockup is fine (it's part of the mockup). A number in the case-study narrative claiming measured business impact is not.

## Reasoning Chain Check

Before delivering the deck, trace the reasoning chain end-to-end. Read in order:

```text
Background → Problem #1 → Strategy principle that addresses Problem #1 → Design decision that applies that principle → UI proof showing that decision → Outcome (or expected outcome) for that decision
```

Every problem must be addressed by a principle. Every principle must produce a decision. Every decision must have UI proof. Every UI proof must connect back to the original problem. **A senior reviewer reads the deck this way — if the chain breaks, the case study reads as decorative.**

If a problem has no addressing principle, either delete the problem or add the principle. Do not leave dangling threads.

## Anti-Generic Self-Check

Before saving any analysis page, ask:

1. Could this exact paragraph appear in a portfolio for any other project? If yes, rewrite with specific names / numbers / scenarios.
2. Did I use any of these banned filler phrases? If yes, replace.
   - 提升用户体验
   - 优化操作流程
   - 增强视觉层级
   - 让产品更现代
   - 符合用户心智模型
   - 提高了效率
   - 满足了用户需求
3. Did I name a specific user segment, scenario, count, and principle on this page?
4. Did I show one tradeoff or unresolved tension? Senior portfolios always do.
5. Does this page connect to the previous page (problem ← analysis ← strategy ← decision ← proof)?

If any answer is no, rework before shipping.

## Persona / User Profile Page Discipline

If the deck includes a user persona / user portrait page (common in case studies), do NOT use AI-generated photorealistic faces. Reasons:

- AI faces still look uncanny at portfolio scale.
- They imply "real user" when it is in fact synthetic.

Allowed alternatives:

- Stylized 3D character render in the project PADB style (declared as illustration).
- Silhouette + named persona attributes (age, role, scenario, goal, pain point).
- A clearly-marked sample profile card with `[示例画像 / Sample Persona]` badge.
- Real photo provided by the user (with permission).

The persona is what carries the analysis, not the face. Make the attributes specific.
