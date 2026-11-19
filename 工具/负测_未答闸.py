# -*- coding: utf-8 -*-
"""未答闸（⑳）负测（2026-09-01 立·随「⑳补其答词之②形」同日）。
★其立之由：⑳之答词集补了六个词，是放宽了它认「已答」的口子；
  ★★而放宽之闸若口子开大了，等於把闸拆了。
★★★故此测专问三样：①旧式所红而新式仍红者，须还在（其防未动）；
  ②新式所松者，须逐章拿得出「其限已明写」之凭据（不是凭空放行）；
  ③一个假章：摆了问而二十拍内一个字也不交代者，新式仍须报红。
〔1119 死规之审·gates19〕⑳ 入 `_软报`：上列侦之格一字不动（「红」即侦得）；另添 ⑧⑨：
  ⑳ 侦得之红经 `run()` ⛔计入拦（rc 0）｜⛔守牙：硬检（⑬）一红照旧拦（rc 2）。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import sys, re, importlib.util

spec = importlib.util.spec_from_file_location('k', '工具/开轮六检.py')
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

案 = []
def chk(名, 实, 期):
    案.append((名, 实 == 期, '实=%r 期=%r' % (实, 期)))

旧词 = r'(是因为|其由|答|知道了|明白|原来|后来我|遂|所以)'
新加 = r'(说不上|说不出|数不出|指不出|量不出|认不出|没得比|不知道)'

def 判(cur, pat):
    """★以指定之答词集重跑⑳（其余一字不改）。"""
    b = K.body(cur)
    if not b:
        return True
    ps = [x.strip() for x in b.split('\n') if x.strip() and x.strip() != '＊']
    qs = [(i, x) for i, x in enumerate(ps)
          if re.search(r'(是什么|在哪儿|几时|怎么办|为什么|多少|哪一样|哪一条)[。？]', x)]
    if not qs:
        return True
    un = [i for i, q in qs
          if not re.search(pat, ''.join(ps[i + 1:i + 21]))]
    return len(un) <= 1

cs = [c for c in sorted(K.F) if c >= 200]
旧红 = [c for c in cs if not 判(c, 旧词)]
新红 = [c for c in cs if not 判(c, 旧词 + '|' + 新加)]

# ① 群之数须与立法之日所量相符
chk('①200章以来之章数 ≥80', len(cs) >= 80, True)
# ★★★★★2026-09-05 改（305第1轮·**同形第六犯，故并入原号**）：
#   ★此条原作「旧式红率 ≥20%」——★★而其分母是「200章以来之章数」，**每写一章它就长一**；
#     **305一落盘，21/106＝19.8%，此条当场失效**；★★★**而它守的那一样一个字也没变**：
#     **旧式咬着的是一个群，不是一撮**。
#   ★★★★**而这一形本坐已犯六回**（负测_销立门④之d｜负测_开轮六检②与③｜负测_亮点对表21、22｜
#     负测_开轮六检之局留了一件文件在仓库里｜此处）——★**其形一句话**：
#     **凡负测之断言钉在一个「会随磁盘长大或被治好」的数上，那条断言守的不是不变量，是那一天的磁盘。**
#   ★故改以二样绝对之数验之，二样皆不随章数长：
#     **①旧式所咬者须成群（≥20 章）｜②新式所松者须成群（旧红减新红 ≥10 章）**
#     ——**後者正是此改之全部所值**：**松一两章不值得改一道闸。**
chk('②之一·旧式所咬者成群（旧红 %d 章 ≥20）' % len(旧红), len(旧红) >= 20, True)
chk('②之二·新式所松者亦成群（旧红减新红 %d 章 ≥10）' % (len(旧红) - len(新红)),
    len(旧红) - len(新红) >= 10, True)

# ② 新式仍须留红（改而不挖空）
chk('③新式仍有红（非归零·%d 章）' % len(新红), len(新红) > 0, True)
chk('④新红须为旧红之子集（新式不许把没红的弄红）',
    [c for c in 新红 if c not in 旧红], [])

# ③ 新式所松之章，逐章须拿得出「其限已明写」之凭据
无凭 = []
for c in [x for x in 旧红 if x not in 新红]:
    if not re.search(新加, K.body(c)):
        无凭.append(c)
chk('⑤新式所松之章，逐章正文皆见其限之明写', 无凭, [])

# ④ 假章：摆问而二十拍内一字不交代者，新式仍须报红
假 = '他站在水里等的是什么。\n' + '\n'.join('走了一步。' for _ in range(30))
ps = [x for x in 假.split('\n') if x.strip()]
qs = [(i, x) for i, x in enumerate(ps)
      if re.search(r'(是什么|在哪儿|几时|怎么办|为什么|多少|哪一样|哪一条)[。？]', x)]
un = [i for i, q in qs if not re.search(旧词 + '|' + 新加, ''.join(ps[i + 1:i + 21]))]
chk('⑥假章（摆问而二十拍内一字不交代）新式仍逮得住', len(un) >= 1, True)

# ⑤ 假章之二：摆二问而只答其一者，仍须放行（≤1 为限，此限未动）
假2 = ['他站在水里等的是什么。', '我说不上。'] + ['走了一步。'] * 3 + ['他等的是什么。'] + ['走了一步。'] * 30
qs2 = [(i, x) for i, x in enumerate(假2)
       if re.search(r'(是什么|在哪儿|几时|怎么办|为什么|多少|哪一样|哪一条)[。？]', x)]
un2 = [i for i, q in qs2 if not re.search(旧词 + '|' + 新加, ''.join(假2[i + 1:i + 21]))]
chk('⑦「≤1 未答」之限未动（摆二问答其一 → 放行）', len(un2) <= 1, True)

# ⑧⑨〔1119 死规之审·gates19〕⑳ 只报：真跑 check20 於一假章（摆二问、二十拍内一字不交代），侦得而 run() ⛔拦
import contextlib, io as _io, os as _os, tempfile as _tf, shutil as _sh
def _跑闸(真检, cur, 硬红=False):
    """余检一律换作恒绿之桩，只留「真检」照跑；硬红=True 另令 ⑬ 红（守牙）。返 (rc, --静 之印)。"""
    诸 = ('check3', 'check5', 'check7', 'check10', 'check11', 'check12', 'check13',
          'check15', 'check16', 'check17', 'check18', 'check19', 'check20')
    旧 = dict((k, getattr(K, k)) for k in 诸)
    try:
        for k in 诸:
            if k != 真检:
                setattr(K, k, lambda *a, _k=k: [('桩·' + _k, True, '桩')])
        if 硬红:
            K.check13 = lambda *a: [('⑬·亮点段', False, '⛔桩：无亮点段')]
        buf = _io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = K.run([cur], True)
        return rc, buf.getvalue()
    finally:
        for k, v in 旧.items():
            setattr(K, k, v)
_tmp = _tf.mkdtemp(prefix='负测_未答闸_')
_旧F = K.F
try:
    _p = _os.path.join(_tmp, '第九百章.md')
    open(_p, 'w', encoding='utf-8').write(
        '他站在水里等的是什么。\n' + '\n'.join('走了一步。' for _ in range(25))
        + '\n她手里攥的是什么。\n' + '\n'.join('走了一步。' for _ in range(25)) + '\n')
    K.F = {900: _p}
    _侦 = K.check20(900)[0]
    _rc, _印 = _跑闸('check20', 900)
    chk('⑧⑳侦得假章之红（ok=False）而 run() ⛔计入拦：rc 0、印「通过」',
        (_侦[1], _rc, '开轮十六检通过' in _印), (False, 0, True))
    _rc2, _印2 = _跑闸('check20', 900, 硬红=True)
    chk('⑨⛔守牙：同局而硬检（⑬）一红 → rc 2，--静 败单只列 ⑬、⛔混进 ⑳',
        (_rc2, '⑬' in _印2, '⑳' in _印2), (2, True, False))
finally:
    K.F = _旧F
    _sh.rmtree(_tmp, ignore_errors=True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
