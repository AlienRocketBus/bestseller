# -*- coding: utf-8 -*-
"""负测·在场之兑（2026-09-12 立·随 `书级体检._在场` 认「兑」栏同日落）。

★所守者两句：
　①**一笔真兑过的账，须算它的人在场**（不然本书「不点名」之法与此闸永远相犯）；
　②**而「兑」那一栏须记章、记拍号、并逐条列其凭——少一样即不认**
　　（⛔**填不出拍号的账，写一百个「已还」也过不去**）。
★★头一格拿 CHAR-317A 真局回灌；其反证拿 CHAR-315A（只落其形、人未回场、无「兑」栏）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import copy
import io
import json
import os
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账路 = os.path.join(ROOT, '设定', '到期账.json')


def _mod():
    spec = importlib.util.spec_from_file_location(
        '_bk', os.path.join(ROOT, '工具', '书级体检.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def _账():
    d = json.load(io.open(账路, encoding='utf-8'))
    return d if isinstance(d, list) else (d.get('账') or d.get('items') or [])


def 跑():
    m = _mod()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    xs = _账()
    a317 = [x for x in xs if x.get('id') == 'CHAR-317A']
    a315 = [x for x in xs if x.get('id') == 'CHAR-315A']
    判('①', 'CHAR-317A 在账上', bool(a317), True)
    判('②', 'CHAR-315A 在账上', bool(a315), True)
    if not a317:
        print('⛔ 取不着 CHAR-317A，余格不跑'); return 2
    x7 = a317[0]

    # ③【头一格·真局】其兑栏三样俱全
    兑 = x7.get('兑') or {}
    判('③', 'CHAR-317A 之兑栏记章、记拍、列凭三样俱全',
       bool(兑.get('章') and 兑.get('拍') and 兑.get('凭')), True)
    判('④', '其凭逐条不止一条（一条不算逐条）',
       isinstance(兑.get('凭'), list) and len(兑['凭']) >= 3, True)
    判('⑤', 'CHAR-317A 已判 done', x7.get('状态') == 'done', True)

    # ⑥【反证·不许连坐】CHAR-315A（只落其形、人未回场）无兑栏，故不入此路
    if a315:
        判('⑥', 'CHAR-315A 无兑栏（故其 done 不算在场之凭）',
           bool((a315[0].get('兑') or {}).get('拍')), False)

    # ⑦⑧⑨【沙盘·三样缺一即不认】
    fn = getattr(m, 'check_presence', None)
    判('⑦', '书级体检有在场之函（check_presence）', fn is not None, True)
    if fn:
        chs = m.load_chapters()
        # ★★2026-09-24 改其局（⛔牙一格未拔）：364 白文「老头」二字亲数 2（13、217 行），白文那一路之末遂 364 > 诸兑之末 328，
        #   ⑧⑨⑩ 齐塌——**塌的又是这一支测钉的前提（「白文末见早於诸兑」），不是闸**（同 0914 之 ㊩）。
        #   ★故沙盘里把白文之「老头」二字抹去，**只验兑那一路**：⑧ 其末＝诸兑之最大；⑨⑩ 逐笔抽／改 open 即退回。
        #   ⛔而白文那一路之真判，另由 ⑧之三 验其照旧认得（不许为了验兑把白文一路弄瞎）。
        _白末 = fn(chs, copy.deepcopy(xs))[2].get('老头') or 0
        chs = {k: v.replace('老头', '') for k, v in chs.items()}
        base = copy.deepcopy(xs)
        # ★★★★★2026-09-14 改其局（⛔而其牙加了一格，不是拔了一格）：
        #   ⛔旧局把 ⑧⑨⑩ 三格钉死在「老头之末章＝319」与「只动 CHAR-317A 一笔」上；
        #   ★而 328 已把 `CHAR-326A` 真兑（**底下那几页边上的毛两头都不挂，是折进去再压平的**·
        #     由场里的人自己撞见·其兑栏记章 328／记拍二十至二十四／逐条列凭），**其章 328 > 319**——
        #   **於是旧局之 ⑨⑩ 抽掉 317A 那一笔，末章照旧係 328，三格齐塌**；
        #   ⛔**而塌的不是闸，是这一支测自己钉的那个数**（体检账 ㊩ 之同族：**一格钉的是立日那天的数**）。
        #   ★**故改作「照实取其末，且一动就动全部」**：⑧问其实之末与其所出之笔；
        #     ⑨⑩ 把**凡与老头相干之兑逐笔**抽拍号／改 open，**其末须退到白文那一路之数（311）以下或等**——
        #     ★**旧局只动一笔，新局动全部**：**一笔漏网它就报绿，正是它该逮的那一样。**
        老头兑 = [y for y in xs
                  if '老头' in str(y.get('事', '')) and (y.get('兑') or {}).get('拍')]
        _, _, last = fn(chs, copy.deepcopy(xs))
        真末 = max([(y.get('兑') or {}).get('章') or 0 for y in 老头兑] or [0])
        判('⑧', '兑栏俱全者，老头之末章＝盘上诸兑之最大者（今 %s）' % 真末,
           last.get('老头'), 真末)
        判('⑧之二', '其所出之笔在账上找得着（今 %s）'
           % '、'.join(y['id'] for y in 老头兑 if ((y.get('兑') or {}).get('章') == 真末)),
           bool([y for y in 老头兑 if (y.get('兑') or {}).get('章') == 真末]), True)
        判('⑧之三', '白文一路照旧认得（真盘之末 %s ≥ 诸兑之末 %s）' % (_白末, 真末), _白末 >= 真末 > 0, True)
        # 乙·抽掉拍号（⛔凡与老头相干者逐笔抽，一笔不留）：即不认
        bad = copy.deepcopy(xs)
        for y in bad:
            if '老头' in str(y.get('事', '')) and isinstance(y.get('兑'), dict):
                y['兑'].pop('拍', None)
        _, _, last2 = fn(chs, bad)
        判('⑨', '抽掉拍号即不认（老头之末章退回 %d 之前）' % 真末,
           (last2.get('老头') or 0) < 真末, True)
        # 丙·状态改回 open（同样逐笔）：即不认
        bad2 = copy.deepcopy(xs)
        for y in bad2:
            if '老头' in str(y.get('事', '')) and isinstance(y.get('兑'), dict):
                y['状态'] = 'open'
        _, _, last3 = fn(chs, bad2)
        判('⑩', '状态非 done 即不认',
           (last3.get('老头') or 0) < 真末, True)

    # ⑪ 磁盘未被本测改动
    判('⑪', '到期账逐字未动', _账() == xs, True)

    # ══════════════════════════════════════════════════════════
    # ★★★★★★2026-09-16 补第二路（随 `check_presence` 之「这账到期了没有」同日落）
    #   ⛔**沙盘造局，一字不动磁盘**；★**每一格皆验其反面**（⛔旧式也过者即陪跑）。
    # ══════════════════════════════════════════════════════════
    def _局(cur, 末见, 限章):
        """造一部只有『老头』一人之书：末见在第`末见`章，今写到`cur`章，其账限`限章`。"""
        chs = {}
        for c in range(1, cur + 1):
            chs[c] = ('老头把手伸过去。' if c == 末见 else '他把手伸过去。')
        due = [{'id': 'X', '类': '人', '事': '老头缺席之账', '状态': 'open',
                '到期章': 限章}]
        return m.check_presence(chs, due)

    # 〔1119 死规之审·gates10〕①之距逾 lim、lim×2 只印 ⚠、⛔入 bad——⑬⑭⑮⑰ 改验「侦得而只报」：
    #   其状（在役／⚠逾二倍／⚠无账）照分、照印；bad 一律空（人之下落归 人账「投注×下落」判）。
    def _行(rows, who):
        return [x for x in rows if x[0] == who][0]
    # ⑬ 老头之实局：末见 328、今 339、其限 345 —— **未到期，作账在役论**
    _r, _bad, _ = _局(339, 328, 345)
    判('⑬', '⛔账未到期者不判红，且其状照印「未到期」（老头：缺席11章而其限在345）',
       ([b for b in _bad if '老头' in b], _行(_r, '老头')[4], '未到期' in _行(_r, '老头')[5]), ([], True, True))
    # ⑭ 其反面·一：到期了而人仍不回 —— **照旧按 lim*2 侦得，今只印 ⚠**（老头之限 3，二倍 6）
    _r2, _bad2, _ = _局(346, 328, 345)
    判('⑭', '过了那一限仍不回者：照旧侦得（其行 ok=False、印 ⚠ 与限）而⛔入 bad（今346·限345·缺席18章）',
       (_行(_r2, '老头')[4], _行(_r2, '老头')[5].startswith('⚠已挂账'), '345' in _行(_r2, '老头')[5],
        bool([b for b in _bad2 if '老头' in b])), (False, True, True, False))
    # ⑮ 其反面·二·沈鸢那一局（本订所不许放走的那一个）：限早已过去八十五章
    def _局沈(cur, 末见, 限章):
        chs = {}
        for c in range(1, cur + 1):
            chs[c] = ('沈鸢坐下。' if c == 末见 else '他把手伸过去。')
        due = [{'id': 'Y', '类': '人', '事': '沈鸢之账', '状态': 'open', '到期章': 限章}]
        return m.check_presence(chs, due)
    _r3, _bad3, _ = _局沈(295, 210, 210)
    判('⑮', '沈鸢那一局照旧侦得（末见210·限210·今295·缺席85章）——印 ⚠ 而⛔入 bad（〔1119·gates10〕）',
       (_行(_r3, '沈鸢')[4], _行(_r3, '沈鸢')[5].startswith('⚠'), bool([b for b in _bad3 if '沈鸢' in b])),
       (False, True, False))
    # ⑯ 非陪跑之凭：**旧式（不问到期）之下⑬那一局必红**
    _r4, _bad4, _ = _局(339, 328, 345)
    _旧红 = (339 - 328) > m.PRESENCE_LIMIT['老头'] * 2
    判('⑯', '⛔旧式（只比 gap 与 lim*2，不问到期）之下⑬那一局必红，故⑬非陪跑',
       _旧红, True)
    # ⑰ 无账者一格未动
    _chs = {c: '他把手伸过去。' for c in range(1, 340)}
    _r5, _bad5, _ = m.check_presence(_chs, [])
    判('⑰', '逾限而无账者照旧侦得（印「⚠逾限而无账」）而⛔入 bad（〔1119·gates10〕）',
       (_行(_r5, '老头')[4], _行(_r5, '老头')[5].startswith('⚠逾限而无账'), _bad5), (False, True, []))
    # ⑱ 〔1119·gates10〕其罚辞「补回切／插暗线章」⛔再印（照它办即硬塞人声·332之裁）
    判('⑱', '⚠之印里⛔再有「须补回切或插暗线章」之罚辞',
       any('回切' in x[5] or '插暗线' in x[5] for x in _r2 + _r3 + _r5), False)

    print('════ 负测·在场之兑 ════（守：兑须记章记拍列凭，少一样即不认）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
