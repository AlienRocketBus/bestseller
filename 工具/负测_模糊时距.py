# -*- coding: utf-8 -*-
"""负测·模糊时距（2026-09-05·机制总审·硬闸探伤审第1条所立）

★所测者一句话：**预检认不认得着「不知过了多久」这一类失了尺的时距词。**
★★其红在哪一行：崩坏对照第121条初版自称「永禁词表（不知过了多久一类）」已机化——**而永禁词表里一个时间词也没有**；
   `grep -l 不知过了多久 正文/*.md` 得 7 章。★★★旧式（改前之 预检.py）之软项只印净重／段数／最长段／长段数，此词一个字不出。
★★★★故其要害在③：以旧式回灌（git HEAD 之 预检.py）须证其无此项。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load():
    spec = importlib.util.spec_from_file_location('yj', os.path.join(ROOT, '工具', '预检.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run():
    R = []
    m = _load()
    # ①认六形
    六 = ['不知过了多久', '不知多久', '过了很久', '许多天后', '转眼间', '几天后']
    got = [w for w in 六 if m.模糊时距('他坐着。%s，他站起来。' % w) == [w]]
    R.append(('①认六形（%d/6）' % len(got), len(got) == 6))
    # ②不认三形（半晌／良久／一晃七年）——认了即喊狼（全书半晌44章）
    R.append(('②不认 半晌／良久／一晃七年', m.模糊时距('他半晌没说话。良久，他一晃七年没回过家。') == []))
    # ③旧式回灌：改前之预检（钉在改前末一笔提交 10aaeb22，非 HEAD——HEAD 一提交即含新式，钉 HEAD 是自绿之陪跑）无此项
    try:
        old = subprocess.run(['git', 'show', '10aaeb22:工具/预检.py'], cwd=ROOT, capture_output=True, text=True).stdout
    except Exception:
        old = ''
    R.append(('③旧式回灌·改前（10aaeb22）之预检无「模糊时距」（%s）' % ('无' if old and '模糊时距' not in old else '有／取不着'), bool(old) and '模糊时距' not in old))
    # ④磁盘之实：第1章有之，第305章无之
    import glob
    c1 = [p for p in glob.glob(os.path.join(ROOT, '正文', '*第一章_*.md'))][0]
    c305 = [p for p in glob.glob(os.path.join(ROOT, '正文', '*第三百零五章_*.md'))][0]
    n1 = len(m.模糊时距(io.open(c1, encoding='utf-8').read()))
    n305 = len(m.模糊时距(io.open(c305, encoding='utf-8').read()))
    R.append(('④磁盘之实·第1章 %d 处（须≥1）、第305章 %d 处（须0）' % (n1, n305), n1 >= 1 and n305 == 0))
    # ⑤亮点段不计（只量白文）
    R.append(('⑤亮点段不计', m.模糊时距('正文。\n【本章亮点】\n不知过了多久') == []))
    # ⑥自陈在册：它认哪几样，本书同类共几样；不认之三样写明其由
    src = io.open(os.path.join(ROOT, '工具', '预检.py'), encoding='utf-8').read()
    R.append(('⑥自陈在册·认六形／不认半晌良久一晃及其由／报而不拦', '它认哪几样' in src and '不认「半晌」' in src and '报而不拦' in src))
    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·模糊时距 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
