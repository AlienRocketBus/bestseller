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
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
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
    # ★★★★★2026-09-14 改其引之键（⛔非放宽，是归一）：
    #   ⛔0913 亲数：一笔账销了，其章在盘上有三种写法——`清偿章` 133／`结账章` 11／`清账章` 1，
    #     **而 `书级体检::check_due_net` 只读 `清偿章`**，故那十二笔在闸眼里从来没有销过（体检账 ㊯）。
    #   ★今已归一作 `清偿章`，本格随之改引；**其所验之事一字未改**：那三笔仍须状态「清」、其章仍须 301。
    chk('②那三笔在账上，且状态皆係「清」、清偿章皆係301',
        len(三笔) == 3 and all(o.get('状态') == '清' and o.get('清偿章') == 301 for o in 三笔))

    # ③旧式回灌须报红（非陪跑）
    chk('③旧表（无「清」）回灌那三笔：三笔皆判「未清」——故此改非陪跑',
        all(o.get('状态') not in old for o in 三笔))
    # ④新式须放行
    chk('④新表：三笔皆判已清', all(o.get('状态') in cur for o in 三笔))

    # ⑤此改非挖空：open 照旧催得着
    # ★★★★★2026-09-09·307封版之序自逮（案席）：**本格原以「账上现有几笔 open」为凭**
    #   （`len(opens) >= 1`）——★而 307 封版之日，末二笔 open（DEBT-297C／DEBT-298A）当场结清，
    #   **全表 open 之数归零，本格遂当场判红**；★★**而那一红报的不是伤，是「账还完了」**。
    #   ★★★即：**一道负测把它的判据挂在活数据上，於是活干完了它就喊**——
    #     **闸错了，当场说出来，不去把 open 之数凑回一笔来让它绿**（那才是真挖空）。
    #   ★★★★故改：**不问账上有没有 open，改回灌一笔造出来的 open**——
    #     **它须照旧判「未清」**；★**如此则本格与账上还剩几笔无干，而它所守的那一样（词表不许把 open 也放进去）反而更紧。**
    opens = [o for o in items if o.get('状态') == 'open']
    造 = {'id': 'NEG-OPEN-回灌', '状态': 'open', '到期章': 1}
    chk('⑤而新表未挖空：回灌一笔 open 须照旧判「未清」（账上现有 open %d 笔·不作判据）' % len(opens),
        造.get('状态') not in cur and all(o.get('状态') not in cur for o in opens))

    # ⑥其群：全表之状态全集，逐样列得出（令§六④）
    st = {}
    for o in items:
        st[str(o.get('状态'))] = st.get(str(o.get('状态')), 0) + 1
    # ★★★★★2026-09-09·同日同因改（案席）：本格原钉死「其全集恰係那六样」，
    #   ★而 open 归零之後，全集只剩五样，本格亦当场判红——**同一处伤，两个格一起喊。**
    #   ★★故改：**判其为那六样之子集，且不许空**——
    #     **多出一样没登记过的状态词照旧当场红**（这正是本器立法之由：一坐写下一个新词，闸跟不上），
    #     **而少一样只说明那一类的账还完了，不是伤**；★★★并把今日之全集逐样印出来，供人看。
    知 = {'done', 'closed', 'cold', 'half', 'open', '清'}
    chk('⑥全表266项上下，其状态之全集须係已登记之六样之子集且不空（今 %s）'
        % '／'.join('%s%d' % (k, v) for k, v in sorted(st.items())),
        len(items) >= 200 and st and set(st) <= 知)

    # ⑦而「清」是少数，其群小而其害大：三笔全在同一坐写下
    # ★★★★★2026-09-14 改其判（⛔而牙未拔，反加一格）：
    #   ⛔旧格钉死「『清』只 3 笔」——**而 328 已把 `PLOT-328A` 真清**（那一条界离齿口两指，其尺已钉死），
    #     **於是这一格一到第四笔就自栽**；**其所栽者不是闸，是它自己钉的那个数**（体检账 ㊩ 之同族）。
    #   ★故改作**照实取其数，而逐笔须有其清偿章**；★★**并留旧三笔同係 301 那一问**（一坐一新词之据）；
    #   ★★★**新加一格之牙**：**凡状态作「清」者，`清偿章` 一个也不许缺**——**缺其章即是空口一个「清」字。**
    _清 = [o for o in items if o.get('状态') == '清']
    chk('⑦「清」共 %d 笔，旧三笔之清偿章同係 301（一坐一新词）' % len(_清),
        st.get('清') == len(_清) and len({o.get('清偿章') for o in 三笔}) == 1
        and {o.get('清偿章') for o in 三笔} == {301})
    chk('⑦之二·⛔凡作「清」者，清偿章一个不许缺（缺其章即空口一个「清」字）',
        all(isinstance(o.get('清偿章'), int) for o in _清))

    # ⑧批123之旧订仍在（closed 不许被本次改动挤掉）
    chk('⑧批123所补之 closed 仍在词表内', 'closed' in cur)

    # ⑨而词表未被扩成「什么都算清」：open 与空值皆不在
    chk('⑨词表未挖空：open 与 None 皆不在其内',
        'open' not in cur and 'None' not in cur and '' not in cur)

    print('  ── %d/%d %s ──' % (OK[0], OK[1], '全通' if OK[0] == OK[1] else '有红'))
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
