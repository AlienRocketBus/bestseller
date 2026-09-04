# -*- coding: utf-8 -*-
"""负测·两册对限（2026-09-04·300第7轮立）

★所治之伤：2026-09-04 本坐把 PRES-297B刘二 之限由300改作301，同笔改了四处档，
　**而 `设定/到期账.json` 照旧写着 300，三坐无人看见**——直到第7轮五钩之口把它印出来。
★★本测断三样：①今日二册同限｜②回灌真犯之原物（刘二放回300）须报红｜③其主口拦得动。
★★★而本测断的是不变之则，不是今日之天气（第二十八犯之戒）。
"""
import io, json, os, sys
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = _iu.spec_from_file_location('_lc', os.path.join(ROOT, '工具', '两册对限.py'))
M = _iu.module_from_spec(_s); _s.loader.exec_module(M)

原 = io.open(M.到期, encoding='utf-8').read()
ok = bad = 0


def chk(名, 得, 期):
    global ok, bad
    if 得 == 期:
        ok += 1; print('  ✓ %s' % 名)
    else:
        bad += 1; print('  ✗ %s ← 得 %r，期 %r' % (名, 得, 期))


def 写限(pid, n):
    d = json.loads(原)
    for it in d['items']:
        if it.get('id') == pid:
            it['到期章'] = n
    json.dump(d, io.open(M.到期, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


try:
    print('════ 负测·两册对限 ════')
    pair, badp = M.对()
    chk('①两册认得上者须为2对（东头｜刘二）', sorted(x[0] for x in pair), ['东头', '刘二'])
    chk('①之b今日二册逐笔同限', badp, [])

    # ②旧式回灌：把刘二那一笔放回它原来的到期章300 → 须报红
    写限('PRES-297B', 300)
    _, bad2 = M.对()
    chk('②回灌真犯之原物（到期账·刘二·限300）→ 须报红', [x[0] for x in bad2], ['刘二'])
    io.open(M.到期, 'w', encoding='utf-8').write(原)
    _, bad2b = M.对()
    chk('②改回301 → 须复绿', bad2b, [])

    # ③另一笔（东头）单独改，须只报它一笔（证其逐笔而判，非一坏俱坏）
    写限('PRES-297A', 999)
    _, bad3 = M.对()
    chk('③只改东头一笔 → 只报东头，不牵连刘二', [x[0] for x in bad3], ['东头'])
    io.open(M.到期, 'w', encoding='utf-8').write(原)

    # ④二册之一不在，本器不许瞎判（宁可不认，不许假认）
    os.rename(M.到期, M.到期 + '.bak')
    try:
        p4, b4 = M.对()
        chk('④到期账不在 → 认不上，亦不报红', (p4, b4), ([], []))
    finally:
        os.rename(M.到期 + '.bak', M.到期)

    # ⑤其主口拦得动
    src = io.open(os.path.join(ROOT, '工具', '两册对限.py'), encoding='utf-8').read()
    chk('⑤其主口拦得动（见 sys.exit(1 if _b ...)）', 'sys.exit(1 if _b' in src, True)
    chk('⑤之b并自印「其余N笔只在一册上，本器一个字也不说」（§一⑤）', '一个字也不说' in src, True)
finally:
    io.open(M.到期, 'w', encoding='utf-8').write(原)

print('  ── %d/%d %s ──' % (ok, ok + bad, '全通' if bad == 0 else '⛔未过'))
sys.exit(0 if bad == 0 else 1)
