#!/usr/bin/env python3
"""改记（1008 立·作者令「每一次修改都要有详细的记录与备份——以最高效之法」）——零 token 读出改动之详录。

虫洞之法：⛔另造一套备份与日志（费时、会漏、会与实物不符）——**git 本身就是逐字之全记**：
  每一回提交＝改了哪档、哪几行、改前改後逐字；任何一版可原样取回（`git show <号>:<档>`）；
  推上 GitHub、又存存底枝＝双备份。重档（圣经、canon、状态册、正文）另有改单（改前整份备份＋修改清单，有闸）。
本器只把那份全记**读成人看得懂的样子**：哪一天、哪一档、哪一章，每一回改了什么、哪几行、为何改。

用法：
  python3 工具/改记.py                    # 末 20 回提交之详录（档、增删行数、所改之行段、说明）
  python3 工具/改记.py --日 2026-10-08     # 某一日之全部改动
  python3 工具/改记.py --档 设定/00_镇冢秘术_唯一总圣经.md   # 某一档之改动史
  python3 工具/改记.py --章 380            # 某一章（正文与版本目录）之改动史
  python3 工具/改记.py ... --细             # 并印所改之行（每档至多 40 行）
  python3 工具/改记.py --取 <提交号> <档>    # 取回某一版之原文（备份即在 git 里）
  python3 工具/改记.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob, subprocess, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _git(args, root):
    return subprocess.run(['git', '-c', 'core.quotepath=off'] + args, cwd=root, capture_output=True, text=True).stdout


def 章之档(n, root):
    try:
        from 对账预筛 import 章号
    except Exception:
        return ['版本/第%d章' % n]
    出 = [os.path.relpath(f, root) for f in glob.glob(os.path.join(root, '正文', '*.md')) if 章号(f) == n]
    return 出 + ['版本/第%d章' % n]


def 录(root=ROOT, 日=None, 档=None, 末=20, 细=False):
    args = ['log', '--date=format:%Y-%m-%d %H:%M', '--format=\x01%h|%ad|%s', '-p', '--unified=0', '--no-color']
    if 日:
        args += ['--since=%s 00:00' % 日, '--until=%s 23:59' % 日]
    else:
        args += ['-n', str(末)]
    if 档:
        args += ['--'] + 档
    out = _git(args, root)
    条 = []
    for 块 in out.split('\x01')[1:]:
        头, _, 身 = 块.partition('\n')
        号, 时, 说 = (头.split('|', 2) + ['', ''])[:3]
        档们 = []
        for 段 in re.split(r'^diff --git ', 身, flags=re.M)[1:]:
            m = re.match(r'a/(\S+) b/(\S+)', 段)
            名 = m.group(2) if m else 段.split('\n', 1)[0]
            区 = re.findall(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', 段, re.M)
            增 = len(re.findall(r'^\+(?!\+\+)', 段, re.M))
            删 = len(re.findall(r'^-(?!--)', 段, re.M))
            行段 = []
            for a, an, b, bn in 区:
                bn = int(bn) if bn != '' else 1
                行段.append(('%s' % b) if bn <= 1 else ('%s—%d' % (b, int(b) + bn - 1)))
            改行 = [l for l in 段.split('\n') if (l.startswith('+') and not l.startswith('+++')) or (l.startswith('-') and not l.startswith('---'))]
            档们.append((名, 增, 删, 行段, 改行))
        条.append((号, 时, 说, 档们))
    for 号, 时, 说, 档们 in 条:
        print('■ %s｜%s｜%s' % (时, 号, 说[:160]))
        for 名, 增, 删, 行段, 改行 in 档们:
            段s = '、'.join(行段[:12]) + ('……（共 %d 段）' % len(行段) if len(行段) > 12 else '')
            print('   · %s　+%d／−%d　行：%s' % (名, 增, 删, 段s or '—'))
            if 细:
                for l in 改行[:40]:
                    print('       ' + l[:200])
    if not 条:
        print('（无改动）')
    return 条


def 取(号, 档, root=ROOT):
    sys.stdout.write(_git(['show', '%s:%s' % (号, 档)], root))


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        g = lambda *a: subprocess.run(['git'] + list(a), cwd=t, capture_output=True, text=True)
        g('init', '-q'); g('config', 'user.email', 'x@y'); g('config', 'user.name', 'x')
        os.makedirs(os.path.join(t, '设定'))
        p = os.path.join(t, '设定', '甲.md')
        open(p, 'w', encoding='utf-8').write('一\n二\n三\n')
        g('add', '-A'); g('commit', '-qm', '立甲')
        open(p, 'w', encoding='utf-8').write('一\n贰\n三\n四\n')
        g('add', '-A'); g('commit', '-qm', '改甲：二作贰、添四')
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            条 = 录(t, 末=5, 细=True)
        共 += 1; ok += (len(条) == 2 and 条[0][2] == '改甲：二作贰、添四')
        档们 = 条[0][3]
        共 += 1; ok += (档们 and 档们[0][0] == '设定/甲.md' and 档们[0][1] == 2 and 档们[0][2] == 1)
        共 += 1; ok += ('-二' in buf.getvalue() and '+贰' in buf.getvalue())
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            取(条[1][0], '设定/甲.md', t)
        共 += 1; ok += (buf2.getvalue() == '一\n二\n三\n')       # 旧版原样取回
    finally:
        shutil.rmtree(t)
    print('改记·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a[:1] == ['--取'] and len(a) == 3:
        取(a[1], a[2]); sys.exit(0)
    细 = '--细' in a
    a = [x for x in a if x != '--细']
    if a[:1] == ['--日'] and len(a) == 2:
        录(日=a[1], 细=细)
    elif a[:1] == ['--档'] and len(a) >= 2:
        录(档=a[1:], 末=200, 细=细)
    elif a[:1] == ['--章'] and len(a) == 2 and a[1].isdigit():
        录(档=章之档(int(a[1]), ROOT), 末=200, 细=细)
    elif not a:
        录(细=细)
    else:
        print(__doc__); sys.exit(2)
