# UIUX Image Prompt Style — Default Paradigm

> **适用于所有 `page_type: cover / case-study / anatomy / process / system / hero` 的图片生成。**
> **不适用** 于海报、品牌视觉、editorial 静物（那些走 `image-style-presets.md`）。
>
> ⚠️ **PRIORITY**: This file OVERRIDES `image-generation-protocol.md` §Preset-first and `image-style-presets.md` for all UIUX pages. When this file and the preset system conflict, this file wins. The two systems are mutually exclusive — never mix a UIUX intent label with a preset tag in the same prompt.

---

## 范式总则

UIUX 作品集的图片是**产品 mockup 视觉**——不是杂志静物，不是编辑摄影，不是品牌海报。

参考真实模板：iPhone / MacBook / iPad mockup 居于纯色 flat BG 上，屏内显示项目真实 UI，可能伴随 1-2 个浮起的辅助元素（玻璃质感数据卡 / 局部放大图 / 通知 chip）。背景大片留白用于 HTML overlay 文字。

**核心原则**：把构图、角度、阴影、光晕这些视觉决策**交给 image2 自由发挥**。我们只负责说清楚 ① 排版意图 ② 屏内必读 UI 内容 ③ 配色基调 ④ 必须留白 ⑤ 不要写任何标题文字。

---

## Prompt 5 句结构

```
[1] <排版意图词>。
[2] <几台什么设备>，屏内显示<项目名>的<具体页面>：<3-6 个屏内必读 UI 元素>。
[3] (可选) 旁边有<浮起辅助元素>。
[4] 背景纯色 <hex 色>。
[5] 背景不要任何标题文字，不要项目名，不要 logo。16:9。
```

总长度控制在 **40-80 中文字 / 60-120 英文词**。更长 = image2 反而执行变差。

---

## 排版意图词词典

每个 prompt 第一句**只用 1 个**意图标签。不要堆叠。

| 标签 | 含义 | 适用页面 |
|---|---|---|
| **排版干净，留白充足** | 一个主体 + 大片空 BG | 案例锚定页、anatomy 页 |
| **排版严谨，对齐工整，网格感强** | 多元素按网格排列、无歪斜 | 多设备阵列、流程条、系统页 |
| **排版创新，构图大胆，有节奏** | 允许非常规角度、错位、尺寸跳跃 | 封面、概念视觉页 |
| **排版克制，单一焦点** | 只一个主体，不要任何配件 | 封面、hero shot |
| **排版编辑感，左右分栏** | 主体偏一侧，另一侧大片留白给文字 | 双屏对比、before/after |
| **排版动态，对角线张力** | 元素沿对角线排布，方向感强 | 流程页、process 页 |

---

## 配色基调（建议从这里挑，不要每次乱定）

| 基调 | hex | 适用 |
|---|---|---|
| 深海军蓝 | `#0F1729` | 科技 / B 端 / 物流 / 数据 |
| 深紫梅 | `#1F1326` | 社交 / 内容 / 夜间产品 |
| 深墨黑 | `#0A0A0A` | 高端 / 品牌 / 概念 |
| 暖米 | `#F2EDE0` | 生活 / 工具 / 内容浅色 |
| 奶油白 | `#F8F6F1` | 设计系统 / SaaS 浅色 |
| 柔灰 | `#EDEEF0` | 流程 / 中性展示 |

主题强相关时另行决定（医疗=薄荷绿、金融=墨绿、餐饮=橙等），但 BG 永远是**单色 flat**，最多一道径向光晕。

---

## 6 个验证 prompt 模板

### M1 · 单设备居中（最常用 · 案例锚定 / anatomy）

```
排版干净，留白充足。一台 iPhone 展示<项目名>的<某页面> UI：<必读 UI 元素 1>，<必读 UI 元素 2>，<必读 UI 元素 3>。背景纯色 <hex>。背景不要任何标题文字，不要项目名，不要 logo。16:9。
```

### M2 · 双屏对比（before / after · 方案对比）

```
排版编辑感，左右分栏。两台 iPhone 并排，左边显示<旧版页面> UI，右边显示<新版页面> UI，下方各有小标签 BEFORE / AFTER。背景纯色 <hex>。背景不要任何标题文字，不要项目名。16:9。
```

