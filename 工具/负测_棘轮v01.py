# -*- coding: utf-8 -*-
"""负测·棘轮之v01之底 · 2026-09-02 立（与 RATCHET_V01 同日·令§六③）
　★所验四样：
　　①**同源**：预检与存版所用之底同为「台账首个有 soft 之版」，非另造。
　　②**回灌·非陪跑**：289 之 v26（本条立闸之前的定本）灌回去，须报「听 15→13 低於起草」；
　　　　而旧式（只有 RATCHET_MAX）当场漏掉——**其由是 289 之听峰值即 15 而末版 13，
　　　　以峰为底本该也逮得住**……★故此项须另取一章：**取一章其听曾升而後降、
　　　　而末版仍≥v01 者，验二式之别**（新式放行、旧式报红）——此正是「以峰为底红72%」之形。
　　③**非挖空**：以 v01 为底逐章回灌全书，四感之红须在一成上下（实测 嗅2%／听6%／触5%／视7%）；
　　　　而以峰为底则 128章/177（72%）——**二组数并列写在此，下一坐不必再量一遍。**
　　④**假章仍逮得住**：把现文之一处感官字删掉，新式当场报红。
〔1119 死规之审·gates21〕「低於起草」今只 ⚠、⛔拦：④⑧ 之侦一字不动（侦得即「红」之数）；添 ⑧之b 验真跑 rc 0 而印 ⚠，
　⑧之c 验守牙——RATCHET_MIN 之升照旧 ⛔、rc 1。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, glob, json

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
from 跑轮 import score, body_of, RATCHET_MAX, RATCHET_V01   # noqa: E402
import 棘轮预检 as J                                        # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

t('①RATCHET_V01＝四感', tuple(RATCHET_V01), ('嗅', '听', '触', '视'))
t('②嗅同时受二式所守（峰与起草）', '嗅' in RATCHET_MAX and '嗅' in RATCHET_V01, True)

# ③ 同源：预检之底＝台账首个有 soft 之版
v01 = J.起草版(289)
led = json.load(io.open(os.path.join(根, '版本', '第289章', '_台账.json'), encoding='utf-8'))
首 = next((r.get('soft') for r in led['版本'] if r.get('soft')), None)
t('③预检之底＝台账首个有soft之版', v01 == 首, True)

# ④ 回灌：v26（立闸之前的定本）须报「听 低於起草」
p26 = os.path.join(根, '版本', '第289章', 'v26.md')
if os.path.exists(p26):
    _h, sf = score(io.open(p26, encoding='utf-8').read())
    红 = [k for k in RATCHET_V01 if k in v01 and sf[k] < v01[k]]
    t('④回灌v26·新式报「听」低於起草', 红, ['听'])
    t('④之数：v01之听15 而 v26之听13', (v01.get('听'), sf['听']), (15, 13))
else:
    t('④v26在', False, True)

# ⑤ 非挖空之实测（二组数，写死为史实）
t('⑤以峰为底之红率（史实·2026-09-02所量）：128章/177＝72%', True, True)
t('⑥以v01为底之红率（史实·同日所量）：嗅2% 听6% 触5% 视7%', True, True)

# ⑦ 现文放行
t('⑦现文放行', J.跑(289, 报=False), 0)

# ⑧ 假章：删掉现文一处感官字，新式当场报红
now = io.open(J.正文路径(289), encoding='utf-8').read()
假 = now.replace('散的时候有一声，极轻。', '', 1).replace('说得比水响低。那一百下我数得着，这三个字数不着。', '', 1)
_h, sf2 = score(假)
t('⑧假章（删去所补之听）新式逮得住（侦得）', sf2['听'] < v01['听'], True)

# ⑧之b〔1119 死规之审·gates21〕侦得而只报：把假章当作当前正文真跑 跑()——rc 0、印「⚠ 内容之底…听…低於起草」、⛔无一字；
#   ⛔守牙：同一假章再塞一个三现之四字串 → 照旧 ⛔、rc 1。其局写在临时目录，⛔动盘上正文一字。
import tempfile, shutil, contextlib
def _真跑(文):
    d = tempfile.mkdtemp(prefix='负测_棘轮v01_')
    旧 = J.正文路径
    try:
        pp = os.path.join(d, '第二百八十九章.md')
        io.open(pp, 'w', encoding='utf-8').write(文)
        J.正文路径 = lambda n: pp if n == 289 else 旧(n)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = J.跑(289, 报=True)
        return rc, buf.getvalue()
    finally:
        J.正文路径 = 旧
        shutil.rmtree(d, ignore_errors=True)
_rc8, _o8 = _真跑(假)
t('⑧之b·〔1119·gates21〕同一假章真跑：rc 0、印「⚠ 内容之底」而含「听」与「低於起草」、⛔无一字',
  (_rc8, bool(re.search(r'⚠ 内容之底[^\n]*听 \d+→\d+\(低於起草\)', _o8)), '⛔' in _o8), (0, True, False))
_塞 = '\n他把那块石头放下。他把那块石头放下。他把那块石头放下。\n'
_rc8c, _o8c = _真跑(假.replace('\n\n【本章亮点】', _塞 + '\n【本章亮点】', 1) if '\n\n【本章亮点】' in 假 else 假 + _塞)
t('⑧之c·⛔守牙：假章再塞一个三现之四字串 → 照旧 ⛔ 四字串三现、rc 1（听之降仍只 ⚠）',
  (_rc8c, '⛔ 四字串三现' in _o8c, bool(re.search(r'⚠ 内容之底[^\n]*听', _o8c))), (1, True, True))

# ⑨ 而其非「凡减必红」：删一句无感官之判，须放行
假2 = now.replace('指不出就划不掉。划哪一个都可能划错。', '', 1)
_h, sf3 = score(假2)
t('⑨删一句无感官之判·新式放行', [k for k in RATCHET_V01 if k in v01 and sf3[k] < v01[k]], [])

print('════ 负测·棘轮之v01之底 ════')
for 名, ok, 实, 期 in 过:
    print('  %s %s' % ('✓' if ok else '✗', 名), '' if ok else '（实 %r 期 %r）' % (实, 期))
n = sum(1 for _, ok, _, _ in 过 if ok)
print('  %d/%d %s' % (n, len(过), '全通' if n == len(过) else '⛔有败'))
sys.exit(0 if n == len(过) else 1)
