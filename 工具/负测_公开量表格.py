# -*- coding: utf-8 -*-
"""负测 · 开镜庭十一「公开量表动了几格」（2026-09-24 立·同日负测·令§一⑤）

★其所验非「今日之盘绿不绿」——**盘绿得了，是因为盘上本来就没有这一问**；
  ★★故头一格係**旧式回灌**：**把 353 那一张卡的实情造成一张卡**
  （量表之句原样抄过来、答 0），**旧式（无此闸）放行，新式须当场红**。
⛔本负测一律造局，**不动真盘一个字**。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import importlib.util as _u, os, sys, tempfile, shutil, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器():
    s = _u.spec_from_file_location('开镜庭', os.path.join(ROOT, '工具', '第零轮开镜庭.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _卡(m, c, 文):
    d = tempfile.mkdtemp(prefix='负测量表_')
    os.makedirs(os.path.join(d, '版本', '第%d章' % c))
    if 文 is not None:
        io.open(os.path.join(d, '版本', '第%d章' % c, '_开镜卡.md'),
                'w', encoding='utf-8').write(文)
    老 = m.ROOT
    m.ROOT = d
    try:
        return m._check_gauge(c)[0]
    finally:
        m.ROOT = 老
        shutil.rmtree(d, ignore_errors=True)


def 跑():
    m = _器()
    R = []
    问 = m._量表问
    头 = '# 卡\n\n## ★问五\n'

    # ①⛔旧式回灌：353 之实（量表之句原样抄来、读数不动）——新式须红
    卡353 = 头 + ('- **上一篇同线之章**：**第351章**\n'
                  '- **其量表今日之读数**：**「白的那一头还剩两个指腹」**\n'
                  '- **%s**：**0**\n' % 问)
    r = _卡(m, 400, 卡353)
    R.append(('①⛔旧式回灌·353 之实（抄同一句、读数不动）新式当场红', r[1] is False and '本章是多的' in r[2]))
    R.append(('①之二·旧式（本闸未立之日，卡上根本无此问）放行——证本格非陪跑',
              问 not in open(os.path.join(ROOT, '版本', '第353章', '_开镜卡.md'),
                             encoding='utf-8', errors='replace').read()))

    # ②答非 0 者过（⛔证本闸不是一律判否）
    R.append(('②答 2 格者过（⛔证本闸不是一律判否）',
              _卡(m, 400, 头 + '- **%s**：**2**\n' % 问)[1] is True))
    R.append(('②之二·答汉数「三」亦认',
              _卡(m, 400, 头 + '- **%s**：**三格**\n' % 问)[1] is True))
    R.append(('②之三·答「零」与答 0 同判',
              _卡(m, 400, 头 + '- **%s**：**零**\n' % 问)[1] is False))

    # ③占位符不算答
    r = _卡(m, 400, 头 + '- **%s**：〔数〕 ← ⛔答 0 即本章是多的\n' % 问)
    R.append(('③占位符〔数〕不算答', r[1] is False and '占位符' in r[2]))

    # ④卡上无此问者红
    r = _卡(m, 400, 头 + '- **本章之品**：**常章**\n')
    R.append(('④卡上无此问者红', r[1] is False and '无此问' in r[2]))

    # ⑤⛔不许拿问那一行里的字当答（本文件已栽过两回「取行不取答」）
    r = _卡(m, 400, 头 + ('- **%s**：**0**\n'
                          '  - ★而此问不是「有没有写到它」（此行内有 1 个数字·⛔不许被取作答）\n' % 问))
    R.append(('⑤⛔取的是答那一行，不是後面那一行（旧伤同族·321之日栽过）',
              r[1] is False))
    r2 = _卡(m, 400, 头 + '- ★**%s**之说明：一格也算动\n' % 问)
    R.append(('⑤之二·说明行若答不出数即红（⛔不许把说明当答）', r2[1] is False))

    # ⑥答不是数者红
    R.append(('⑥答「已动」者红（⛔它须是一个数得着的数）',
              _卡(m, 400, 头 + '- **%s**：**已动**\n' % 问)[1] is False))

    # ⑦⛔自 364 起看：363 及其前一律不红（⛔本闸不回头红一张已用过的卡）
    R.append(('⑦⛔第363章（其卡 0923 已立并据以起草）不红', _卡(m, 363, 头)[1] is True))
    R.append(('⑦之二·第364章无卡即红（⛔证⑦不是一路放行）', _卡(m, 364, None)[1] is False))
    R.append(('⑦之三·其自係 364，⛔不是一个会随今章往後挪的数', m._量表自 == 364))

    # ⑧真盘：363 之卡在，且本闸於其上为绿（⛔证接进 run 不会立时把在跑之章打红）
    R.append(('⑧真盘·第363章之卡在盘上', os.path.exists(
        os.path.join(ROOT, '版本', '第363章', '_开镜卡.md'))))

    # ⑨模子里带着这一问（⛔一问不在模子上，那一格就永远没人填）
    src = io.open(os.path.join(ROOT, '工具', '第零轮开镜庭.py'), encoding='utf-8').read()
    模 = src.split('def make_card')[1].split('def check0')[0]
    R.append(('⑨模子（--立）里带着这一问', 问 in 模))
    R.append(('⑨之二·模子里那一行係占位符〔数〕（⛔不许预先填一个数进去）', '〔数〕' in 模))

    # ⑩它接进了 run（⛔写了函数而没接线，等於没立）
    R.append(('⑩已接进 run（⛔写了函数没接线等於没立·律⑫）',
              '_check_gauge(c)' in src.split('def run(c')[1]))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·公开量表格 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
