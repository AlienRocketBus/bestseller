# -*- coding: utf-8 -*-
"""负测·验收空说明只查不存（批131·293第3轮所立·第二十四犯第二形之根治）
所治之伤：`--验收 N` 不带说明时自动存版并落一行占位说明。
        其果是一个来回，一坐之内我走了六回：
        做完活 → 跑一次不带说明的 --验收 查硬项 → 它把版存了 →
        我带着说明再存，空轮闸判「正文与末版逐字相同」→ 拦 → 回头 --填记。
数其群（令§六①②）：全书台账 3,352 版，占位行旧史只 1 行（第101章 v03）；
        **而今日一坐造出 8 行**——群不在旧史里，在今日这一坐里，而它是同一个口。
本测所验者为不变量，非快照：
  ①不带说明之 --验收：只查不存（台账一行不动）；
  ②带说明者照旧存版（批103之单一入口未动，只少了「空说明也存」这一路）；
  ③而填记口未被删——旧史那些占位行还得有路可填；
  ④其语须说得出「只查不存」四字，且给出带说明之写法。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, json, glob, shutil, tempfile, subprocess
_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

_jc = io.open(os.path.join(_D, '小说检察官.py'), encoding='utf-8').read()
chk('①空说明之路须 return，不落占位', "print('  ⚠说明未填：**本次只查不存**（不落占位行）。')" in _jc, True)
chk('①之b 且其 return 在 _m.save 之前（落了再回头等於没改）',
    _jc.find('本次只查不存') < _jc.find("_m.save(n, note or"), True)
chk('②带说明者照旧存版（单一入口未动）', "_m.save(n, note or" in _jc, True)
chk('④其语须给出带说明之写法', '--验收 %d "第N轮·某庭：所改何事"' in _jc, True)
chk('④之b 并须说明「带说明者照旧自动存版」（免得读成「验收不再存版」）',
    '带说明者照旧自动存版' in _jc, True)
_pl = io.open(os.path.join(_D, '跑轮.py'), encoding='utf-8').read()
chk('③填记口未被删（旧史之占位行还得有路可填）', "cmd == '--填记'" in _pl, True)
chk('③之b 而占位之文仍在跑轮一侧（填记口据之认洞）', '_占位 = ' in _pl, True)

# ── 实跑：一间沙盘，验「不带说明跑一回，台账一行不动」 ──
tmp = tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(tmp, '工具'))
    for f in ('小说检察官.py', '跑轮.py', '硬闸.py', '法典闸.py'):
        s = os.path.join(_D, f)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(tmp, '工具', f))
    os.makedirs(os.path.join(tmp, '正文'))
    os.makedirs(os.path.join(tmp, '设定'))
    vd = os.path.join(tmp, '版本', '第996章'); os.makedirs(vd)
    io.open(os.path.join(vd, '_台账.json'), 'w', encoding='utf-8').write(json.dumps(
        {'章': 996, '版本': [{'版': 'v01', '说明': '第1轮·起草', 'hard': {}, 'soft': {'净重': 2000}}]},
        ensure_ascii=False, indent=1))
    io.open(os.path.join(vd, 'v01.md'), 'w', encoding='utf-8').write('旧文\n')
    io.open(os.path.join(tmp, '正文', '镇冢秘术_第九百九十六章_试.md'), 'w',
            encoding='utf-8').write('《镇冢秘术》\n\n第九百九十六章　试\n\n新文。\n')
    def 版数():
        return len(json.load(io.open(os.path.join(vd, '_台账.json'), encoding='utf-8'))['版本'])
    _before = 版数()
    # 直调 jj_hook（不跑整个验收，免其别的红把本项带偏）
    import importlib.util as iu
    _sp = iu.spec_from_file_location('_jc996', os.path.join(tmp, '工具', '小说检察官.py'))
    _m996 = iu.module_from_spec(_sp)
    _cwd = os.getcwd()
    try:
        os.chdir(tmp)
        _sp.loader.exec_module(_m996)
        import contextlib, io as _io
        _buf = _io.StringIO()
        with contextlib.redirect_stdout(_buf):
            _m996.jj_hook(996, '')
        _out = _buf.getvalue()
    finally:
        os.chdir(_cwd)
    chk('①之c 沙盘·不带说明跑一回，台账一行不动', 版数(), _before)
    chk('①之d 且其语印出「只查不存」', '只查不存' in _out, True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ⑤回灌：全书占位行之数（旧史１，今日之８已逐行填毕）
_占 = 0
for f in glob.glob(os.path.join(_R, '版本', '*', '_台账.json')):
    try:
        for r in json.load(io.open(f, encoding='utf-8'))['版本']:
            if str(r.get('说明', '')).startswith('（本轮说明未填'):
                _占 += 1
    except Exception:
        pass
chk('⑤全书占位行今须≤2（旧史第101章 v03 之外，今日所造者已逐行填毕）', _占 <= 2, True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
