# -*- coding: utf-8 -*-
"""刻意之疲——**看一段一段的章尾，查全书有没有落进「每章都吊一下」的套子。**

【其立之由（2026-09-25·作者令，逐字之意）】
  「不要在每一个章节里刻意去制造上瘾的东西——每一章都这么写，读者会审美疲劳，觉得作者在故意吊他们的胃口，
   那还有谁愿意看？整本书会变得割裂，每一章都在自立山头。是整本书让人上瘾：剧情从头到尾连贯、丝滑，
   每一章做它该做的事、质量最高。我最怕的是刻意。」
  ★一章一章地看，看不出「刻意」——**一个钩是好的，十二个钩连着就是套子**。故本器只按段看，不按章判。

【怎么量（只量形，不判好坏）】
  取已入库（git 已跟踪）之末 12 章，逐章取其末段（去「＊」行），判它是不是「吊式收尾」：
    ①以问号、省略号、破折号收；或 ②末段里有「就在这时／突然／忽然／下一刻／还没完／没说完／不知道的是／谁知」之类掐断语。
  ★**吊式收尾本身不是错**；错的是它成了惯性。
【乙·收尾同式】末 12 章之末段，凡有一个 ≥5 字之串在 ≥4 章之尾里同见者，即「收尾成了一个模子」（0925 当场逮出：
  355／357／359／361／363 五章皆收在「白的那一头」）。**最新一章若又落进这个模子 → 红**；旧章已在模子里者 → 黄（开回修之账）。
【判】末 12 章里吊式收尾 ≥8 → 红（套子已成，下一章起草须收在事上，且须回头看这一段哪几章该改）；≥6 → 黄。

用法：python3 工具/刻意之疲.py [--自测]
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
窗 = 12
红线, 黄线 = 8, 6
掐断语 = re.compile(r'就在这时|突然|忽然|下一刻|还没完|没说完|不知道的是|谁知|话音未落|戛然')


def _章号(名):
    _cn = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    m = re.search(r'第([零〇一二三四五六七八九十百千]+)章', 名)
    if not m:
        return 0
    tot = cur = 0
    for ch in m.group(1):
        if ch in _cn:
            cur = _cn[ch]
        elif ch in '十百千':
            tot += (cur or 1) * {'十': 10, '百': 100, '千': 1000}[ch]; cur = 0
    return tot + cur


def 末段(文):
    文 = 文.split('【本章亮点】')[0]   # ★亮点段是编者之注，非正文
    段 = [x.strip() for x in 文.split('\n') if x.strip() and x.strip() != '＊' and not x.startswith('#')]
    return 段[-1] if 段 else ''


def 吊否(段):
    尾 = 段.rstrip('」』"”）) ')
    if 尾.endswith(('？', '?', '……', '…', '——')):
        return True
    return bool(掐断语.search(段))


def 已入库之章():
    try:
        out = subprocess.run(['git', '-c', 'core.quotepath=off', 'ls-files', '正文'], cwd=ROOT, capture_output=True, text=True).stdout
    except Exception:
        return []
    fs = [l for l in out.splitlines() if l.endswith('.md') and '第' in l]
    return sorted(((_章号(f), f) for f in fs if _章号(f)), key=lambda x: x[0])


def 同式(判):
    """回 (串, [章号…])：≥5 字、见於 ≥4 章之尾者，取最长之一。"""
    尾 = {n: re.sub(r'[\s，。、“”：；！？…—]', '', t) for n, _, t in 判}
    最 = ('', [])
    for n, t in 尾.items():
        for L in range(12, 4, -1):
            for i in range(0, max(0, len(t) - L) + 1):
                串 = t[i:i + L]
                见 = [m for m, u in 尾.items() if 串 in u]
                if len(见) >= 4 and len(串) > len(最[0]):
                    最 = (串, sorted(见))
    return 最


def 查(印=True):
    章 = 已入库之章()[-窗:]
    判 = []
    for n, f in 章:
        段 = 末段(open(os.path.join(ROOT, f), encoding='utf-8').read())
        判.append((n, 吊否(段), 段[-40:]))
    k = sum(1 for _, x, _ in 判 if x)
    串, 见 = 同式(判) if 判 else ('', [])
    新章入模 = bool(串) and 判 and 判[-1][0] in 见
    if 印:
        print('════ 刻意之疲 ════（末 %d 章之章尾·吊式收尾 %d 章｜红线 %d·黄线 %d）' % (len(判), k, 红线, 黄线))
        for n, x, t in 判:
            print('  %s 第%d章 …%s' % ('⚠吊' if x else '  收', n, t))
        if k >= 红线:
            print('  ⛔ 刻意之疲：末 %d 章里 %d 章吊式收尾——套子已成。下一章须收在事上；并回头看这一段哪几章的尾是硬掐的。' % (len(判), k))
        elif k >= 黄线:
            print('  ⚠ 刻意之疲（黄）：%d 章吊式收尾，已近成套。' % k)
        else:
            print('  ✓ 刻意之疲：章尾有收有放，未成套子。')
        if 串:
            print('  %s 收尾同式：「%s」见於 %d 章之尾（%s）%s' % (
                '⛔' if 新章入模 else '⚠', 串, len(见), '、'.join('第%d章' % x for x in 见),
                '——**最新一章又落进这个模子**，须换一个收法（收在本章自己的事上）。' if 新章入模
                else '——旧章已成模子，须开回修之账；下一章⛔不许再落进去。'))
    return (k < 红线 and not 新章入模), k


def 自测():
    ok = [
        ('①问号收即吊', 吊否('他到底是谁？')),
        ('②省略号收即吊', 吊否('门开了……')),
        ('③掐断语即吊', 吊否('就在这时，灯灭了。')),
        ('④收在事上不吊', not 吊否('她把碗洗了，搁回架上。')),
        ('⑤末段去＊行', 末段('甲\n\n乙。\n＊\n') == '乙。'),
        ('⑤之b 亮点段不算正文', 末段('正文末句。\n【本章亮点】\n注。') == '正文末句。'),
        ('⑥章号汉数', _章号('镇冢秘术_第三百六十六章_x.md') == 366),
        ('⑧同式：四章同串即逮', 同式([(1, 0, '甲乙丙丁戊己'), (2, 0, '子甲乙丙丁戊'), (3, 0, '甲乙丙丁戊丑'), (4, 0, '寅甲乙丙丁戊')])[0] == '甲乙丙丁戊'),
        ('⑧之b 三章同串不逮', 同式([(1, 0, '甲乙丙丁戊'), (2, 0, '甲乙丙丁戊'), (3, 0, '甲乙丙丁戊'), (4, 0, '子丑寅卯辰')])[0] == ''),
        ('⑦只看已入库之章（写到一半的不算）', 'ls-files' in open(__file__, encoding='utf-8').read()),
    ]
    坏 = [n for n, v in ok if not v]
    for n, v in ok:
        print(('  ✓ ' if v else '  ⛔ ') + n)
    print('负测·刻意之疲 %d/%d' % (len(ok) - len(坏), len(ok)))
    return not 坏


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 查()[0] else 1)
