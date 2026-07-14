#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把正文 Markdown 同步进全本 HTML 阅读器。

默认写回阅读器；传入 --check 时只检查，不写文件。
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "正文"
READER = ROOT / "阅读器" / "镇冢秘术_全本阅读器.html"
CANON_ID = "ZM-CANON-20260714-02"


def cn_to_int(value: str) -> int:
    digits = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
              "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    if value == "十":
        return 10
    if "十" in value:
        left, right = value.split("十", 1)
        tens = digits[left] if left else 1
        ones = digits[right] if right else 0
        return tens * 10 + ones
    return digits[value]


def read_chapters() -> list[dict[str, object]]:
    chapters: list[dict[str, object]] = []
    header_re = re.compile(r"^第([一二三四五六七八九十]+)章[\u3000 ]*(.+?)\s*$")
    for path in CHAPTER_DIR.glob("镇冢秘术_第*章_*.md"):
        source = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        lines = source.splitlines()
        match = None
        header_index = -1
        for index, line in enumerate(lines):
            match = header_re.match(line.strip())
            if match:
                header_index = index
                break
        if not match:
            raise ValueError(f"找不到章节标题：{path}")

        number_cn, title = match.groups()
        number = cn_to_int(number_cn)
        body_text = "\n".join(lines[header_index + 1:]).strip()
        paragraphs = [
            " ".join(part.strip().splitlines())
            for part in re.split(r"\n\s*\n", body_text)
            if part.strip()
        ]
        char_count = len(re.findall(r"[\u4e00-\u9fff]", body_text))
        chapters.append({
            "number": number,
            "number_cn": number_cn,
            "title": title,
            "paragraphs": paragraphs,
            "char_count": char_count,
            "path": path,
        })

    chapters.sort(key=lambda item: int(item["number"]))
    expected = list(range(1, len(chapters) + 1))
    actual = [int(item["number"]) for item in chapters]
    if actual != expected:
        raise ValueError(f"章节编号不连续：{actual}")
    return chapters


def render_section(chapter: dict[str, object]) -> str:
    number = int(chapter["number"])
    number_cn = html.escape(str(chapter["number_cn"]))
    title = html.escape(str(chapter["title"]))
    count = int(chapter["char_count"])
    paragraphs = "\n".join(
        f"<p>{html.escape(str(paragraph), quote=False)}</p>"
        for paragraph in chapter["paragraphs"]
    )
    return (
        f'<section class="chapter" id="ch{number}" data-ch="{number}">'
        f'<div class="chead"><div class="cnum">第 {number_cn} 章</div>'
        f'<h2 class="cname">{title}</h2>'
        f'<div class="cmeta">本章 {count} 字</div></div>'
        f'{paragraphs}<div class="cend">◇</div></section>'
    )


def build_reader(original: str, chapters: list[dict[str, object]]) -> str:
    result = original
    for chapter in chapters:
        number = int(chapter["number"])
        title = html.escape(str(chapter["title"]))
        count = int(chapter["char_count"])
        toc_re = re.compile(
            rf'(<li><a href="#ch{number}" data-ch="{number}"><span class="tn">)'
            r'.*?(</span><span class="tt">).*?'
            r'(</span><span class="tc">).*?(</span></a></li>)'
        )
        toc_replacement = (
            rf'\g<1>第{chapter["number_cn"]}章\g<2>{title}'
            rf'\g<3>{count}\g<4>'
        )
        result, toc_hits = toc_re.subn(toc_replacement, result, count=1)
        if toc_hits != 1:
            raise ValueError(f"阅读器目录缺少第 {number} 章")

        section_re = re.compile(
            rf'<section class="chapter" id="ch{number}" data-ch="{number}">.*?</section>',
            re.S,
        )
        result, section_hits = section_re.subn(render_section(chapter), result, count=1)
        if section_hits != 1:
            raise ValueError(f"阅读器正文缺少第 {number} 章")

    total = sum(int(chapter["char_count"]) for chapter in chapters)
    count = len(chapters)
    result, cover_hits = re.subn(
        r'<div class="desc">.*?</div><div class="meta"(?:\s+data-canon-id="[^"]*")?>',
        '<div class="desc">给爷爷守灵那夜，我在自家地窖里，<br>'
        '撞见一具身着秦衣、经久不腐、周身之气却仍在呼吸的古尸。<br>'
        '它手中的血图，正指向我即将采访的柏冢。</div>'
        f'<div class="meta" data-canon-id="{CANON_ID}">',
        result,
        count=1,
        flags=re.S,
    )
    if cover_hits != 1:
        raise ValueError("阅读器封面简介或 meta 标签缺失／重复")

    def stamp_html(match: re.Match[str]) -> str:
        tag = re.sub(r'\s+data-canon-id="[^"]*"', '', match.group(0))
        return f'{tag[:-1]} data-canon-id="{CANON_ID}">'

    result, html_hits = re.subn(r'<html\b[^>]*>', stamp_html, result, count=1)
    if html_hits != 1:
        raise ValueError("阅读器 html 根标签缺失")
    result = re.sub(
        r"共 [\d,]+ 字 · 约 [\d.]+ 万字",
        f"共 {total:,} 字 · 约 {total / 10000:.1f} 万字",
        result,
        count=1,
    )
    result = re.sub(
        r"全 \d+ 章 · [\d,]+ 字",
        f"全 {count} 章 · {total:,} 字",
        result,
        count=1,
    )
    canon_stamps = re.findall(r'data-canon-id="([^"]+)"', result)
    if len(canon_stamps) < 2 or set(canon_stamps) != {CANON_ID}:
        raise ValueError(f"阅读器 CANON-ID 未统一：{canon_stamps}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只检查阅读器是否与正文同步")
    args = parser.parse_args()

    chapters = read_chapters()
    original = READER.read_text(encoding="utf-8")
    updated = build_reader(original, chapters)

    if args.check:
        if updated != original:
            print("阅读器未与正文同步；请运行：python3 工具/同步全本阅读器.py")
            return 1
        print(f"阅读器同步检查通过：{len(chapters)} 章")
        return 0

    READER.write_text(updated, encoding="utf-8")
    total = sum(int(chapter["char_count"]) for chapter in chapters)
    print(f"已同步阅读器：{len(chapters)} 章，{total:,} 字")
    return 0


if __name__ == "__main__":
    sys.exit(main())
