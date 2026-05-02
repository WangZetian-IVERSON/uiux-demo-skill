# UI/UX Portfolio Deck · AI Skill

<p align="center">
  <b>一句话 → 完整的作品集 deck</b><br>
  <sub>One prompt → complete image-rich case study deck. Multi-agent orchestrated.</sub>
</p>

<p align="center">
  <a href="#-quick-start--快速开始"><b>Quick Start</b></a> ·
  <a href="#-multi-agent-workflow--多agent工作流"><b>Workflow</b></a> ·
  <a href="#-operating-modes--运行模式"><b>Modes</b></a> ·
  <a href="#-file-structure--文件结构"><b>Structure</b></a>
</p>

---

## 🎬 Demo · 效果展示

<p align="center">
  <img width="80%" src="https://github.com/user-attachments/assets/37b395f1-b339-4a09-955c-e5cf4a200b86" alt="Cover Page Example">
</p>
<p align="center">
  <img width="80%" src="https://github.com/user-attachments/assets/8625e88f-0239-45ee-9c53-f9711f407ba0" alt="Case Study Page Example">
</p>
<p align="center">
  <img width="80%" src="https://github.com/user-attachments/assets/f7fdc843-37ab-4e49-b170-2fcf787db168" alt="Anatomy Page Example">
</p>

---

## 🤖 Multi-Agent Workflow · 多 Agent 工作流

这个 skill 不像传统 skill 那样由一个 agent 线性执行。它内部编排了 **6 个专业 Agent 角色**，各司其职，模拟一个真正的设计团队：

```
用户说： "做一份运动 App 的作品集"
                │
    ┌───────────┴───────────┐
    │   🧠 Lead Agent       │  总指挥：收集需求、分配任务、整合交付
    │   拥有最终决策权        │
    └───────────┬───────────┘
                │
    ┌───────────┼───────────┬───────────────┬───────────────┬──────────────┐
    │           │           │               │               │              │
    ▼           ▼           ▼               ▼               ▼              ▼
┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────────┐
│🎯       │ │🎨       │ │🖼️        │ │✍️             │ │🏗️        │ │🔍          │
│Strategy │ │Style    │ │Image     │ │Copy &        │ │Builder   │ │Reviewer    │
│Agent    │ │Advisor  │ │Prompt    │ │Layout        │ │Agent     │ │Agent       │
│         │ │         │ │Agent     │ │Agent         │ │          │ │            │
│案例逻辑  │ │视觉方向  │ │图片生成   │ │文案+overlay  │ │HTML组装   │ │闭环QA      │
│页面骨架  │ │风格三选一│ │prompt    │ │排版          │ │deck输出   │ │质量把关    │
└────────┘ └────────┘ └──────────┘ └──────────────┘ └──────────┘ └────────────┘
    │           │           │               │               │              │
    └───────────┴───────────┴───────────────┴───────────────┴──────────────┘
                                    │
                                    ▼
                          📦 交付完整 HTML Deck
                    (全屏图片背景 + HTML 文字叠加 + 键盘翻页)
```

### Agent 角色说明

| Agent | 中文名 | 职责 | 使用的工具/参考 |
|-------|--------|------|----------------|
| **Lead Agent** | 主编 | 用户沟通、需求澄清、任务分派、最终交付 | 全局协调 |
| **Strategy Agent** | 策略 | 案例逻辑、页面骨架、叙事弧线 | `portfolio-logic.md` `deck-narrative-architecture.md` |
| **Style Advisor** | 风格顾问 | 3 方向差异化视觉提案 | `guided-style-selection.md` `style-directions.md` |
| **Image Prompt Agent** | 生图 | 每页图片 prompt 编写、模型路由 | `image-prompt-style-uiux.md` `image-generation-protocol.md` |
| **Copy & Layout Agent** | 排版 | overlay 文案、layout.json 几何排版 | `page-patterns.md` `overlay-layout-spec.md` |
| **Builder Agent** | 施工 | HTML 组装、deck stage 集成 | `build_interactive_page.py` `deck_stage.js` |
| **Reviewer Agent** | 质检 | 闭环 QA：遮挡检测、图文对应、对齐审查 | `build_with_qa.py` `closed-loop-overlay-qa.md` |

### 10 步 Auto-Run 流水线

```
Step 0 · OPENING CHECKLIST    →  缺失信息一次性问完
Step 1 · CAPABILITY CHECK     →  探测生图模型 / 终端 / 脚本可用性
Step 2 · ASSET SCAN           →  扫描截图、品牌色、事实数据
Step 3 · SCOPE DECIDE         →  案例分析 / 视觉提案 / 设计评审
Step 3.5 · NARRATIVE ARCHETYPE →  选叙事弧线 + 确认每页角色
Step 4 · STYLE PICK           →  3 方向差异化风格提案
Step 5 · LOCK ART DIRECTION   →  冻结 PADB（调色板/字体/禁词）
Step 6 · ASSET ROUTING        →  每页决定生图或 HTML overlay
Step 7 · SHOWCASE FIRST       →  先生成 3 页，确认一致后再展开
Step 8 · CONFIRM              →  用户确认视觉语法
Step 9 · EXPAND               →  批量生成全部页面
Step 10 · CLOSED-LOOP QA      →  自动化 QA：生成→截图→检测→修复→重检
```

