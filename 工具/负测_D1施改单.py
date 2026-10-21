#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测_D1施改单（★1021·W58 环2 立）——`工具/D1施.py --改单` 之负测。零 token；只在临时之根里跑，⛔碰本仓一字。

为何立：W58 环4 之 4b（亮点撰）、4c（设定层义判）、4d（待判单、器物册）诸席之改，一律以「单」记之、由器照单施；
  器若松（多见而猜一处、不见而静过、二跑再改一回、插行删行），模型之改就会「抄错一字、落错一行」而无人逮。
  故逐格造坏单，器须红且一字不写；好单须恰施、二跑零改、行数不变。

格（≥8，照 W58 环2 Fix 席之令）：恰一见、多见红、不见红、行移之容、无根拒、主树无落拒、二跑零改、行数⛔变；
  另补：窗内多见红、两可红、--验 只核不写、单之式（据、由、出根、重条、空改、新空）、新含原（史料加注）二跑零改、
  一条红则同单好条亦不写、CRLF 与尾换行照留、叠改（同单两条互吞）红、CLI 之接。

用法：python3 工具/负测_D1施改单.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

此 = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location('D1施_负测', os.path.join(此, 'D1施.py'))
D1 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(D1)

ok = 共 = 0


def T(名, 真, 注=''):
    global ok, 共
    共 += 1
    ok += bool(真)
    print('  %s %s%s' % ('✓' if 真 else '✗', 名, '' if 真 else ('　' + str(注)[:300])))


章名 = os.path.join('正文', '镇冢秘术_第一百一十一章_测.md')
设名 = os.path.join('设定', '全书记忆', '第111章.md')
章文 = '\n'.join(['第一百一十一章　测', '', '他四十八年前来过。', '', '【本章亮点】', '',
                 '★送信：二十七年前那一趟，他送过信。', '★又：那人二十七年没回来。']) + '\n'
设文 = '\n'.join(['# 第111章', '', '- L3：老头二十七年前来过（D1 施前之数）。', '- 甲', '- 乙',
                 '- 丙：二十七年。', '- 丁', '- 戊', '- 己：二十七年前的事，二十七年後才说。', '- 庚']) + '\n'


def 造根():
    r = tempfile.mkdtemp(prefix='负测D1改单_')
    os.makedirs(os.path.join(r, '正文'))
    os.makedirs(os.path.join(r, '设定', '全书记忆'))
    open(os.path.join(r, 章名), 'w', encoding='utf-8').write(章文)
    open(os.path.join(r, 设名), 'w', encoding='utf-8').write(设文)
    return r


def 快照(r):
    出 = {}
    for d, _, fs in os.walk(r):
        for f in fs:
            p = os.path.join(d, f)
            if '单' in os.path.relpath(p, r).split(os.sep)[0]:
                continue
            出[os.path.relpath(p, r)] = open(p, 'rb').read()
    return 出


def 跑(r, 条们, *加, 主=None):
    """→ (rc, 印)；单写在根外之临时档"""
    fd, p = tempfile.mkstemp(suffix='.json', prefix='负测D1改单单_')
    os.close(fd)
    open(p, 'w', encoding='utf-8').write(json.dumps(条们, ensure_ascii=False))
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            a = ['--改单', p] + (['--根', r] if r else []) + list(加)
            rc = D1.跑改单(r, a, 主=主 or D1.主树)
    finally:
        os.remove(p)
    return rc, buf.getvalue()


def 条(档=设名, 行=3, 原='二十七年前', 新='四十八年前', 据='4c', 由='测'):
    return dict(档=档.replace(os.sep, '/'), 行=行, 原=原, 新=新, 据=据, 由=由)


def 读(r, rel):
    return open(os.path.join(r, rel), encoding='utf-8', newline='').read()


根们 = []


def 新根():
    r = 造根()
    根们.append(r)
    return r


