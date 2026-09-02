# -*- coding: utf-8 -*-
"""立价查（2026-09-02·292第13轮所立·答第12轮之一疑）
所答之问：**这一章立了几个价，收了几个？**

★其立之由：292第12轮逮出②「页边不是行」立了一价（**写上去这一行就得往里挪**）
  而全章从未收（**她把字写得比行里的小一半**）；★★而那一根是我逐层读出来的，
  **读一回只逮得着一根**。★★★而第12轮之一疑令：**须由器出，不由我口出。**

★★★★其法：**价之形是条件句**——「A就得B」「A就成了C」「非A不可」「A就是B」；
  ★而其收，是B在其後的白文里真发生一回。故：
    ①扫全章白文之条件句，取其果（B）；
    ②在其後之拍里找B之实（以B之实词回落白文，≥MIN字之串即算）；
    ③找不着者报出——**立了而没收。**
  ★★**而「没收」不必是伤**：一章尽可以立一个价，让人物绕过去，那正是这一章的事；
    ★★★**其伤在「没收而册上不记」**——**骨记里若把这个价当成一层的内容，那一层就是空的。**
    故本器只报，不判；判归人，而人须逐条回话。
用法：python3 工具/立价查.py 292 [最小串长]
"""
import io, os, re, sys, glob

# 价之式：(名, 正则, 果之组号)
FORMS = [
    ('就得',   r'([^。；！？\n]{2,40}?)就得([^。；！？\n]{1,30})', 2),
    ('就成了', r'([^。；！？\n]{2,40}?)就成了([^。；！？\n]{1,30})', 2),
    ('非…不可', r'([^。；！？\n]{2,40}?)非([^。；！？\n]{1,20})不可', 2),
    ('就是',   r'([^。；！？\n]{2,40}?)一(?:回|下|样)就([^。；！？\n]{1,25})', 2),
]
STOP = set('的了着过和与而她他它我你这那一二三四五六七八九十个是不在有把从到就再又也都还没')


def _num(f):
    d = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    m = re.search(r'第(.+?)章', os.path.basename(f))
    if not m:
        return -1
    v, cur = 0, 0
    for ch in m.group(1):
        if ch in d: cur = d[ch]
        elif ch == '十': v += (cur or 1) * 10; cur = 0
        elif ch == '百': v += (cur or 1) * 100; cur = 0
    return v + cur


def 查(n, minlen=3):
    fs = [f for f in glob.glob('正文/*.md') if _num(f) == n]
    if not fs:
        print('  ✗ 无第%d章正文' % n); return 2
    t = io.open(fs[0], encoding='utf-8').read()
    bw = t.split('【本章亮点')[0]
    hl = t[t.find('【本章亮点'):] if '【本章亮点' in t else ''
    pai = [re.sub(r'\s', '', p) for p in bw.split('＊') if p.strip()]
    pai = [p for p in pai if p and not p.startswith('《')]
    print('\n████ 立价查 · 第%d章 ████' % n)
    print('  ★价之形係条件句；其收，是那个果在其後的白文里真发生一回。')
    print('  ★★本器只报，不判——**立而不收未必是伤，伤在没收而册上把它当成一层的内容。**\n')
    found = []
    for i, p in enumerate(pai):
        for 名, pat, g in FORMS:
            for m in re.finditer(pat, p):
                果 = m.group(g)
                实 = [c for c in 果 if c not in STOP]
                if len(实) < minlen:
                    continue
                key = ''.join(实[:minlen])
                收 = [j for j in range(i + 1, len(pai))
                      if all(c in pai[j] for c in 实[:minlen])]
                found.append((i, 名, m.group(0), 果, key, 收))
    if not found:
        print('  ✓全章无立价之句。'); return 0
    未收 = 0
    for i, 名, 全, 果, key, 收 in found:
        st = '收於拍%s' % ','.join(str(x) for x in 收[:4]) if 收 else '⛔未收'
        if not 收:
            未收 += 1
        print('  拍%-4d【%s】%s' % (i, 名, 全[:44]))
        print('        果「%s」（实字%s）→ %s' % (果, key, st))
    print('\n  ── 计 ──')
    print('  立价 %d 处，其中未收 %d 处。' % (len(found), 未收))
    if hl and 未收:
        print('\n  ── 未收者在骨记里占没占一层（此问归人，器只把料摆出来）──')
        for i, 名, 全, 果, key, 收 in found:
            if 收: continue
            在 = [k for k, b in re.findall(r'^([①-⑳])(.*?)(?=^[①-⑳]|\Z)', hl, flags=re.M | re.S)
                  if any(c in b for c in 果) and 果[:4] in re.sub(r'[*★\s]', '', b)]
            print('  拍%-4d 果「%s」→ 骨记 %s' % (i, 果, '、'.join(在) if 在 else '（未入骨记）'))
        print('  ★凡「未收」而「入了骨记」者，须当场回话：**那一层靠什么站着？**')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__.strip()); raise SystemExit(1)
    raise SystemExit(查(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 3))
