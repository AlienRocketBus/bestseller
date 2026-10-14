#!/usr/bin/env python3
"""欠账闸（1014 立·W25 造之回报审之升级案第一条「天花板」）——零 token：主案之 G 号（正文改处）执行了没有。

为何立：W25 全段逻辑评逮——383 整场粮房戏与现行 261、263 白文当面相抵、385 之扳机与 273「三天前」相抵、384 之绝拍缺 161 之种：
  俱因 D6 六审主案 §四 之 G 号（G43、G44、G48、G65、G6、G4、G14……）裁而未落正文；而造章.js 无一处问「本章所赖之 G 号落了没有」。
判法（W25 两位反方驳倒原判法後所改·⛔另造）：按 G 表第三栏「式」分流，只查该章**白文**（「【本章亮点】」以下係骨记、常回引原句，⛔查）：
  · 式含「後添」或「添」（护句只添）：改作（第五栏）之首段「」在白文里 → 已执行；原句在不在不论（原句照留）。
  · 式为「删」：原句之首段「」不在白文 → 已执行。
  · 其余（此句改为／改／此段改为／删＋改／正一字／照五审 S#）：原句之首段「」不在白文、且改作之首段「」（若有）在白文 → 已执行。
  · 取不出「」者（改作照五审 S# 而本表无其文等）→ 判「不可机判」，照实列，⛔当已执行、⛔当未执行。
⛔限：只判「字落没落」，不判改得好不好；处栏之章号取其首个三位或二位数。

用法：
  python3 工具/欠账闸.py [主案档]        # 默认 设定/剧情庭题/D6_床上那人_六审主案.md；印每号之判与合计
  python3 工具/欠账闸.py --章 383        # 只印本章所赖（「由」栏提到本章号）之 G 号之判；有未执行者 rc=1
  python3 工具/欠账闸.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
默认 = os.path.join('设定', '剧情庭题', 'D6_床上那人_六审主案.md')


def 白文(n, root=ROOT):
    import 章料
    f = 章料.章档(n, root)
    if not f:
        return None
    t = open(f, encoding='utf-8').read()
    i = t.find('【本章亮点】')
    return t[:i] if i >= 0 else t


def 首引(格):
    m = re.search(r'「([^」]{2,})」', 格 or '')
    return m.group(1) if m else ''


def 章号(处):
    m = re.search(r'(?<!\d)(\d{2,3})(?=[:：（(]|\s|$)', 处 or '')
    return int(m.group(1)) if m else None


def 行们(文):
    """G 表之行 → [(号, 处, 式, 原, 改, 由)]。"""
    出 = []
    for l in 文.split('\n'):
        m = re.match(r'\|\s*(G\d+)\s*\|(.*)\|\s*$', l)
        if not m:
            continue
        c = [x.strip() for x in m.group(2).split('|')]
        if len(c) < 4:
            continue
        处, 式, 原, 改 = c[0], c[1], c[2], c[3]
        由 = c[4] if len(c) > 4 else ''
        出.append((m.group(1), 处, 式, 原, 改, 由))
    return 出


def 判一(处, 式, 原, 改, 取白=白文):
    n = 章号(处)
    if n is None:
        return '不可机判', '处栏取不出章号'
    白 = 取白(n)
    if 白 is None:
        return '不可机判', '第%d章正文不在' % n
    原句 = 首引(原)
    改句 = 首引(改.split('→', 1)[1]) if '→' in (改 or '') else 首引(改)   # ★「旧」→「新」之式：取箭後之新（1014 自测逮：旧取箭前之「三天前」，判 273:345 未执行）
    if re.search(r'後添|添', 式) and not re.search(r'删|改', 式):
        if not 改句:
            return '不可机判', '添而改作无「」'
        return ('已执行' if 改句 in 白 else '未执行'), '添「%s」%s' % (改句[:20], '在' if 改句 in 白 else '不在')
    if 式.strip().startswith('删') and '改' not in 式:
        if not 原句:
            return '不可机判', '删而原句无「」'
        return ('已执行' if 原句 not in 白 else '未执行'), '原「%s」%s' % (原句[:20], '已去' if 原句 not in 白 else '仍在')
    if not 原句:
        return '不可机判', '原句无「」'
    原在 = 原句 in 白
    改在 = (改句 in 白) if 改句 else None
    if not 原在 and 改在 is not False:
        return '已执行', '原「%s」已去%s' % (原句[:20], '' if 改在 is None else '、改作在')
    return '未执行', '原「%s」%s%s' % (原句[:20], '仍在' if 原在 else '已去', '' if 改在 is None else ('、改作在' if 改在 else '、改作不在'))


def 查(档=默认, root=ROOT, 章=None):
    t = open(os.path.join(root, 档), encoding='utf-8').read()
    结 = []
    for 号, 处, 式, 原, 改, 由 in 行们(t):
        if 章 is not None and str(章) not in (由 + 处):
            continue
        判, 说 = 判一(处, 式, 原, 改, lambda n: 白文(n, root))
        结.append((号, 处[:30], 式[:16], 判, 说))
    return 结


def 自测():
    ok = 共 = 0
    假 = {161: '有气。慢，可是有。气是从牙缝里出来的。他的牙咬着。\n', 273: '昨天有一个人隔着五步看她这一页。\n', 261: '一本记多少天她知道：她在粮房管过那一摞。\n', 300: '十七行。\n'}
    取 = lambda n: 假.get(n)
    共 += 1; ok += 判一('161:57 後', '後添', '161:57「有气。慢，可是有。」', '「气是从牙缝里出来的。他的牙咬着。」', 取)[0] == '已执行'   # 添：原句照留不碍
    共 += 1; ok += 判一('273:345', '照五审 S55', '273:345「三天前有一个人隔着五步看她这一页。」', '「三天前」→「昨天」', 取)[0] == '已执行'
    共 += 1; ok += 判一('261（来路）', '此段改为', '261:129「一本记多少天她知道：她在粮房管过那一摞。」', '「一本记多少天她知道。」', 取)[0] == '未执行'  # 原句仍在
    共 += 1; ok += 判一('115:281 後', '後添', '115:281「不用排。」', '「过柱子的时候」', 取)[0] == '不可机判'   # 正文不在
    共 += 1; ok += 判一('300:233', '删', '300:233「十七行。」', '', 取)[0] == '未执行'
    共 += 1; ok += 章号('261:509、513') == 261 and 章号('273:301、341、345') == 273 and 章号('115:281 後') == 115
    print('欠账闸·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    章 = int(a[a.index('--章') + 1]) if '--章' in a else None
    档 = next((x for x in a if x.endswith('.md')), 默认)
    结 = 查(档, ROOT, 章)
    计 = {}
    for 号, 处, 式, 判, 说 in 结:
        计[判] = 计.get(判, 0) + 1
        print('  %s %-4s %-30s %-16s %s' % ({'已执行': '✓', '未执行': '⛔', '不可机判': '？'}[判], 号, 处, 式, 说))
    print('欠账闸·%s%s：%s' % (os.path.basename(档), '' if 章 is None else '·第%d章所赖' % 章, '｜'.join('%s %d' % kv for kv in 计.items())))
    sys.exit(1 if 计.get('未执行') else 0)
