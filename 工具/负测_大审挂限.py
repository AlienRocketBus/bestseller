# -*- coding: utf-8 -*-
"""负测·大审挂限（2026-09-13 立·`大审.py` 自己欠的那一样）。

★所守者一句：**「已挂」带着限，到期不裁即是逾期，器须报。**
★★其根：**大审册自书「『挂』不是把裁推开：它带着限，到期不裁即是逾期，器会报」**
　——⛔**而 `大审.py` 从来没有数过那个限到没到**：**它只问「已挂带没带一个数」。**
　**即一句写在册上的话，盘上没有一只手兑它**（体检账 ㊚ 之同骨：**账断了一头**）；
　★**而这一路比那一路更难见**：**它不是报错了，是它从头到尾没在看。**
★★★**并记立日自栽一回**：头一版拿整行去找「限N」取其最小，
　**而一笔之「其由」那一格里常引着别的限**（第11笔引 FS 之旧限 309），
　**於是它把别人的旧限当成了这一笔的限，当场报了一个假逾期**；
　⛔**故收窄：一笔之限只认「已挂」所在那一格（裁之格），其由之格一个数也不取。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io
import os
import re
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mod():
    spec = importlib.util.spec_from_file_location(
        '_ds', os.path.join(ROOT, '工具', '大审.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def 跑():
    m = _mod()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    src = io.open(os.path.join(ROOT, '工具', '大审.py'),
                  encoding='utf-8').read()

    # ①【今日之实】盘上此刻无逾限之挂
    末, 上, 距, 判语 = m.账()
    判('①', '今日盘上无「已挂逾限」之报',
       any('逾限' in x for x in 判语), False)

    # ②【其问真在码里】⛔否则下面几格全是空转
    判('②', '大审.py 确有「逾限」这一问', '逾限' in src, True)

    # ③【收窄之据仍在】限只认「已挂」那一格
    判('③', '其限只认「已挂」所在之格（⛔不取其由之格）',
       "[c for c in x.split('|') if '已挂' in c]" in src, True)

    # ④⑤⑥【假盘·三局回灌】⛔皆用真形：一行裁定表
    def _算(行, 末章):
        """照 大审.py 之法算一行：返回 (是否逾限, 其限)。"""
        if '已挂' not in 行:
            return False, None
        cs = [c for c in 行.split('|') if '已挂' in c]
        ms = re.findall(r'限\s*(\d+)', cs[0]) if cs else []
        if not ms:
            return False, None
        lim = min(int(y) for y in ms)
        return (末章 >= lim), lim

    真形 = ('| 11 | 某席之题 | 其据 | **已挂·限 330·交作者裁** | '
            '其由：★此笔引 FS 之旧限 309，⛔而那不是本笔之限。 |')
    判('④', '⛔其由之格里的旧限 309 不许被当成本笔之限（0913 真局回灌）',
       _算(真形, 325), (False, 330))
    判('⑤', '末章过其限即报（330 → 第331章）', _算(真形, 331), (True, 330))
    判('⑥', '⛔已治之笔不入此问（其格无「已挂」）',
       _算('| 1 | 题 | 据 | **已治·本坐落刀** | 其由：限 300 已过。 |', 999),
       (False, None))

    # ⑦【挂而无限者归旧问·不由本路收】
    判('⑦', '挂而无限者本路不报（其红由「落了裁者只N行」那一问出）',
       _算('| 9 | 题 | 据 | **已挂** | 其由 |', 999), (False, None))

    print('════ 负测·大审挂限 ════（守：「已挂」带限，到期不裁即逾期）')
    for x in 败:
        print('  ⛔ ' + x)
    print(('  ✓ %d/%d 全通' % (过, 过 + len(败))) if not 败
          else '  ⛔ %d/%d 有败' % (过, 过 + len(败)))
    return not 败


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
