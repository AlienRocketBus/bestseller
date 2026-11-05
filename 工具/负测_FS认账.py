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
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
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
# ★★★★★【294封版之序·同修】①之b 原写作「复原毕·仍放行」——**而那也是钉在快照上的**：
#   它预设复原之後盘上还有逾期之根；而294把逾期填平之後，无根可放行，f 遂返 False，此条当场红。
#   ★其真不变量是「**测前测後同判**」，不是「测後必放行」——故先记其测前之判，测後与之相比。
_判前 = None
_sf = iu.spec_from_file_location('_fs', os.path.join(_D, 'FS闸.py'))
_fs = iu.module_from_spec(_sf)
_sf.loader.exec_module(_fs)
_n, _f, _欠, _未答, _答 = _fs.查()
_ids = [str(x['id']) for x in _未答]
_判前 = f('')

# ★【293封版之序·第五度所修】此处原写作一句断言：「本章确有逾期而未答之根」。
#   ★★而那是把断言钉在快照上：**本章回执一交，逾期之根即俱已回话，_未答 遂为空，
#     这一组当场判红——而器一分没坏，坏的是测所站的那一刻。**
#   ★★★**同一形我已改过四回**（负测_冷轮否决记⑤⑦⑩、负测_棘轮裁⑦⑧⑨、
#     负测_冷轮否决记③⑤⑧、负测_封版档冷轮⑬⑮），**四回都没记进病历本，故第五回它又来了**
#     （今立第二十八犯）。
#   ★★★★**其治不是把这一组跳过去**——一份只在某一刻才验得动的测，其余时候就是陪跑（令§六③）；
#     ★**治法是让它自己把那个窗口造出来**：暂时把本章回执挪开，FS闸 即复报逾期未答，
#     於是①②两组照旧验得动；★★而挪开之物在 finally 里必还原，且还原之後另验一遍（①之b）。
# ★★★★★【294封版之序·第六度所修——同一形之第六回，且这一回是自己昨天的治法不够深】
#   ★上一修（第五度）造了窗口的一半：**把本章回执挪开**，於是「回执已交」这一半不再挡路；
#   ★★**而另一半没造**：**它仍旧要盘上此刻真有一根逾期之伏笔**——
#     而294封版之序落实了293所判而未落盘之改期（FS01→302／FS03→298），
#     **逾期之根遂由二变零，这一组当场又红**；**器一分没坏，坏的还是测所站的那一刻。**
#   ★★★**故第六度之治：连那一根也由测自己造**——暂时把一根伏笔之 due 挪到本章之前，
#     验毕在 finally 里逐字还原（且还原之後另验一遍，证本测未把账改坏）。
#   ★★★★**其判准（令§六④）**：**改後它还逮不逮得住它本来要逮的东西？**
#     ——①一根逾期而无人写「未兑」者照旧拦｜②少认一根即拦；**二者皆由本测自造之根验得动。**
_rc = None
_rcs = []   # ★0925·367 起一章可有两份回执（封版席＋案席）；只挪头一份，FS闸 读着第二份即判「已答」，窗口造不出——须逐份挪开
_canon = os.path.join(_R, '设定', 'canon事实库.json')
_canon_orig = None
_synth = None
if not _ids:
    import glob as _g
    _cand = _g.glob(os.path.join(_R, '设定', '回执_*_第%d章*.md' % _n))
    if _cand:
        _rc = _cand[0]
        _rcs = list(_cand)
        for _p in _rcs:
            os.rename(_p, _p + '.负测暂移')

    def _再查():
        _sf2 = iu.spec_from_file_location('_fs2', os.path.join(_D, 'FS闸.py'))
        _fs2 = iu.module_from_spec(_sf2)
        _sf2.loader.exec_module(_fs2)
        return _fs2.查()

    _n, _f, _欠, _未答, _答 = _再查()
    _ids = [str(x['id']) for x in _未答]

    if not _ids:
        # ★盘上一根逾期也没有——自造一根（挪一根 open 之伏笔的 due 到本章之前）
        import json as _json
        _canon_orig = io.open(_canon, encoding='utf-8').read()
        _d = _json.loads(_canon_orig)
        for _x in _d.get('foreshadows', []):
            if _x.get('status') == 'open' and _x.get('due'):
                _synth = str(_x.get('id'))
                _x['due'] = max(1, _n - 3)
                break
        if _synth:
            io.open(_canon, 'w', encoding='utf-8').write(
                _json.dumps(_d, ensure_ascii=False, indent=2))
            _n, _f, _欠, _未答, _答 = _再查()
            _ids = [str(x['id']) for x in _未答]
chk('②之前置·有逾期未答之根可验（本章回执已交者，测自造其窗口；盘上一根不欠者，连那一根也自造）', len(_ids) >= 1, True)

