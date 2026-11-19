# -*- coding: utf-8 -*-
"""负测·摆问之嵌（2026-09-23·限359 立·随 `开轮六检::check20` 补嵌式同日）。
★所守者：**⑳ 所数的那个「问」，是不是真的一个问。**
★★其立之由（第358章推闸之红所逮）：
  ⛔**旧式只看「疑问词＋。／？」**——**而中文里疑问词嵌在陈述句中极常见**：
    **「黑到看不出底在哪儿。」｜「放平了看它离缝那两边各多少。」｜「我知道他想问的是什么。」**
    **三句皆无一问，而旧式逐句判作「摆了一问」。**
  ★**其数（0923 全书亲扫）**：**嵌者 279 处、分布 161 章｜真摆问 289 处**——**旧式所数之「问」，近半不是问。**
⛔⛔**而本测头一格所守者，不是「新式对不对」，是「本坐动它之时它正拦着本坐的推」**：
  **故 ①格以全书回灌钉死其误伤之广（161 章），⛔证此改非自赦**；
  **②③格守其不许放松（真摆问照旧数得着）。**
〔1119 死规之审·gates19〕⑳ 入 `_软报`：上列数问之格一字不动；另添 ⑦：⑳ 所出之行名落在软报之列（⛔计入拦），
  而硬检之名（⑬）不落（守牙）——run() 之拦与否另由 负测_未答闸 ⑧⑨ 真跑验之。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io, os, re, sys, glob, importlib.util

_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
_sp = importlib.util.spec_from_file_location('k6', os.path.join(_D, '开轮六检.py'))
_m = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_m)

案 = []


def chk(名, 得, 期):
    案.append((名, 得 == 期, '得 %r 期 %r' % (得, 期)))


def _摆问(句):
    """★照 `check20` 同一式复算：一句之内，是不是一处真摆问。"""
    for mo in _m._问式.finditer(句):
        _s0 = max(句.rfind('。', 0, mo.start()), 句.rfind('\n', 0, mo.start())) + 1
        if _m._嵌式.search(句[_s0:mo.end()]):
            continue
        return True
    return False


# ① ⛔旧式回灌·全书之广（⛔本格係「此改非自赦」之凭）
_旧 = 0
_新 = 0
_章 = set()
for _f in glob.glob(os.path.join(_R, '正文', '*.md')):
    _t = io.open(_f, encoding='utf-8', errors='replace').read().split('【本章亮点】')[0]
    for _mo in _m._问式.finditer(_t):
        _s1 = max(_t.rfind('。', 0, _mo.start()), _t.rfind('\n', 0, _mo.start())) + 1
        _旧 += 1
        if _m._嵌式.search(_t[_s1:_mo.end()]):
            _章.add(_f)
        else:
            _新 += 1
chk('①⛔旧式回灌·误伤遍全书（≥100 章），⛔非 358 一章之事', len(_章) >= 100, True)
chk('①之b 而旧式所数近半不是问（新式之数显著少於旧式）', _新 < _旧 * 0.75, True)
chk('①之c ★而新式不是把它数成零（真摆问照旧有其数）', _新 >= 100, True)

# ② ⛔真摆问照旧数得着（⛔此改不许放松）
chk('②真摆问·「这是什么。」', _摆问('他把那一样东西递过来。这是什么。'), True)
chk('②之b 真摆问·「为什么。」', _摆问('他不肯说。为什么。'), True)
chk('②之c 真摆问·带问号者', _摆问('他抬头：哪一条？'), True)

# ③ ⛔嵌在陈述句里者不作摆问（本改所治）
chk('③嵌·「黑到看不出底在哪儿。」', _摆问('往里看是黑的，黑到看不出底在哪儿。'), False)
chk('③之b 嵌·「放平了看它离缝那两边各多少。」',
    _摆问('另一头往东放平，放平了看它离缝那两边各多少。'), False)
chk('③之c 嵌·「我知道他想问的是什么。」', _摆问('我没应声。我知道他想问的是什么。'), False)
chk('③之d 嵌·「不列，你就不知道差多少。」', _摆问('不列，你就不知道差多少。'), False)

# ④ ⛔其界只在同一句之内（⛔不许跨句去找那个嵌之动词）
chk('④⛔跨句不算嵌：上一句有「看」而本句係真问',
    _摆问('我看了他一眼。这是什么。'), True)

# ⑤ ★真盘回灌：358 之三处皆嵌，故本章未摆明问
_f358 = glob.glob(os.path.join(_R, '正文', '*第三百五十八章*.md'))
if _f358:
    _t8 = io.open(_f358[0], encoding='utf-8', errors='replace').read().split('【本章亮点】')[0]
    _ps = [x.strip() for x in _t8.split('\n') if x.strip() and x.strip() != '＊']
    chk('⑤真盘回灌·358 之内无一处真摆问', any(_摆问(x) for x in _ps), False)
    chk('⑤之b ⛔而旧式之下它有三处', 
        len([x for x in _ps if _m._问式.search(x)]), 3)

# ⑥ ⛔器里那二式确已拆出（⛔免测改了而器没改）
_src = io.open(os.path.join(_D, '开轮六检.py'), encoding='utf-8').read()
chk('⑥⛔器里 `_嵌式` 已在，且 `check20` 用着它',
    ('_嵌式 = re.compile' in _src and '_嵌式.search' in _src), True)

# ⑦〔1119 死规之审·gates19〕⑳ 只报：check20 真出之行名（造一真摆二问不答之局）落在 _软报；⑬ 不落（守牙仍硬）
import tempfile as _tf, shutil as _sh
_tmp = _tf.mkdtemp(prefix='负测_摆问之嵌_')
_旧F = _m.F
try:
    _p = os.path.join(_tmp, '第九百章.md')
    io.open(_p, 'w', encoding='utf-8').write(
        '他把那一样东西递过来。这是什么。\n' + '\n'.join('走了一步。' for _ in range(25))
        + '\n他不肯说。为什么。\n' + '\n'.join('走了一步。' for _ in range(25)) + '\n')
    _m.F = {900: _p}
    _行 = _m.check20(900)[0]
finally:
    _m.F = _旧F
    _sh.rmtree(_tmp, ignore_errors=True)
chk('⑦真摆二问不答 → ⑳侦得（ok=False），其行名落在 _软报（⛔计入拦）；⑬ 之名不落（守牙）',
    (_行[1], _m._是软报(_行[0]), _m._是软报('⑬·亮点段')), (False, True, False))

坏 = [x for x in 案 if not x[1]]
print('════ 负测·摆问之嵌 ════（守：⑳ 所数的那个「问」，是不是真的一个问）')
print('  ★全书之数：旧式数得 %d 处｜新式数得 %d 处｜其差分布 %d 章' % (_旧, _新, len(_章)))
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
