# -*- coding: utf-8 -*-
"""闸十·法典闸（283封版后立）

★其立之由：本坐立过之法，写在轮记散文里的，一条也没被调起来过
  （LAW-279A「掘层须有身」连犯五章：279/280/281/282/283 之第4轮）；
  而写进闸里的（LAW-280A「起草轮须裁感官三密度」，280第13轮立），立了就没再犯过。
★★故法之生效不在措辞，在它卡不卡在路上。
  此闸不新增命令、不新增流程——挂在 跑轮.py --存版 里，每章跑十三回，漏不掉。
★★★所机化者，只取「能变成一个数」的那几条；其余在 设定/法典.json 里挂账等着被机化。
〔1119 W908 环7〕LAW-279A（掘层须有身）之支删：其触唯「第4轮」，而十三轮 1027 汰（领轮闸今恒拦第N轮之说明）——
  其支恒不触（死支），其手之识随删；今唯 LAW-283A（削拍须查承前之字·只警不拦）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def 拍(body):
    """切正文为拍（去章题、去亮点段、去分隔星）。"""
    t = (body or '').split('【本章亮点】')[0]
    t = re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)
    return [re.sub(r'\s', '', x) for x in t.split('\n')
            if x.strip() and x.strip() != '＊']


def 轮号(note):
    m = re.search(r'第\s*([0-9]+)\s*轮', note or '')
    return int(m.group(1)) if m else None


def 查(note, prev_body, body):
    """返回 (halt, lines)。halt 为真则拦停存版。"""
    lines, halt = [], False

    # ── LAW-283A·削拍须查承前之字（283一章两犯）──────────────
    bs = 拍(body)
    孤 = []
    for i, x in enumerate(bs):
        m = re.match(r'^没(.)', x)
        if not m or i == 0:
            continue
        if m.group(1) not in bs[i - 1]:
            孤.append((i, x[:26]))
    if 孤:
        lines.append('   ⚠法典闸·LAW-283A（削拍须查承前之字）：%d处「没X」其前拍未出该动，疑为削拍所留之孤字。'
                     % len(孤))
        for i, x in 孤[:3]:
            lines.append('     拍%d：%s' % (i, x))
        lines.append('     此法立於283第10轮，而283第12轮当轮再犯（「没加」「没动」）。只警不拦，落刀者自裁。')

    return halt, lines


if __name__ == '__main__':
    # 自测：LAW-283A 二例——削拍之孤字须警、承前者⛔警；俱⛔拦（halt 恒假）
    头 = '《镇冢秘术》\n\n第一章　试\n\n'
    孤 = 头 + '\n\n＊\n\n'.join(['她把册子解下来。', '没加。'])
    承 = 头 + '\n\n＊\n\n'.join(['她想加一行。', '没加。'])
    败 = 0
    for 名, 文, 期 in [('孤字', 孤, True), ('承前', 承, False)]:
        h, L = 查('', '', 文)
        警 = any('LAW-283A' in x for x in L)
        败 += not (警 == 期 and not h)
        print('【%s】警=%s（期 %s）halt=%s %s' % (名, 警, 期, h, '✓' if (警 == 期 and not h) else '⛔'))
        for x in L:
            print(x)
    # 〔1119 W908 环7 复核〕册与码同：法典.json 状态「已机化」而拦在「法典闸」之条，其 id 须在 查 之码
    #   （LAW-279A 之支删而册仍书「已机化·拦在存版·法典闸」——复核所逮；册言其拦而码无其支，即纸上之法）
    import io, json, inspect, sys
    册 = json.load(io.open(os.path.join(ROOT, '设定', '法典.json'), encoding='utf-8'))
    码 = inspect.getsource(查)
    悬 = [x.get('id') for x in 册.get('items') or []
         if str(x.get('状态', '')).startswith('已机化') and '法典闸' in str(x.get('拦在', '')) and x.get('id') not in 码]
    败 += bool(悬)
    print('【册与码同】法典.json 已机化而拦在法典闸之条，俱有其支%s %s' % (('（悬：%s）' % '、'.join(悬)) if 悬 else '', '⛔' if 悬 else '✓'))
    sys.exit(1 if 败 else 0)
