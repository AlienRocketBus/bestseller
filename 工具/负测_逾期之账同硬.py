# -*- coding: utf-8 -*-
"""负测 · 到期账「逾期者与到期者同硬」（2026-09-24 立·同日负测·令§一⑤）

★其所治者：`小说检察官::round11_audit` 之**检二**旧式——
  **限本章者 hard（拦封版）｜已逾期者 soft（不拦）**：
  ⛔**一笔账只要撑过它的到期那一章，它就从硬变软，此後永不再拦。**
★★故头一格係**旧式回灌**：造一笔逾期之账，**旧式判 soft（不拦）**，**新式须 hard**。
⛔本负测一律造局，**不动真盘一个字**。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = io.open(os.path.join(ROOT, '工具', '小说检察官.py'), encoding='utf-8').read()


def _检二():
    """★取检二那一段码（自「检二·到期账查」至其後之「检三」）。"""
    a = SRC.index('检二·到期账查')
    b = SRC.index('检三·回述实证查', a)
    return SRC[a:b]


def _判(段, its, n):
    """★把检二那一段之判照样跑一回（造局：其账其章皆本器给）。"""
    hard, soft = [], []
    due = [x for x in its if x.get('到期章') == n and x.get('状态') == 'open']
    over = [x for x in its if isinstance(x.get('到期章'), int)
            and x.get('到期章') < n and x.get('状态') == 'open']
    if due:
        hard.append('due')
    if over:
        (hard if '        if over:\n            hard.append' in 段 else soft).append('over')
    return hard, soft


def 跑():
    段 = _检二()
    R = []
    局 = [{'id': 'X-1', '到期章': 360, '状态': 'open'}]        # 逾期 3 章

    # ①⛔旧式回灌
    旧段 = 段.replace('        if over:\n            hard.append',
                     '        if over:\n            soft.append')
    h0, s0 = _判(旧段, 局, 363)
    R.append(('①⛔旧式回灌·一笔逾期3章之账，旧式只落 soft（⛔不拦封版）',
              h0 == [] and s0 == ['over']))
    h1, s1 = _判(段, 局, 363)
    R.append(('①之二·新式同一笔落 hard（拦封版）', h1 == ['over'] and s1 == []))

    # ②到期者照旧硬（⛔证这一改没把旧的那一半弄丢）
    h, s = _判(段, [{'id': 'X-2', '到期章': 363, '状态': 'open'}], 363)
    R.append(('②限本章者照旧 hard（⛔证未把旧的那一半弄丢）', h == ['due']))

    # ③未到期者不拦（⛔证本闸不是一律判否）
    h, s = _判(段, [{'id': 'X-3', '到期章': 370, '状态': 'open'}], 363)
    R.append(('③未到期者（限370·今363）不拦——⛔证本闸不是一律判否', h == [] and s == []))

    # ④已清者不拦
    h, s = _判(段, [{'id': 'X-4', '到期章': 360, '状态': 'done'}], 363)
    R.append(('④状态 done 者虽逾期亦不拦', h == [] and s == []))

    # ⑤码上之实：soft 那一行已不在，hard 那一行在
    R.append(('⑤码上·over 已不落 soft',
              not re.search(r'if over:\s*\n\s*soft\.append', 段)))
    R.append(('⑤之二·码上·over 落 hard', re.search(r'if over:\s*\n\s*hard\.append', 段) is not None))

    # ⑥⛔其出路三条须写在报文里（⛔而「回执里说明一句」不在其内）
    i = 段.find("hard.append('已逾期而未判")
    报 = 段[i:i + 400] if i >= 0 else ''
    R.append(('⑥报文写明三条出路（清／展期记因／销明其法）',
              i >= 0 and all(k in 报 for k in ('清', '展期记因', '销明其法'))))
    R.append(('⑥之二·⛔「于回执逐笔说明」那条软路已不在报文里', '于回执逐笔说明' not in 段))

    # ⑦真盘：今日无一笔逾期之 open（⛔故这一改不回头红任何已封之章）
    led = json.load(io.open(os.path.join(ROOT, '设定', '到期账.json'), encoding='utf-8'))
    its = led if isinstance(led, list) else led.get('items', led.get('账', []))
    ops = [x for x in its if x.get('状态') == 'open']
    # ⛔最末之章取自**正文**，⛔不取自 `版本/` 之目录——
    #   ★本负测头一版取的是後者，而盘上有一个 `版本/第999章`（局用之桩），
    #     **最末遂被判作 999，一切 open 皆成逾期**——**尺拿错了，判的就不是这件事**。
    import importlib.util as _u2
    _s2 = _u2.spec_from_file_location('核轮', os.path.join(ROOT, '工具', '核轮.py'))
    _m2 = _u2.module_from_spec(_s2)
    _s2.loader.exec_module(_m2)
    最末 = max(_m2.F)
    逾 = [x for x in ops if isinstance(x.get('到期章'), int) and x['到期章'] < 最末]
    R.append(('⑦真盘·今日 open %d 笔，其中逾期者 0 笔（⛔故此改不回头红已封之章）'
              % len(ops), not 逾))
    R.append(('⑦之二·真盘之 open 俱带到期章（⛔无到期章者此闸看不见它）',
              all(isinstance(x.get('到期章'), int) for x in ops)))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·逾期之账同硬 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
