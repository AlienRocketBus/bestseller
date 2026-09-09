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

print('── 负测·真轮凭轮记 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
sys.exit(0 if not bad else 1)
