# -*- coding: utf-8 -*-
"""闸十·法典闸（283封版后立）

★其立之由：本坐立过之法，写在轮记散文里的，一条也没被调起来过
  （LAW-279A「掘层须有身」连犯五章：279/280/281/282/283 之第4轮）；
  而写进闸里的（LAW-280A「起草轮须裁感官三密度」，280第13轮立），立了就没再犯过。
★★故法之生效不在措辞，在它卡不卡在路上。
  此闸不新增命令、不新增流程——挂在 跑轮.py --存版 里，每章跑十三回，漏不掉。
★★★所机化者，只取「能变成一个数」的那几条；其余在 设定/法典.json 里挂账等着被机化。
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

# 手上之事：动拍之识。★不取「看／想／知道／记得」，那些是判不是动。
手 = re.compile(
    r'(把|拿|摸|按|抓|挪|捻|捏|压|搁|插|抽|悬|落笔|划|迈|坐下|起身|伸手|量|盖|刮|擦|系|解开|端|舀|磕|撬|抱'
    r'|翻[到回开页过一二三四五六七八九十第那这])'
)
# ★「翻」须带宾方算动：翻到／翻回／翻开／翻页／翻那一页。
#   单「翻不着」是判不是动——283自测所逮（无身之例误中二拍，恰卡在线上放行）。


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
    r = 轮号(note)
    放行 = bool(re.search(r'判不补|零刀|不补|无真伤', note or ''))

    # ── LAW-279A·掘层须有身（犯五章）───────────────────────────
    if r == 4 and prev_body:
        旧 = set(拍(prev_body))
        新 = [x for x in 拍(body) if x not in 旧]
        if len(新) >= 8:
            动 = sum(1 for x in 新 if 手.search(x))
            比 = 动 / len(新)
            if 比 < 0.20 and not 放行:
                halt = True
                lines.append('   ⛔法典闸·LAW-279A（掘层须有身）：本轮新增%d拍，有身者%d拍（%.0f%%，须≥20%%）。'
                             % (len(新), 动, 比 * 100))
                lines.append('     此法立於279第5轮，而279、280、281、282、283之第4轮连犯五回，')
                lines.append('     回回是下一轮（在场庭）方逮出，回回补身。本闸即为断此连犯而设。')
                lines.append('     **处方**：每一层须给一处手上之事可托')
                lines.append('     （她按下去纸不陷／他抱着石头下去／指头搁第一行往下走）。')
                lines.append('     若本层之身确在前轮已补，说明中明写「判不补·记因」放行。')
            else:
                lines.append('   ✓法典闸·LAW-279A：新增%d拍，有身%d拍（%.0f%%）。'
                             % (len(新), 动, 比 * 100))

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
    # 自测：负测二例，皆须如所期
    头 = '《镇冢秘术》\n\n第一章　试\n\n'
    旧 = 头 + '\n\n＊\n\n'.join(['她把册子解下来。', '翻到那一页。', '十三行。', '剩七八行。', '她数着页边。'])
    无身 = ['这一样她先前没想过。', '想过也不会写。', '不写就是没有。', '没有的东西往后翻不着。',
            '翻不着就是没记过。', '没记过跟没发生一个样。', '一个样是纸上说的。', '纸上说的不算全。',
            '不算全她今天才看出来。', '看出来也补不上。']
    有身 = ['她把指头按在那一页上。', '按下去纸不陷。', '这一样她先前没想过。',
            '她把册子合上，再打开。', '打开还是那一页。', '不写就是没有。',
            '她拿指头量了量那道边。', '宽不到半指。', '半指里写不下第二样。', '她没加。']
    for 名, 加, 期 in [('无身', 无身, True), ('有身', 有身, False)]:
        新 = 旧 + '\n\n＊\n\n' + '\n\n＊\n\n'.join(加)
        h, L = 查('第4轮·深掘', 旧, 新)
        print('【%s】halt=%s（期 %s）%s' % (名, h, 期, '✓' if h == 期 else '⛔'))
        for x in L:
            print(x)
        print()
