#!/usr/bin/env python3
"""升华之闸（0927·作者令「改不是为了及格，是为了升华：改就改到 95 分以上，且比原文更好；机制必须跑起来」）：
凡经大升级重写之章（版本/第N章/大升级前.md 在），须有 版本/第N章/_升华评.md，
三席（小说家、总编辑、顶尖读者）之新分皆 ≥95 且皆高於旧分；缺或不达即红。
用法：python3 工具/升华之闸.py ｜ --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, glob, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
行式 = re.compile(r'(小说家|总编辑|顶尖读者)[^\n]*?旧\s*(\d+)\s*[→\-—>]+\s*新\s*(\d+)')


def 查(root=ROOT):
    红 = []
    for d in sorted(glob.glob(os.path.join(root, '版本', '第*章'))):
        if not os.path.exists(os.path.join(d, '大升级前.md')):
            continue
        名 = os.path.basename(d)
        f = os.path.join(d, '_升华评.md')
        if not os.path.exists(f):
            红.append('%s无升华评' % 名); continue
        t = open(f, encoding='utf-8', errors='replace').read()
        分 = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in 行式.finditer(t)}
        if len(分) < 3:
            红.append('%s升华评缺席（%s）' % (名, '、'.join(分) or '无'))
            continue
        坏 = [k for k, (旧, 新) in 分.items() if 新 < 95 or 新 <= 旧]
        if 坏:
            红.append('%s未升华（%s）' % (名, '、'.join('%s %d→%d' % (k, *分[k]) for k in 坏)))
    return 红


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        d = os.path.join(t, '版本', '第5章'); os.makedirs(d)
        共 += 1; ok += (查(t) == [])                                   # 未重写不查
        open(os.path.join(d, '大升级前.md'), 'w').write('旧')
        共 += 1; ok += (查(t) == ['第5章无升华评'])
        open(os.path.join(d, '_升华评.md'), 'w').write('- 小说家：旧 80 → 新 96\n- 总编辑：旧 82 → 新 95\n- 顶尖读者：旧 78 → 新 97\n')
        共 += 1; ok += (查(t) == [])
        open(os.path.join(d, '_升华评.md'), 'w').write('- 小说家：旧 80 → 新 90\n- 总编辑：旧 82 → 新 95\n- 顶尖读者：旧 78 → 新 97\n')
        共 += 1; ok += (len(查(t)) == 1 and '未升华' in 查(t)[0])      # 只到及格 → 红
        open(os.path.join(d, '_升华评.md'), 'w').write('- 小说家：旧 97 → 新 96\n- 总编辑：旧 82 → 新 95\n- 顶尖读者：旧 78 → 新 97\n')
        共 += 1; ok += (len(查(t)) == 1)                              # 改了反而不如原文 → 红
    finally:
        shutil.rmtree(t)
    print('升华之闸·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    红 = 查()
    if 红:
        print('⛔ 升华之闸：%d 章（改就须改到 ≥95 且胜原文）：%s' % (len(红), '｜'.join(红[:12])))
        sys.exit(1)
    print('✓ 升华之闸：凡重写之章皆三席 ≥95 且胜原文')
