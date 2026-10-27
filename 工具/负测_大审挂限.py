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

    真形 = ('| 11 | 某席之题 | 其据 | **已挂·限 330·交总编辑裁** | '
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

    # ⑧【录册之限⛔早於下一章】1024 实踩：裁席给还账限 408（包之首章）、录成「已挂·限408」，册一成即逾限、推闸全红
    裁 = getattr(m, '裁之文', None)
    判('⑧', '还账限 408 於至第410章之册 → 正为限411',
       裁 and 裁({'ruling': '还账', 'limit': 408}, 410), '已挂·限411（还账·器施）')
    判('⑧之二', '已挂限 ≤b → 正为 b+1；限在後者照录；还账无限 → b+1',
       裁 and (裁({'ruling': '已挂', 'limit': '410'}, 410), 裁({'ruling': '已挂', 'limit': 415}, 410),
              裁({'ruling': '还账'}, 410), 裁({'ruling': '已治'}, 410)),
       ('已挂·限411', '已挂·限415', '已挂·限411（还账·器施）', '已治'))
    判('⑧之三', '录用 裁之文（⛔另写一路）', '裁 = 裁之文(x, b)' in src, True)

    # ⑨【拍库随段·1027 #99】裁席之 beats 录入拍库「第{a}段」（⛔重录）；无 beats 者册写「本段无入库之拍：由」；无由⛔代填
    入 = getattr(m, '入库', None)
    if 入:
        import tempfile
        库 = os.path.join(tempfile.mkdtemp(), '库.md')
        io.open(库, 'w', encoding='utf-8').write('# 库\n\n---\n\n## 已定未写之标杆\n- y\n')
        r1 = 入({'beats': [{'ch': 415, 'beat': '7', 'quote': '她把灯吹了。', 'why': '对标 01'}]}, 411, 420, 库)
        入({'beats': [{'ch': 416, 'quote': '又一拍。', 'why': 'x'}]}, 411, 420, 库)
        文 = io.open(库, encoding='utf-8').read()
        判('⑨', '入库：拍库得「## 第411段」一节（在标杆之前、⛔重录），册列其拍',
           (文.count('## 第411段') == 1 and 文.index('## 第411段') < 文.index('## 已定未写之标杆') and '又一拍' not in 文
            and any('415:7「她把灯吹了。」' in x for x in r1)), True)
        判('⑨之二', '无拍：有由 → 「本段无入库之拍：由」；无由 → 未交（⛔代填，421 法用即红）',
           (入({'beats': [], 'no_beats_reason': '十章无一拍够对标'}, 411, 420, 库)[0], 入({'beats': []}, 411, 420, 库)[0].startswith('本段无入库之拍')),
           ('本段无入库之拍：十章无一拍够对标', False))
    判('⑨之三', '录册接入库（⛔另写一路）', "入库(裁果, a, b)" in src, True)
    # ⑩【大审.js 之数随参】1024 实踩之根：裁令写死「limit 408／409 起／409—418」，410 之审照旧数挂限——数须由 B 推
    js = io.open(os.path.join(ROOT, '工具', '席', '大审.js'), encoding='utf-8').read()
    判('⑩', '大审.js 裁令无写死之章号（4xx）、有 beats 之栏', (re.findall(r'(?<![\d$])4\d\d(?!\d)', js), "beats:" in js and 'no_beats_reason' in js), ([], True))

    print('════ 负测·大审挂限 ════（守：「已挂」带限，到期不裁即逾期）')
    for x in 败:
        print('  ⛔ ' + x)
    print(('  ✓ %d/%d 全通' % (过, 过 + len(败))) if not 败
          else '  ⛔ %d/%d 有败' % (过, 过 + len(败)))
    return not 败


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
