# -*- coding: utf-8 -*-
"""负测·棘轮预检 · 2026-09-01 立（与 工具/棘轮预检.py 同日）
　★令§六③：改闸必同日立负测，且须以旧式回灌验。
　★★而本器之要害不是「会不会报红」，是「它报的红与 --存版 之棘轮闸是不是同一个红」。
　　　一个自己另造一把尺的预检，绿了也不作数（§六③之「陪跑」）。
　★★★故九项之中，④⑤⑥⑦为回灌：拿本坐真撞过棘轮的两版原物灌回去，须逐版报红且所指之串正确。
〔1119 死规之审·gates21〕添 ⑪：嗅／沈鸢之降、四感低於起草 → 只 ⚠、rc 0；四字串三现／顿悟起手之升照旧 ⛔、rc 1（守牙）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, glob, json, tempfile, shutil

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 棘轮预检 as J                                   # noqa: E402
from 跑轮 import score, RATCHET_MIN, RATCHET_MAX, RATCHET_V01       # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

# ①②③ 同源：不许另造尺
t('①所比之项＝跑轮之 RATCHET_MIN', tuple(RATCHET_MIN), ('四字串三现', '顿悟起手'))
t('②所比之项＝跑轮之 RATCHET_MAX', tuple(RATCHET_MAX), ('嗅', '沈鸢'))
t('③量法＝跑轮之 score（非自写）', J.score is score, True)

# ④ 无此章者 rc=2
t('④无此章 rc=2', J.跑(9999, 报=False), 2)

# ⑤⑥ 回灌：本坐真撞过棘轮的两版
#   v14：第5轮补身，「是哪一样」撞成三现（11→12）
#   v16：第6轮承前，「馊压过甜」撞成三现（11→12）
def 灌(vpath, 台账最优):
    """把某一版之文当作当前正文，看预检报不报红、所指之串对不对"""
    txt = io.open(vpath, encoding='utf-8').read()
    _h, sf = score(txt)
    worse = []
    for k in RATCHET_MIN:
        if k in 台账最优 and sf[k] > 台账最优[k]:
            worse.append(k)
    for k in RATCHET_MAX:
        if k in 台账最优 and sf[k] < 台账最优[k]:
            worse.append(k)
    return sf, worse

d = os.path.join(根, '版本', '第289章')
best = {'四字串三现': 11, '顿悟起手': 0, '嗅': 11, '沈鸢': 0}
for v, 串 in (('v14.md', '是哪一样'), ('v16.md', '馊压过甜')):
    p = os.path.join(d, v)
    if not os.path.exists(p):
        t('⑤%s 在' % v, False, True); continue
    sf, worse = 灌(p, best)
    t('⑤%s 回灌·棘轮报红' % v, worse, ['四字串三现'])
    t('⑥%s 回灌·所增之串正是「%s」' % (v, 串),
      串 in J.三现串(io.open(p, encoding='utf-8').read()), True)

# ⑦ 旧式（无此器时）之实：那两版当日皆存版成功而後补存 —— 即「事後才知」
led = json.load(io.open(os.path.join(d, '_台账.json'), encoding='utf-8'))
补存 = [r for r in led['版本'] if '补存' in (r.get('说明') or '')]
t('⑦旧式之害留有实证：台账中确有补存之版', len(补存) >= 1, True)

# ⑧ 不挖空：拿现文之最优当底，预检须放行（新器不许把好的判红）
t('⑧现文放行', J.跑(289, 报=False), 0)

# ⑨ 造一假章：把现文之一词重复三次，预检须逮住
p = J.正文路径(289)
txt = io.open(p, encoding='utf-8').read()
假 = txt.replace('我把本子合上收进怀里。',
                 '我把本子合上收进怀里。合上收进怀里。合上收进怀里。', 1)
_h, sf0 = score(txt)        # ★底取现文自身，不许写死一个数——
_h, sf = score(假)          #   写死的数会随文而陈（本器⑨於289第8轮即因此自败一回）
t('⑨假章（一串三现）预检逮得住', sf['四字串三现'] > sf0['四字串三现'], True)

# ⑩ 四感删证（2026-09-05·305第8、9两轮所立·欠-305A之治）
#    ★其红在哪一行：二回减法轮各减一句转述，器只印「听 14→13」而不印那一句是什么。
#    ★★旧式即「无此块」——其判据里没有「所删之句」这一样，故它对二回一言不发。
import re as _re
_旧文 = 'A他说硬，针上说一响。B我把手贴上去。C那十道白是直的。'
_新文 = 'B我把手贴上去。C那十道白是直的。'
_切 = lambda t: [x for x in _re.split(r'[。！？\n]', t) if x.strip()]
_有 = set(_切(_新文))
_删 = [x for x in _切(_旧文) if x not in _有]
t('⑩造一处「删一句转述」之局：所删恰一句', len(_删), 1)
t('⑩之二·所删之句含「听」之字（响）', bool(_re.search(J._感式['听'], _删[0])), True)
t('⑩之三·所留之句不入表（不许把没删的算成删的）',
  any(_re.search(J._感式['触'], x) for x in _有), True)
t('⑩之四·器认得四感四样，与 RATCHET_V01 同源（§六④）',
  sorted(J._感式) == sorted(RATCHET_V01), True)
t('⑩之五·旧式（判据里无「所删之句」）对同一局一言不发', hasattr(J, '_四感删证'), True)

# ⑪〔1119 死规之审·gates21〕RATCHET_MAX（嗅／沈鸢对末版降）与 RATCHET_V01（四感低於起草）→ ⚠ 只报、rc 0；
#    ⛔守牙：RATCHET_MIN（四字串三现／顿悟起手）对末版升 → 照旧 ⛔、rc 1。
#    其局：正文取 289 现文（只读），末版／起草版／最优／拆章 四函换桩，⛔写盘一字。
import contextlib as _cl
def _局跑(末=None, v01=None):
    旧 = (J.末版, J.起草版, J.最优, J._末版係拆章前, J._拆出章)
    J.末版 = lambda n: (dict(末 or {}), 'v桩')
    J.起草版 = lambda n: dict(v01 or {})
    J.最优 = lambda n: {}
    J._末版係拆章前 = lambda n, 档=None: (0, None)
    J._拆出章 = lambda n: None
    buf = io.StringIO()
    try:
        with _cl.redirect_stdout(buf):
            rc = J.跑(289, 报=True)
    finally:
        J.末版, J.起草版, J.最优, J._末版係拆章前, J._拆出章 = 旧
    return rc, buf.getvalue()
_h, _今 = score(io.open(J.正文路径(289), encoding='utf-8').read())
_末MAX = dict(_今, 嗅=_今['嗅'] + 1, 沈鸢=_今['沈鸢'] + 1)
_rcA, _oA = _局跑(末=_末MAX)
t('⑪嗅／沈鸢对末版各降一 → rc 0、印「⚠ 内容之底」二行、⛔无一字（起草闸.红行 见⛔即红）',
  (_rcA, _oA.count('⚠ 内容之底'), '⛔' in _oA), (0, 2, False))
_rcB, _oB = _局跑(末=dict(_今), v01=dict(_今, 听=_今['听'] + 1, 视=_今['视'] + 1))
t('⑪之二·听／视低於起草 → rc 0、印「⚠ 内容之底…低於起草」二行、⛔无一字',
  (_rcB, _oB.count('(低於起草)'), '⛔' in _oB), (0, 2, False))
_rcC, _oC = _局跑(末=dict(_今, 四字串三现=_今['四字串三现'] - 1))
t('⑪之三·⛔守牙：四字串三现对末版升 → 照旧 ⛔、rc 1',
  (_rcC, '⛔ 四字串三现' in _oC), (1, True))
_rcD, _oD = _局跑(末=dict(_末MAX, 顿悟起手=_今['顿悟起手'] - 1), v01=dict(_今, 听=_今['听'] + 1))
t('⑪之四·⛔守牙：顿悟起手升而嗅降、听低於起草 → rc 1；⛔只落在顿悟起手，余二样只 ⚠',
  (_rcD, [l.strip().split()[1] for l in _oD.split('\n') if l.strip().startswith('⛔ ')],
   '⚠ 内容之底' in _oD), (1, ['顿悟起手'], True))
print('════ 负测·棘轮预检 ════')
for 名, ok, 实, 期 in 过:
    print('  %s %s' % ('✓' if ok else '✗', 名), '' if ok else '（实 %r 期 %r）' % (实, 期))
n = sum(1 for _, ok, _, _ in 过 if ok)
print('  %d/%d %s' % (n, len(过), '全通' if n == len(过) else '⛔有败'))
sys.exit(0 if n == len(过) else 1)
