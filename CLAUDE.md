# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## 这是什么

软考高级·系统架构设计师**备考学习库**，不是软件项目。多源（希赛讲义 / 一本通 / 32小时通关 / 官方教程）融合，产出 Obsidian 笔记库 `StudyVault/`。没有编译/测试套件；"交付"= 一章笔记+练习题+dashboard 同步且 `check_links.py` 零缺陷。

两大任务对称：**建库**（多源融合产笔记，走 `ruankao-build` skill）与**用库**（测验教学，经验见 `出题教学经验.md`）。本文件主体因此分两部分。

四大区：根目录 `第N章：XX/` + PDF（讲义原件与源书）｜`StudyVault/`（Obsidian 笔记库，最终产物）｜`artifacts/`（建章中间与永久产物）｜`.claude/skills/ruankao-build/`（建章 skill）。

---

# 第一部分 · 建库说明

## 常用命令

所有脚本 CWD 须为项目根 `llm_ruankao`，Python 依赖仅 PyMuPDF（`pip install -r .claude/skills/ruankao-build/requirements.txt`，即 `PyMuPDF>=1.28`，提供 `fitz`）。

```bash
# 质检（最接近 lint/test，交付前必须零缺陷；退出码 1=有缺陷）
# 查断链 / 练习题≥8且 [!answer]- 折叠数≥题数 / frontmatter 齐全
python .claude/skills/ruankao-build/scripts/check_links.py
python .claude/skills/ruankao-build/scripts/check_links.py <vault路径>   # 指定路径，默认 StudyVault

# 官方书定位/摘录（建章补肉、质疑核对都用它；--out 纯文件名落 artifacts/）
python .claude/skills/ruankao-build/scripts/locate_section.py --id 2.3.2          # 节号直查
python .claude/skills/ruankao-build/scripts/locate_section.py --kw 云计算          # 全文检索关键词
python .claude/skills/ruankao-build/scripts/locate_section.py --extract 611-615 --out official_cloud3 --label "§11.6 云计算"

# 渲染书/讲义页为图（视觉读图前必需）
python .claude/skills/ruankao-build/scripts/render_pages.py --book official --pages 600-620          # --book: ybt|32h|official
python .claude/skills/ruankao-build/scripts/render_pages.py --pdf 自定义.pdf --pages 1-10 --dpi 150

# build_toc_index.py：官方书书签→artifacts/toc_index.json（一次性，已跑，无需再跑）
```

建新章节：触发项目级 skill **ruankao-build**（"建第X章" / "建下一章" / "构建知识体系"）。**不要手搓建章**——七步 SOP、subagent 模板、12 条踩坑经验都在 `.claude/skills/ruankao-build/` 下（`SKILL.md` = 七步流程，`references/pitfalls.md` = 实战坑，`references/prompts.md` = subagent prompt 模板）。建章前先读这三份。

## 目录架构

```
llm_ruankao/
├── 第N章：XX/              # 讲义原件（希赛 PPT 各章 PDF，多 PDF 时需逐个勘察定性）
├── *.pdf                   # 源书：一本通 / 32h / 官方教程[第二版] / 大纲
├── 出题教学经验.md         # 用库（测验教学）经验 9 节，第二部分的原文件
├── StudyVault/             # Obsidian 笔记库（最终产物）
│   ├── 00-Dashboard/       # 索引层：MOC（章节地图）/ Quick-Reference / Exam-Traps / dashboard（进度统计）/ 串讲
│   ├── NNNN-主题/          # 主题文件夹，四位编号跟讲义主节（0101/0203/0303…），内放概念笔记+练习题
│   └── concepts/           # 同号追踪表（NNNN-主题.md），建章时建空表、教学时填尝试/正误/🟢🔴+错答笔记
├── artifacts/              # 永久产物（不删）
│   ├── toc_index.json      # 官方书目录索引（一次性产物）
│   ├── scan_toc_ybt.json / scan_toc_32h.json   # 一本通/32h 目录缓存（按篇/小时页范围）
│   ├── dagang/dagang_full.md  # 大纲全文转录，一次解析复用，建章比对考点不重转录
│   └── chNN/               # 各章产物：讲义_XX.json（中文键）+ mapping-chNN.md + excerpts/ + official_*.md
│                           #   渲染中间产物（pages_*/pNNN.jpg）与 part_*.json 抽完即删
└── .claude/skills/ruankao-build/   # 建章 skill + 四件套脚本 + references
```

## 硬约定（所有场景适用）

**源角色与页码换算**：

| 书 | 简称 | 角色 | 页码换算 |
|---|---|---|---|
| 希赛讲义 PPT | 讲义 | 骨架（结构/星级/考情/真题），无文字层→视觉读 | 物理=渲染 pNNN |
| 一本通·精华知识点 | 一本通 | 补浓缩图表/口诀 | 印刷=物理 |
| 32小时通关 | 32h | 补题 | 物理=印刷+9 |
| 官方教程[第二版] | 官方 | 按需字典（补定义/仲裁冲突） | 印刷=物理−15 |

