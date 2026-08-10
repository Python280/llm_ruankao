# -*- coding: utf-8 -*-
"""官方教程按需定位：节号直查 / 标题模糊 / 全文检索兜底 + 段落摘录。
用法:
  python locate_section.py --id 2.3.2
  python locate_section.py --title 操作系统
  python locate_section.py --kw 页面置换 --range 39-119
  python locate_section.py --extract 43-46 --out official_2.3.2.md --label "§2.3.2 操作系统"
页码一律物理页；摘录头自动带引用块（印刷页=物理页-15）。
"""
import fitz, json, re, os, argparse

BASE = os.path.dirname(os.path.abspath(__file__))
IDX = json.load(open(os.path.join(BASE, "..", "source", "toc_index.json"), encoding="utf-8"))
PDF = IDX["pdf"]


def find_kw(kw, lo=1, hi=None):
    """逐页 search_for（fitz1.28 无 Document.search_for），返回连续命中区间按命中数排序。"""
    hi = hi or IDX["pages_total"]
    doc = fitz.open(PDF)
    kw = kw.replace(" ", "")
    hits = {}
    for i in range(lo - 1, hi):
        n = len(doc[i].search_for(kw))
        if n:
            hits[i + 1] = n
    doc.close()
    runs, cur = [], None
    for p, n in sorted(hits.items()):
        if cur and p == cur["end"] + 1:
            cur["end"], cur["n"] = p, cur["n"] + n
        else:
            if cur:
                runs.append(cur)
            cur = {"start": p, "end": p, "n": n}
    if cur:
        runs.append(cur)
    return sorted(runs, key=lambda r: -r["n"])


NUM = re.compile(r"^(\d+[.)、．]|\(\d+\)|（\d+）|[①-⑩])")


def extract(lo, hi):
    """提取页范围文字，按编号/短行启发式切段，去页眉页码，修 C P U 空格。"""
    doc = fitz.open(PDF)
    paras = []
    for i in range(lo - 1, hi):
        lines = [l.strip() for l in doc[i].get_text().split("\n")]
        lines = [l for l in lines if l and not l.startswith("系统架构设计师教程")
                 and not re.fullmatch(r"\d{1,3}", l)]
        med = sorted(len(l) for l in lines)[len(lines) // 2] if lines else 0
        para = ""
        for l in lines:
            if para and (NUM.match(l) or len(para) < med * 0.7):
                paras.append(para)
                para = l
            else:
                para += l
        if para:
            paras.append(para)
    doc.close()
    text = "\n\n".join(paras)
    return re.sub(r"(?<=[A-Za-z]) +(?=[A-Za-z])", "", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", help="节号直查，如 2.3.2")
    ap.add_argument("--title", help="标题模糊匹配")
    ap.add_argument("--kw", help="全文检索关键词")
    ap.add_argument("--range", help="检索页范围 lo-hi（物理页）")
    ap.add_argument("--extract", help="摘录页范围 lo-hi")
    ap.add_argument("--out", help="摘录输出文件（source/chNN/ 下相对名或绝对路径）")
    ap.add_argument("--label", help="摘录引用块标签，如 '§2.3.2 操作系统'")
    a = ap.parse_args()

    if a.id:
        for s in IDX["sections"]:
            if s["id"] == a.id or (a.id + "." == (s["id"] or "")[:len(a.id) + 1]):
                print(f'{s["id"]}  {s["title"]}  p{s["phys_start"]}–{s["phys_end"]}')
    if a.title:
        for s in IDX["sections"]:
            if a.title in s["title"]:
                print(f'{s["id"]}  {s["title"]}  p{s["phys_start"]}–{s["phys_end"]}')
    if a.kw:
        lo, hi = (int(x) for x in a.range.split("-")) if a.range else (1, None)
        for r in find_kw(a.kw, lo, hi)[:8]:
            print(f'p{r["start"]}–{r["end"]}  命中{r["n"]}')
    if a.extract:
        lo, hi = (int(x) for x in a.extract.split("-"))
        text = extract(lo, hi)
        out = a.out or "excerpt.md"
        if not os.path.isabs(out):
            out = os.path.join(BASE, "..", "source", out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        head = (f"> 摘录自 官方教程[第二版] {a.label or ''} · 物理页 p{lo}–{hi}"
                f"（印刷页=物理页−{IDX['printed_offset']}）\n"
                f"> 原文照录，仅供浓缩；表格/图版式丢失，见原书对应页。\n\n")
        open(out, "w", encoding="utf-8").write(head + text)
        print(f"extracted {len(text)} chars -> {out}")


if __name__ == "__main__":
    main()
