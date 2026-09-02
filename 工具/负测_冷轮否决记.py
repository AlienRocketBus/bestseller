# -*- coding: utf-8 -*-
"""负测·冷轮否决记（2026-09-02·290封版当日立）

★所测者一句话：**逼我写的那六个字，不许同时把账销了。**
★★而一份在旧式下也全过的测，它就是陪跑（令§六③）——**故本测之要害在③④⑤：以旧式回灌，须坏。**
"""
import glob
import io
import os
import re
import sys
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _u.spec_from_file_location('_六检', os.path.join(ROOT, '工具', '开轮六检.py'))
_m6 = _u.module_from_spec(_sp)
_sp.loader.exec_module(_m6)

RC = os.path.join(ROOT, '设定')


def _rcs():
    out = []
    for fp in glob.glob(os.path.join(RC, '回执_*.md')):
        try:
            out.append(io.open(fp, encoding='utf-8').read())
        except OSError:
            pass
    return out


def _old(n, rcs):
    """旧式：回执里有那六个字即算已执。"""
    return any('%d章冷眼轮' % n in t for t in rcs)


def run():
    rcs = _rcs()
    R = []

    # ①器在
    R.append(('①器在·_cold_done 可调', callable(getattr(_m6, '_cold_done', None))))

    # ②正测：一笔真办过的（回执有六字、无否决记）须判已执
    R.append(('②正测·COLD-286（286之轮於288办毕）判已执', _m6._cold_done(286) is True))

    # ③真红：今日之实（290之回执明写 COLD-288·本章未执）须判待执
    R.append(('③真红·COLD-288 判待执（290回执有六字而有否决记）', _m6._cold_done(288) is False))

    # ④回灌·旧式须坏：同一笔，旧式判已执
    R.append(('④回灌·旧式於 COLD-288 判已执（故此闸非陪跑）', _old(288, rcs) is True))

    # ⑤回灌·全书 1—290 逐笔并列，二式相异者须**只此一笔**
    diff = [n for n in range(1, 291) if _old(n, rcs) != _m6._cold_done(n)]
    R.append(('⑤回灌·全书二式相异者只 COLD-288 一笔（非拆书）', diff == [288]))

    # ⑥不许挖空：一笔既无六字亦无否决记者，照旧判待执
    R.append(('⑥未挖空·无凭无据者判待执', _m6._cold_done(999999) is False))

    # ⑦否决记之式须严：近似之句不算否决（不许拿「未执」二字到处误伤）
    hit = [n for n in range(1, 291)
           if any(('COLD-%d·本章未执' % n) in t for t in rcs)]
    R.append(('⑦式严·全书带否决记者只 1 笔', len(hit) == 1 and hit == [288]))

    # ⑧否决在先：一份回执既有六字又有否决记，以否决为准（288即此形）
    both = any(('288章冷眼轮' in t) and ('COLD-288·本章未执' in t) for t in rcs)
    R.append(('⑧序·同一回执六字与否决记并存，判待执', both and _m6._cold_done(288) is False))

    # ⑨一坐与六检同判（二器不许各记各的）
    _sp2 = _u.spec_from_file_location('_一坐', os.path.join(ROOT, '工具', '一坐.py'))
    ok = True
    try:
        src = io.open(os.path.join(ROOT, '工具', '一坐.py'), encoding='utf-8').read()
        ok = '_cold_done' in src
    except OSError:
        ok = False
    R.append(('⑨同判·一坐仍走六检之 _cold_done', ok))

    # ⑩令§十①未被架空：六字仍是签核之凭（无六字者不因新式转绿）
    R.append(('⑩令§十①仍在·无六字者仍判待执', _m6._cold_done(289) == _old(289, rcs)))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·冷轮否决记 %d/%d %s' % (len(R) - len(bad), len(R),
                                   '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