try:
    # ① 恰一见
    r = 新根()
    rc, 印 = 跑(r, [条()])
    t = 读(r, 设名)
    T('①恰一见：该行原一见 → 施（rc 0、印改 1 条、他行他字不动、行数同）',
      rc == 0 and '改 1 条' in 印 and t == 设文.replace('老头二十七年前来过', '老头四十八年前来过') and t.count('\n') == 设文.count('\n'), (rc, 印))

    # ② 多见红：该行两见；同单之好条亦⛔写
    r = 新根()
    前 = 快照(r)
    rc, 印 = 跑(r, [条(), 条(行=9, 原='二十七年', 新='四十八年')])
    T('②多见红：该行原两见 → 红、全单一字不写（同单之好条亦不写）', rc == 1 and '多见' in 印 and 快照(r) == 前, (rc, 印))

    # ③ 不见红
    r = 新根()
    前 = 快照(r)
    rc, 印 = 跑(r, [条(原='二十八年前')])
    T('③不见红：该行与 ±3 内俱无原、亦无新 → 红、一字不写', rc == 1 and '不见' in 印 and 快照(r) == 前, (rc, 印))

    # ④ 行移之容
    r = 新根()
    rc, 印 = 跑(r, [条(行=1, 原='老头二十七年前', 新='老头四十八年前')])       # 实在 3 行：+2
    t = 读(r, 设名)
    r2 = 新根()
    前2 = 快照(r2)
    rc2, 印2 = 跑(r2, [条(行=10, 原='老头二十七年前', 新='老头四十八年前')])    # 实在 3 行：-7（逾 ±3）
    T('④行移之容：原在 行+2 → 移施（黄）；逾 ±3 → 不见红、一字不写',
      rc == 0 and '移 → 3 行' in 印 and '老头四十八年前来过' in t and rc2 == 1 and '不见' in 印2 and 快照(r2) == 前2, (印, 印2))

    # ⑤ 无根拒
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = D1.main(['--改单', '/nonexistent/单.json'])
        rc_b = D1.跑改单(None, ['--改单', '/nonexistent/单.json'])
    T('⑤无根拒：--改单 无 --根 → rc 2', rc == 2 and rc_b == 2 and '无 --根 即拒' in buf.getvalue(), buf.getvalue())

    # ⑥ 主树无落拒（以临时之根作「主树」）；--落 方施；--验 只核
    r = 新根()
    前 = 快照(r)
    rc, 印 = 跑(r, [条()], 主=r)
    rc验, 印验 = 跑(r, [条()], '--验', 主=r)
    后 = 快照(r)
    rc落, 印落 = 跑(r, [条()], '--落', 主=r)
    T('⑥主树无落拒：根为主树而无 --落 → rc 2、一字不写；--验 许而不写；加 --落 → 施',
      rc == 2 and '为主树' in 印 and rc验 == 0 and 后 == 前 and rc落 == 0 and '老头四十八年前来过' in 读(r, 设名), (印, 印验, 印落))

    # ⑦ 二跑零改（含新含原：史料行照留加行内注）
    r = 新根()
    单 = [条(), 条(档=章名, 行=7, 原='二十七年前那一趟', 新='四十五年前那一趟', 据='4b'),
          条(档=章名, 行=8, 原='二十七年', 新='二十七年（D1 前之数，照留）', 据='4d')]
    rc1, 印1 = 跑(r, 单)
    一 = 快照(r)
    rc2, 印2 = 跑(r, 单)
    T('⑦二跑零改：首跑改 3；再跑 rc 0、改 0、已施 3、档字节同（新含原之条⛔再加注）',
      rc1 == 0 and '改 3 条' in 印1 and rc2 == 0 and '改 0 条' in 印2 and '已施 3' in 印2 and 快照(r) == 一
      and 读(r, 章名).count('（D1 前之数，照留）') == 1, (印1, 印2))

    # ⑧ 行数⛔变
    r = 新根()
    前 = 快照(r)
    rc, 印 = 跑(r, [条(新='四十八年前\n（另起一行）')])
    rc_b, 印_b = 跑(r, [条(原='二十七年前来过（D1 施前之数）。\n- 甲', 新='x')])
    红_c, _, _, 写_c = D1.施改单(r, [条(新='四十八年前\n（另起一行）')])        # 越过读单：内层之行数守亦须自逮
    T('⑧行数⛔变：新或原含换行 → 红、一字不写；越过单之式，内层行数守亦红',
      rc == 1 and rc_b == 1 and '换行' in 印 and '换行' in 印_b and 快照(r) == 前 and any('行数 10→11' in x for x in 红_c), (印, 印_b, 红_c))

    # ⑨ 窗内多见
    r = 新根()
    前 = 快照(r)
    rc, 印 = 跑(r, [条(行=8, 原='二十七年', 新='四十八年')])     # 8 行无；±3 内：6 行一见、9 行两见
    T('⑨窗内多见：该行无原而 ±3 内原多见 → 首判即红（⛔猜；非待二跑之模拟方逮）、一字不写',
      rc == 1 and '±3 内原 3 见' in 印 and '二跑零改不成' not in 印 and 快照(r) == 前, 印)

    # ⑩ 两可
    r = 新根()
    open(os.path.join(r, 设名), 'w', encoding='utf-8').write(设文.replace('- 甲', '- 甲：四十八年前'))
    前 = 快照(r)
    rc, 印 = 跑(r, [条(行=5, 原='老头二十七年前', 新='四十八年前')])     # 5 行无；3 行原一见，4 行新已在
    T('⑩两可：该行无原；±3 内原一见而新亦在 → 红（已施与否⛔猜）', rc == 1 and '两可' in 印 and 快照(r) == 前, 印)

    # ⑪ --验 只核不写
    r = 新根()
    前 = 快照(r)
    rc, 印 = 跑(r, [条()], '--验')
    T('⑪--验 只核不写：rc 0、印「将改 1 条」、档不动', rc == 0 and '将改 1 条' in 印 and 快照(r) == 前, 印)

    # ⑫ 单之式
    r = 新根()
    前 = 快照(r)
    坏 = [('据', 条(据='4a')), ('由', 条(由=' ')), ('出根', 条(档='../外.md')), ('绝对', 条(档='/etc/passwd')),
          ('.git', 条(档='.git/config')), ('空改', 条(新='二十七年前')), ('新空', 条(新='')), ('行', 条(行=0)),
          ('缺键', {k: v for k, v in 条().items() if k != '由'}), ('非列', 条())]
    全红 = True
    败 = []
    for 名, x in 坏:
        rc, 印 = 跑(r, x if 名 == '非列' else [x])
        if rc != 1 or '单之式有红' not in 印 or (名 in ('出根', '绝对', '.git') and '须为根下之相对路径' not in 印):
            全红 = False
            败.append((名, rc, 印[-120:]))
    rc, 印 = 跑(r, [条(), 条()])
    红_d, _, _, _ = D1.施改单(r, [条(档='../外.md')])                       # 越过读单：内层之 realpath 亦拒出根
    T('⑫单之式：据非 4b|4c|4d、由空、档出根／绝对／.git、空改、新空、行非正、缺键、非列、重条 → 俱於单之式即红、一字不写；内层亦拒出根',
      全红 and rc == 1 and '重条' in 印 and 快照(r) == 前 and any('不在根下' in x for x in 红_d), 败 or 印)

    # ⑬ 叠改（同单两条互吞）→ 二跑之模拟逮之
    r = 新根()
    前 = 快照(r)
    rc, 印 = 跑(r, [条(), 条(原='老头四十八年前', 新='老头二十七年前')])
    T('⑬叠改：同单後条吞前条之改（施後再判非已施）→ 红、一字不写', rc == 1 and '二跑零改不成' in 印 and 快照(r) == 前, 印)

    # ⑭ CRLF 与尾换行照留；他档不动
    r = 新根()
    p = os.path.join(r, 设名)
    open(p, 'w', encoding='utf-8', newline='').write(设文.replace('\n', '\r\n'))
    章前 = 读(r, 章名)
    rc, 印 = 跑(r, [条()])
    t = 读(r, 设名)
    T('⑭CRLF 与尾换行照留、单外之档一字不动', rc == 0 and t == 设文.replace('\n', '\r\n').replace('老头二十七年前', '老头四十八年前')
      and 读(r, 章名) == 章前, (rc, 印))

    # ⑮ 白文之改 → 黄（白文归 D1施 之 A／B）
    r = 新根()
    rc, 印 = 跑(r, [条(档=章名, 行=3, 原='他四十八年前来过', 新='他四十八年前到过', 据='4d')])
    T('⑮改落正文白文 → 施而列黄（查其由）', rc == 0 and '改在第111章白文' in 印, 印)

    # ⑰ 新已在该行（他处，偶合）而原亦一见未盖 → 合而施（⛔误判已施）
    r = 新根()
    open(os.path.join(r, 设名), 'w', encoding='utf-8').write(设文.replace('- L3：老头二十七年前来过', '- L3：他四十八年前走、老头二十七年前来过'))
    rc, 印 = 跑(r, [条()])
    T('⑰新已偶在该行而原亦一见（未为新所盖）→ 合施（⛔误判已施而漏改）', rc == 0 and '改 1 条' in 印 and '二十七年前来过' not in 读(r, 设名), 印)

    # ⑯ CLI 之接：真跑 D1施.py --改单 … --根 …
    r = 新根()
    fd, p = tempfile.mkstemp(suffix='.json', prefix='负测D1改单CLI_')
    os.close(fd)
    open(p, 'w', encoding='utf-8').write(json.dumps([条()], ensure_ascii=False))
    try:
        cp = subprocess.run([sys.executable, os.path.join(此, 'D1施.py'), '--改单', p, '--根', r], capture_output=True, text=True)
        cp验 = subprocess.run([sys.executable, os.path.join(此, 'D1施.py'), '--改单', '--验', p, '--根', r], capture_output=True, text=True)
    finally:
        os.remove(p)
    T('⑯CLI：D1施.py --改单 单 --根 R → rc 0、印改 1 条；--改单 --验 单 → 已施 1、改 0',
      cp.returncode == 0 and '改 1 条' in cp.stdout and '老头四十八年前' in 读(r, 设名)
      and cp验.returncode == 0 and '已施 1' in cp验.stdout and '将改 0 条' in cp验.stdout, (cp.stdout[-300:], cp.stderr[-300:], cp验.stdout[-200:]))
finally:
    for r in 根们:
        shutil.rmtree(r, ignore_errors=True)

print('负测_D1施改单 %d/%d' % (ok, 共))
sys.exit(0 if ok == 共 else 1)
