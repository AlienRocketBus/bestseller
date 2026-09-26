# -*- coding: utf-8 -*-
"""负测 · 自进化环（2026-09-24 立·同日负测·令§一⑤）

⛔**其所验者：这一环自己会不会也变成「只会报」或「量错东西」的那一道。**
★**头一格係旧式回灌**：**0924 之 `未上库哨` 旧式只量主枝**——
  **於真盘上它报「未上库 205 笔」而判不安**；**新式先量存底枝，判「书在云端，安全」**。
  **二判确实不同，本测非陪跑。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re, tempfile
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器(名):
    s = _u.spec_from_file_location(名, os.path.join(ROOT, '工具', 名 + '.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def 跑():
    环 = _器('自进化环')
    哨 = _器('未上库哨')
    R = []

    # ①⛔旧式回灌：只量主枝者，主枝一领先即报「未上库」（而书其实在存底枝）。
    #   ★0926·375 救章席治其根：旧式此格读「真盘今日领先几笔」——那是盘之况，不是器之性：
    #     主枝一推上去（领先 0—2 笔）此格即红，而旧式之病一分未变；每推一回就逼人「先别推」，自相咬死。
    #   ★今造其局：以领先恰到限之数（笔之限）喂旧式之量，验旧式确判「未上库」——病照样回灌得出；
    #     真盘之数只印不判（①之三），⛔不以盘况充器性。
    _旧跑 = 哨._跑
    try:
        哨._跑 = lambda *a: (str(哨.笔之限) if 'rev-list' in a else _旧跑(*a))
        n, 日, _ = 哨.量()
    finally:
        哨._跑 = _旧跑
    R.append(('①⛔旧式回灌·只量主枝：造局领先 %s 笔，旧式判「未上库」' % n,
              isinstance(n, int) and n >= 哨.笔之限))
    n真, _, _ = 哨.量()
    R.append(('①之三·真盘之实（只印不判）：主枝领先 %s 笔' % n真, True))
    # ①之二·新式先量存底枝：云端章数＝本地
    底章, 底分 = 哨._存底枝之况()
    import glob
    本 = len(glob.glob(os.path.join(ROOT, '正文', '*.md')))
    R.append(('①之二·新式先量存底枝：云端 %s 章＝本地 %d 章（**书在云端**）' % (底章, 本),
              底章 == 本))

    # ②L0 只查（不修）之判：真盘今日安
    ok0, 语0 = 环.L0(自修=False)
    R.append(('②L0 只查：真盘今日判「安」（存底枝新、章数齐）', ok0))

    # ③⛔挂账之牙：同一因连两回即卡死；修好即销
    老 = dict(环._读挂())
    try:
        环._写挂({})
        环.挂('测', '造局', False)
        二 = 环.挂('测', '造局', False)
        R.append(('③⛔同一因连 2 回即达卡死之限（%d）' % 环.卡死之回, 二 >= 环.卡死之回))
        环.挂('测', '造局', True)
        R.append(('③之二·修好即销', '测｜造局' not in 环._读挂()))
    finally:
        环._写挂(老)

    # ④⛔L3 之牙：造一本病族账，一族「器之族」例 2 而器写「无」→ 当场红
    d = tempfile.mkdtemp(prefix='病族_')
    p = os.path.join(d, '病族账.md')
    io.open(p, 'w', encoding='utf-8').write(
        '| 族名 | 例数 | 管它的器 |\n|---|---|---|\n| 造局之病 | 2 | 无 |\n')
    老账 = 环.病族账
    环.病族账 = p
    try:
        # ★0924 改作不变式：沙盘之判只看「病族」那一半之语（L3 另跑真盘进化链棘轮——
        #   ⛔旧式以 ok 之真假判，真盘棘轮一红，④之二即假红、④／④之三／④之五即假绿：牙是借来的）。
        def _点(语, 名):
            return any(('无器管它' in x and 名 in x) for x in 语)
        ok3, 语3a = 环.L3()
        R.append(('④⛔造局·器之族例 2 而无器 → L3 当场红（且点其名）', ok3 is False and _点(语3a, '造局之病')))
        io.open(p, 'w', encoding='utf-8').write(
            '| 族名 | 例数 | 管它的器 |\n|---|---|---|\n| 造局之书 | 2 | 无·书之族 |\n')
        ok3b, 语3b = 环.L3()
        R.append(('④之二·书之族例 2 而无器 → ⛔不红（第三回方判）',
                  not _点(语3b, '造局之书') and any('✓L3 自进化' in x for x in 语3b)))
        io.open(p, 'w', encoding='utf-8').write(
            '| 族名 | 例数 | 管它的器 |\n|---|---|---|\n| 造局之书 | 3 | 无·书之族 |\n')
        ok3c, 语3c = 环.L3()
        R.append(('④之三·书之族例 3 而无器 → 红（⛔证④之二非一路放行）', ok3c is False and _点(语3c, '造局之书')))

        # ④之四·⛔族名後带括注者须读得出（0924 L3 头一版看不见四族，係此）
        io.open(p, 'w', encoding='utf-8').write(
            '| 族名 | 例数 | 管它的器 |\n|---|---|---|\n'
            '| **造局之病**（带一段括注） | 2 | ⛔**无器守它** |\n')
        族 = 环.读病族()
        R.append(('④之四·⛔族名後带括注者读得出（旧式看不见四族）',
                  len(族) == 1 and 族[0]['名'] == '造局之病'))
        ok3d, 语3d = 环.L3()
        R.append(('④之五·⛔「⛔**无器守它**」认作无器，例 2 即红（旧式只认以「无」开头者）',
                  ok3d is False and _点(语3d, '造局之病')))
    finally:
        环.病族账 = 老账
    # ⑤真盘 L3：今日病族账逐族有器
    ok3r, 语3 = 环.L3()
    R.append(('⑤真盘·L3：%s' % (语3[0][:50] if 语3 else ''), ok3r))
    import re as _re
    账行 = len([l for l in io.open(os.path.join(ROOT, '设定', '病族账.md'), encoding='utf-8')
               if _re.match(r'\|\s*\*\*', l)])
    R.append(('⑤之二·⛔L3 所读之族数＝账上之行数（%d）——**不许有看不见的族**' % 账行,
              len(环.读病族()) == 账行))

    # ⑥⛔L1 走闸不绕
    src = io.open(os.path.join(ROOT, '工具', '自进化环.py'), encoding='utf-8').read()
    L1码 = src.split('def L1')[1].split('def L2')[0]
    码行 = '\n'.join(l.split('#')[0] for l in L1码.split('\n')
                     if not l.lstrip().startswith('#'))
    R.append(('⑥⛔L1 之推走闸不绕（码行里无 --no-verify／ZM_SKIP_HOOK）',
              '--no-verify' not in 码行 and 'ZM_SKIP_HOOK' not in 码行))

    # ⑦接在 自走 头上
    走 = io.open(os.path.join(ROOT, '工具', '自走.py'), encoding='utf-8').read()
    R.append(('⑦已接在 自走.py 之头（L0／L1／L3）', "'自进化环'" in 走 and '_m6.L0' in 走))

    # ⑧总纲在
    R.append(('⑧总纲 设定/00_自进化机制总纲.md 在',
              os.path.exists(os.path.join(ROOT, '设定', '00_自进化机制总纲.md'))))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·自进化环 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
