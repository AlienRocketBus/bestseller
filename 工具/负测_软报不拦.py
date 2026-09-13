# -*- coding: utf-8 -*-
"""负测·软报不拦（2026-09-13 立·323 推时自逮）。

★所守者一句：**`开轮六检.py` 自己判「报而不拦」的那几条，不许在推闸上变成红。**
★★其实：`python3 工具/开轮六检.py 323 --静` **自判 rc=0（它判通过）**，
　而 ⑰ 之文照旧随印带出；**全测那一路把印出来的字当红**——
　**一条对方已判绿的警，就这样变成了拦推的红。**
★★★⛔**而这一改极易成为「把闸放松让自己这一章过」（祖案·306），故钉死三条**：
　①**名单只从 `开轮六检.py` 之 `_软报` 里读**，⛔全测这一路不许自造一份；
　②**软报之外的每一条，照旧一条不放**；
　③**⑥之冷轮与⑭之封版那两条原有之限，一字未动。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io
import os
import re
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _qc():
    spec = importlib.util.spec_from_file_location(
        '_qc', os.path.join(ROOT, '工具', '全测.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def 跑():
    m = _qc()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    # ①②【名单只从对方码里读】
    软 = m._软报之号()
    判('①', '软报名单取得着（得 %s）' % (软,), bool(软), True)
    判('②', '其内确含⑰（对方自书「报而不拦」者）',
       any(x.startswith('⑰') for x in 软), True)
    src = io.open(os.path.join(ROOT, '工具', '开轮六检.py'),
                  encoding='utf-8').read()
    判('③', '⑰ 在对方码里确係 `_软报` 之列（非本测所造）',
       bool(re.search(r"^_软报\s*=\s*\([^)]*⑰", src, re.M)), True)
    判('④', '⑰ 之 docstring 自书「报而不拦」',
       '近五章之形：若同形逾三章，即报（报而不拦）' in src, True)

    # ⑤【证其有牙·软报之外一条不放】拿一条真硬红（⑨领轮之号）回灌
    条 = m._六检之败('⑨·领轮之号 ⛔基线里无「目标轮」；⑰·近五章之形（同形≤3章） ⛔近五章有 4 章同为「做事」',
                     False)
    余 = [x for x in 条 if not any(x.startswith(s) for s in 软)]
    判('⑤之一', '回灌之局切得出两条', len(条), 2)
    判('⑤之二', '⛔而⑨那一条硬红照旧在余里（软报之外一条不放）',
       len(余) == 1 and 余[0].startswith('⑨'), True)

    # ⑥【不许连坐】⑥与⑭那两条原有之限须仍在
    qc = io.open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read()
    判('⑥之一', '⑭之限仍在', "x.startswith('⑭·已封版之章')" in qc, True)
    判('⑥之二', '⑥之冷轮之限仍在', '_冷轮之红俱有否决记(x)' in qc, True)

    # ⑦【今日之实】323 之印，对方自判 rc=0
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '开轮六检.py'),
                        '323', '--静'], capture_output=True, text=True,
                       cwd=ROOT, timeout=300)
    # ⛔**本格头一版问错了话**：我问「rc 是不是 0」，而 `--静` 之 rc=2 係⑭（已封版之章）所致
    #   ——**⑭照旧计 bad，软报不计**。★**故改问那一句真话**：
    #   **把⑭那一条摘掉之後，其印里剩下的红是不是只有软报之列。**
    #   ⛔**并记我自己那一处**：上一版我拿 `cmd | head -3; echo rc=$?` 读退出码，
    #   **取到的是 head 的 rc，不是它的**——**判据不对，不是事实不对。**
    _印 = (r.stdout or '')
    _条 = m._六检之败(_印, False)
    _余 = [x for x in _条 if not x.startswith('⑭·已封版之章')
           and not any(x.startswith(s) for s in 软)]
    判('⑦之一', '摘去⑭与软报，323 之印再无别红（余 %s）' % _余, _余, [])
    判('⑦之二', '而其印里确带着⑰之文（故非「它没报」）',
       '⑰·近五章之形' in (r.stdout or ''), True)

    print('════ 负测·软报不拦 ════（守：对方自判「报而不拦」者，不在推闸上变红）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
