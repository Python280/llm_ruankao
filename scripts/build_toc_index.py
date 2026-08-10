# -*- coding: utf-8 -*-
"""官方教程书签 → 「小节标题→物理页范围」索引（一次性）。
用法: python build_toc_index.py
产物: ../source/toc_index.json（含印刷页 offset=15 校准记录）
"""
import fitz, json, re, os

PDF = "D:/2study/软考高级学习记录/26年下-最终章/llm_ruankao/系统架构设计师教程[第二版](可搜索+字体修正+书签修正).pdf"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "toc_index.json")

doc = fitz.open(PDF)
toc = doc.get_toc()
N = doc.page_count
sections = []
for i, (lv, title, page) in enumerate(toc):
    end = toc[i + 1][2] - 1 if i + 1 < len(toc) else N
    m = re.match(r"^(\d+(?:\.\d+)*)[\.、\s]", title.strip())
    sections.append({
        "id": m.group(1) if m else None,
        "title": title.strip(),
        "level": lv,
        "phys_start": page,
        "phys_end": max(page, end),
    })
doc.close()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({
    "pdf": PDF,
    "pages_total": N,
    "printed_offset": 15,  # 印刷页 = 物理页 - 15
    "calibration": [{"phys": 62, "printed": 47}, {"phys": 116, "printed": 101}, {"phys": 45, "printed": 30}],
    "sections": sections,
}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"sections: {len(sections)} -> {OUT}")
