# -*- coding: utf-8 -*-
"""可逆册负测（2026-08-30 立·随「可逆册」同日）。
★其立之由：作者授权「不可逆之事亦可做」，其条件是它变成可复原的；
  ★★而「可复原」若只是一句话，那这条授权就是白给的。
★★★故此测专问三样：①存了真能复原吗 ②库损了它认不认得出 ③认不出的时候它敢不敢拦。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import sys, os, io, json, shutil, tempfile, importlib.util

_旧cwd = os.getcwd()

spec = importlib.util.spec_from_file_location('kn', '工具/可逆.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

案 = []
def chk(名, 实, 期):
    案.append((名, 实 == 期, '实=%r 期=%r' % (实, 期)))

def 造场(t):
    # ★测具亦须换到那一处去跑：器之路径以仓库根为准，而「仓库根」在测里就是这个临时目录
    os.chdir(t)
    m.ROOT = t
    m.LIB = os.path.join(t, '版本', '_可逆库')
    m.CE = os.path.join(t, '设定', '可逆册.md')
    os.makedirs(os.path.join(t, '正文'), exist_ok=True)
    os.makedirs(os.path.join(t, '设定'), exist_ok=True)
    m._git = lambda *a: 'deadbeef' if a and a[0] == 'rev-parse' else 'zhi'
    p = os.path.join(t, '正文', '甲.md')
    io.open(p, 'w', encoding='utf8').write('原文一二三。\n')
    return p

def 读(p):
    return io.open(p, encoding='utf8').read()

# ① 存了真能复原：改文之后复原，逐字回到原样
with tempfile.TemporaryDirectory() as t:
    p = 造场(t)
    chk('①存·返零', m.存('试', ['正文/甲.md']), 0)
    io.open(p, 'w', encoding='utf8').write('我把它改坏了。\n')
    chk('①之b 复原·返零', m.复原('R0001'), 0)
    chk('①之c 复原之后逐字回到原样', 读(p), '原文一二三。\n')

# ② 整篇被删也能复原（此为「删章」之形）
with tempfile.TemporaryDirectory() as t:
    p = 造场(t)
    m.存('删章之前', ['正文/甲.md'])
    os.remove(p)
    chk('②删章之后·复原·返零', m.复原('R0001'), 0)
    chk('②之b 删章之后·文回来了', 读(p), '原文一二三。\n')

# ③ 库中之件被改 → 验须报坏，且复原须拒办
with tempfile.TemporaryDirectory() as t:
    p = 造场(t)
    m.存('试', ['正文/甲.md'])
    lib = [x for x in os.listdir(m.LIB) if x.startswith('R0001')][0]
    io.open(os.path.join(m.LIB, lib, '原', '正文', '甲.md'), 'w', encoding='utf8').write('库被人动过。\n')
    chk('③库中之件被改·验须报坏', m.验(True), 2)
    io.open(p, 'w', encoding='utf8').write('现文。\n')
    chk('③之b 库已损·复原须拒办', m.复原('R0001'), 2)
    chk('③之c 拒办之后不许动现文', 读(p), '现文。\n')

# ④ 库中之件被删 → 验须报坏
with tempfile.TemporaryDirectory() as t:
    造场(t)
    m.存('试', ['正文/甲.md'])
    lib = [x for x in os.listdir(m.LIB) if x.startswith('R0001')][0]
    os.remove(os.path.join(m.LIB, lib, '原', '正文', '甲.md'))
    chk('④库中之件被删·验须报坏', m.验(True), 2)

# ⑤ _单.json 坏 → 验须报坏
with tempfile.TemporaryDirectory() as t:
    造场(t)
    m.存('试', ['正文/甲.md'])
    lib = [x for x in os.listdir(m.LIB) if x.startswith('R0001')][0]
    io.open(os.path.join(m.LIB, lib, '_单.json'), 'w', encoding='utf8').write('{不是json')
    chk('⑤单坏·验须报坏', m.验(True), 2)

# ⑥ 路径不在 → 存须拒办（存不下来即不许落刀）
with tempfile.TemporaryDirectory() as t:
    造场(t)
    chk('⑥路径不在·存须拒办', m.存('试', ['正文/没有这一篇.md']), 2)
    chk('⑥之b 拒办即不许留号', os.path.isdir(m.LIB) and len(os.listdir(m.LIB)) or 0, 0)

# ⑦ 无路径 → 存须拒办
with tempfile.TemporaryDirectory() as t:
    造场(t)
    chk('⑦无路径·存须拒办', m.存('试', []), 2)

# ⑧ 册上无此号 → 复原须拒办
with tempfile.TemporaryDirectory() as t:
    造场(t)
    chk('⑧无此号·复原须拒办', m.复原('R9999'), 2)

# ⑨ 一笔存多件，逐件皆须复原
with tempfile.TemporaryDirectory() as t:
    p = 造场(t)
    q = os.path.join(t, '设定', '乙.md')
    io.open(q, 'w', encoding='utf8').write('乙之原。\n')
    m.存('二件', ['正文/甲.md', '设定/乙.md'])
    os.remove(p); io.open(q, 'w', encoding='utf8').write('乙被改。\n')
    chk('⑨二件·复原·返零', m.复原('R0001'), 0)
    chk('⑨之b 甲回来了', 读(p), '原文一二三。\n')
    chk('⑨之c 乙回来了', 读(q), '乙之原。\n')

# ⑩ 号须递增，不许覆盖前一笔
with tempfile.TemporaryDirectory() as t:
    p = 造场(t)
    m.存('头一笔', ['正文/甲.md'])
    io.open(p, 'w', encoding='utf8').write('第二版。\n')
    m.存('第二笔', ['正文/甲.md'])
    chk('⑩号须递增（二笔并存）', len([x for x in os.listdir(m.LIB) if x.startswith('R')]), 2)
    io.open(p, 'w', encoding='utf8').write('第三版。\n')
    m.复原('R0001')
    chk('⑩之b R0001 复的是头一笔之文', 读(p), '原文一二三。\n')
    m.复原('R0002')
    chk('⑩之c R0002 复的是第二笔之文', 读(p), '第二版。\n')

# ⑪ 册须逐笔留痕（记录之册不许空）
with tempfile.TemporaryDirectory() as t:
    造场(t)
    m.存('其由甲乙丙', ['正文/甲.md'])
    txt = 读(m.CE)
    chk('⑪册上须见其号', 'R0001' in txt, True)
    chk('⑪之b 册上须见其由', '其由甲乙丙' in txt, True)
    chk('⑪之c 册上须见复原之法', '--复原 R0001' in txt, True)


# ⑫ 库中之件未入 git → 验须报坏（sha256 只证库没烂，不证库存得住）
with tempfile.TemporaryDirectory() as t:
    造场(t)
    m.存('试', ['正文/甲.md'])
    def _假git(*a):
        if a and a[0] == 'ls-files':
            return None          # ★一件也没入 git
        return 'deadbeef' if a and a[0] == 'rev-parse' else 'zhi'
    m._git = _假git
    chk('⑫库中之件未入git·验须报坏', m.验(True), 2)

# ⑬ 逐件皆入 git → 验须过
with tempfile.TemporaryDirectory() as t:
    造场(t)
    m.存('试', ['正文/甲.md'])
    m._git = lambda *a: (None if a and a[0] == 'ls-remote' else
                         ('deadbeef' if a and a[0] == 'rev-parse' else 'zhi'))
    chk('⑬逐件皆入git·验须过', m.验(True), 0)

# ⑭ 只单.json 未入 git（原物入了）→ 验仍须报坏
with tempfile.TemporaryDirectory() as t:
    造场(t)
    m.存('试', ['正文/甲.md'])
    def _半git(*a):
        if a and a[0] == 'ls-files':
            return None if str(a[-1]).endswith('_单.json') else 'zhi'
        return 'deadbeef' if a and a[0] == 'rev-parse' else 'zhi'
    m._git = _半git
    chk('⑭只单.json未入git·验仍须报坏', m.验(True), 2)

os.chdir(_旧cwd)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
