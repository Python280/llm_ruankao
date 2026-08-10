# -*- coding: utf-8 -*-
"""扫描书/讲义视觉读页：fitz 渲染 PNG（pdftoppm 缺失时的唯一渲染器）。
用法: python render_pages.py --book 32h|ybt|official --pages 3-8 或 3,5,7 [--pdf 自定义路径] [--dpi 150]
产物: ../source/pages_<book>/pNNN.png
"""
import fitz, os, argparse

BOOKS = {
    "32h": "D:/2study/软考高级学习记录/26年下-最终章/llm_ruankao/第二版--系统架构设计师考试32小时通关.pdf",
    "ybt": "D:/2study/软考高级学习记录/26年下-最终章/llm_ruankao/(一本通）系统架构设计师-精华知识点.pdf",
    "official": "D:/2study/软考高级学习记录/26年下-最终章/llm_ruankao/系统架构设计师教程[第二版](可搜索+字体修正+书签修正).pdf",
}


def parse_pages(spec):
    pages = []
    for part in spec.split(","):
        if "-" in part:
            lo, hi = (int(x) for x in part.split("-"))
            pages.extend(range(lo, hi + 1))
        else:
            pages.append(int(part))
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", choices=list(BOOKS))
    ap.add_argument("--pdf", help="自定义 PDF 路径（优先于 --book）")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--dpi", type=int, default=150)
    a = ap.parse_args()

    pdf = a.pdf or BOOKS[a.book]
    tag = a.book or os.path.splitext(os.path.basename(pdf))[0][:8]
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", f"pages_{tag}")
    os.makedirs(outdir, exist_ok=True)

    doc = fitz.open(pdf)
    for p in parse_pages(a.pages):
        pix = doc[p - 1].get_pixmap(dpi=a.dpi)
        fn = os.path.join(outdir, f"p{p:03d}.png")
        pix.save(fn)
        print(f"p{p:03d} -> {fn}")
    doc.close()


if __name__ == "__main__":
    main()
