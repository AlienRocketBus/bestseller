# -*- coding: utf-8 -*-
"""负测·约到期闸（2026-09-02·九席审读所逮之伤·立闸同日）

★所验之闸：`工具/约到期.py`——**一句写在正文里的约，到期那一章须在轮记／回执里回话。**
★★**其要害在③**：**以第291章拍139「要分出来得有第三天」回灌，须报欠**——
   ★★★**其到期在第293章（第一百零四天），而293全章：东头0｜担架0｜毡子0｜甜0｜馊0｜刘二0**；
   ★★★★**而十三轮＋封版之序＋五十八项全测＋看官五席，一处也没出声**——
   **故一份逮不着这一根的测，就是陪跑（令§六③）。**
★**而④另验一样，其位与前者同等要紧**：**此闸不许用「猜」来判兑没兑**——
   立闸当日我试过两回（取实词比字面），**中文不分词，切片切出「了闻／天一／我蹲」，碎片在任一章都撞得上**；
   ★★**故④验其源里没有那条路，且明写弃它之由**。
"""
import io
import os
import sys
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _iu.spec_from_file_location('_yd', os.path.join(ROOT, '工具', '约到期.py'))
_m = _iu.module_from_spec(_sp)
_sp.loader.exec_module(_m)
_SRC = io.open(os.path.join(ROOT, '工具', '约到期.py'), encoding='utf-8').read()

案 = []


def _t(名, 得, 期):
    案.append((名, 得 == 期, 得, 期))


def 跑():
    xs = _m.扫()
    ids = [x['号'] for x in xs]

    # ①器可跑，且找得着约
    _t('①找得着约（≥2处）', len(xs) >= 2, True)

    # ②按号去重（二式命中同一拍者只算一约）
    _t('②按号去重', len(ids) == len(set(ids)), True)

    # ③★★★回灌·291拍139那一根须在册，且判欠
    一 = [x for x in xs if x['号'] == '约-291.139']
    _t('③291拍139在册', len(一), 1)
    _t('③之b 其到期之窗含第293章', bool(一) and 293 in 一[0]['窗'], True)
    _t('③之c 判其欠（293之轮记／回执一处也没有它）', bool(一) and 一[0]['欠'], True)

    # ③之d★而其所以欠，须以正文复核：293里那几样一次也没出现
    b = _m._mb._白(293) or ''
    _t('③之d 293里 东头/担架/毡子/甜/馊/刘二 俱为0',
       sum(b.count(w) for w in ('东头', '担架', '毡子', '甜', '馊', '刘二')), 0)

    # ④★不许用「猜」判兑没兑——那条路已弃，其由须写在源里
    _t('④已弃「取实词比字面」之路', ('中文不分词' in _SRC) and ('故弃此路' in _SRC), True)
    _t('④之b 且不再有 中 这一键', "'中':" in _SRC, False)

    # ⑤认账即销（写一行「约-NNN」进轮记，闸即放行）
    lj = os.path.join(ROOT, '版本', '第293章', '_轮记.md')
    o = io.open(lj, encoding='utf-8').read()
    try:
        io.open(lj, 'a', encoding='utf-8').write('\n约-291.139·本章未兑：负测所写，验毕即除。\n')
        _t('⑤认账即销', any(x['号'] == '约-291.139' and not x['欠'] for x in _m.扫()), True)
    finally:
        io.open(lj, 'w', encoding='utf-8').write(o)
    _t('⑤之b 复原毕·仍判欠', any(x['号'] == '约-291.139' and x['欠'] for x in _m.扫()), True)

    # ⑥自陈其限须在器上（令§六④）
    _t('⑥自陈其限·三样认不着', ('没有数的约' in _SRC) and ('跨线之约' in _SRC), True)

    # ⑦日号推得准（291＝103日，293＝104日）
    _t('⑦日号', (_m._日号(291), _m._日号(293)), (103, 104))

    # ⑧「第N天」判窗不判点（291之两天已过，其第三天是次日）
    _t('⑧判窗不判点', '判一个窗' in _SRC, True)

    print('\n════ 负测·约到期闸 ════')
    过 = 0
    for 名, ok, 得, 期 in 案:
        print('  %s %s' % ('✓' if ok else '⛔', 名), '' if ok else '  得%r 期%r' % (得, 期))
        过 += ok
    print('  %d/%d %s' % (过, len(案), '全通' if 过 == len(案) else '⛔未过'))
    return 0 if 过 == len(案) else 1


if __name__ == '__main__':
    sys.exit(跑())
