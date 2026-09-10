# -*- coding: utf-8 -*-
"""负测·裁毕闸（2026-09-02·293第12轮立）

★所验之闸：`工具/跑轮.py::caibi_gate`——**凡轮记称「N对…逐对裁毕」，同节之内须数得出 N 条明细。**
★★其要害在③：**以293第9轮之原轮记回灌，须报红**（称21对，写8条）。
   ★★★一份在旧式下也全过的测就是陪跑（令§六③）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import sys
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _iu.spec_from_file_location('_pl', os.path.join(ROOT, '工具', '跑轮.py'))
_m = _iu.module_from_spec(_sp)
_sp.loader.exec_module(_m)
G = _m.caibi_gate

案 = []


def _t(名, 得, 期):
    案.append((名, 得 == 期, 得, 期))


def 跑():
    # ①称五对而写五条 → 不报
    _t('①足数不报', G('五对，逐对裁毕：\n· 拍1\n· 拍2\n· 拍3\n· 拍4\n· 拍5\n'), [])

    # ②称五对而写三条 → 报，且其差为2
    r = G('五对，逐对裁毕：\n· 拍1\n· 拍2\n· 拍3\n')
    _t('②少数即报', [(a, b) for a, b, _ in r], [(5, 3)])

    # ③★★★以293第9轮之原轮记回灌，须报红（此测之要害）
    raw = io.open(os.path.join(ROOT, '版本', '第293章', '_轮记.md'),
                  encoding='utf-8').read()
    if '## 第9轮' in raw:
        sec = raw.split('## 第9轮')[1].split('\n## 第10轮')[0]
        r9 = G(sec)
        _t('③293第9轮回灌须报红', bool(r9) and r9[0][0] == 21 and r9[0][1] < 21, True)
    else:
        _t('③293第9轮回灌须报红', 'SKIP·轮记无第9轮', True)

    # ④阿拉伯数字之称亦认
    _t('④阿拉伯数亦认', [(a, b) for a, b, _ in G('21处，逐处答毕：\n· 拍1\n')], [(21, 1)])

    # ⑤不给数者不管（「大半已裁」无数可数）
    _t('⑤无数者不管', G('大半已裁，余者从略。\n'), [])

    # ⑥明细在下一节者不算（本闸只看同节）
    _t('⑥越节不算', [(a, b) for a, b, _ in
                  G('三对，逐对裁毕：\n\n## 别节\n· 拍1\n· 拍2\n· 拍3\n')], [(3, 0)])

    # ⑦「逐一答毕」亦认（非只「逐对裁毕」）
    _t('⑦逐一答毕亦认', [(a, b) for a, b, _ in G('四句，逐一答毕：\n· 拍1\n')], [(4, 1)])

    # ⑧含拍号之行即算一条（不必以列点起手）
    _t('⑧含拍号即算', G('二处，逐处裁毕：\n改前拍63之文如此\n改后拍64之文如此\n'), [])

    # ⑨二十一之汉数须读得出
    _t('⑨汉数二十一', [a for a, _, _ in G('二十一对，逐对裁毕：\n· 拍1\n')], [21])

    # ⑩一节之内二称，二者各判
    r = G('三对，逐对裁毕：\n· 拍1\n\n## 二\n五处，逐处答毕：\n· 拍9\n· 拍8\n')
    _t('⑩一节二称各判', [(a, b) for a, b, _ in r], [(3, 1), (5, 2)])

    # ⑪★而它不许拦：caibi_gate 只返回单子，不 raise、不改文
    try:
        G('五对，逐对裁毕：\n')
        _t('⑪只报不拦', True, True)
    except Exception:
        _t('⑪只报不拦', False, True)

    # ⑫★★★【立闸当日即修】总数在前、抽样在後者，该数的是抽样那一个
    #   （其群：全书轮记「逐…毕」266处，空档内另有一数者45处，皆此形）
    _t('⑫取近不取远', [(a, b) for a, b, _ in
                  G('（全章4486对）随机抽12对**：**逐对看毕\n· 拍1\n')], [(12, 1)])

    # ⑬★而本轮（293第12轮）自身之轮记须不报——初版於此误报「称161，少137」
    if '## 第12轮' in raw:
        _t('⑬293第12轮不误报', G(raw.split('## 第12轮')[1]), [])
    else:
        _t('⑬293第12轮不误报', 'SKIP·轮记无第12轮', True)

    # ⑭初版之误形须验得出：「161句两两比…21对，逐对裁毕」须取21，不取161
    _t('⑭两数之句取後者', [a for a, _, _ in
                  G('全章161句两两比，近似≥0.60者21对，逐对裁毕\n· 拍1\n')], [21])

    print('\n════ 负测·裁毕闸 ════')
    过 = 0
    for 名, ok, 得, 期 in 案:
        print('  %s %s' % ('✓' if ok else '⛔', 名), '' if ok else '  得%r 期%r' % (得, 期))
        过 += ok
    print('  %d/%d %s' % (过, len(案), '全通' if 过 == len(案) else '⛔未过'))
    return 0 if 过 == len(案) else 1


if __name__ == '__main__':
    sys.exit(跑())
