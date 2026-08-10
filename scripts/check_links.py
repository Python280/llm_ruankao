# -*- coding: utf-8 -*-
"""StudyVault 断链 + 结构质检。
用法: python check_links.py [vault路径]  （默认脚本同级 ../StudyVault）
检查: wiki 断链 / 练习题题数与折叠答案 / frontmatter 齐全。
"""
import re, glob, os, sys

VAULT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "StudyVault")

notes = {}
for f in glob.glob(os.path.join(VAULT, "**", "*.md"), recursive=True):
    notes[os.path.splitext(os.path.basename(f))[0]] = f

bad = []
DASH = {"dashboard", "MOC", "Quick-Reference", "Exam-Traps"}
for name, f in notes.items():
    txt = open(f, encoding="utf-8").read()
    for link in re.findall(r"\[\[([^\]|#]+)", txt):
        target = link.strip().split("/")[-1]  # 兼容 [[concepts/xxx]] 路径式链接
        if target not in notes:
            bad.append((name, "断链 " + link.strip()))
    if "练习题" in name:
        q = len(re.findall(r"^## Q", txt, re.M)) + len(re.findall(r"^F\d+", txt, re.M))
        a = txt.count("[!answer]-")
        if not (q >= 8 and a >= q):
            bad.append((name, f"题数{q}/答案折叠{a}"))
    is_concept_tracker = os.path.basename(os.path.dirname(f)) == "concepts"
    if not txt.startswith("---") and name not in DASH and not is_concept_tracker:
        bad.append((name, "缺frontmatter"))

print("缺陷:", bad if bad else "无")
sys.exit(1 if bad else 0)