> 以上流程全部由 skill 自动驱动。用户只需说一句话，剩下的交给多 Agent 编排。

---

## ⚡ Quick Start · 快速开始

### 1. 安装 / Install

| 平台 Platform | 方法 Method |
|---------------|-------------|
| **VS Code / Copilot** | 将整个文件夹放入项目根目录。SKILL.md 自动被发现。 |
| **Claude Code** | `git clone` → Claude 读取 AGENTS.md → SKILL.md |
| **Codex / OpenAI** | `git clone` → AGENTS.md 为入口 → SKILL.md 为完整指令 |
| **通用 Agent** | 放入项目根目录。Agent 应能发现 AGENTS.md 或 SKILL.md。 |

```bash
git clone https://github.com/WangZetian-IVERSON/uiux-portfolio-deck.git
cd uiux-portfolio-deck
```

### 2. Python 依赖 / Dependencies

```bash
pip install pillow playwright
playwright install chromium
```

### 3. 配置后端 / Configure Backend

All configuration lives in `scripts/config.py`. Set environment variables:

```powershell
# 默认: pockgo relay (OpenAI 兼容)
$env:BACKEND_API_KEY  = "sk-your-key"
$env:BACKEND_BASE_URL = "https://newapi.pockgo.com/v1"

# 直连 OpenAI
$env:BACKEND_API_KEY  = "sk-your-openai-key"
$env:BACKEND_BASE_URL = "https://api.openai.com/v1"

# 本地 ComfyUI Desktop
$env:COMFY_API_KEY = "your-comfy-key"
python scripts/image_client.py --backend comfyui ...
```

### 4. 开始使用 / Start Building

在 AI 对话框中输入一句话：

```
做一份运动 App 的作品集
做一份 B 端 SaaS Dashboard 案例
Create a UI/UX case study for my fintech app
```

Skill 自动启动 10 步流水线，多 Agent 协作完成全部工作。

---

## ⚙️ Operating Modes · 运行模式

Skill 自动检测环境能力，选择最优模式：

| 模式 Mode | 终端 Terminal | 生图 Image | 交付物 What You Get |
|-----------|:-----------:|:--------:|---------------------|
| **FULL** | ✅ | ✅ | 全自动流水线：生图 → overlay 搭建 → 自动 QA 修复 |
| **HEADLESS_GEN** | ❌ | ✅ | Agent 写 prompt；你跑生图；Agent 做视觉 QA |
| **HEADLESS_PROMPT_ONLY** | ❌ | ❌ | Prompt pack（txt + layout.json + README） |

---

## 📁 File Structure · 文件结构

```
uiux-portfolio-deck/
├── SKILL.md                         # 🧠 主 skill 定义 (10 步 Auto-Run + 36 条规则)
├── AGENTS.md                        # 🔌 Claude / Codex 兼容入口
├── README.md                        # 📖 本文件
├── .gitignore
│
├── references/                      # 📚 30+ 参考文档
│   ├── image-prompt-style-uiux.md   #   UIUX 默认 prompt 范式
│   ├── image-generation-protocol.md #   生图协议 & 模型路由
│   ├── headless-mode.md             #   无终端退化路径 + 人工 QA 清单
│   ├── page-patterns.md             #   7 种页面布局模式
│   ├── closed-loop-overlay-qa.md    #   自动化 QA 闭环
│   ├── deck-narrative-architecture.md # 叙事弧线 & 页面角色
│   └── ...                          #   还有 25+ 篇
│
├── scripts/                         # 🐍 Python 工具链 (config.py 驱动，零硬编码)
│   ├── config.py                    #   统一后端配置
│   ├── image_client.py              #   生图客户端 (pockgo/OpenAI/ComfyUI)
│   ├── build_with_qa.py             #   闭环 QA 编排
│   ├── build_interactive_page.py    #   HTML overlay 搭建
│   ├── render_screenshot.py         #   Playwright 截图
│   └── ...
│
├── vendor/design-assets/            # 🎨 Deck 舞台 & 导出
│   ├── assets/deck_stage.js         #   键盘翻页 + 页面切换
│   ├── assets/concept_badge.html    #   概念标签组件
│   └── scripts/                     #   PDF / PPTX 导出
│
└── templates/                       # 📄 空白 deck 骨架
    ├── deck-skeleton.html
    └── styles.css
```

---

## 📋 Configuration Reference · 配置速查

| 变量 Variable | 默认值 Default | 说明 What |
|---------------|---------------|-----------|
| `BACKEND_API_KEY` | (fallback to `POCKGO_KEY`) | API 密钥 |
| `BACKEND_BASE_URL` | `https://newapi.pockgo.com/v1` | 后端地址 |
| `BACKEND_IMAGE_MODEL` | `gpt-image-2` | 默认生图模型 |
| `BACKEND_QA_MODEL` | `gpt-4o` | QA 视觉模型 |
| `COMFY_API_KEY` | — | ComfyUI 平台密钥 |
| `COMFYUI_URL` | `http://127.0.0.1:8188` | ComfyUI 服务器地址 |

---

## 📄 License

MIT — see `vendor/design-assets/LICENSE`.

---

<p align="center">
  <sub>Works with GitHub Copilot · Claude Code · Codex · Any AI Agent</sub>
</p>
