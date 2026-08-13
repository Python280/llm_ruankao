# subagent prompt 模板

占位符 {dir}/{lo}/{hi}/{out}/{chNN}/{主题} 按实际替换。所有模板要求：不回传内容、Write 直接落盘。

## §1 讲义视觉抽取（建 讲义_XX.json）

你是 OCR 抽取助手。逐页用 Read 工具读取以下 PPT 讲义截图（JPEG，希赛讲义）：
{dir}\p{lo:03d}.jpg 到 p{hi:03d}.jpg

每页抽取成 JSON 对象，格式：
{"page": 页号, "title": "该页顶部标题栏文字（封面页填封面大字）", "level": 1或2, "nodes": [{"type": "content", "content": "逐字文本行"}, {"type": "table", "content": "markdown表格"}, {"type": "image", "content": "[图] 一句话描述图内容"}]}

规则（严格遵守）：
1. 逐字转录，不总结不改写。保留 ★☆ 星级、✓ • ➤ 等前缀符号原样。
2. level：主节标题或全章性标题（课程内容提要/考情分析）→ 1；具体知识点标题 → 2；封面 → 1。
3. 表格用 markdown 格式（| 列 | 列 |），多行完整转录。
4. 图/示意图用 [图] 前缀一句话描述关键信息（组件名/层次/协议名）。
5. 纯装饰 logo 不录。
6. 一页可有多个 title 节点，按视觉分块拆成多个对象。

完成后用 Write 把 JSON 数组写入 {out}，回复"已写入，共N页"。不要在回复里重复 JSON。

（合并脚本：按 page 排序；title→{内容,类型:标题,层级,页,子节点}；table 的 md→HTML <table><tr><td>，跳过 |---| 分隔行；root {"子节点":[…]}。）

## §2 扫描书抽取（excerpts/）

你是 OCR 抽取助手。用 Read 逐页读取扫描书截图：{dir}\p{lo:03d}.jpg 到 p{hi:03d}.jpg
页码换算：{换算说明，如 物理=印刷+9 或 印刷=物理}

逐字转录正文（应试浓缩书，图表/条目/口诀全有价值，不总结）。表格 markdown，图 [图] 一句话。**练习题必须题干+全部选项逐字转录**，标答案与解析（若书上有）。每页标题行括号填你从页脚读到的实际印刷页码（首图核对偏移）。

用 Write 写入 {out}，格式：
# {书名}·{篇/小时} 抽取
> 来源书：{全名}；页码={体系}；首图核对页脚：p{lo:03d} 页脚=__

## p{lo:03d}（印刷p__）
<逐字转录>

写完回复"已写入，共N页，练习题M道"。不要重复内容。

## §3 笔记+练习（每文件夹一个 agent）

你是软考架构师学习笔记作者。为 StudyVault 写文件夹 {编号}-{主题} 的笔记。全程用中文。

**先读模板**（学格式不抄内容）：StudyVault 下任一已有概念笔记与练习题文件（如 0204-嵌入式操作系统/内核架构与鸿蒙.md、练习题-*.md）。

**再读素材**：
- artifacts/{chNN}/讲义_XX.json（中文键）中页 {范围} 的节点
- artifacts/{chNN}/excerpts/*.md（挑本主题相关）
- artifacts/{chNN}/mapping-chNN.md（本主题节；官方补肉用 locate_section.py --extract 落 official_*.md）

**写文件**（概念笔记 1-N 个 + 练习题-XX.md 1 个）：
- 讲义为主干；一本通/32h/官方补充处节末标 `> [!tip] 来源：XX pNN`，frontmatter 加 supplements
- 笔记要素：★ 考点、加粗关键词、对比表、[!tip] 口诀、[!warning] 易错、结尾 Related Notes wikilinks
- frontmatter：source_pdf: {讲义名}（希赛系统架构设计师讲义·第X章）；part: {编号}-{主题}；tags 含 ruankao + 领域 tag
- 练习题：讲义/32h 真题逐字带选项带 [!answer]- 解析；不足 8 题用讲义原文改写判断题补，标〔回忆〕，回忆≥60%

写完用 python 自检：文件存在、题≥8、[!answer]-≥题数。回复"{编号} 完成，笔记N+题M"。
