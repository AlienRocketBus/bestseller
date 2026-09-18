# -*- coding: utf-8 -*-
"""负测 · 分量闸取数之口径（2026-09-18 立·随本日之改同日落）

⛔**其病**：`分量闸` 旧式只取 `台账末版.soft.净重`——
　**而本闸所问者是「这一章够不够厚」，那是一件关於 `正文/` 的事，不是一件关於台账的事。**
★**其红之实**：0918 之 346，台账末版记 **2113**，而正文实算 **2503**；
　本闸照印「净重 2113 ＜ 2500，且施工表无短章豁免」——⛔**报了一道假红。**
★★**而那一日正文比台账新，只因一庭回修的刀落在存版之前**——**这不是罕事，是每一次回修庭的常态。**
★★★**其逮着者係 346 回修庭之验席，非本坐**（体检账 九十四之②）。

四局（⛔每一局皆验其反面）：
　①正文比台账厚 → **须取正文**（⛔取台账即报假红）
　②正文比台账薄 → **亦须取正文**（⛔不许只在「对本章有利」那一头取正文——那就成了挑尺）
　③台账无而正文有 → 须能量出来（⛔不许因无账而整章不查）
　④二者不合须印出来 → ⛔**不许静悄悄换掉**（换而不说，下一坐便查不出它换过）
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import 分量闸 as _fl


def 跑():
    局 = []
    src = io.open(_fl.__file__, encoding='utf-8').read()

    # ①②③ 皆验同一条码性：正文为准，无条件
    _取 = '出[_m] = _w'
    局.append(('①②·正文为准且无条件（⛔码里一个「若正文更厚才取」之类的条件也没有）',
               _取 in src and not re.search(r'if[^\n]{0,40}_w\s*[><][^\n]{0,20}出\.get', src)))
    局.append(('③·台账无而正文有 → 照样落进表（⛔不许因无账而整章不查）',
               bool(re.search(r'for _f in glob\.glob\(os\.path\.join\(ROOT, .正文.', src))))
    局.append(('④·二者不合须印出来（⛔不许静悄悄换掉）',
               '台账与正文不合' in src))
    局.append(('④之二·量之法自 `跑轮.score` 取回，⛔不另抄一份',
               '_pl.score(' in src))
    局.append(('⑤·正文亲算取不回来时须明说其数可能已旧（⛔不许假装它是新的）',
               '本闸退回取台账' in src))

    # ⑥实跑一回。⛔**须挑一章其台账与正文确係不同者**——
    #   ★**若挑 346，二者今日皆係 2503（本坐方才存过 v13），那一局便怎么写都过，等於没测。**
    #   ★★**故自盘上找头一个「账与文不合」之章，拿它来问**：本闸取回来的是哪一个数。
    try:
        import json
        import 跑轮 as _pl
        _表 = _fl.诸章之净重()
        _靶 = None
        for _d in sorted(os.listdir(os.path.join(_fl.ROOT, '版本'))):
            _m = re.search(r'第(\d+)章', _d)
            _lp = os.path.join(_fl.ROOT, '版本', _d, '_台账.json')
            if not _m or not os.path.exists(_lp):
                continue
            _n = int(_m.group(1))
            try:
                _账 = json.load(io.open(_lp, encoding='utf-8'))['版本'][-1]['soft']['净重']
            except Exception:
                continue
            _fs = [x for x in os.listdir(os.path.join(_fl.ROOT, '正文'))
                   if _fl._章号(x) == _n]
            if not _fs:
                continue
            _文 = _pl.score(io.open(os.path.join(_fl.ROOT, '正文', _fs[0]),
                                    encoding='utf-8').read())[1]['净重']
            if _账 != _文:
                _靶 = (_n, _账, _文)
                break
        if _靶 is None:
            局.append(('⑥实跑·盘上找不到一章其账与文不合者——⛔此局今日无从测起，原样报出', False))
        else:
            _n, _账, _文 = _靶
            局.append(('⑥实跑·第%d章 账%d／文%d，本闸取得 %s → 须係文那一个'
                       % (_n, _账, _文, _表.get(_n)), _表.get(_n) == _文))
    except Exception as e:
        局.append(('⑥实跑（跑不成：%s）' % e, False))

    红 = 0
    print('════ 负测 · 分量闸取数之口径（%d 局）════' % len(局))
    for 名, 果 in 局:
        print('  %s %s' % ('✓' if 果 else '⛔', 名))
        if not 果:
            红 += 1
    print('  ── %d/%d ──' % (len(局) - 红, len(局)))
    return 红


if __name__ == '__main__':
    sys.exit(1 if 跑() else 0)
