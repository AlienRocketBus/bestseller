# -*- coding: utf-8 -*-
"""★负测·到期账之「已清」词表（303第1轮立）。

★其红在哪一行：`python3 工具/小说检察官.py --全书检` 於303报
  「到期账逾期2章未清: [PRES-297A]／[PRES-297B]／[PROM-295.83]（限第301章）」三笔，
  而三笔在 `设定/到期账.json` 里状态皆係「清」、结账章皆係 301、
  且其「判」逐笔写着「2026-09-04·301第13轮毕·封版之序判「清」」——
  ★★**账已清而闸照旧催，催的是已经还过的三笔。**

★★★它认哪几样，本书同类共几样（令§六④）：
  **它认的是 `_CLEARED_STATES` 那一串状态词**；
  **本书同类**：`设定/到期账.json` 全表 266 项，其状态之全集只六样——
  **done 247｜closed 9｜cold 3｜half 1｜open 3｜清 3**；
  ★**「清」只此三笔，而三笔同出於 301 封版那一坐**——
  ★★**即：一坐写下的一个新词，闸就跟不上；而这已是第二回**（批123之 closed 是头一回）。

★★★★而其治照批123之例：补机器之词表，不改账——「清」是本书判账之本字。
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OK = [0, 0]


def chk(name, cond):
    OK[1] += 1
    if cond:
        OK[0] += 1
        print('  ✓ %s' % name)
    else:
        print('  ⛔ %s' % name)


def main():
    print('\n████ 负测 · 到期账词表 ████')
    src = io.open(os.path.join(ROOT, '工具', '小说检察官.py'), encoding='utf-8').read()
    m = re.search(r"_CLEARED_STATES = \(([^)]*)\)", src)
    chk('①码里找得着 _CLEARED_STATES', m is not None)
    cur = tuple(x.strip().strip("'\"") for x in m.group(1).split(',') if x.strip()) if m else ()
    old = tuple(x for x in cur if x != '清')

    acct = json.load(io.open(os.path.join(ROOT, '设定', '到期账.json'), encoding='utf-8'))
    items = acct['items']
    三笔 = [o for o in items if o.get('id') in ('PRES-297A', 'PRES-297B', 'PROM-295.83')]
    chk('②那三笔在账上，且状态皆係「清」、结账章皆係301',
        len(三笔) == 3 and all(o.get('状态') == '清' and o.get('结账章') == 301 for o in 三笔))

    # ③旧式回灌须报红（非陪跑）
    chk('③旧表（无「清」）回灌那三笔：三笔皆判「未清」——故此改非陪跑',
        all(o.get('状态') not in old for o in 三笔))
    # ④新式须放行
    chk('④新表：三笔皆判已清', all(o.get('状态') in cur for o in 三笔))

    # ⑤此改非挖空：open 之三笔照旧催得着
    opens = [o for o in items if o.get('状态') == 'open']
    chk('⑤而新表未挖空：状态 open 者仍不在词表之内（其数 %d）' % len(opens),
        len(opens) >= 1 and all(o.get('状态') not in cur for o in opens))

    # ⑥其群：全表之状态全集，逐样列得出（令§六④）
    st = {}
    for o in items:
        st[str(o.get('状态'))] = st.get(str(o.get('状态')), 0) + 1
    chk('⑥全表266项上下，其状态之全集只六样（done/closed/cold/half/open/清）',
        len(items) >= 200 and set(st) == {'done', 'closed', 'cold', 'half', 'open', '清'})

    # ⑦而「清」是少数，其群小而其害大：三笔全在同一坐写下
    chk('⑦「清」只 3 笔，且三笔之结账章同係 301（一坐一新词）',
        st.get('清') == 3 and len({o.get('结账章') for o in 三笔}) == 1)

    # ⑧批123之旧订仍在（closed 不许被本次改动挤掉）
    chk('⑧批123所补之 closed 仍在词表内', 'closed' in cur)

    # ⑨而词表未被扩成「什么都算清」：open 与空值皆不在
    chk('⑨词表未挖空：open 与 None 皆不在其内',
        'open' not in cur and 'None' not in cur and '' not in cur)

    print('  ── %d/%d %s ──' % (OK[0], OK[1], '全通' if OK[0] == OK[1] else '有红'))
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
