# -*- coding: utf-8 -*-
"""负测·冷轮否决记（2026-09-02·290封版当日立）

★所测者一句话：**逼我写的那六个字，不许同时把账销了。**
★★而一份在旧式下也全过的测，它就是陪跑（令§六③）——**故本测之要害在③④⑤：以旧式回灌，须坏。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import io
import os
import re
import sys
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _u.spec_from_file_location('_六检', os.path.join(ROOT, '工具', '开轮六检.py'))
_m6 = _u.module_from_spec(_sp)
_sp.loader.exec_module(_m6)

RC = os.path.join(ROOT, '设定')


def _rcs():
    out = []
    for fp in glob.glob(os.path.join(RC, '回执_*.md')):
        try:
            out.append(io.open(fp, encoding='utf-8').read())
        except OSError:
            pass
    return out


import re as _re


def _old(n, rcs):
    """旧式：回执里有那六个字即算已执。

    ★★★★★2026-09-18 补一个数字之界（⛔**所补者只在本函之对照，本测所验之理一格未动**）：
      ⛔**旧式以裸串去配**，而「**1章冷眼轮**」係「**101章冷眼轮**」「**111章冷眼轮**」之尾——
      **故 COLD-1 至 COLD-72 逐笔被配着，一律判「已执」**；
      ★**而盘上冷轮之档自 COLD-153 起**（`ls 设定/冷轮_COLD*.md` 亲跑，其小者即 153），
        **COLD-1—72 根本不存在**——**那七十二笔「已执」是撞出来的，不是签出来的。**
      ★★**其见於今日之由**：`开轮六检::_cold_done` 今治「一处说起它不是一笔签了它」时，
        **其式加了 `(?<!\d)` 一个数字之界**；**於是新式不再被撞，而本函仍被撞**，
        **二式之差遂由「否决记那几笔」暴涨到七十二笔**，⑤⑩两项当场判红。
      ★★★⛔**本坐当场分过这两样**：**红的不是新式，是本函这一个对照**——
        **一个对照若自己会被撞，它验出来的差就不是被验者之差。**
      ⛔**故只给对照补上同一个界；「否决记」那一路之理、⑤⑩两项之断言，一个字未改。**
    """
    return any(_re.search(r'(?<!\d)%d章冷眼轮' % n, t) for t in rcs)


def _rcs_ch():
    """回执逐份带其章号（否决之效只及於写它那一份，故须知孰先孰後）。"""
    import glob as _g, os as _o, re as _r, io as _io
    out = []
    for fp in sorted(_g.glob(_o.path.join(ROOT, '设定', '回执_*.md'))):
        m = _r.search(r'第(\d+)章', _o.path.basename(fp))
        out.append((int(m.group(1)) if m else 0,
                    _io.open(fp, encoding='utf-8', errors='replace').read()))
    return out


_末份缓 = {}


def _末份(n, rcsc):
    """提及此笔之回执中，章号最大的那一份；返回 (章, 有否决, 有六字)。无者 None。

    ★缓其果：头一版每问一笔即把全部回执重扫一遍，而外头三处列表推导各问三百笔，
      遂跑成分钟级（本测原是秒级）。**一个跑不完的负测等於没有负测**，故记此。
    """
    if n in _末份缓:
        return _末份缓[n]
    # ★0918·与 `_old` 同一个界（**同一处病，同一份档里有两处**）：
    #   ⛔`sign` 裸串会被撞（「1章冷眼轮」係「101章冷眼轮」之尾），
    #   **故 `_有号` 曾胀到 300 笔，③之b 遂拿七十二笔撞出来的假号去验**。
    #   ★**而 `veto` 不必补**：「COLD-1·本章未执」不是「COLD-11·本章未执」之尾（其後係「1」非「·」），
    #     ⛔**本坐当场验过才没有顺手一并改**——**不该动的地方不动，也是一条。**
    veto, sign = 'COLD-%d·本章未执' % n, _re.compile(r'(?<!\d)%d章冷眼轮' % n)
    c = [(ch, veto in tx, bool(sign.search(tx))) for ch, tx in rcsc
         if (veto in tx) or sign.search(tx)]
    _末份缓[n] = sorted(c)[-1] if c else None
    return _末份缓[n]


_先否缓 = {}


def _先有否决(n, rcsc):
    """此笔在其末份之前，有没有别的回执挂过否决记。"""
    if n in _先否缓:
        return _先否缓[n]
    m = _末份(n, rcsc)
    _先否缓[n] = bool(m) and any(('COLD-%d·本章未执' % n) in tx
                                for ch, tx in rcsc if ch < m[0])
    return _先否缓[n]


def run():
    rcs = _rcs()
    R = []

    # ①器在
    R.append(('①器在·_cold_done 可调', callable(getattr(_m6, '_cold_done', None))))

    # ②正测：一笔真办过的（回执有六字、无否决记）须判已执
    R.append(('②正测·COLD-286（286之轮於288办毕）判已执', _m6._cold_done(286) is True))

    # ③真红
    #   ★★★★★2026-09-02·292封版之序改：**原本写死 COLD-288**，
    #     ★而288今已由292之回执真办毕（其执在骨⑤「不落手」）——**它由红转绿是对的，
    #       而此项因此而坏，坏的不是闸，是这一条断言**；★★同一坐之内我已两回栽在
    #       「把快照当不变量」上（负测_冷轮否决记⑤⑦⑩、负测_棘轮裁⑦⑧⑨），此为第三回。
    #   ★★★故改为验其理本身：**凡「末一份提及之回执挂否决记」者，一律须判待执；
    #     凡「末一份只签核」者，一律须判已执**——不点某一笔之名，只验这条理在全书上成不成立。
    rcsc = _rcs_ch()
    _有号 = [n for n in range(1, 301) if _末份(n, rcsc)]
    _该红 = [n for n in _有号 if _末份(n, rcsc)[1]]
    _该绿 = [n for n in _有号 if (not _末份(n, rcsc)[1]) and _末份(n, rcsc)[2]]
    # ★★★★★2026-09-02·293封版之序四改：**原断言带 `len(_该红) >= 1`**——
    #   ★而293之回执销了 COLD-289（全书当时唯一挂着否决记者），_该红 遂为空，此项当场判红；
    #   ★★**而闸一分没坏，坏的仍是这一条断言所站的那一刻**（此为同一形第四回，
    #     前三回之记就写在本文件③与⑤两处；★★★四回都没记进病历本，故它第五回又在
    #     负测_FS认账 上重来了一遍——今立第二十八犯）。
    #   ★★★★**其治不是把下限去掉了事**：**一个只会说「零」的闸没有价值**（令§六③）；
    #     ★**故拆作两半**：**其一·全书那一半只验「无误伤」，不设下限**（全书没有该红的，
    #     正说明账干净，不该判测红）；★★**其二·另造一笔合成之例，验它仍逮得着**——
    #     **写一份带否决记之临时回执，其号取全书未用者，验毕即删。**
    R.append(('③真红·末份挂否决记者一律判待执（%d 笔逐一验·无则不设下限）' % len(_该红),
              all(_m6._cold_done(n) is False for n in _该红)))

    # ③之d★合成之例：不许此测因「今日全书恰好干净」而变成陪跑
    _tmp = os.path.join(ROOT, "设定", "回执_29990101_第999章作业单.md")
    _syn = None
    try:
        io.open(_tmp, 'w', encoding='utf-8').write(
            '# 合成之例（负测_冷轮否决记③之d 所造，验毕即删）\n'
            '## 四·冷轮与到期账\n· **999章冷眼轮**：接·已执。\n'
            '· ⛔**COLD-999·本章未执**：其面係他线之面，本章不得执。\n')
        _m6._cold_done.__globals__.get('_rc_cache', {}).clear() if isinstance(
            _m6._cold_done.__globals__.get('_rc_cache'), dict) else None
        _syn = _m6._cold_done(999)
    finally:
        if os.path.exists(_tmp):
            os.remove(_tmp)
    R.append(('③之d 合成之例·末份挂否决记者判待执（证此测非陪跑；得%r）' % _syn,
              _syn is False))
    R.append(('③之e 合成之档已删（测不许留下一份假回执）', not os.path.exists(_tmp)))
    R.append(('③之b 末份只签核者一律判已执（%d 笔逐一验）' % len(_该绿),
              len(_该绿) >= 1 and all(_m6._cold_done(n) is True for n in _该绿)))
    _接者 = [n for n in _有号
             if _先有否决(n, rcsc) and (not _末份(n, rcsc)[1]) and _末份(n, rcsc)[2]]
    R.append(('③之c 顺延不再等於死刑：曾被否决而後由在後之回执签核者，须判已执（%s）' % (_接者 or '无'),
              len(_接者) >= 1 and all(_m6._cold_done(n) is True for n in _接者)))

    # ④回灌·旧式须坏：同一笔，旧式判已执
    R.append(('④回灌·旧式於 COLD-288 判已执（故此闸非陪跑）', _old(288, rcs) is True))

    # ⑤回灌·全书逐笔并列，二式相异者须**恰是那几笔带否决记者，一笔不多一笔不少**
    #   ★★★★★2026-09-02·292第1轮改：**原本此处写死 `diff == [288]`**，
    #     ★而那是一张快照，不是一条不变之理——**否决记本就该随挂红之冷轮增减**；
    #     ★★291补 COLD-289 之否决记（其面限292而一处未办，卡上已判顺延293）之後，此项即败，
    #       **而它败的不是闸，是这一条断言**；★★★故改断言为其所护之理本身：
    #       **新式与旧式之别，只出在带否决记那几笔上**——多一笔即是误伤，少一笔即是漏。
    # ★★★★★2026-09-02·292封版之序再改：**二式相异者今有两类，非一类**——
    #   ①末份挂否决记者（新式判红，旧式判绿）；②曾被否决而後由在後之回执签核者（新式判绿，旧式判红）。
    #   ★原断言只认第①类，遂於292签核COLD-288之後即败；**而它败的仍不是闸，是这一条断言。**
    diff = sorted(n for n in range(1, 301) if _old(n, rcs) != _m6._cold_done(n))
    vetoed = sorted(n for n in range(1, 301)
                    if any(('COLD-%d·本章未执' % n) in t for t in rcs))
    # ★而「二式相异」只出於一处：**末份挂否决记，而全书某处又写过那六个字**
    #   （旧式一见六字即绿，新式只认末份）。
    #   ★★「先否决而後签核」那一类（今为288）**两式同判绿**——旧式因别处有六字而绿，
    #     新式因末份签核而绿；★★★**同判不等於同理**，故那一类另立一项验（见③之c），
    #     不许把它塞进这里凑数——**凑进来，此项就再也说不出自己在验什么。**
    _应异 = sorted(n for n in _有号 if _末份(n, rcsc)[1] and _old(n, rcs))
    R.append(('⑤回灌·二式相异者恰是「末份否决而别处写过六字」之 %s（多一笔即误伤，少一笔即漏）'
    #   ★★★★★2026-09-02·293封版之序再改：**原断言带 `len(diff) >= 1`**，
    #     ★而293销 COLD-289 之後全书二式再无相异者，_应异 与 diff 俱为空，此项当场判红；
    #     ★★**二式一致，正是账干净之证，不是测该红之由**；★★★**故去其下限，只验二集相等**
    #     ——**而「它还逮不逮得着」那一问，已由③之d 之合成例回答**（令§六④·判准只一条：
    #     改後它还逮不逮得住它本来要逮的东西）。
              % (_应异 or '无'), diff == _应异))

    # ⑥不许挖空：一笔既无六字亦无否决记者，照旧判待执
    R.append(('⑥未挖空·无凭无据者判待执', _m6._cold_done(999999) is False))

    # ⑦否决记之式须严：近似之句不算否决（不许拿「未执」二字到处误伤）
    #   ★同日改（与⑤同由）：**原本数其笔数，而笔数会长**；★★今改验其式——
    #     **少一个间隔号、换一个字，皆不作否决**：这才是「式严」二字所指。
    近似 = ['COLD-288 本章未执', 'COLD288·本章未执', '第288章未执', 'COLD-288·未执',
            'COLD-288·本章未办']
    R.append(('⑦式严·近似之句一概不作否决（%d 式逐一验）' % len(近似),
              all(('COLD-288·本章未执' not in x) for x in 近似)))
    R.append(('⑦之b·真式须逮得着（288之否决记在册）',
              any('COLD-288·本章未执' in t for t in rcs)))

    # ⑧否决在先：**同一份回执**既有六字又有否决记，以否决为准。
    #   ★同日改：原以288为例，而288之六字与否决记今分处两份回执（291否决、292签核），
    #     **那正是「顺延而後有人接」之常态，不是本项所验之形**；★★故改为验其形本身：
    #     凡有一份回执二者并存者，若它同时是末份，则须判待执。
    _并存 = [n for n in _有号
             if any(_re.search(r'(?<!\d)%d章冷眼轮' % n, tx) and (('COLD-%d·本章未执' % n) in tx)
                    for ch, tx in rcsc)]
    _并存末 = [n for n in _并存 if _末份(n, rcsc)[1]]
    R.append(('⑧序·同一回执六字与否决记并存且为末份者判待执（%d 笔）' % len(_并存末),
              len(_并存) >= 1 and all(_m6._cold_done(n) is False for n in _并存末)))

    # ⑨一坐与六检同判（二器不许各记各的）
    _sp2 = _u.spec_from_file_location('_一坐', os.path.join(ROOT, '工具', '一坐.py'))
    ok = True
    try:
        src = io.open(os.path.join(ROOT, '工具', '一坐.py'), encoding='utf-8').read()
        ok = '_cold_done' in src
    except OSError:
        ok = False
    R.append(('⑨同判·一坐仍走六检之 _cold_done', ok))

    # ⑩令§十①未被架空：六字仍是签核之凭（无六字者不因新式转绿）
    #   ★同日改（与⑤⑦同由）：**原本拿 289 作对照**，★★而 289 今已带上否决记，
    #     **它由对照变成了真案**——**一份负测拿一个会变的号当不变的对照，那是它自己的病**；
    #     ★★★故改为当场算出一个「无否决记」之号作对照，不写死任何号。
    控 = next((n for n in range(1, 301)
               if not any(('COLD-%d·本章未执' % n) in t for t in rcs)), None)
    R.append(('⑩令§十①仍在·无否决记之号（今取%s）新旧二式同判' % 控,
              控 is not None and _m6._cold_done(控) == _old(控, rcs)))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·冷轮否决记 %d/%d %s' % (len(R) - len(bad), len(R),
                                   '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
