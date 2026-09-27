#!/usr/bin/env python3
"""剧情庭之关（0927·作者令「这个机制一定要跑起来」）：
自第 381 章起，每十章一段（381—390、391—400……）；段内已有章封版（版本/第N章/_十一轮.json 在）者，
须有 设定/剧情庭_势_第<段首>段.md（剧情庭「式：新」所裁之走向），且其内含「裁」字样；缺即红。
见 设定/选剧情之律.md §四。用法：python3 工具/剧情庭之关.py ｜ --自测
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


def 查(root=ROOT):
    红 = []
    段 = set()
    for d in glob.glob(os.path.join(root, '版本', '第*章')):
        m = re.search(r'第(\d+)章$', d)
        if m and int(m.group(1)) >= 起 and os.path.exists(os.path.join(d, '_十一轮.json')):
            段.add(段首(int(m.group(1))))
    for s in sorted(段):
        f = os.path.join(root, '设定', '剧情庭_势_第%d段.md' % s)
        if not os.path.exists(f) or '裁' not in open(f, encoding='utf-8', errors='replace').read():
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
    finally:
        shutil.rmtree(t)
    print('剧情庭之关·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    红 = 查()
    if 红:
        print('⛔ 剧情庭之关：%s（选剧情之律§四：每段动笔前先过剧情庭·式新）' % '｜'.join(红))
        sys.exit(1)
    print('✓ 剧情庭之关：已动笔之段皆有剧情庭所裁之势')