_lj = os.path.join(_R, '版本', '第%d章' % _n, '_轮记.md')
_kj = os.path.join(_R, '版本', '第%d章' % _n, '_开镜卡.md')
_真orig = io.open(_lj, encoding='utf-8').read() if os.path.exists(_lj) else ''
_ko = io.open(_kj, encoding='utf-8').read() if os.path.exists(_kj) else ''
# ★自造之根，其认账亦须自造——否则②之「逐根皆认账」验的就不是闸，是我今天写没写那一行
# ★★★★★【0910·311收尾席·第八度所修——同一形之第八回，而这一回是「自造」两个字只造了一半】
#   ★上一修（第七度）把回执之还原提到①之b 之前，那一处治对了；★★而②这一组仍旧半吊子：
#     **认账只在 `_synth`（自造之根）那一路造，而由「挪开本章回执」开出来的那一路，一行也不造**——
#     於是②所验者不是闸，是「本章之轮记里今天恰好有没有那几行」。
#   ★★★**其所以今日方红、昨日不红（逐条上磁盘核过）**：
#     **昨日末章为310，`grep -c '本章未兑' 版本/第310章/_轮记.md` → 3**（310封版席所落·FS01／FS03／FS05 三行），
#     **回执一挪开，FS闸 复报之三根恰好就是那三根，遂 all(...) 为真，②撞对**；
#     **今日末章为311，`grep -n '本章未兑' 版本/第311章/_轮记.md` → 一行也没有**
#     （311 之三根由其回执答清，本就不须在轮记上认账），**遂 all(...) 为假，②当场红。**
#   ★★★★**故此係测之病，非闸之病，亦非账之欠**：**盘上一根逾期而未答之伏笔也没有**
#     （回执在位时 `_fs.查()` 之 _未答 为空·本席亲跑），**闸之判据一字未动。**
#   ★★★★★**其治：凡此刻 _未答 之根，其认账一律由测自造，验毕逐字还原**——
#     **②之b（抽一根即拦）／①（全抽即拦）之力分毫未减，二者仍由这几行自造之认账验得动。**
_orig = _真orig
_造 = [x for x in _ids if ('%s·本章未兑' % x) not in _真orig]
if _造:
    _orig = _真orig + '\n\n' + ''.join(
        '〔负测自造·验毕即还原〕%s·本章未兑\n' % x for x in _造)
    io.open(_lj, 'w', encoding='utf-8').write(_orig)
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
    if _真orig:
        io.open(_lj, 'w', encoding='utf-8').write(_真orig)
    if _ko:
        io.open(_kj, 'w', encoding='utf-8').write(_ko)
    # ★自造之根须在此还原，且须在「①之b 复原毕」之前——否则那一组验的是一个测自己造出来的欠
    if _canon_orig is not None:
        io.open(_canon, 'w', encoding='utf-8').write(_canon_orig)
# ★★★★★【0910·310封版之序·第七度所修——同一形之第七回，而这一回是「复原毕」四个字没算全】
#   ★①之b 自书其验者为「**复原毕**·其判与测前同」，而复原之物有三样：轮记／开镜卡／canon之根；
#     ★★**第四样没算进去：本章之回执（第82行 os.rename 挪走的那一件）**——
#     它原在第158行方才还原，**在①之b 之後**。
#   ★★★於是①之b 所量者根本不是「复原毕」，是「回执还挪着」那一刻：
#     **回执一挪走，FS闸 即复报三根未答；而本章轮记里恰好写着那三根之认账**
#     （0910 封版席所落·三行「FSxx·本章未兑」），**遂 all(...) 为真，f('') 得 True**；
#     而测前之判 _判前 係在回执还在时取的（ns 空 → `if not ns: return False` → False）。
#     **两个判量的不是同一刻，故必不相等。**
#   ★★★★**其所以今日方红、昨日不红**：昨日轮记里没有那三行认账，
#     那一刻 f('') 亦为 False，**与 _判前 恰好相等——它是撞对的，不是验对的**。
#     ★**一份靠「盘上恰好没有那几个字」才过的测，就是陪跑**（令§六③）。
#   ★★★★★**故治：把回执之还原提到①之b 之前**——**「复原毕」就该是四样全复原**。
#     ⛔**不放松任何一格**：①②两组之判据一字未动；②之c／②之d 照旧在其後复验。
for _p in _rcs:
    os.rename(_p + '.负测暂移', _p)
chk('①之b 复原毕·其判与测前同（证本测未把账改坏）', f(''), _判前)
if _synth:
    chk('②之e 自造之根已还原（测不许留下一笔自己挪过的账）',
        io.open(_canon, encoding='utf-8').read() == _canon_orig, True)
    chk('②之f 自造之认账已抹（轮记须与测前逐字相同）',
        io.open(_lj, encoding='utf-8').read() == _真orig, True)
if _rc:
    chk('②之c 回执已还原（测不许留下一件挪走的档）', all(os.path.exists(_p) for _p in _rcs), True)
    chk('②之d 还原毕·此口自销（回执一交即不走跑轮档之放行）', f('') is False, True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
