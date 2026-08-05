#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全测——一条命令跑完全部回归，一个结论定去留。

【批115·立】病灶：此前验证须分四次调用（检察官 --selftest／--doctor／全书检、十轮精进 --自测），
  四段输出各看各的，遂有「改一处而不知碰坏他处」之隙；本会话已两度自证——
  ZM_REOPEN 所写空 soft 记录令存版必崩、同名夹具后者覆盖前者令二测名义在跑而实测旧局，
  皆是「改bug时造bug」而当时四段输出俱绿。
  故立全测：一条命令、一个退出码；并由 pre-push 钩子强制，不过不许推。

用法：
    python3 工具/全测.py            # 全跑
    python3 工具/全测.py --快        # 略过全书检（仅自检层，供频繁调用）
"""
import os
import re
import sys
import ast
import glob
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, ZM_STREAM=os.environ.get('ZM_STREAM', 'streamA-cli'))


def run(desc, args, timeout=900):
    try:
        r = subprocess.run([sys.executable] + args, cwd=ROOT, env=ENV,
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return '__TIMEOUT__'
    except Exception as e:
        return '__ERR__%s' % e


def chk_selftest():
    out = run('检察官自测', ['工具/小说检察官.py', '--selftest'])
    m = re.search(r'规则回归:(\d+)/(\d+)；契约负测:(\d+)/(\d+)；项目接线:(\S+?)；末章硬闸:(\S+)', out)
    if not m:
        return False, '未取到自测结论行'
    a, b, c, d, e, f = m.groups()
    ok = (a == b and c == d and e == '通过' and f.startswith('通过'))
    return ok, '规则回归%s/%s 契约负测%s/%s 接线%s 末章硬闸%s' % (a, b, c, d, e, f)


def chk_doctor():
    out = run('医生', ['工具/小说检察官.py', '--doctor'])
    m = re.search(r'医生结论: ERROR=(\d+)', out)
    if not m:
        return False, '未取到医生结论'
    return m.group(1) == '0', 'ERROR=%s' % m.group(1)


def chk_shilun():
    out = run('十轮精进负测', ['工具/十轮精进.py', '--自测'])
    m = re.search(r'负测（含端到端真跑）：(\d+)/(\d+)', out)
    if not m:
        m = re.search(r'负测：(\d+)/(\d+)', out)
    if not m:
        return False, '未取到负测结论'
    return m.group(1) == m.group(2), '%s/%s' % m.groups()


def chk_book():
    out = run('全书检', ['工具/小说检察官.py'])
    m = re.search(r'全书仪表盘:ERROR=(\d+)', out)
    if not m:
        return False, '未取到全书仪表盘'
    return m.group(1) == '0', 'ERROR=%s' % m.group(1)


def chk_dup_defs():
    """重名定义扫描。
    病灶实证：批113所加之 s_withlog／s_nolog／s_reopen 落在批114替换区之外而与新写者重名，
    后定义者覆盖前者，令二条负测名义在跑而实测旧局。此类错不报错、不崩、静默改变行为，
    非专测不可得。"""
    bad = []
    for f in sorted(glob.glob(os.path.join(ROOT, '工具', '*.py'))):
        try:
            tree = ast.parse(open(f, encoding='utf-8').read())
        except SyntaxError as e:
            bad.append('%s 语法错误 %s' % (os.path.basename(f), e))
            continue
        for node in ast.walk(tree):
            body = getattr(node, 'body', None)
            if not isinstance(body, list):
                continue
            seen = {}
            for st in body:
                if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if st.name in seen:
                        bad.append('%s: %s 于同一作用域重复定义（行%d 覆盖 行%d）'
                                   % (os.path.basename(f), st.name, st.lineno, seen[st.name]))
                    seen[st.name] = st.lineno
    return not bad, ('；'.join(bad) if bad else '工具目录内无重名定义')


def chk_zishu():
    """字数对齐探测器之回归。
    此规则住在 check_file 内，而检察官 138 条自测只跑 canon 正则（hits 不经 check_file），
    故其从来无回归——批117 修其二处误报时才发现。修探测器最忌静默削弱，
    故正测（真错须报）与负测（误报须不报）并立。"""
    import tempfile, importlib.util as u, sys
    sys.argv = ['x']
    sp = u.spec_from_file_location('_i2', os.path.join(ROOT, '工具', '小说检察官.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)

    def flagged(body):
        d = tempfile.mkdtemp()
        f = os.path.join(d, '镇冢秘术_第七章_测.md')
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n' + body + '\n')
        iss, _, _ = m.check_file(f)
        return any(x.startswith('[字数对齐]') for x in iss)

    POS = [   # 真错，必须报
        ('前向·数在前引在后', '过了几步他说了四个字。\n\n“今天你对了。”\n\n他点了点头。'),
        ('后向·引在前数在后', '“不知道。”\n\n这两个字从他嘴里出来，我心里咯噔一下。'),
        ('换行·引在前数在后', '“留给回来的人。”\n\n这四个字他说得很平。'),
    ]
    NEG = [   # 误报，必须不报
        ('数指前句非后句', '“等。”他说。\n\n就一个字。\n\n“等天黑。”'),
        ('数指前句非后句·二', '“不信。”\n\n就两个字。\n\n“那你来干什么。”'),
        ('数指前句非后句·三', '“摸。”\n\n一个字。\n\n“我先过。”'),
        ('两句合计报数', '“发烫，就回来。”\n\n他看着我。\n\n“灯灭。莫回头。”\n\n十个字，一个不差。'),
        ('数与引全合', '他说了五个字。\n\n“水一直在流。”'),
    ]
    bad = []
    for name, body in POS:
        if not flagged(body):
            bad.append('漏报:' + name)
    for name, body in NEG:
        if flagged(body):
            bad.append('误报:' + name)
    n = len(POS) + len(NEG)
    return not bad, ('；'.join(bad) if bad else '正测%d/负测%d 全通' % (len(POS), len(NEG)))


def chk_hookspath():
    """钩子须挂上：容器每次重建后 .git 皆新，故 hooksPath 须指向受版本管理之目录。"""
    want = '工具/githooks'
    try:
        r = subprocess.run(['git', 'config', '--get', 'core.hooksPath'],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
        cur = r.stdout.strip()
    except Exception as e:
        return False, '读取失败 %s' % e
    hook = os.path.join(ROOT, want, 'pre-push')
    if not os.path.exists(hook):
        return False, '缺 %s' % want + '/pre-push'
    if cur != want:
        subprocess.run(['git', 'config', 'core.hooksPath', want],
                       cwd=ROOT, capture_output=True, text=True, timeout=30)
        return True, '原为「%s」，已自动挂回 %s' % (cur or '未设', want)
    if not os.access(hook, os.X_OK):
        os.chmod(hook, 0o755)
        return True, '已挂，并补回执行位'
    return True, '已挂 %s' % want


def main():
    quick = '--快' in sys.argv
    items = [('重名定义扫描', chk_dup_defs), ('钩子挂载', chk_hookspath),
             ('字数对齐回归', chk_zishu),
             ('检察官自测', chk_selftest), ('医生', chk_doctor),
             ('十轮精进负测', chk_shilun)]
    if not quick:
        items.append(('全书检', chk_book))
    print('\n████ 全测 · %d 项 ████' % len(items))
    fails = []
    for name, fn in items:
        ok, detail = fn()
        print('  %s %-14s %s' % ('✓' if ok else '✗', name, detail))
        if not ok:
            fails.append(name)
    if fails:
        print('\n  ⛔全测未过：%s' % '、'.join(fails))
        print('  【批115】不过不许推——pre-push 钩子据此拦停。')
        return 1
    print('\n  ✓全测通过%s。' % ('（快测，未含全书检）' if quick else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
