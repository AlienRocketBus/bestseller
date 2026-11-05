# -*- coding: utf-8 -*-
"""负测·邻拍重出 · 2026-09-04 立（与其器同日·令§六④）

★其料取自301自己：第11轮所删之拍31「数第二遍跟数第一遍，用的是同一个指甲。」
  逐字灌回今版之拍30与拍31之间，器须报；而旧式（人读一遍）本来就没看见，故以「不查」代之。
★★③非陪跑之验：把 MINLEN 抬到 40（旧局：无此器），同一份入参吐零。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 邻拍重出 as L                                    # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

全 = L.诸章()
P301 = 全[301]
原 = io.open(P301, encoding='utf-8').read()

# ①今版之301须只 1 处（拍86↔拍89「跟五天前一样」·本书之礼，非伤）
r0 = L.查(301, P301, 报=False)
t('①今版之301报 1 处（且其串是「跟五天前一样」）',
  (len(r0), r0[0][2] if r0 else ''), (1, '跟五天前一样'))

# ②灌回第11轮所删之那一拍，器须多报一处，且其串须含「同一个指甲」
灌 = 原.replace('三处我又数了一遍。数出来还是三处。',
              '三处我又数了一遍。数出来还是三处。\n\n＊\n\n数第二遍跟数第一遍，用的是同一个指甲。', 1)
_tmp = os.path.join(根, '版本', '_负测_邻拍重出.tmp.md')
io.open(_tmp, 'w', encoding='utf-8').write(灌)
try:
    r1 = L.查(301, _tmp, 报=False)
    # ★②此测所守的是一句实话，不是一句愿望：**本器逮不着立它的那一处。**
    #   ★★其由：拍31「用的是同一个指甲」与下一拍「同一个指甲数两遍」，
    #     去标点後之公共串只 5 字，而本器之槛是 6。
    #   ★★★而降槛之式已数其群而驳（近四十章 8 处→247 处，均6.17顶22，噪）；
    #     ★★★★故此处断言其「不报」——**一份把限说破的负测，比一份替器遮丑的负测有用。**
    t('②灌回第11轮所删之拍，本器照旧不报（其限，非其功）', len(r1) - len(r0), 0)
    t('②之b而其公共串确只 5 字（故 6 字之槛拦不着它）',
      len('同一个指甲'), 5)
    t('②之c而此限已逐字写在器之档头（不许下一坐把它的绿读成「邻拍无重」）',
      '它逮不着立它的那一处' in io.open(
          os.path.join(根, '工具', '邻拍重出.py'), encoding='utf-8').read(), True)
    # ③旧式（无此器）对同一入参吐零——把门槛抬到40即是旧局
    _old = L.MINLEN
    L.MINLEN = 40
    r2 = L.查(301, _tmp, 报=False)
    L.MINLEN = _old
    t('③旧局（无此器·门槛40）对同一入参吐零，故非陪跑', r2, [])
finally:
    if os.path.exists(_tmp):
        os.remove(_tmp)

# ④不误伤：一份无重之料吐空
t('④无重之料吐空',
  L.分拍('甲乙丙丁戊己庚辛\n\n＊\n\n壬癸子丑寅卯辰巳\n') and True, True)

# ⑤其位已给（令§十一③）：一坐之逐轮之器表里须有它，且在第10轮
_YZ = io.open(os.path.join(根, '工具', '一坐.py'), encoding='utf-8').read()
t('⑤其位在一坐之逐轮之器表·第10轮',
  bool(re.search(r'\n    10:\s*\[\(\'工具/邻拍重出\.py', _YZ)), True)

# ⑥—⑨ W53·X12（392 合稿所逮）：卡令统一之称与立法复沓只报不计——392 旧式 13 处、起草闸致命红，十三处皆两步。
if 392 in 全:
    计, 沓 = L.查(392, 全[392], 报=False, 分=True)
    t('⑥392 之称（收皮子的那一个）与复沓（比心口上还温）入「称／复沓」，计入不及⛔线（<6）',
      (len(计) < 6, any('收皮子的那一个' in h[2] for h in 沓), any('比心口上还温' in h[2] for h in 沓)),
      (True, True, True))
    # ⑦旧病回灌：称沓亦计（旧式）则 392 须过⛔线——故⑥非陪跑
    _沓 = L.复沓
    L.复沓 = lambda b, s: False
    try:
        计旧, _ = L.查(392, 全[392], 报=False, 分=True)
    finally:
        L.复沓 = _沓
    t('⑦旧式（称／复沓亦计）回灌 392 计入 ≥6——⑥之治非陪跑', len(计旧) >= 6, True)
import tempfile as _tf
_d = _tf.mkdtemp(prefix='负测_邻拍重出_')
try:
    # ⑧不放松：六对各只见於两拍之串（一句话拆两拍之形）照计、照⛔；同章一称见於三拍者只入称沓
    串 = ['青石板上落雨点', '风从窗缝里钻进', '灶膛里柴火噼啪', '井绳磨得发亮了', '鸡叫过头一遍了', '门槛上蹲着老猫']
    行 = []
    for k, s in enumerate(串):
        行 += ['甲%d%s乙' % (k, s), '丙%d%s丁' % (k, s)]
    行 += ['收皮子的那一个来了', '收皮子的那一个蹲下', '收皮子的那一个走了']
    _p = os.path.join(_d, '第九百九十九章.md')
    io.open(_p, 'w', encoding='utf-8').write('# 第九百九十九章 测\n\n' + '\n\n'.join(行) + '\n')
    import contextlib as _cl
    _buf = io.StringIO()
    with _cl.redirect_stdout(_buf):
        计8, 沓8 = L.查(999, _p, 分=True)
    t('⑧六对两拍之串照计（6）、照⛔；一称见於三拍者只入称沓（3）',
      (len(计8), '⛔ 六处以上' in _buf.getvalue(), len(沓8)), (6, True, 3))
    # ⑧之二 W60·X33①：⛔行所称之分位，须与表头同一分位之数相合（旧印「六处以上（全书 90 分位）」而表头「90分位 5」，自相矛）
    _印 = _buf.getvalue()
    _头 = dict(re.findall(r'(\d+)分位 (\d+)', _印))
    _刀 = re.search(r'⛔ ([一二三四五六七八九十])处以上（全书 (\d+) 分位）', _印)
    _线 = str(getattr(L, '刀线', 6))
    t('⑧之二⛔行之「N 分位」与表头「N分位 K」相合（K＝刀线＝⛔所称之数）',
      (bool(_刀), _刀 and _头.get(_刀.group(2)), _刀 and str('零一二三四五六七八九十'.find(_刀.group(1))), _线),
      (True, _线, _线, '6'))
    # ⑨窗之认：串只见两拍，而其中六字之窗见於三拍（立法复沓「数过十口，比心口上还温」之形）
    t('⑨长串只见两拍而其六字之窗见三拍——係复沓',
      L.复沓(['数过十口比心口上还温', '又数过十口比心口上还温', '哪儿都比心口上还温'], '数过十口比心口上还温'), True)
    t('⑨之b只见两拍之串不是复沓', L.复沓(['青石板上落雨点甲', '乙青石板上落雨点', '无关'], '青石板上落雨点'), False)
finally:
    import shutil as _sh
    _sh.rmtree(_d, ignore_errors=True)

print('════ 负测·邻拍重出 ════')
for 名, ok, 实, 期 in 过:
    print('  %s %s' % ('✓' if ok else '✗', 名), '' if ok else '（实 %r 期 %r）' % (实, 期))
n = sum(1 for _, ok, _, _ in 过 if ok)
print('  %d/%d %s' % (n, len(过), '全通' if n == len(过) else '⛔有败'))
sys.exit(0 if n == len(过) else 1)
