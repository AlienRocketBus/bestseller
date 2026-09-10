# -*- coding: utf-8 -*-
"""负测·棘轮裁（2026-09-02·第292章第3轮所立）

★所测者二样，皆出於一处：**那道专为「裁棘轮回退」而立的器，自己是歪的。**
· **①方向**：其「历史最优」用 `min()`，不分方向；★而棘轮三类里 MIN 二目、MAX 二目、V01 四目，
  **八目里六目愈高愈好**——★★跑 `--棘轮 292 --项 嗅` 得「历史最优 2（出於 v01）」，
  **而 v01 正是最薄那一版**；★★★照它读，嗅 8 反倒该记功。
· **②举证**：292第2轮裁一处回退，其由是「所删那一拍係逐字抄290」——**而那句话是我说的，不是器说的**；
  ★其疑（292第2轮之一疑）：**闸一旦可以由我一句话推翻，它就不是闸了。**
  ★★其治不是让器替我免裁（回灌全书：此判据可免裁者 18/28＝64%，含拆章之版，**太松，那是挖空闸**），
  ★★★而是**举证**：器摆凭据，裁仍归人——**我那一句话由此变成可查之实。**
★★★★而一份在旧式下也全过的测就是陪跑（令§六③）——**故其要害在③⑦：以旧式回灌，须坏。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YJ = os.path.join(ROOT, '工具', '预检.py')


def _run(args):
    p = subprocess.run([sys.executable, YJ] + args, capture_output=True, text=True, cwd=ROOT)
    return (p.stdout or '') + (p.stderr or '')


def run():
    R = []
    src = io.open(YJ, encoding='utf-8').read()

    # ①器在册
    R.append(('①方向之判在册（_MIN 与 _取）', '_MIN = ' in src and '_取 = min if 项 in _MIN else max' in src))
    R.append(('②举证之函在册（_棘轮删证）', 'def _棘轮删证' in src))

    out = _run(['--棘轮', '292', '--项', '嗅'])

    # ③真红·新式於嗅得最优12（旧式得2）——故此改非陪跑
    R.append(('③方向·嗅（MAX）之最优今为 12（旧式 min 得 2）', '历史最优 12' in out))
    R.append(('④其向须印出来（不许只印一个数）', '愈高愈好（MAX／V01）' in out))

    # ⑤不误伤·MIN 之项仍取 min
    out2 = _run(['--棘轮', '292', '--项', '四字串三现'])
    R.append(('⑤不误伤·四字串三现（MIN）仍报「愈低愈好」', '愈低愈好（MIN）' in out2))
    import re as _r
    m = _r.search(r'历史最优 (\d+)', out2)
    vals = [int(x) for x in _r.findall(r'^  v\d+\s+(\d+)', out2, _r.M)]
    R.append(('⑥MIN之最优须等於逐版之最小值（今 %s）' % (m.group(1) if m else '?'),
              bool(m) and bool(vals) and int(m.group(1)) == min(vals)))

    # ⑦⑧⑨举证·**须以指定之二版验其函，不许靠「末二版恰好是哪两版」**
    #   ★★★★★2026-09-02·同日自改：**头一版把 292 之实（末二版恰为 v02→v03）写成了断言**，
    #     ★而下一轮一存版（v04→v05），末二版即变，三项当场败——**那是快照，不是不变之理**；
    #     ★★**而今晨我刚在 负测_冷轮否决记 里治过同一个病（⑤⑦⑩三项写死其笔数与对照号），这一份上又犯了一回**；
    #     ★★★故改断言为其所护之理本身：**给它一对确实删过「逐字见於他章之句」的版，它须摆得出来。**
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location('_yj', YJ)
    _yj = _iu.module_from_spec(_sp)
    _sp.loader.exec_module(_yj)
    _f = getattr(_yj, '_棘轮删证', None)
    _d = os.path.join(ROOT, '版本', '第292章')
    _档 = [os.path.join(_d, 'v02.md'), os.path.join(_d, 'v03.md')]
    _证 = _f(292, _档) if callable(_f) and all(os.path.exists(x) for x in _档) else []
    _句 = [x[0] for x in _证]
    R.append(('⑦举证·v02→v03 之间所删，摆得出「干了以后印子还在，比湿的时候浅」',
              any('干了以后印子还在' in x for x in _句)))
    R.append(('⑧举证·同上，且指出其见於何章（今 %s）' % (_证[0][1] if _证 else '无'),
              bool(_证) and all(isinstance(x[1], str) and x[1] for x in _证)))
    R.append(('⑨真红·未删任何见於他章之句者，其证为空（v04→v05）',
              _f(292, [os.path.join(_d, 'v04.md'), os.path.join(_d, 'v05.md')]) == []
              if callable(_f) and os.path.exists(os.path.join(_d, 'v05.md')) else False))
    R.append(('⑨之b·其限须印於源码（不答「该不该删」）', '不答「该不该删」' in src))

    # ⑩不免裁·全篇不许出现「免裁」二字（免裁即挖空闸）
    R.append(('⑩不免裁·裁仍归人（源码与其印皆无「免裁」之判）',
              '免裁' not in out and '回退免裁' not in src))

    # ⑪不误伤·所删而只见於本章他处者不入举证（本章自身不作他章）
    R.append(('⑪不误伤·本章之文不入举证（其扫跳过本章）',
              "if ('第%d章' % n) in os.path.basename(fp):" in src))

    # ⑫裁毕须写进轮记之令仍在（此器不许变成一个只会说「过」的器）
    R.append(('⑫「认／驳／留后轮，三者必居其一」之令仍在', '三者必居其一' in out))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·棘轮裁 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
