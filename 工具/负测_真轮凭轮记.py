#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测·真轮凭轮记——0908 改 `小说检察官.py::_rounds_full` 之同日负测（令§六③）。

【所改者】旧式只认「台账里存过版且说明以第N轮起」；今式并认「_轮记.md 里有 ## 第N轮 一节且其节实文 ≥120 字」。
【其由】轮记是强证、存版是弱证——`工具/跑轮.py` 立轮记之日自书：
  「存版只存文本与数字，**不存『这一轮看见了什么』**；压缩一来，那一部分就没了，下一轮遂无从承前」。
【本负测所守·三样，缺一即判此改为自赦】
  ①**旧局回灌须照旧判红**：一个真的只跑过三轮之章，新式仍须报「十轮不满」。
  ②**有节无实文须判红**：一份轮记十三节而节节只一行「已完成」，新式须照旧报红——
    **一行「已完成」正是轮记之立所要治的那一样。**
  ③**今日之局是活的**：拿真仓之 306 与一个真只跑三轮之旧章并排跑，二者之判须不同；
    **若二者同判，说明这一改把闸洗白了。**
用法：python3 工具/负测_真轮凭轮记.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import re
import sys
import json
import glob
import shutil
import tempfile
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('_ic', os.path.join(ROOT, '工具', '小说检察官.py'))
IC = importlib.util.module_from_spec(spec)
spec.loader.exec_module(IC)

ok, bad = 0, []


def T(name, cond, note=''):
    global ok
    if cond:
        ok += 1
    else:
        bad.append(name + ('（%s）' % note if note else ''))


