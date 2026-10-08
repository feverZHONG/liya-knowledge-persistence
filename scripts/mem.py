#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mem — 记忆账本（MEMORY.md / USER.md 逐条分解）

为什么有它：记忆有硬上限（config.yaml → memory.memory_char_limit / user_char_limit），
满了要腾位置时，光看全文挑不出「哪条最长、哪两条能合并」——逐条数字符太脏活。
这个只做一件事：把账摊开。（跟 `hygiene` 同一条原则——只报告，不修改。）

用法
  mem                  汇总 + 逐条列表（默认 MEMORY.md）
  mem --who user      换成 USER.md
  mem --top 5          只看最大的 N 条（腾位置时先看这个）
  mem --dupes          疑似同主题条目（bigram 相似度）＝合并候选
  mem --find 关键词    搜条目
  mem --json           给脚本吃

口径
  总占用 = 整个文件的字符数（已与 Hermes 报的 N/limit 对齐：2198）
  条目字数 = 该条正文（不含与相邻条之间的 "\\n§\\n" 三个字符）
"""

import argparse
import json
import os
import re
import sys
import unicodedata

def _default_root():
    """数据根探测：$HERMES_ROOT ＞ 脚本上溯三层（<root>/skills/<skill>/scripts/）＞
    ~/.hermes ＞ 家目录本身——命中判据是该层下存在 memories/ 目录。"""
    env = os.environ.get("HERMES_ROOT")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.path.abspath(os.path.join(here, "..", "..", "..")),
             os.path.expanduser("~/.hermes"),
             os.path.expanduser("~")]
    for cand in cands:
        if os.path.isdir(os.path.join(cand, "memories")):
            return cand
    return os.path.expanduser("~/.hermes")


ROOT = _default_root()
CONFIG = os.path.join(ROOT, "config.yaml")
MEM_DIR = os.path.join(ROOT, "memories")
FILES = {"memory": "MEMORY.md", "user": "USER.md"}
DEFAULT_LIMITS = {"memory": 2200, "user": 1375}
SEP = "\n§\n"


def limits():
    lim = dict(DEFAULT_LIMITS)
    try:
        import yaml  # noqa
        with open(CONFIG, encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        blk = cfg.get("memory") or {}
        if isinstance(blk.get("memory_char_limit"), int):
            lim["memory"] = blk["memory_char_limit"]
        if isinstance(blk.get("user_char_limit"), int):
            lim["user"] = blk["user_char_limit"]
    except Exception:
        pass
    return lim


def load(which):
    path = os.path.join(MEM_DIR, FILES[which])
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    items, cur, start = [], [], 1
    for i, ln in enumerate(lines, 1):
        if ln.strip() == "§":
            if any(x.strip() for x in cur):
                items.append({"text": "\n".join(cur).strip(), "line": start})
            cur, start = [], i + 1
        else:
            cur.append(ln)
    if any(x.strip() for x in cur):
        items.append({"text": "\n".join(cur).strip(), "line": start})
    for it in items:
        it["chars"] = len(it["text"])
    return path, text, items


def width(s):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def pad(s, n):
    return s + " " * max(0, n - width(s))


def brief(s, n=44):
    s = re.sub(r"\s+", " ", s).strip()
    out, w = "", 0
    for c in s:
        cw = 2 if unicodedata.east_asian_width(c) in "WF" else 1
        if w + cw > n:
            return out + "…"
        out += c
        w += cw
    return out


def bigrams(s):
    s = re.sub(r"[\s，。；：、（）：()\[\]【】.,;:!?！？\"'`—\-]+", "", s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    ap = argparse.ArgumentParser(add_help=True, description="记忆账本（只读）")
    ap.add_argument("--who", choices=["memory", "user"], default="memory")
    ap.add_argument("--top", type=int, default=0, help="只列最大的 N 条")
    ap.add_argument("--dupes", action="store_true", help="疑似同主题（合并候选）")
    ap.add_argument("--find", metavar="词", help="搜条目")
    ap.add_argument("--min-sim", type=float, default=0.30)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--root", metavar="目录",
                    help="Hermes 数据根（默认取 $HERMES_ROOT，或自动探测 ~/.hermes / 家目录）")
    args = ap.parse_args()
    if args.root:
        global CONFIG, MEM_DIR
        CONFIG = os.path.join(os.path.abspath(args.root), "config.yaml")
        MEM_DIR = os.path.join(os.path.abspath(args.root), "memories")

    path, text, items = load(args.who)
    lim = limits()[args.who]
    total = len(text)
    pct = total / lim * 100 if lim else 0
    sizes = sorted(i["chars"] for i in items) or [0]
    median = sizes[len(sizes) // 2]

    if args.find:
        hits = [it for it in items if args.find in it["text"]]
        if args.json:
            print(json.dumps({"query": args.find, "hits": hits}, ensure_ascii=False, indent=2))
            return 0
        print(f"{FILES[args.who]} · 命中 {len(hits)} 条（「{args.find}」）")
        for it in hits:
            print(f"  L{it['line']:<4} {it['chars']:>4}字  {brief(it['text'], 60)}")
        return 0

    if args.dupes:
        pairs = []
        bg = [(it, bigrams(it["text"])) for it in items]
        for i in range(len(bg)):
            for j in range(i + 1, len(bg)):
                s = jaccard(bg[i][1], bg[j][1])
                if s >= args.min_sim:
                    pairs.append((s, i, j))
        pairs.sort(reverse=True)
        if args.json:
            print(json.dumps([{"sim": round(s, 3), "a": items[i]["text"], "b": items[j]["text"]}
                              for s, i, j in pairs], ensure_ascii=False, indent=2))
            return 0
        print(f"{FILES[args.who]} · 疑似同主题 {len(pairs)} 对（阈值 {args.min_sim}）")
        if not pairs:
            print("  没找到——记忆里暂时没有能合并的。")
        for s, i, j in pairs:
            print(f"  相似 {s:.2f}  L{items[i]['line']} ↔ L{items[j]['line']}")
            print(f"      A: {brief(items[i]['text'], 56)}")
            print(f"      B: {brief(items[j]['text'], 56)}")
        return 0

    order = list(range(len(items)))
    if args.top:
        order = sorted(order, key=lambda k: -items[k]["chars"])[:args.top]

    if args.json:
        print(json.dumps({"file": FILES[args.who], "total": total, "limit": lim,
                          "count": len(items), "items": items}, ensure_ascii=False, indent=2))
        return 0

    head = "满" if total >= lim else f"余 {lim - total}"
    print(f"{FILES[args.who]} · {len(items)} 条")
    print(f"占用 {total} / {lim} 字符（{pct:.1f}%，{head}）")
    print(f"最长 {max(sizes)} · 中位 {median} · 最短 {min(sizes)}")
    print()
    print(pad("  #", 5) + pad("字符", 7) + pad("行", 6) + "摘要")
    for k in order:
        it = items[k]
        print(pad(f" {k + 1}", 5) + pad(f"{it['chars']}", 7) + pad(f"L{it['line']}", 6)
              + brief(it["text"], 52))
    if not args.top:
        print()
        print("腾位置：mem --top 5 看最大的 · mem --dupes 找能合并的 · mem --find 词 定位")
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except BrokenPipeError:      # 管道接了 head/tail：静默收工
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        rc = 0
    sys.exit(rc)
