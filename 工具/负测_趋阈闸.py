# -*- coding: utf-8 -*-
"""负测·趋阈闸（2026-09-02·291第7轮所立）

★所测者一句话：**一个数差一点就够到一条有名之限，而补几个字把它顶过去这一下，须留在账上。**
★★而一份在旧式下也全过的测，它就是陪跑（令§六③）——**故其要害在③⑤：以全书台账回灌，须逮得住那四章。**
★★★而本闸最险之处不在逮不逮得住，在**误伤**：一次真掘出四层而顺带跨了限的版，
   不该与一次「补两个字顶上线」同罪；故⑤专验二者之别。
"""
import glob
import importlib.util as _u
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _u.spec_from_file_location('_跑轮', os.path.join(ROOT, '工具', '跑轮.py'))
_m = _u.module_from_spec(_sp)
_sp.loader.exec_module(_m)


def _回灌():
    """★逐章逐版并列，数其红。"""
    hit, tot, chs = [], 0, 0
    for f in sorted(glob.glob(os.path.join(ROOT, '版本', '第*章', '_台账.json'))):
        try:
            d = json.load(io.open(f, encoding='utf-8'))
        except Exception:
            continue
        vs = d.get('版本') or []
        if len(vs) < 2:
            continue
        chs += 1
        for i in range(1, len(vs)):
            a, b = (vs[i - 1].get('soft') or {}), (vs[i].get('soft') or {})
            if not a or not b:
                continue
            tot += 1
            for h in _m.趋阈(a, b):
                hit.append((f.split(os.sep)[-2], vs[i].get('版'), h))
    return hit, tot, chs


def run():
    R = []
    src = io.open(os.path.join(ROOT, '工具', '跑轮.py'), encoding='utf-8').read()

    # ①器在
    R.append(('①器在·跑轮立有趋阈闸与其表', callable(getattr(_m, '趋阈', None))
              and hasattr(_m, 'THRESHOLDS')))

    # ②必跑·其调用在存版之路上，非另一条命令
    R.append(('②必跑·存版之路上调用趋阈（非另开命令）',
              '_qy = 趋阈(_prev, soft)' in src and 'raise_flag(n, \'趋阈闸' in src))

    # ③真红·275之实（3498→3500）须报，且判「落在线上」
    r275 = _m.趋阈({'净重': 3498}, {'净重': 3500})
    R.append(('③真红·275之实 3498→3500 报「落在线上」，余量0',
              len(r275) == 1 and r275[0]['落在线上'] and r275[0]['余量'] == 0))

    # ④未挖空·今日291之实（3895→3946，未跨4000）须放行
    R.append(('④未挖空·291今日 3895→3946 未跨限，零报',
              _m.趋阈({'净重': 3895}, {'净重': 3946}) == []))

    # ⑤未误伤·一次真掘（差得远而跨得阔）不该与「补两字顶上线」同罪
    #   ★★★★★2026-09-02·291第7轮改带之後，4,000 与 5,500 二线已废（转章带改 3,501—5,999），
    #     故此项之料由「289之3443→4070」改取仍在册之线（3,500）上一次阔跨：3,000→3,900。
    #   ★其差500而余量400，远逾四分之一——**须零报**。
    R.append(('⑤未误伤·3000→3900（差500而余量400）零报',
              _m.趋阈({'净重': 3000}, {'净重': 3900}) == []))

    # ⑥降不报·减法轮之净重下降不入此闸
    R.append(('⑥降不报·4070→3900 零报', _m.趋阈({'净重': 4070}, {'净重': 3900}) == []))

    # ⑦回灌·全书台账，其红率须非零且不成灾（0<red<8%）
    hit, tot, chs = _回灌()
    rate = 100.0 * len(hit) / max(tot, 1)
    R.append(('⑦回灌·全书%d章／版际%d次／红%d次＝%.2f%%（非陪跑，亦非拆书）'
              % (chs, tot, len(hit), rate), 0 < rate < 8.0))

    # ⑧回灌之要害·四章落在3500线上须逐章逮着
    onlin = set()
    for ch, v, h in hit:
        if h['落在线上'] and h['限'] == 3500:
            onlin.add(ch)
    want = {'第275章', '第276章', '第283章', '第284章'}
    R.append(('⑧回灌之要害·275/276/283/284 四章落在3500线上俱逮着（实逮：%s）'
              % '、'.join(sorted(onlin)), want <= onlin))

    # ⑨自证之口·须是「非凑数」四字，且其检在存版之路上
    R.append(('⑨自证之口·须写「非凑数」方许落盘', "'非凑数' not in (note or '')" in src))

    # ⑩其由落账·过闸之後其数与其由一并写进台账
    R.append(('⑩其由落账·台账记 趋阈 字段', "_entry['趋阈'] = _qy" in src))

    # ⑪表之全·须与令四今日之带逐线对齐（291第7轮改带之後）
    #   ★常章带 2,500—3,500｜转章带 3,501—5,999｜爆章 6,000起
    #   ★★故有名之线只三条：常章带下沿2,500、常章带上沿3,500、爆章下沿6,000；
    #     **旧之4,000与5,500已废，若它们还在表上，趋阈闸报的线名就是错的。**
    ts = set((k, T) for k, T, _ in _m.THRESHOLDS)
    R.append(('⑪表之全·净重2500/3500/6000 与 最长段120／长段数1 俱在，而4000/5500已废',
              {('净重', 2500), ('净重', 3500), ('净重', 6000),
               ('最长段', 120), ('长段数', 1)} <= ts
              and ('净重', 4000) not in ts and ('净重', 5500) not in ts))

    # ⑫落线之阈·「余量」量的是它落在限之上多少，非此前之差
    #   ★276之实 3495→3500：此前之差5，而**余量0**——它落在线上，判「落在线上」；
    #   ★★而 3400→3510：此前之差100、余量10，虽勉强而未落线，判「勉强跨过」。
    _a = _m.趋阈({'净重': 3495}, {'净重': 3500})[0]
    _b = _m.趋阈({'净重': 3400}, {'净重': 3510})[0]
    R.append(('⑫落线之阈·3495→3500 余量0判落线；3400→3510 余量10判勉强',
              _a['余量'] == 0 and _a['落在线上'] and
              _b['余量'] == 10 and not _b['落在线上']))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·趋阈闸 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
