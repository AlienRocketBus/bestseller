# -*- coding: utf-8 -*-
"""窗界哨（2026-09-18 立·⛔只报不拦，而其报须有人答）

★**立此哨之由（本日一日之内，同一个形咬了四回，一回比一回重）**：
　①`小说检察官` canon forbid：窗只挡 `。\\n`，**而骨记两段引文之间跨了一个句号**，
　　二者被缝作一句 → **一个章因为写下「本章没有犯这一条」而被判犯了这一条。**
　②`FS闸` 付语：窗开八十字而只挡 `。\\n`，**而回执一行之内数根并列以「｜」「、」相隔**，
　　窗遂咬到隔壁那一根的付语上。
　③`FS闸` 报不合：**「未销」与「已还」隔着二十字各说各的**，窗把一句报不合之话当成一笔付。
　④`开轮六检::_cold_done`：**本坐自己新写的窗只断句号**，
　　**而那几处签核写在 `## 标题` 里，其前无句号**，遂把上文一整段吞进来——
　　⛔**头两版各扫掉二十七笔旧账**（COLD-73—99），皆未落盘。

⛔**其形一句话**：**一个窗式正则，若它认「到头了」的那一组字里少一样，
　它就会跨过那一样，把两件不相干的事缝成一件。**
★★**而其害有两向，轻重不同**：
　**误报**（把没犯的判成犯了）——吵，但看得见；
　**漏报／误销**（把说起它当成签了它）——⛔**它替一笔真账签了字，而盘上一处红也没有。**

【其法·⛔只数形，不判对错】
　逐样器里找 `[^…]{0,N}` 之式，看它排除之界里有没有 `。` 与 `\\n` 二者。
　**缺一即入报单**——⛔**而「入报单」不等於「它错了」**：
　　**一个只在一行之内找东西的窗，不挡句号是对的；一个跨行找东西的窗，不挡换行才是对的。**
　★**故本哨不判，只把它们摆出来，并索一处回答**：`设定/窗界账.md`。
【⛔何以只报不拦】其一，六十五处之中多数是对的，一律拦即逼人去改对的那些；
　其二，**本日之四处皆係人读出来的，不是数出来的**——**一道数得出来的哨，只能把人领到门口。**
【⛔而「只报不拦」不等於不答】（承 `体检账 九十一`）：
　**本哨每回印出「账上答过几条、未答几条」**；**未答者过其限，即当面升作硬项。**
"""
import io, os, re, sys

import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_窗 = re.compile(r"\[\^([^\]]{1,24})\]\{0,(\d+)\}")


def 扫():
    """回 [(档, 行, 其界, 其长, 缺哪一样)]；⛔只数形，不判对错。"""
    出 = []
    for f in sorted(glob.glob(os.path.join(ROOT, '工具', '*.py'))):
        if os.path.basename(f) == '窗界哨.py':
            continue
        src = io.open(f, encoding='utf-8', errors='replace').read()
        for m in _窗.finditer(src):
            cls, n = m.group(1), int(m.group(2))
            缺 = []
            if '。' not in cls:
                缺.append('。')
            if '\\n' not in cls and '\n' not in cls:
                缺.append('换行')
            if 缺:
                出.append((os.path.basename(f), src[:m.start()].count('\n') + 1,
                           cls, n, '＋'.join(缺)))
    return 出


def 报(quiet=False):
    rows = 扫()
    zh = os.path.join(ROOT, '设定', '窗界账.md')
    txt = io.open(zh, encoding='utf-8', errors='replace').read() if os.path.exists(zh) else ''
    答 = len(re.findall(r'^\|\s*✅', txt, re.M))
    if not quiet:
        print('════ 窗界哨 · 只报不拦 ════')
        print('  【何以立】0918 一日之内同一个形咬了四回；其重者係「说起它」被当成「签了它」，')
        print('            ⛔**替两笔真账签了字，而盘上一处红也没有**。')
        print('  窗式正则共 %d 处，其界缺一样者 %d 处：'
              % (len(_窗.findall(''.join(io.open(f, encoding='utf-8', errors='replace').read()
                                         for f in glob.glob(os.path.join(ROOT, '工具', '*.py'))))),
                 len(rows)))
        by = {}
        for f, ln, cls, n, 缺 in rows:
            by.setdefault(f, []).append((ln, cls, n, 缺))
        for f in sorted(by, key=lambda x: -len(by[x]))[:10]:
            print('   %-26s %2d 处｜%s' % (f, len(by[f]),
                                          '、'.join('%d行(缺%s)' % (a, d) for a, _c, _n, d in by[f][:4])))
        print('  ── 答过 %d 条（`设定/窗界账.md` 之 ✅）｜未答 %d 条 ──' % (答, len(rows) - 答))
        if not os.path.exists(zh):
            print('  ⛔ `设定/窗界账.md` 不在——**报了没人答，等於没报**。')
        print('  ★⛔而入报单不等於它错了：**只在一行之内找东西的窗，不挡句号是对的；**')
        print('    **跨行找东西的窗，不挡换行才是对的。本哨只把它们摆出来，判在人。**')
    return rows


if __name__ == '__main__':
    报()
    sys.exit(0)   # ★只报不拦
