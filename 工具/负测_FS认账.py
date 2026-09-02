# -*- coding: utf-8 -*-
"""负测·FS认账（批131·293第1轮所立）
所治之伤：FS沉默闸之销在本章回执，而回执须待十三轮跑毕；
        故一根逾期之伏笔可以拦住此後十二轮的每一次推——
        **而拦十二回并不能让回执早交一天，只能教出「见红就 --no-verify」**
        （绕行审计.log 里那四十五次绕行，正是⑥当年这么长出来的）。
其治之式（与⑥之否决记同）：**放行之价是一行写下来的字，不是一次沉默**——
        逾期之每一根 FS，须在本章之轮记或开镜卡里写着「FSxx·本章未兑」。
本测所验者为不变量，非快照：
  ①一根逾期而无人写「未兑」者，照旧拦（此係本闸之本职，不许放走）；
  ②逐根皆认账者方许放行——**少认一根即拦**（不许拿「认了大半」蒙混）；
  ③其单取自 FS闸 自己那一支，不取自报文（报文里本就没有根号）；
  ④放行只在跑轮档（回执未交时）；回执一交，此口自销。
"""
import io, os, re, sys, importlib.util as iu
_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

_s = iu.spec_from_file_location('_qc', os.path.join(_D, '全测.py'))
_qc = iu.module_from_spec(_s)
_s.loader.exec_module(_qc)
f = getattr(_qc, '_逾期伏笔俱已认账', None)
chk('①口在·_逾期伏笔俱已认账 可调', callable(f), True)

_src = io.open(os.path.join(_D, '全测.py'), encoding='utf-8').read()
chk('③其单取自 FS闸 自己那一支，不取自报文',
    "_fs.查()" in _src and "_未答" in _src, True)
chk('③之b 而报文里本就没有根号（此係头一版之坏因，须与器同存）',
    '报文里没有根号' in _src, True)
chk('④放行只在跑轮档（其位在 _已封版 之後那一段）',
    _src.find("elif name == 'FS沉默闸':") > _src.find('【封版档】'), True)
chk('④之b 且其语明写「其销须待第N章回执」（放行不是销账）',
    '其销须待第%d章回执；逾期者俱已在轮记认账' in _src, True)

# ── 取本章之实：逾期之根与其认账 ──
_sf = iu.spec_from_file_location('_fs', os.path.join(_D, 'FS闸.py'))
_fs = iu.module_from_spec(_sf)
_sf.loader.exec_module(_fs)
_n, _f, _欠, _未答, _答 = _fs.查()
_ids = [str(x['id']) for x in _未答]
chk('②之前置·本章确有逾期而未答之根（无则本组无从验，须当场说出来）', len(_ids) >= 1, True)

_lj = os.path.join(_R, '版本', '第%d章' % _n, '_轮记.md')
_kj = os.path.join(_R, '版本', '第%d章' % _n, '_开镜卡.md')
_orig = io.open(_lj, encoding='utf-8').read() if os.path.exists(_lj) else ''
_ko = io.open(_kj, encoding='utf-8').read() if os.path.exists(_kj) else ''
try:
    chk('②逐根皆认账·放行', f('') is True, True)
    # 抽掉其中一根之认账 → 须拦
    if _ids:
        _one = _ids[0]
        io.open(_lj, 'w', encoding='utf-8').write(
            _orig.replace('%s·本章未兑' % _one, '%s·（认账被抽走）' % _one))
        if os.path.exists(_kj):
            io.open(_kj, 'w', encoding='utf-8').write(
                _ko.replace('%s·本章未兑' % _one, '%s·（认账被抽走）' % _one))
        chk('②之b 抽掉一根之认账即拦（不许拿「认了大半」蒙混·今抽 %s）' % _one, f('') is False, True)
    # 全抽 → 须拦
    _t2 = _orig
    for _x in _ids:
        _t2 = _t2.replace('%s·本章未兑' % _x, '%s·（认账被抽走）' % _x)
    io.open(_lj, 'w', encoding='utf-8').write(_t2)
    if os.path.exists(_kj):
        _k2 = _ko
        for _x in _ids:
            _k2 = _k2.replace('%s·本章未兑' % _x, '%s·（认账被抽走）' % _x)
        io.open(_kj, 'w', encoding='utf-8').write(_k2)
    chk('①一根也没认账·照旧拦（此係本闸之本职）', f('') is False, True)
finally:
    if _orig:
        io.open(_lj, 'w', encoding='utf-8').write(_orig)
    if _ko:
        io.open(_kj, 'w', encoding='utf-8').write(_ko)
chk('①之b 复原毕·仍放行（证本测未把账改坏）', f('') is True, True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
