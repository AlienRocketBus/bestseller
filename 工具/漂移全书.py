# -*- coding: utf-8 -*-
"""漂移·全书（2026-09-16 立）——**漂移哨看得见，而从来没有人拿它去看别的章。**

★**其所由来·0916 之实**：337 之席在跑之时，**`正文/…第三百三十五章_一道指甲宽.md` 被改了两处**
　（`蹲下去`→`跪下去`、`两个膝头并拢`→`两个膝头分开一点`），**而 335 早已封版。**
　⛔**其改之由是真的**：337 之第7轮逮出一处跨章之相犯——
　**337 白文自书「她昨天摊册子跪着的那一块地」并倚着两个膝印，而 `335:29` 逐字作「蹲下去，两个膝头并拢」**，
　**蹲者土上留不下两个膝印**；**读席当日明书「⛔本席只报不代改……交封版席与作者当面了断」。**
　★**而後来那一刀还是落在了 335 身上**——**落没落对是另一问，本器不判；**
　**本器只问一句：一个已封版之章被改了，盘上有没有一样东西当场说出来。**

★★**其要害在「谁去看」**：`工具/跑轮.py::drift_of` 这只哨**本来就看得见**（本坐今日拿 335 试过，
　它当场印「⛔漂移哨：第335章回执已交（已封版），而工作区正文与 HEAD 不同」）——
　⛔**而其八处跑口，`n` 一律是「此刻正在跑的那一章」**：
　**跑 337 之时它查的是 337，没有一处去查 335。**
　★**即：这只哨不是瞎的，是从来没有人带它去别的屋子看一眼。**

★★★**故本器只办一件事**：**把 `drift_of` 拿去逐章跑一遍**（凡已交回执者）。
⛔**其判不涉对错**：**封版之後的改动本来就许走「回补／定案并记因」那一条路**——
　**本器逼出来的正是那一个「记因」**；**红着不等於改错了，红着等於「还没有人写下为什么」。**
⛔**并及一样不许**：**正在写的那一章尚无回执，`drift_of` 自会放它过去**——**不许拿本器去拦一个正在写的人。**

★**其数·0916 亲跑**：已交回执 262 章，**逐章比过 HEAD，漂移者恰一章：335。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, io, glob, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _借():
    """⛔借 `跑轮.py` 之 `drift_of` 与 `chap_num`——**不另写一份**（旧借 十轮精进 之 drift_of，其码同；1027 十轮精进汰）。
    ★**其由**：**同一件事两处各写一份，早晚两份说的不是一件事**（体检账 五十三之族）。"""
    def 载(名):
        spec = importlib.util.spec_from_file_location('_' + 名, os.path.join(ROOT, '工具', 名 + '.py'))
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except SystemExit:
            pass
        return mod
    _跑 = 载('跑轮')
    return _跑.drift_of, _跑.chap_num


def 查():
    drift_of, chap_num = _借()
    漂 = []
    for f in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md')), key=chap_num):
        n = chap_num(f)
        if n < 1:
            continue
        rec = glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章作业单.md' % n))
        if not rec:
            continue                      # ⛔未交回执者＝正在写的那一章，不辖
        try:
            d, lines = drift_of(n, rec, f, io.open(f, encoding='utf-8').read())
        except Exception:
            continue
        if d:
            漂.append((n, lines))
    return 漂


def 自测():
    格 = []
    def 报(名, 得, 期): 格.append((名, 得 == 期, 得, 期))
    drift_of, chap_num = _借()

    # ①⛔未交回执者一律不判（正在写的那一章不许被本器拦）
    报('①未交回执者不判', drift_of(999, [], 'x', 'y')[0], False)
    # ②★借来的两样都真拿得着（⛔不另写一份，免得两份说的不是一件事）
    报('②drift_of 借得着', callable(drift_of), True)
    报('②之二 chap_num 借得着且算得对', chap_num('正文/镇冢秘术_第三百三十五章_一道指甲宽.md'), 335)
    # ③★实走一遍
    漂 = 查()
    报('③实走得列', isinstance(漂, list), True)
    # ④⛔其数须小（㊮：一只新闸红几十章，多半是闸错了）
    报('④漂移之数 ≤3（㊮）', len(漂) <= 3, True)
    # ⑤⛔本器不判对错，只逼一个记因（其语须在码里）
    码 = io.open(os.path.join(ROOT, '工具', '漂移全书.py'), encoding='utf-8').read().split('def 自测')[0]
    报('⑤明写「红着不等於改错了」', '红着不等於改错了' in 码, True)
    # ⑥⛔本器不动盘
    报('⑥不动盘（无写口／无 remove）',
       "'w'" not in 码 and 'os.remove' not in 码 and 'shutil' not in 码, True)

    过 = sum(1 for _, ok, _, _ in 格 if ok)
    for 名, ok, 得, 期 in 格:
        if not ok:
            print('  ⛔%s：得 %r，期 %r' % (名, 得, 期))
    print('%s 漂移全书·自测 %d/%d' % ('✓' if 过 == len(格) else '⛔', 过, len(格)))
    return 0 if 过 == len(格) else 1


def 全书():
    漂 = 查()
    if not 漂:
        print('✓ 漂移全书：已封版之章，章章与 HEAD 同——封版之後无人动过。')
        return 0
    for n, lines in 漂:
        for l in lines:
            print(l)
    print('  ★其治两路：①**这一改是对的** → 走回补／定案，**当场把记因写下来**'
          '（其形与 `改期记因哨` 同：一行「因故改之」不算）；')
    print('  ②**这一改是误落的** → `python3 工具/跑轮.py --还原 <N> 确认` 复原。')
    print('  ⛔**红着不等於改错了，红着等於「还没有人写下为什么」。**')
    print('⛔ 漂移全书：已封版而被改过者 %d 章：%s'
          % (len(漂), '、'.join('第%d章' % n for n, _ in 漂)))
    return 1


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 全书())
