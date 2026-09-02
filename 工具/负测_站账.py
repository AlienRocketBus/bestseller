# -*- coding: utf-8 -*-
"""负测·站账闸（2026-09-02·293封版之後立·作者令「一切服务於质量」之机化）

★所验之闸：`工具/站账.py`——**凡一站之章数及其三数而无对站之记者，报红。**
★★**其要害在③④**：**以真账回灌，收E3（71/30）与E4（22/23）须俱报红**——
   ★★★**一份在旧式（无对站之记）下也全过的测就是陪跑**（令§六③）。
★★★★**而另验一样，其位与前者同等要紧**：**此闸不许变成催字数的闸**（令§二）——
   **故⑦验其报文里无「须补至N字」「净重不足」之类语**。
"""
import io
import os
import sys
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _iu.spec_from_file_location('_zz', os.path.join(ROOT, '工具', '站账.py'))
_m = _iu.module_from_spec(_sp)
_sp.loader.exec_module(_m)

案 = []


def _t(名, 得, 期):
    案.append((名, 得 == 期, 得, 期))


def _移(名):
    """★把某站之对站之记暂移开，验闸复红；finally 必还原。"""
    p = os.path.join(ROOT, '设定', '站账_%s_对站.md' % 名)
    return p if os.path.exists(p) else ''


def 跑():
    rows, 判 = _m.账()

    # ①站表逐条须有其据（令§六④·表是报，档是场）
    _t('①站表逐条带其据', all(len(x) == 4 and x[3] for x in _m.站表), True)

    # ②今日之实：二站俱有对站之记 → 不报
    _t('②记已在·不报', 判, [])

    # ③★★★回灌·抽掉 E4 之对站之记，须复红（证其非陪跑）
    p4 = _移('E4巴蜀水下')
    o4 = io.open(p4, encoding='utf-8').read() if p4 else ''
    try:
        if p4:
            os.rename(p4, p4 + '.负测暂移')
        _r = _m.账()[1]
        # ★立闸当日此项即逮着一处：E4为22章而其三数23，`用>=约章` 不成立，
        #   遂抽掉其记而闸不出声——**闸差一格「近其数」**，当日补之。
        _t('③抽掉E4之对站即出声（22/23＝96%，走判一之b）',
           any('E4' in x for x in _r), True)
        _t('③之c 且其为⚠而非⛔（近其数者报而不拦）',
           any(x.startswith('⚠') and 'E4' in x for x in _r), True)
    finally:
        if p4 and os.path.exists(p4 + '.负测暂移'):
            os.rename(p4 + '.负测暂移', p4)
    _t('③之b E4之记已还原', bool(p4) and os.path.exists(p4), True)

    # ④★★★回灌·抽掉收E3之对站之记，须复红二条（及数＋逾倍）
    p3 = _移('收E3')
    try:
        if p3:
            os.rename(p3, p3 + '.负测暂移')
        _r = _m.账()[1]
        _t('④抽掉收E3之对站即复红二条（71/30·2.37倍）',
           len([x for x in _r if '收E3' in x]), 2)
    finally:
        if p3 and os.path.exists(p3 + '.负测暂移'):
            os.rename(p3 + '.负测暂移', p3)
    _t('④之b 收E3之记已还原', bool(p3) and os.path.exists(p3), True)

    # ⑤逾倍之销须见其实用之数（一份不带这个数的对站，多半是照模子填的）
    _t('⑤收E3之对站里见「71」', '71' in (io.open(
        os.path.join(ROOT, '设定', '站账_收E3_对站.md'), encoding='utf-8').read()), True)

    # ⑥末章以「正文在不在」为准，不以「版本目录在不在」为准
    #   ★其由：翻页八件套一办，下一章之目录即在盘上，而那一章尚未起草；
    #     以目录计，E4即虚长一章（22→23），恰好抵着其三数。
    _t('⑥末章不认空目录', _m._末章() == 293, True)

    # ⑦★★★★此闸不许变成催字数之闸（令§二）
    _src = io.open(os.path.join(ROOT, '工具', '站账.py'), encoding='utf-8').read()
    _t('⑦不催字数·报文无「须补至」「字数不足」之语',
       ('须补至' in _src) or ('字数不足' in _src) or ('净重不足' in _src), False)
    _t('⑦之b 且其源里明写「只作压章之据，不作添字之据」',
       '不作「添字」之据' in _src, True)

    # ⑧其自陈之限须在器上（令§六④·不许把绿读成「本站没事」）
    _t('⑧自陈其限·数不出「事摸完几件」', '数不出' in _src and '那一判是人下的' in _src, True)

    # ⑨未立三数之站不判章数（表里没有的站，不许它凭空判）
    _t('⑨表外之章不入任一站', _m.站表[-1][0] <= 293, True)

    print('\n════ 负测·站账闸 ════')
    过 = 0
    for 名, ok, 得, 期 in 案:
        print('  %s %s' % ('✓' if ok else '⛔', 名), '' if ok else '  得%r 期%r' % (得, 期))
        过 += ok
    print('  %d/%d %s' % (过, len(案), '全通' if 过 == len(案) else '⛔未过'))
    return 0 if 过 == len(案) else 1


if __name__ == '__main__':
    sys.exit(跑())