冲突规则：考情跟讲义；定义跟官方；真冲突 `[!warning]` 两说并存（考试跟讲义）。讲义独有标"无旁证，考试跟讲义"。

**内容规范**：
- 主题文件夹四位编号跟讲义主节（`01xx/02xx/03xx…`）；`concepts/` 追踪表同号命名
- 补肉必标来源：frontmatter `supplements: [一本通 pNN, …]` + 节末 `> [!tip] 来源：书简称 pNN`
- 练习题 ≥8 题/夹；题源优先 讲义真题 > 32h > 原文逐字改判断题；〔回忆〕≥60%；`[!answer]-` 折叠
- 产物 JSON 用中文键（子节点/内容/类型/层级/页）
- 骨架划分必须给用户过目再动笔；dashboard 统计数字由用户自己维护（只加 ⬜ 行，不改其数字）
- 全程中文回复；文件夹名禁用 `/`（TCP/IP→`TCP_IP`）；wikilink 按实际文件名，别链文件夹名
- 动手编辑前先 `git status` + Read 当前版（用户会自行改笔记/重命名/维护统计，别按记忆中的旧内容编辑）

## 操作坑

**视觉读图（会话报废级风险）**：
- 一次 Read 多张大图撞 6MB 请求体上限，会话报废 → fitz 渲染 JPEG（dpi100、q75）+ subagent 分批读图（≤8 页/agent），主上下文只收文本
- subagent 用 Write 直接落盘抽取结果，不回传内容
- 完成的 subagent 不要 SendMessage resume（图上文 URL 失效报 400）；需要时从磁盘 transcript 提取
- glm-5.2 无视觉；qwen3.8-max 读图正常

**文件更新技术（Edit/Write 易翻车）**：
- Obsidian 自动格式化表格空格 → Edit 前必须 Read 当前内容，否则 `old_string` 不匹配（dashboard 多次因此失败）
- `concepts/` 空模板 Write 要求 Read 工具读过（cat 不算）→ 用 `Bash heredoc` 绕过：`cat > "路径" << 'EOF' … EOF`
- 中文路径在 bash `for` 循环变量里编码出错 → heredoc 用直接路径（引号包裹）稳
- 用户会重构文件名（如加编号 `0203-`）→ 编辑前先 Glob 确认当前文件名，别按记忆编辑

---

# 第二部分 · 教学经验（用库）

> 完整 9 节见 `出题教学经验.md`（第一、二章 tutor-zh 测验实战提炼）。以下为每会话必知铁律。与 ruankao-build（建库）对称，这份是**用库（测验教学）**。

## 出题前必做
- 先 `Bash cat` 章节概念笔记 + 已有练习题，**换新数据新角度避免重复**。
- Read 工具对 Glob/Grep 扫过的文件会误判"unchanged since last read" → 用 `Bash cat` 读稳。

## 先讲后考（新领域尤其重要）
新领域先通俗讲解再出题，效果远好于直接测。讲解三件套：**类比**（缓冲区=2段流水线）｜**口诀**（压缩四字：应中操抽硬）｜**英文词根拆解**（MPU=Micro+Processor+Unit=微处理器，用户"联想不到中文"时用）。

## 出题质量
- **真题应用+计算为主**，不只记忆辨析（0203 全记忆太简单翻车；0204 加 EDF 计算题才像真题）。
- **干扰项似是而非**：张冠李戴（MMDB 特点说成 FDB）、说反（PC=冯 写成 DSP=冯）、概念混淆（指令流水线混进 RTOS 三指标）。不要一眼假。
- **难度平均**，简单/中等/困难分布；正确答案位置随机不固定。
- **零提示**：选项描述不透露正确性，不加"(Recommended)"，题目问行为/用途不暗示答案。

## 判分讲解
- **错题讲透**：不只判错，讲"为什么错 + 正确理解 + 记忆口诀"。
- **Confusion + Key point**：错答笔记记"用户怎么错的（Confusion）+ 正确理解（Key point）"，保留作学习历史；🔴 转绿后笔记不删。
- 每题对应一个概念，更新 `concepts/` 追踪表（尝试/正确/🟢🔴）。

## 质疑核对（重要）
用户质疑时**核对官方原文**（`locate_section.py`），不盲信笔记/自己。**质疑精神必须保留**——可找artifacts目录下的原文内容做一句

## 学习追踪
- **概念级**：`concepts/` 表按概念记尝试/正确/🟢🔴；🔴 换新场景重练（不重复原题），答对转🟢。
- **领域汇总**：dashboard 按领域算掌握度（🟥0-39 / 🟨40-69 / 🟩70-89 / 🟦90-100 / ⬜未测）。
- **薄弱点专项**：🔴 概念换新场景出题。
- **跨章节统一抽象**：用户自己抽象的统一模型（如"访问次数=映射层数+1"统一存储管理+文件系统）最值钱，鼓励+存速查表。
- 判分后同步更新 `concepts/`（追踪表+错答笔记）+ `dashboard`（领域行+总计+统计区）。

## 多题场景
- AskUserQuestion 一次 ≤4 题（工具硬限）。
- 多题用**文本一次性列出**（分节+ABCD 选项），用户一条回复答完，统一判分。
