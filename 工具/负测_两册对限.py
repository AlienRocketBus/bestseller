# -*- coding: utf-8 -*-
"""负测·两册对限（2026-09-04·300第7轮立）

★所治之伤：2026-09-04 本坐把 PRES-297B刘二 之限由300改作301，同笔改了四处档，
　**而 `设定/到期账.json` 照旧写着 300，三坐无人看见**——直到第7轮五钩之口把它印出来。
★★本测断三样：①今日二册同限｜②回灌真犯之原物（刘二放回300）须报红｜③其主口拦得动。
★★★而本测断的是不变之则，不是今日之天气（第二十八犯之戒）。

★★★★2026-09-04·301封版之序改（令§五：报与场不合者以场为准，且当场正其报）：
　★原①②③三条钉在「东头｜刘二二笔仍 open」这一处快照上；
　★★而301封版之序把 PRES-297A／PRES-297B 二笔逐笔判「清」，**二册遂不再认得上它们**——
　　**那不是伤，那正是账清了**；★★★故三条今日皆假红。
　★★★★照其本意重述：**所守者是「凡两册都认得上的一笔，其限须同」**，
　　**而其料不再取自今日之活账，由本测自己在沙盘上造一对**——
　　**造得出、改得动、报得准，方算它逮得住**（旧式回灌之验仍在，见②之旧）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
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
    chk('①今日二册认得上者，逐笔同限（其数随账之清而变，不钉死在某二笔上）',
        badp, [])

    # ①之b 沙盘：自挂账取一笔活的，往到期账里造一条同形之新账，二册即认得上
    挂 = M.读挂()
    chk('①之b 挂账里须有活的挂笔（无则本测取不着料）', bool(挂), True)
    名0, 限0, 形0 = 挂[0]
    def 造(限):
        d = json.loads(原)
        d['items'].append({'id': '_NEG-两册', '类': '测', '事': 形0,
                           '立账章': 1, '到期章': 限, '状态': 'open'})
        json.dump(d, io.open(M.到期, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
    造(限0)
    p1, b1 = M.对()
    chk('①之c 造一对同限之笔 → 二册认得上，且不报红',
        (名0 in [x[0] for x in p1], b1), (True, []))

    # ②旧式回灌（其形即2026-09-04所治之真伤：一册改了限，另一册没跟着改）
    造(限0 + 1)
    _, bad2 = M.对()
    chk('②回灌真犯之形（一册改限而另一册没跟着）→ 须报红',
        [x[0] for x in bad2], [名0])
    io.open(M.到期, 'w', encoding='utf-8').write(原)
    _, bad2b = M.对()
    chk('②之b 撤回即复绿', bad2b, [])

    # ③逐笔而判，非一坏俱坏：造二笔，只歪其一
    d3 = json.loads(原)
    for _i, (_n, _x, _f) in enumerate(挂[:2]):
        d3['items'].append({'id': '_NEG-%d' % _i, '类': '测', '事': _f,
                            '立账章': 1, '到期章': _x + (1 if _i == 0 else 0),
                            '状态': 'open'})
    json.dump(d3, io.open(M.到期, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    _, bad3 = M.对()
    chk('③只歪一笔 → 只报那一笔，不牵连另一笔',
        [x[0] for x in bad3], [挂[0][0]])
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