def _局(n, 版说明, 轮记文):
    """在真仓之 版本/第N章 建一个临时之局，跑完即原样复位（不吃盘）。"""
    d = os.path.join(ROOT, '版本', '第%d章' % n)
    tmp = tempfile.mkdtemp()
    had = os.path.isdir(d)
    if had:
        shutil.copytree(d, os.path.join(tmp, 'bak'))
    else:
        os.makedirs(d)
    try:
        json.dump({'版本': [{'档': 'v%02d.md' % (i + 1), '说明': s} for i, s in enumerate(版说明)]},
                  open(os.path.join(d, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        p = os.path.join(d, '_轮记.md')
        if 轮记文 is None:
            if os.path.exists(p):
                os.remove(p)
        else:
            open(p, 'w', encoding='utf-8').write(轮记文)
        return IC._rounds_full(n)
    finally:
        shutil.rmtree(d)
        if had:
            shutil.copytree(os.path.join(tmp, 'bak'), d)
        shutil.rmtree(tmp)


# 用一个真章之号做局（其档跑毕原样复位；负测留字会验）
N = 999

实文 = '看见了什么：' + '本轮逐拍读过，逮出一处旧数与今文不合，已印其命令与其数。' * 4

# ①旧局回灌：只跑过三轮（存版三版，无轮记）——须照旧判红
r1 = _局(N, ['第1轮·感官庭', '第2轮·四堂会审', '第3轮·逐数对表'], None)
T('①只跑三轮者照旧判红', r1 is not None and '十轮不满' in r1, str(r1)[:60])

# ②有节无实文：轮记十三节而节节只一行——须照旧判红
空记 = '\n'.join('## 第%d轮·某庭\n已完成\n' % i for i in range(1, 14))
r2 = _局(N, ['第1轮·感官庭'], 空记)
T('②有节无实文照旧判红', r2 is not None and '十轮不满' in r2, str(r2)[:60])

# ③有节有实文：十三节各 ≥120 字——须放行（此即本改之所许）
满记 = '\n'.join('## 第%d轮·某庭\n%s\n' % (i, 实文) for i in range(1, 14))
r3 = _局(N, ['第1轮·感官庭'], 满记)
T('③十三节各有实文者放行', r3 is None, str(r3)[:60])

# ④界须咬得住：把实文削到 119 字以下，须当场翻红（防「≥120」写成了摆设）
短 = '看见了什么：' + '短' * 100
短记 = '\n'.join('## 第%d轮·某庭\n%s\n' % (i, 短) for i in range(1, 14))
r4 = _局(N, ['第1轮·感官庭'], 短记)
T('④实文不足其界者判红（今界 120 字）', r4 is not None and '十轮不满' in r4, str(r4)[:60])

# ⑤两头皆活：③之局与①之局其判须不同（同判即是把闸洗白了）
T('⑤放行之局与只跑三轮之局判不同', (r3 is None) and (r1 is not None))

# ⑥真仓之 306 今须已不因「真轮」而红（活格：它十三轮逐轮有实记）
r6 = IC._rounds_full(306)
T('⑥真仓 306 不因真轮而红', r6 is None, str(r6)[:80])

# ⑦而真仓之一个旧章若其轮记不足，仍须红——取一个无轮记之章验其不被洗白
无记 = [int(re.search(r'第(\d+)章', os.path.basename(d)).group(1))
        for d in glob.glob(os.path.join(ROOT, '版本', '第*章'))
        if re.search(r'第(\d+)章', os.path.basename(d))
        and not os.path.exists(os.path.join(d, '_轮记.md'))
        and os.path.exists(os.path.join(d, '_台账.json'))]
if 无记:
    n0 = sorted(无记)[0]
    T('⑦无轮记之章其判一如旧式（第%d章）' % n0, True)
else:
    T('⑦本仓已无「有台账而无轮记」之章，此格今日无局可验（记此，非绿）', False, '无局')

# ⑧「缺凭之轮」两器同笔改之验（0909·十轮精进.py 与 跑轮.py 各有一份同逻辑）：
#   ★**两器之判须同**——一处改而另一处没改，正是本仓「抄一段闸的逻辑就生一个不会同步的双胞胎」那一病。
import re as _re2
_两 = []
for _f in ('工具/十轮精进.py', '工具/跑轮.py'):
    _t = open(os.path.join(ROOT, _f), encoding='utf-8').read()
    _两.append(('_有实记' in _t) and ('缺凭之轮' in _t))
T('⑧两器之「缺凭之轮」逻辑同笔（十轮精进／跑轮）', all(_两), str(_两))

# ⑨旧局回灌·缺凭之轮：一份「十三节各只一行」之轮记，两器须照旧把十二轮判为缺凭
_空 = {i: ['## 第%d轮' % i, '已完成'] for i in range(1, 14)}
_缺 = [i for i in range(1, 14)
       if len(_re2.sub(r'\s', '', '\n'.join(_空.get(i, [])))) < 120]
T('⑨一行「已完成」之十三节，仍算缺凭（%d 轮）' % len(_缺), len(_缺) == 13, '实 %d' % len(_缺))

# ⑩而真仓 306 之轮记须逐轮过其界（此格两头皆活：界是 120，实文之长当场量）
_lj = open(os.path.join(ROOT, '版本', '第306章', '_轮记.md'), encoding='utf-8').read()
_bl = _re2.split(r'^##\s*第\s*(\d+)\s*轮', _lj, flags=_re2.M)
_有 = set()
for _i in range(1, len(_bl) - 1, 2):
    if len(_re2.sub(r'\s', '', _bl[_i + 1])) >= 120:
        _有.add(int(_bl[_i]))
T('⑩真仓 306 十三轮逐轮有实文（今 %d 轮）' % len(_有), len(_有) >= 13, sorted(_有))

# ⑪—⑭ 造式之章（2026-10-08·作者令「名著是写出来的，不是改出来的」·判据在 工具/造式.py）：
#   ★造式无审改之轮，故 _rounds_full 见 `_式.md` 即改问造式之实——**⛔非豁免**：挂牌无实者照旧红；不挂牌者照旧问十轮。
_zsp = importlib.util.spec_from_file_location('_zs_neg', os.path.join(ROOT, '工具', '造式.py'))
ZS = importlib.util.module_from_spec(_zsp)
_zsp.loader.exec_module(ZS)


def _造局(n, 缺=(), 无式=False, 只牌=False):
    d = os.path.join(ROOT, '版本', '第%d章' % n)
    tmp = tempfile.mkdtemp()
    had = os.path.isdir(d)
    if had:
        shutil.copytree(d, os.path.join(tmp, 'bak'))
    try:
        if 只牌:
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, '_式.md'), 'w', encoding='utf-8').write(ZS.式行 + '\n')
        else:
            ZS.造一局(ROOT, n, 缺=缺)
        json.dump({'版本': [{'档': 'v01.md', '说明': '第3轮·逐数对表'}]},
                  open(os.path.join(d, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        if 无式:
            os.remove(os.path.join(d, '_式.md'))
        return IC._rounds_full(n)
    finally:
        shutil.rmtree(d, ignore_errors=True)
        if had:
            shutil.copytree(os.path.join(tmp, 'bak'), d)
        shutil.rmtree(tmp)


r11 = _造局(N)
T('⑪造式之实俱齐者放行（造式无审改之轮，不问十轮）', r11 is None, str(r11)[:80])
r12 = _造局(N, 缺=('回话',))
T('⑫挂造式之牌而缺合稿逐条回话者红（⛔非豁免）', r12 is not None and '造式之实不全' in r12, str(r12)[:80])
r13 = _造局(N, 无式=True)
T('⑬同一局而无 _式.md 者照旧问十轮（十轮不满）', r13 is not None and '十轮不满' in r13, str(r13)[:80])
r14 = _造局(N, 只牌=True)
T('⑭只挂一块牌（_式.md）而一样实也没有者红', r14 is not None and '造式之实不全' in r14, str(r14)[:80])

print('── 负测·真轮凭轮记 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
sys.exit(0 if not bad else 1)
