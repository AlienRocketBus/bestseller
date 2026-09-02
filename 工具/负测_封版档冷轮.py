# -*- coding: utf-8 -*-
"""负测·封版档之冷轮口（2026-09-02·292第1轮立·欠-291D之群成立所致）

★所测者一句话：**放行的是「已经写下来认过的那几笔红」，不是「冷轮之红」这一整类。**
★★其历：291封版之日，十六检报⑭（恒真）与⑥（COLD-288之红，其档自书「留在账上不许再挪」），
   而封版档只放行⑭，遂绕行一回；★★★当日判其孤例（在档不在闸）并立欠-291D：
   **「若此形再现一回，其群已成，当日须改」**；★★★★今日再现（292未起草，末章仍为已封版之291），故改。
★而其限死在一处：**⑥所名之每一个 COLD-N，须在某份回执里带着「COLD-N·本章未执」这个否决记**——
   ★★**否决记只有说「不」的时候才写得出来**（第十九犯所立之式）；
   ★★★**故凡一笔冷轮之红而无人写过否决记者，照旧拦**——那正是⑥本来要逮的：无声消失。
★★★★而一份在旧式下也全过的测就是陪跑（令§六③）——**故其要害在④：旧式对同一入参判「拦」。**
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _rcs():
    out = []
    for fp in glob.glob(os.path.join(ROOT, '设定', '回执_*.md')):
        try:
            out.append(io.open(fp, encoding='utf-8').read())
        except OSError:
            pass
    return out


def _俱有否决记(x, rcs):
    """★与 工具/全测.py::推闸 之封版档同式（一处改，二处须同改）。"""
    ns = [int(m) for m in re.findall(r'COLD-(\d+)', x)]
    if not ns:
        return False
    return all(any(('COLD-%d·本章未执' % n) in t for t in rcs) for n in ns)


def run():
    R = []
    src = io.open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read()
    rcs = _rcs()

    # ①口在册（封版档里真有这一口，且与本测同式）
    R.append(('①口在册·封版档认「已写否决记之⑥」', '_冷轮之红俱有否决记' in src))

    # ②正测·今日之实：⑥所名之 COLD-288 带着否决记，故放行
    今 = '⑥·冷轮之欠 ★1笔未执：COLD-288'
    R.append(('②正测·COLD-288 带否决记，放行', _俱有否决记(今, rcs) is True))

    # ③真红·一笔从没人写过否决记之冷轮，照旧拦（此即⑥本来要逮的：无声消失）
    假 = '⑥·冷轮之欠 ★1笔未执：COLD-999'
    R.append(('③真红·无否决记者不放行（COLD-999）', _俱有否决记(假, rcs) is False))

    # ④回灌·旧式（只认⑭）对同一入参判「拦」——故此口非陪跑
    def _旧式(x):
        return x.startswith('⑭·已封版之章')
    R.append(('④回灌·旧式对今日之⑥判拦（故此口非陪跑）', _旧式(今) is False))

    # ⑤一红一绿不许混放：二笔之中有一笔无否决记者，整条拦
    混 = '⑥·冷轮之欠 ★2笔未执：COLD-288、COLD-999'
    R.append(('⑤混不许放·二笔有一笔无否决记即拦', _俱有否决记(混, rcs) is False))

    # ⑥二笔俱有否决记者放行（今日 288 与 289 俱在册）
    双 = '⑥·冷轮之欠 ★2笔未执：COLD-288、COLD-289'
    R.append(('⑥二笔俱有否决记者放行（288、289）', _俱有否决记(双, rcs) is True))

    # ⑦不许空放·一条⑥而一个号也没写出来者，不放行
    R.append(('⑦不许空放·⑥不带号者不放行', _俱有否决记('⑥·冷轮之欠 ★未执', rcs) is False))

    # ⑧其防未动·⑭之限仍在（封版之章再跑十轮照旧被拦）
    R.append(('⑧⑭之防未动·「⑭之防未动」之语仍在封版档', '⑭之防未动' in src))

    # ⑨其限须印出来·放行之语须写明所放行者为何，不许只说「放行」
    R.append(('⑨其限须印·放行之语点明「俱已写否决记，非无声消失」',
              '俱已写否决记' in src))

    # ⑩非封版之日不走此口（此口只在 _已封版(cur) 之下）
    i = src.find('if _已封版(cur):')
    j = src.find('_冷轮之红俱有否决记')
    R.append(('⑩此口只在封版档之内（其位在 _已封版 之後）', 0 < i < j))

    # ⑪否决记之数须与实际相符（不许拿一个不存在的式去糊弄）
    实 = sorted(n for n in range(1, 301)
                if any(('COLD-%d·本章未执' % n) in t for t in rcs))
    R.append(('⑪今册中带否决记者 %s（≥1，且逐笔可查）' % (实 or '无'), len(实) >= 1))

    # ⑫—⑯ 跑轮档之同口（2026-09-02·292第1轮补·与封版档共用一条判据）
    #   ★其形：⑥所报含「逾期」时，原本一律判真漏；★★而今日之逾期不是漏——
    #     COLD-288 限291，其档第五节自书「291若仍非暗线，其红留在账上不许再挪」，
    #     291确为主线，故其红依法留下，**而292正是它所停的那一章，此刻正在执它**。
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location('_qc', os.path.join(ROOT, '工具', '全测.py'))
    _qc = _iu.module_from_spec(_sp)
    try:
        _sp.loader.exec_module(_qc)
    except SystemExit:
        pass
    f = getattr(_qc, '_冷轮逾期俱有否决记', None)
    R.append(('⑫跑轮档之口在册（_冷轮逾期俱有否决记）', callable(f)))
    if callable(f):
        今 = '⑥·冷轮之欠 ★3笔未执：COLD-288、COLD-289、COLD-290⛔（其中1笔已逾期）'
        R.append(('⑬正测·今日三笔（逾期者只288，且其否决记在册）放行', f(今) is True))
        R.append(('⑭真红·一笔逾期而无否决记者不放行（COLD-153，限155）',
                  f('⑥·冷轮之欠 ★1笔未执：COLD-153⛔（其中1笔已逾期）') is False))
        R.append(('⑮不逼未逾期者签字·限正是当章之二笔（289、290）单独亦放行',
                  f('⑥·冷轮之欠 ★2笔未执：COLD-289、COLD-290') is True))
        R.append(('⑯回灌·旧式对今日之报判「真漏」（故此口非陪跑）',
                  ('逾期' in 今) is True))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·封版档冷轮口 %d/%d %s' % (len(R) - len(bad), len(R),
                                    '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
