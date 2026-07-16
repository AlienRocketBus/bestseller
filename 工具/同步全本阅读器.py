#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把正文 Markdown 同步进全本 HTML 阅读器。

默认写回阅读器；传入 --check 时只检查，不写文件。正文新增章节时，
同步器会按章号自动补进目录和正文，不要求先在 HTML 里手工留占位。
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "正文"
READER = ROOT / "阅读器" / "镇冢秘术_全本阅读器.html"
CANON_ID = "ZM-CANON-20260715-08"


def cn_to_int(value: str) -> int:
    digits = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
              "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
              "〇": 0}
    units = {"十": 10, "百": 100, "千": 1000, "万": 10000}
    if not value or any(char not in digits and char not in units for char in value):
        raise ValueError(f"非法中文章号：{value}")
    total = section = digit = 0
    for char in value:
        if char in digits:
            digit = digits[char]
            continue
        unit = units[char]
        if unit == 10000:
            section = (section + digit) * unit
            total += section
            section = digit = 0
        else:
            section += (digit or 1) * unit
            digit = 0
    return total + section + digit


def read_chapters() -> list[dict[str, object]]:
    chapters: list[dict[str, object]] = []
    header_re = re.compile(
        r"^第([零〇一二三四五六七八九十百千万]+)章[\u3000 ]*(.+?)\s*$"
    )
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
        filename_match = re.search(
            r"第([零〇一二三四五六七八九十百千万]+)章_", path.name
        )
        if not filename_match:
            raise ValueError(f"文件名章号无法解析：{path}")
        filename_number = cn_to_int(filename_match.group(1))
        if filename_number != number:
            raise ValueError(
                f"文件名与标题章号不一致：{path.name}={filename_number}，"
                f"标题={number}"
            )
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


def render_toc_item(chapter: dict[str, object]) -> str:
    number = int(chapter["number"])
    number_cn = html.escape(str(chapter["number_cn"]))
    title = html.escape(str(chapter["title"]))
    count = int(chapter["char_count"])
    return (
        f'<li><a href="#ch{number}" data-ch="{number}">'
        f'<span class="tn">第{number_cn}章</span>'
        f'<span class="tt">{title}</span>'
        f'<span class="tc">{count}</span></a></li>'
    )


def insert_toc_item(reader: str, chapter: dict[str, object]) -> str:
    """把缺失的目录项插到下一现有章之前；末章则放到目录尾。"""
    number = int(chapter["number"])
    entries = list(re.finditer(
        r'<li><a href="#ch(\d+)" data-ch="\1">', reader
    ))
    next_entry = next(
        (match for match in entries if int(match.group(1)) > number), None
    )
    item = render_toc_item(chapter)
    if next_entry:
        return reader[:next_entry.start()] + item + "\n" + reader[next_entry.start():]

    marker = "</ul></nav>"
    if reader.count(marker) != 1:
        raise ValueError("阅读器目录结束标记缺失／重复")
    return reader.replace(marker, item + "\n" + marker, 1)


def insert_section(reader: str, chapter: dict[str, object]) -> str:
    """把缺失的正文插到下一现有章之前；末章则放到正文容器尾。"""
    number = int(chapter["number"])
    sections = list(re.finditer(
        r'<section class="chapter" id="ch(\d+)" data-ch="\1">', reader
    ))
    next_section = next(
        (match for match in sections if int(match.group(1)) > number), None
    )
    section = render_section(chapter)
    if next_section:
        return reader[:next_section.start()] + section + reader[next_section.start():]

    marker = '</div></div></div><button id="top">'
    if reader.count(marker) != 1:
        raise ValueError("阅读器正文结束标记缺失／重复")
    return reader.replace(marker, section + marker, 1)


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
        toc_hits = len(toc_re.findall(result))
        if toc_hits > 1:
            raise ValueError(f"阅读器目录重复第 {number} 章")
        if toc_hits == 1:
            result = toc_re.sub(toc_replacement, result, count=1)
        else:
            result = insert_toc_item(result, chapter)

        section_re = re.compile(
            rf'<section class="chapter" id="ch{number}" data-ch="{number}">.*?</section>',
            re.S,
        )
        section_hits = len(section_re.findall(result))
        if section_hits > 1:
            raise ValueError(f"阅读器正文重复第 {number} 章")
        if section_hits == 1:
            result = section_re.sub(render_section(chapter), result, count=1)
        else:
            result = insert_section(result, chapter)

    expected_numbers = [int(chapter["number"]) for chapter in chapters]
    toc_numbers = [
        int(match.group(1))
        for match in re.finditer(
            r'<li><a href="#ch(\d+)" data-ch="\1">', result
        )
    ]
    section_numbers = [
        int(match.group(1))
        for match in re.finditer(
            r'<section class="chapter" id="ch(\d+)" data-ch="\1">', result
        )
    ]
    if toc_numbers != expected_numbers:
        raise ValueError(
            f"阅读器目录章号与正文不完全一致：{toc_numbers} != {expected_numbers}"
        )
    if section_numbers != expected_numbers:
        raise ValueError(
            f"阅读器正文章号与 Markdown 不完全一致："
            f"{section_numbers} != {expected_numbers}"
        )

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


