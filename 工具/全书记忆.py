#!/usr/bin/env python3
"""全书记忆之闸（0927·作者令「通读一回就要全书记住，以後直接调取，不必每回再读」）：
自 设定/全书记忆/总览.md 立起之後启用：每一正文章须有 设定/全书记忆/第N章.md，且其所记 sha1（前十二位）与现正文相符；
正文改了而详记未随即红——记忆不许过期。用法：python3 工具/全书记忆.py ｜ --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, glob, hashlib, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
数 = {c: i for i, c in enumerate('零一二三四五六七八九')}


def 汉转(s):
    n = 0; 段 = 0
    for c in s:
        if c in 数:
            段 = 数[c]
        elif c == '十':
            n += (段 or 1) * 10; 段 = 0
        elif c == '百':
            n += 段 * 100; 段 = 0
    return n + 段


def 诸章(root):
    r = {}
    for p in glob.glob(os.path.join(root, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(p))
        if m:
            r[汉转(m.group(1))] = p
    return r


def 查(root=ROOT):
    d = os.path.join(root, '设定', '全书记忆')
    if not os.path.exists(os.path.join(d, '总览.md')):
        return None
    红 = []
    for n, p in sorted(诸章(root).items()):
        f = os.path.join(d, '第%d章.md' % n)
        if not os.path.exists(f):
            红.append('第%d章无详记' % n); continue
        h = hashlib.sha1(open(p, 'rb').read()).hexdigest()[:12]
        if h not in open(f, encoding='utf-8', errors='replace').read():
            红.append('第%d章详记过期（正文 sha1 %s）' % (n, h))
    return 红


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '正文')); os.makedirs(os.path.join(t, '设定', '全书记忆'))
        p = os.path.join(t, '正文', '镇冢秘术_第一百零七章_某.md'); open(p, 'w').write('正文甲')
        共 += 1; ok += (查(t) is None)                      # 总览未立，不启
        open(os.path.join(t, '设定', '全书记忆', '总览.md'), 'w').write('览')
        共 += 1; ok += (查(t) == ['第107章无详记'])
        h = hashlib.sha1(b'\xe6\xad\xa3\xe6\x96\x87\xe7\x94\xb2').hexdigest()[:12]
        open(os.path.join(t, '设定', '全书记忆', '第107章.md'), 'w').write('sha1：' + h)
        共 += 1; ok += (查(t) == [])
        open(p, 'w').write('正文乙')
        共 += 1; ok += (len(查(t)) == 1 and '过期' in 查(t)[0])   # 正文改而记未随 → 红
        共 += 1; ok += (汉转('三百七十九') == 379 and 汉转('十一') == 11 and 汉转('一百一十七') == 117)
    finally:
        shutil.rmtree(t)
    print('全书记忆·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    红 = 查()
    if 红 is None:
        print('ℹ 全书记忆：总览未立，闸未启')
        sys.exit(0)
    if 红:
        print('⛔ 全书记忆：%d 处（正文改了而详记未随，记忆不许过期）：%s' % (len(红), '｜'.join(红[:12])))
        sys.exit(1)
    print('✓ 全书记忆：诸章详记齐全且与正文相符')
