---
name: ruankao-build
description: 软考架构师 StudyVault 多源融合建章管线。触发：用户说"建第X章""建下一章""构建知识体系"。七步：讲义视觉抽取→骨架过目→对齐表→扫描书抽取→笔记练习→Dashboard→自检。约定（页码/编号/来源标注）以项目 CLAUDE.md 为准。
metadata:
  version: "1.0.0"
---

# ruankao-build · 多源融合建章管线

在 D:\2study\软考高级学习记录\26年下-最终章\llm_ruankao 下建新章节。硬约定见项目 CLAUDE.md。

## 目录结构

```
ruankao-build/
├── SKILL.md                  # 本文件：七步 SOP + checklist + 坑
├── requirements.txt          # PyMuPDF（fitz）
├── scripts/                  # 管线四件套（CWD 须为项目根 llm_ruankao）
│   ├── build_toc_index.py    #   官方书书签→artifacts/toc_index.json（一次性）
│   ├── locate_section.py     #   官方书定位/摘录（--id/--title/--kw/--extract）
│   ├── render_pages.py       #   扫描书/讲义渲染 PNG（--book ybt|32h|official）
│   └── check_links.py        #   断链/题数/frontmatter 质检
└── references/
    └── prompts.md            # 三套 subagent prompt 模板（讲义/扫描书/笔记）
```

**首次使用**：先读本文件 SOP；**读 references/pitfalls.md（第二~四章实战经验，12 条）**；派 subagent 时从 references/prompts.md 取模板。
**调用脚本**：`cd llm_ruankao && python .claude/skills/ruankao-build/scripts/xxx.py …`

## 七步 SOP

**0 勘察**：**新会话接手先摸现状：读 StudyVault/00-Dashboard/MOC.md + dashboard.md 看已建章节与进度，ls artifacts/ 看可复用产物（不依赖旧会话记忆）**；确认讲义 PDF（第X章：XX/*.pdf）页数与文字层（fitz，讲义均无文字层）；**章目录多 PDF 时逐个勘察定性：知识点主讲义做骨架，案例/特训类做补题源（单独抽取进 excerpts，不并入骨架 JSON）**；查 scan_toc_ybt.json / scan_toc_32h.json 定一本通/32h 对应篇/小时页范围；locate_section.py --title/--kw 定官方书小节。

**1 讲义 JSON**：fitz 渲染全册 JPEG（dpi100 q75）→ 并行 subagent（≤8 页/agent，用 prompts.md §1）各自 Write 落盘 artifacts/chNN/part_*.json → 合并脚本产 讲义_XX.json（中文键；md 表→HTML；加 page 键）→ 校验页覆盖无缺。

**2 骨架过目**：抽 L1 序列 + 考情分析表 → 按讲义主节划四位编号文件夹清单 → AskUserQuestion 给用户过目，批了再动笔。注意：讲义可能是多 PPT 拼接（两个封面/提要），同主题页合并。

**3 对齐表** mapping-chNN.md：讲义主题 ↔ 一本通页 ↔ 32h页（印/物换算）↔ 官方§ ↔ 缺口标记；附抽取任务清单。

**4 扫描书抽取**：render/fitz 渲染目标页（150dpi q75）→ subagent 抽取直接 Write 落盘 excerpts/（prompts.md §2；ybt 超 8 页拆两半再合并）；首图核对页脚偏移。

**5 笔记+练习**：每文件夹一个 subagent（prompts.md §3），读讲义 JSON+excerpts+mapping+第一章模板笔记写概念笔记与练习题；concepts/ 建同号空追踪表；官方补肉用 locate_section --extract 落 official_*.md。

**6 Dashboard**：MOC 加本章 Topic Map + 源构成表行 + tags；Quick-Reference/Exam-Traps 增条目；dashboard 加 ⬜ 行（统计数字留给用户）。

**7 自检+收尾**：check_links 零缺陷；删渲染中间产物与 part_*.json；读 artifacts/dagang/dagang_full.md 做考点比对补漏（大纲已一次解析复用，不重转录）；汇报等用户自查 + tutor 验收。

## 交付 checklist

- [ ] 讲义 JSON 页覆盖无缺页
- [ ] 骨架已过目获批
- [ ] 补肉全标来源（supplements + [!tip]）
- [ ] 练习题 ≥8/夹、回忆≥60%、[!answer]-≥题数
- [ ] concepts 同号空表已建
- [ ] MOC/Quick-Ref/Exam-Traps/dashboard 同步
- [ ] check_links 零缺陷
- [ ] 中间产物已清
- [ ] 大纲比对补漏完成

## 坑备忘

- Windows 文件夹名禁 `/`；wikilink 按实际文件名，别链文件夹名
- 大纲新考点（二版新增如 DO-178/国产芯片）讲义常无 → 官方补 + 标"大纲补漏"
- 官方书缺应试新内容时标"无旁证，考试跟讲义"
- subagent 不 resume；图读取结果不回传主上下文
- 用户会自行改笔记/重命名/维护统计，动手前先 git status + Read 当前版，别按记忆中的旧内容编辑