def run_selftest(chapters: list[dict[str, object]], original: str) -> None:
    """纯内存回归：新增章可补齐，重复／幽灵章会拒绝，百章可解析。"""
    if build_reader(original, chapters) != original:
        raise AssertionError("当前阅读器尚未同步，不能作为自测基线")
    last = int(chapters[-1]["number"])
    missing, toc_hits = re.subn(
        rf'<li><a href="#ch{last}" data-ch="{last}">.*?</li>\n?',
        "", original, count=1,
    )
    missing, section_hits = re.subn(
        rf'<section class="chapter" id="ch{last}" data-ch="{last}">.*?</section>',
        "", missing, count=1, flags=re.S,
    )
    if toc_hits != 1 or section_hits != 1:
        raise AssertionError("无法构造末章缺失样本")
    if build_reader(missing, chapters) != original:
        raise AssertionError("自动追加末章后未能精确还原阅读器")

    duplicated = original.replace(
        "</ul></nav>", render_toc_item(chapters[-1]) + "\n</ul></nav>", 1
    )
    try:
        build_reader(duplicated, chapters)
    except ValueError:
        pass
    else:
        raise AssertionError("重复目录项未被拒绝")

    ghost = last + 1
    ghosted = original.replace(
        "</ul></nav>",
        f'<li><a href="#ch{ghost}" data-ch="{ghost}">'
        '<span class="tn">幽灵章</span><span class="tt">幽灵</span>'
        '<span class="tc">0</span></a></li>\n</ul></nav>',
        1,
    )
    ghosted = ghosted.replace(
        '</div></div></div><button id="top">',
        f'<section class="chapter" id="ch{ghost}" data-ch="{ghost}">'
        '<p>幽灵</p></section></div></div></div><button id="top">',
        1,
    )
    try:
        build_reader(ghosted, chapters)
    except ValueError:
        pass
    else:
        raise AssertionError("正文不存在的幽灵章未被拒绝")

    expected = {"九十九": 99, "一百": 100, "一百零一": 101, "三百": 300}
    if any(cn_to_int(text) != number for text, number in expected.items()):
        raise AssertionError("百章以上中文章号解析失败")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只检查阅读器是否与正文同步")
    parser.add_argument("--selftest", action="store_true", help="纯内存运行目录／正文同步回归")
    args = parser.parse_args()

    chapters = read_chapters()
    original = READER.read_text(encoding="utf-8")
    updated = build_reader(original, chapters)

    if args.selftest:
        run_selftest(chapters, original)
        print("阅读器同步器自检通过：自动追加／幂等／重复／幽灵章／百章解析")
        return 0

    if args.check:
        if updated != original:
            print("阅读器未与正文同步；请运行：python3 工具/同步全本阅读器.py")
            return 1
        print(f"阅读器同步检查通过：{len(chapters)} 章")
        return 0

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=READER.parent,
            prefix=READER.name + ".", suffix=".tmp", delete=False,
        ) as handle:
            handle.write(updated)
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = Path(handle.name)
        os.replace(temp_path, READER)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
    total = sum(int(chapter["char_count"]) for chapter in chapters)
    print(f"已同步阅读器：{len(chapters)} 章，{total:,} 字")
    return 0


if __name__ == "__main__":
    sys.exit(main())
