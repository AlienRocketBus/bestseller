#!/usr/bin/env python3
"""剧情庭之关（0927·作者令「这个机制一定要跑起来」）：
自第 381 章起，每十章一段（381—390、391—400……）；段内已有章封版（版本/第N章/_十一轮.json 在）者，
须有 设定/剧情庭_势_第<段首>段.md（剧情庭「式：新」所裁之走向），且其内含「裁」字样；缺即红。
见 设定/选剧情之律.md §四。用法：python3 工具/剧情庭之关.py ｜ --章 N（动笔前：N 所在之段须已有势）｜ --自测
★1015 进化（W43 逮）：①旧只认「裁」一字——第381段之档自写「此裁无效」亦过；今自注无效者须有「代裁：」一行，所点之档俱在盘上，方算有势。
  ②旧只在封版後验（391 已写才红）；今 --章 N 供动笔前之验，造式验 --料 调之（左移）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, glob, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
起 = 381


def 段首(n):
    return 起 + (n - 起) // 10 * 10


def 有势(s, root=ROOT):
    f = os.path.join(root, '设定', '剧情庭_势_第%d段.md' % s)
    if not os.path.exists(f):
        return False
    t = open(f, encoding='utf-8', errors='replace').read()
    if '裁' not in t:
        return False
    if '此裁无效' in t:                       # 自注无效：须「代裁：」点出真裁之档，且俱在
        m = re.search(r'^代裁：(.+)$', t, re.M)
        档们 = re.findall(r'设定/[^\s、，,；;）)]+\.md', m.group(1)) if m else []
        return bool(档们) and all(os.path.exists(os.path.join(root, x)) for x in 档们)
    return True


def 欠引(s, root=ROOT):
    """★1117 X104：瑕疵总账「未治」之条，其主写「S 段剧情庭」者，本段之势须引其号；缺即红（⛔段势漏账而动笔）。"""
    f = os.path.join(root, '设定', '瑕疵总账.md')
    if not os.path.exists(f):
        return []
    账 = open(f, encoding='utf-8').read().split('## 已治')[0]
    势 = open(os.path.join(root, '设定', '剧情庭_势_第%d段.md' % s), encoding='utf-8', errors='replace').read()
    号们 = [m.group(1) for m in re.finditer(r'^\|\s*(X\d+)\s*\|([^\n]*)$', 账, re.M) if ('%d 段剧情庭' % s) in m.group(2)]
    return ['第%d段之势未引瑕疵总账 %s（其主係本段剧情庭）——裁档须排其治' % (s, x) for x in 号们 if x not in 势]


def 查(root=ROOT, 章=None):
    if 章 is not None:                        # 动笔前之验
        if 章 < 起:
            return []
        s = 段首(章)
        if not 有势(s, root):
            return ['第%d—%d段无剧情庭之势（第%d章动笔前须先裁：工具/席/剧情庭.js 式段）' % (s, s + 9, 章)]
        return 欠引(s, root)
    红 = []
    段 = set()
    for d in glob.glob(os.path.join(root, '版本', '第*章')):
        m = re.search(r'第(\d+)章$', d)
        if m and int(m.group(1)) >= 起 and os.path.exists(os.path.join(d, '_十一轮.json')):
            段.add(段首(int(m.group(1))))
    for s in sorted(段):
        if not 有势(s, root):
            红.append('第%d—%d段无剧情庭之势' % (s, s + 9))
    return 红


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '设定'))
        d = os.path.join(t, '版本', '第383章'); os.makedirs(d)
        共 += 1; ok += (查(t) == [])                      # 未封不查
        open(os.path.join(d, '_十一轮.json'), 'w').write('{}')
        共 += 1; ok += (len(查(t)) == 1)                  # 封而无势 → 红
        open(os.path.join(t, '设定', '剧情庭_势_第381段.md'), 'w').write('一、裁定：……')
        共 += 1; ok += (查(t) == [])
        d2 = os.path.join(t, '版本', '第380章'); os.makedirs(d2)
        open(os.path.join(d2, '_十一轮.json'), 'w').write('{}')
        共 += 1; ok += (查(t) == [])                      # 段前不查
        共 += 1; ok += (len(查(t, 章=391)) == 1 and 查(t, 章=385) == [] and 查(t, 章=300) == [])   # 动笔前：段无势即红
        f = os.path.join(t, '设定', '剧情庭_势_第381段.md')
        open(f, 'w').write('## ⛔此裁无效\n（原文·无效）裁：守原')
        共 += 1; ok += (len(查(t)) == 1)                  # 自注无效而无代裁 → 红
        open(os.path.join(t, '设定', '真裁.md'), 'w').write('裁')
        open(f, 'w').write('## ⛔此裁无效\n代裁：设定/真裁.md、设定/无此档.md\n裁')
        共 += 1; ok += (len(查(t)) == 1)                  # 代裁所点之档有缺 → 红
        open(f, 'w').write('## ⛔此裁无效\n代裁：设定/真裁.md\n裁')
        共 += 1; ok += (查(t) == [])
        # ★1117 X104：未治之账主写「381 段剧情庭」者，势未引其号 → 动笔前红；引之 → 过；已治之条不算
        open(os.path.join(t, '设定', '瑕疵总账.md'), 'w').write('## 未治\n| X9 | 缺 | 源 | 381 段剧情庭：排一章 | 385 |\n## 已治\n| X8 | 缺 | 源 | 381 段剧情庭 | 381 |\n')
        共 += 1; ok += (len(查(t, 章=385)) == 1 and 'X9' in 查(t, 章=385)[0])
        open(f, 'a').write('\n治 X9：……')
        共 += 1; ok += (查(t, 章=385) == [])
    finally:
        shutil.rmtree(t)
    print('剧情庭之关·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    a = sys.argv[1:]
    红 = 查(章=int(a[a.index('--章') + 1])) if '--章' in a else 查()
    if 红:
        print('⛔ 剧情庭之关：%s（选剧情之律§四：每段动笔前先过剧情庭·式段或式新）' % '｜'.join(红))
        sys.exit(1)
    print('✓ 剧情庭之关：已动笔之段皆有剧情庭所裁之势')