### M3 · 主屏 + 局部放大（anatomy 详情 · 设计点强调）

```
排版干净，留白充足。一台 iPhone 展示<项目名>的<某页面> UI（包含<必读 UI 元素>）。旁边有 1-2 张玻璃质感的浮起卡片，是屏内某个细节的局部放大（<细节 1>、<细节 2>）。背景纯色 <hex>。背景不要任何标题文字。16:9。
```

### M4 · 多设备阵列（系统 / 多端展示）

```
排版严谨，对齐工整，网格感强。三台设备一字排开：MacBook 显示<网页/后台界面>、iPhone 显示<手机界面>、Apple Watch 显示<手表界面>。三屏都属于<项目名>同一系统。背景纯色 <hex>。背景不要任何标题文字，不要项目名。16:9。
```

### M5 · 流程条（process / flow 页）

```
排版严谨，对齐工整，网格感强。四台 iPhone 横排，分别显示<项目名><流程名>的四步：第 1 步<界面 1>，第 2 步<界面 2>，第 3 步<界面 3>，第 4 步<界面 4>，相邻屏之间有细箭头连接。背景纯色 <hex>。背景不要任何标题文字。16:9。
```

### M6 · Hero shot（封面 / 概念页）

```
排版克制，单一焦点。一台 iPhone 大尺寸展示<项目名>的<标志性界面> UI（<最关键的视觉/交互元素>）。背景纯色 <hex>。背景不要任何标题文字，不要项目名，不要 logo。16:9。
```

---

## 禁词清单（写 prompt 时自检，出现即重写）

**视觉道具类（来自 editorial 海报范式，不属于 UIUX）**:
editorial / flat-lay / paper / pen / coffee / scribble / washi tape / binder clip / desk / textured cotton / handwritten / 钢笔 / 便签 / 纸胶带 / 咖啡渍 / 笔记本 / 桌面 / 棉纸 / 手写

**像素级排版指令（image2 不擅长，反而会僵硬）**:
向右倾斜 X 度 / 倾斜 8 度 / 占画面高度 70% / 居于画面中央 / 中央偏左 / 偏置右下 / 距上 200px / 仰视 / 俯视 / 阴影偏移 X px / radial glow at top-left / 90 度正面

**preset 系列（来自 huashu-design 海报范式）**:
preset: cinematic-velvet-jewel / editorial-paper-ink / brutalist-concrete / dark-botanical-sanctum / nocturne-festival / 等任何 `image-style-presets.md` 里的 12 个 preset 标签

**所有标题文字**:
任何要求图里出现项目名 / 标语 / 大标题 / 章节号 / "PAGE 01" / "CASE 01" 的描述。屏内 UI 文字 OK，BG 上的任何标题/标语**绝对禁止**。

---

## 工作流

1. 写 prompt：选 1 个意图标签 + 5 句结构填空 + 1 个 BG 基调
2. 通读自检禁词清单（看到禁词立刻删/换）
3. 字数核查：40-80 中文 / 60-120 英文，超了就砍
4. 跑 image2
5. 看图：BG 是否有大片留白、UI 是否真实可读、是否冒出意外的标题文字
6. 通过 → 进 multi-zone overlay 流程，把标题/段落/role 放在 BG 留白上

---

## 与其他 spec 的关系

- **取代** `image-generation-protocol.md` 中「Lean Natural-Language Mode」以及「Preset-first lean prompts」对 UIUX 案例页的指导。`image-generation-protocol.md` §Preset-first 已在 2026-05 加上 DOMAIN RESTRICTION 警告框确认此优先级。
- **取代** `image-style-presets.md` 在 UIUX 案例页的应用（presets 仅保留给海报/品牌 deck）。
- 与 `deck-narrative-architecture.md` 正交：archetype 决定页面在讲什么，本文件决定图片怎么生。
- 与 `multi-zone overlay`（layout_fitter + build_interactive_page --mode multi-zone）配合：图生成后，HTML overlay 在 BG 留白处放标题/desc/role。
