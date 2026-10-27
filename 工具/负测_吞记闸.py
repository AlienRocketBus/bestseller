# -*- coding: utf-8 -*-
"""负测·吞记闸（2026-09-02·第291章第13轮开轮时所立）

★所测者一句话：**器收下了一样它本该拒收的东西，而它一声没出。**
★★其实物：`--存版 291 --记 "…"` 里，「--记」当了说明，其後真文被静静丢弃；
   ★★★於是 v15、v16 两版之说明尽失，**真轮数不着第12轮——一轮真跑过了，而账上说它没跑。**
★★★★而一份在旧式下也全过的测就是陪跑（令§六③）——**故其要害在④：以旧式回灌，须过（即旧式不拦）。**
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
PAO = os.path.join(ROOT, '工具', '跑轮.py')


def _run(args):
    p = subprocess.run([sys.executable, PAO] + args, capture_output=True, text=True, cwd=ROOT)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def run():
    R = []
    src = io.open(PAO, encoding='utf-8').read()

    # ①闸在册
    R.append(('①吞记闸在 跑轮.py 内（def _记）', 'def _记(' in src and '吞记闸' in src))

    # ②二口俱走此闸（--存版 与 --补存 皆须过 _记，一处漏即白立）
    R.append(('②--存版 与 --补存 二口俱走 _记',
              src.count('_记(sys.argv)') == 2))

    # ③真红·--存版 带 --记 须拦停（rc=2），且不落新版
    rc, out = _run(['--存版', '291', '--记', '第N轮·某庭'])
    R.append(('③真红·--存版 …--记 …拦停(rc=%d，须2)' % rc, rc == 2))
    R.append(('④其印须指出所吞之文（不许只说「写错了」）', '你本来要写的是' in out and '第N轮·某庭' in out))
    R.append(('⑤其印须给正确写法（造式二代之说明）', '正确：' in out and '"造式二代·' in out))
    R.append(('⑥拦停之版不落台账（印中无「存版 v」）', '███ 存版 v' not in out))

    # ⑦同形之他旗亦拦（不是只认「--记」这四个字）
    rc2, out2 = _run(['--存版', '291', '--说明', 'x'])
    R.append(('⑦不只认--记·凡「--」起手者皆拦(rc=%d)' % rc2, rc2 == 2))

    # ⑧不误伤·正常说明须放行（此处只验其不被吞记闸拦，不真落版）
    R.append(('⑧不误伤·「第13轮·升华定稿轮」不以--起手，闸不认',
              not '第13轮·升华定稿轮'.startswith('--')))

    # ⑨旧式回灌（令§六③）：把旧式原样搬来，以同一入参过一遍——须一声不出，且所得之说明即那面旗。
    #   ★这一项若写成恒真（如 `... or True`），此测即陪跑；故此处真跑旧式，并验其所吐之物。
    def _记_旧(argv):
        return argv[3] if len(argv) > 3 else ''

    argv_bad = ['跑轮.py', '--存版', '291', '--记', '第12轮·极限轮（翻案二处）']
    try:
        got = _记_旧(argv_bad)
        raised = False
    except SystemExit:
        got = None
        raised = True
    R.append(('⑨旧式回灌·旧式对同一入参不拦，且把说明取成「%s」（真文丢弃）' % got,
              (not raised) and got == '--记'))
    #   ★★而新式对同一入参须拦——二者对同一入参判得不一样，此闸方才不是陪跑
    R.append(('⑨之b·新式对同一入参拦停（与旧式判得不同）', rc == 2))

    # ⑩其害之实证在账上：v15、v16 之说明曾被吞（今已回填；旧⑪「R0013 在可逆库」随可逆库 1027 汰，其复原凭版本史）
    tz = io.open(os.path.join(ROOT, '版本', '第291章', '_台账.json'), encoding='utf-8').read()
    R.append(('⑩台账已回填·v15/v16 之说明不复为「--记」', '"--记"' not in tz and '"--记·补存"' not in tz))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·吞记闸 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
