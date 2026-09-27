#!/usr/bin/env python3
"""圣经随裁（0927·作者令「圣经不是一成不变的，要随时更新；机制必须跑起来」）：
凡 0927 以後之裁（设定/裁_MMDD_*.md，MMDD≥0927）与剧情庭之裁（设定/剧情庭_*.md），
须已落进圣经——圣经（设定/00_镇冢秘术_唯一总圣经.md）里须有该档之名（作「据」），
或该档自书「圣经无改」并写其由（如守原）。缺即红：做了的决定，不许只躺在裁档里。
用法：python3 工具/圣经随裁.py ｜ --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, glob, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
经 = os.path.join('设定', '00_镇冢秘术_唯一总圣经.md')


def 查(root=ROOT):
    本 = ''
    for q in (经, os.path.join('设定', '02_余章之势_总纲.md')):   # 势之裁可落总纲
        p = os.path.join(root, q)
        if os.path.exists(p):
            本 += open(p, encoding='utf-8', errors='replace').read()
    红 = []
    档 = []
    for f in glob.glob(os.path.join(root, '设定', '裁_*.md')):
        m = re.match(r'裁_(\d{4})_', os.path.basename(f))
        if m and m.group(1) >= '0927':
            档.append(f)
    档 += glob.glob(os.path.join(root, '设定', '剧情庭_*.md'))
    for f in sorted(档):
        名 = os.path.basename(f)[:-3]
        if 名 in 本:
            continue
        if '圣经无改' in open(f, encoding='utf-8', errors='replace').read():
            continue
        红.append(名)
    return 红


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '设定'))
        open(os.path.join(t, 经), 'w').write('# 圣经\n')
        共 += 1; ok += (查(t) == [])
        open(os.path.join(t, '设定', '剧情庭_D9.md'), 'w').write('裁：改甲为乙')
        共 += 1; ok += (查(t) == ['剧情庭_D9'])             # 裁了而圣经未随 → 红
        open(os.path.join(t, 经), 'a').write('某律（据 剧情庭_D9）\n')
        共 += 1; ok += (查(t) == [])
        open(os.path.join(t, '设定', '裁_0930_某.md'), 'w').write('裁：守原。圣经无改（由：现文已是最好）')
        共 += 1; ok += (查(t) == [])
        open(os.path.join(t, '设定', '裁_0901_旧.md'), 'w').write('旧裁')
        共 += 1; ok += (查(t) == [])                        # 0927 前之旧裁不查
    finally:
        shutil.rmtree(t)
    print('圣经随裁·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    红 = 查()
    if 红:
        print('⛔ 圣经随裁：%d 份裁未落进圣经：%s（圣经里写「据 档名」，或裁档自书「圣经无改」并其由）' % (len(红), '｜'.join(红)))
        sys.exit(1)
    print('✓ 圣经随裁：0927 以後之裁与剧情庭之裁，份份已落进圣经')
