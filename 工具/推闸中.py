#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""推闸中（1022 立·坑：推闸之全测跑时改 设定／版本／正文，「负测留字」即红、推被拦）——PreToolUse 钩。

【其由】pre-push 跑全测（十余分），其「负测留字」於起止各照 设定／版本／正文 诸档之 sha256，二者之差即判
  「负测改了真仓未复原」而红、拦推。1022 总编辑於全测之中改坑账诸表（设定/方法升级_*.md 等），推遂被拦，
  白耗一回全测——此坑旧已知之（W51 记「主仓库之项以 _留字快照 查之」），而凭记性守，复踩。
【其法】pre-push 起时写 `<git 公目>/推闸中.pid`（毕即删）；本钩见其 pid 尚活，而工具之调用要写
  设定／版本／正文 者——Edit／Write 之 file_path 在其下，或 Bash 之令点到其下且有写之状——即拦，印候其毕之由。
  读（cat、grep、git show、Read）照放。
【1027·律⑮之机化（线B·#34）】席在跑时，主环只许动自己手上那几条明路径——⛔动整个工作区：
  `git stash`（list／show 除外）、`git checkout .`（或 -- .）、`git reset --hard`、`git clean -f`、`git add -A／--all／.` → 拦。
  「席在跑」取 `席在跑吗.流在跑()`（读本机工作流之 journal 与其目之 mtime·毫秒级；⛔调 心跳.py——其每调必 git fetch，
  而本钩挂在每一个 Bash 之上）。只拦对主工作区之令：命令先 cd 入他目（worktree）、或钩入之 cwd 在 .claude/worktrees/ 下者放（⛔误拦·丝滑）。
用法：钩自 stdin 取 JSON；`python3 工具/推闸中.py --自测`
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
管目 = ('设定', '版本', '正文')
写之状 = re.compile(r"open\([^)]*['\"][wa]['\"]|>>?\s*\S|\bsed\s+-i|\btee\b|\bcp\s|\bmv\s|\brm\s|"
                   r"git\s+(checkout|merge|reset|stash|apply|am|cherry-pick|pull)|--立|--守|--格|--同步|--复踩|\.write\(|write_text")


def _仓目():
    try:
        p = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if p:
            return p if os.path.isabs(p) else os.path.join(ROOT, p)
    except Exception:
        pass
    return os.path.join(ROOT, '.git')


def 推闸在跑(档=None):
    """→ pid 或 None：pre-push 之全测在跑否（pid 档在且其进程尚活）。"""
    档 = 档 or os.path.join(_仓目(), '推闸中.pid')
    try:
        pid = int(open(档).read().strip())
        os.kill(pid, 0)
        return pid
    except Exception:
        return None


def 触管(入):
    """→ 所触之管目之路（无则 ''）：此调用要写 设定／版本／正文 否。"""
    名 = (入.get('tool_name') or '')
    参 = 入.get('tool_input') or {}
    if 名 in ('Edit', 'Write', 'NotebookEdit', 'MultiEdit'):
        p = os.path.abspath(str(参.get('file_path') or 参.get('notebook_path') or ''))
        for d in 管目:
            if p.startswith(os.path.join(ROOT, d) + os.sep):
                return os.path.relpath(p, ROOT)
        return ''
    if 名 == 'Bash':
        c = re.sub(r'[0-9&]*>>?\s*(/dev/null\b|&[0-9])', ' ', str(参.get('command') or ''))   # 1023：2>/dev/null、2>&1 非写（只读之令被误拦）
        if not 写之状.search(c):
            return ''
        for d in 管目:
            if (d + '/') in c or ('/' + d + '/') in c:
                return d + '/'
        if re.search(r'方法坑账\.py\s+--(立|守|格|同步|复踩)', c):
            return '设定/（方法坑账）'
    return ''


整区之令 = re.compile(r'\bgit\s+(?:-C\s+\S+\s+)?(?:'
                     r'stash(?!\s+(?:list|show)\b)|'
                     r'checkout\s+(?:--\s+)?\.(?=\s|$|;|&|\|)|'
                     r'reset\s+(?:\S+\s+)*--hard\b|'
                     r'clean\s+(?:\S+\s+)*-[a-zA-Z]*f|'
                     r'add\s+(?:\S+\s+)*(?:-A|--all|\.)(?=\s|$|;|&|\|))')


def _剔引(c):
    c = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", '', c, flags=re.S)
    c = re.sub(r'"(?:[^"\\]|\\.)*"', '""', c)
    return re.sub(r"'[^']*'", "''", c)


def 整区之触(入):
    """→ 所中之令（无则 ''）：Bash 之令动整个主工作区否（命令先 cd 入他目、钩入之 cwd 在 worktree 者⛔算）。"""
    if (入.get('tool_name') or '') != 'Bash':
        return ''
    c = _剔引(str((入.get('tool_input') or {}).get('command') or ''))
    m = 整区之令.search(c)
    if not m:
        return ''
    前 = c[:m.start()]
    cd = re.findall(r'(?:^|[;&|(\n])\s*cd\s+(\S+)', 前)
    目 = cd[-1] if cd else str(入.get('cwd') or ROOT)
    目 = os.path.realpath(os.path.expanduser(目)) if os.path.isabs(os.path.expanduser(目)) else os.path.realpath(os.path.join(str(入.get('cwd') or ROOT), 目))
    根 = os.path.realpath(ROOT)
    if (目 + os.sep).startswith(os.path.join(根, '.claude', 'worktrees') + os.sep) or not (目 == 根 or 目.startswith(根 + os.sep)):
        return ''
    if re.search(r'\bgit\s+-C\s+\S*\.claude/worktrees/', c[:m.end()]):
        return ''
    return m.group(0).strip()


def 流在跑():
    try:
        import 席在跑吗
        return bool(席在跑吗.流在跑())
    except Exception:
        return False


def 判(入, 在跑=None, 流=None):
    令 = 整区之触(入)
    if 令 and (流 or 流在跑)():
        return True, ('⛔推闸中（律⑮·1027 机化）：有席在跑（本机工作流之 journal 新、未收），此令「%s」动整个工作区——'
                      '会冲掉席所写之档或把半成之档收进提交。只动自己手上之明路径（git add <档>…、git checkout -- <档>）；'
                      '或候其流毕再动。' % 令[:60])
    pid = (在跑 if 在跑 is not None else 推闸在跑)
    if callable(pid):
        pid = pid()
    if not pid:
        return False, ''
    p = 触管(入)
    if not p:
        return False, ''
    return True, ('⛔推闸中：pre-push 之全测在跑（pid %d）——此时写 %s 即令「负测留字」红、推被拦（1022 实踩）。'
                  '候其毕（後台之推之通知到）再写；只读照放。' % (pid, p))


def 自测():
    import tempfile
    r = []

    def T(名, 条):
        r.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    在 = lambda: 4242
    E = lambda p: {'tool_name': 'Edit', 'tool_input': {'file_path': os.path.join(ROOT, p)}}
    B = lambda c: {'tool_name': 'Bash', 'tool_input': {'command': c}}
    T('①推闸在跑：Edit 设定/ 下之档 → 拦', 判(E('设定/甲.md'), 在)[0])
    T('①之二 Write 正文/、版本/ → 拦', 判({'tool_name': 'Write', 'tool_input': {'file_path': os.path.join(ROOT, '正文/x.md')}}, 在)[0]
      and 判(E('版本/第1章/a.md'), 在)[0])
    T('①之三 Edit 工具/、仓根之档 → 放（留字不照）', not 判(E('工具/甲.py'), 在)[0] and not 判(E('00_总章.md'), 在)[0])
    T('②Bash 以 python 写 设定/ → 拦', 判(B("python3 - <<'EOF'\nopen('设定/瑕疵总账.md','w').write(s)\nEOF"), 在)[0])
    T('②之二 Bash 方法坑账 --立／--同步 → 拦（写 设定/）', 判(B('python3 工具/方法坑账.py --同步'), 在)[0])
    T('②之三 Bash 只读 设定/（cat、grep、git show）→ 放', not 判(B('cat 设定/甲.md | head'), 在)[0]
      and not 判(B("git show origin/x:设定/甲.md"), 在)[0])
    T('②之四 Bash git merge（改工作区）而点到 正文/ → 拦', 判(B('git merge origin/x && ls 正文/'), 在)[0])
    T('②之五 只读之令带 2>/dev/null、2>&1 而点到 设定/ → 放（1023 误拦）；真写 > 设定/ 仍拦',
      not 判(B('grep -c 417 设定/甲.json 2>/dev/null; ls 设定/ 2>&1 | head'), 在)[0] and 判(B('echo x > 设定/甲.md 2>/dev/null'), 在)[0])
    T('③推闸未跑 → 一概放', not 判(E('设定/甲.md'), lambda: None)[0])
    # ★1027 律⑮之机化（#34）：席在跑时⛔动整个工作区；流未跑、读之令、明路径、他目（worktree）→ 放
    跑 = lambda: True
    停 = lambda: False
    Bc = lambda c, cwd=ROOT: {'tool_name': 'Bash', 'cwd': cwd, 'tool_input': {'command': c}}
    T('⑦席在跑：git stash／checkout .／reset --hard／clean -fd／add -A 俱拦',
      all(判(Bc(c), lambda: None, 跑)[0] for c in ('git stash', 'git stash push -u -m x', 'git checkout .', 'git checkout -- .',
                                                  'git reset --hard HEAD', 'git reset -q --hard origin/x', 'git clean -fd',
                                                  'cd %s && git add -A && git commit -m x' % ROOT, 'git add --all', 'git add .')))
    T('⑦之二 流未跑 → 放（⛔误拦·丝滑）', not 判(Bc('git stash'), lambda: None, 停)[0] and not 判(Bc('git reset --hard'), lambda: None, 停)[0])
    T('⑦之三 席在跑而只动明路径、只读 → 放：git add 档、checkout -- 档、stash list、clean -n、status',
      not any(判(Bc(c), lambda: None, 跑)[0] for c in ('git add 工具/甲.py 设定/乙.json', 'git checkout -- 工具/甲.py', 'git stash list',
                                                     'git stash show -p', 'git clean -n', 'git status', 'git checkout -B zh/B abc',
                                                     'git commit -m "git add -A 之禁"', "echo 'git reset --hard'")))
    T('⑦之四 席在跑而令先 cd 入 worktree、或钩之 cwd 在 worktree → 放',
      not 判(Bc('cd %s/.claude/worktrees/wf_x && git add -A' % ROOT), lambda: None, 跑)[0]
      and not 判(Bc('git add -A', cwd=os.path.join(ROOT, '.claude', 'worktrees', 'wf_x')), lambda: None, 跑)[0]
      and not 判(Bc('cd /tmp/x && git stash'), lambda: None, 跑)[0])
    _src = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    T('⑦之五 流在跑取 席在跑吗.流在跑（本地 mtime）、⛔调心跳（其每调 git fetch）', '席在跑吗.流在跑()' in _src and 'import 心跳' not in _src)
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, 'p')
        open(f, 'w').write(str(os.getpid()))
        T('④pid 档在而其进程活 → 在跑', 推闸在跑(f) == os.getpid())
        open(f, 'w').write('999999999')
        T('④之二 pid 已死 → ⛔在跑（推崩而档残⛔永拦）', 推闸在跑(f) is None)
    p = subprocess.run([sys.executable, os.path.abspath(__file__)], input=json.dumps(E('设定/甲.md')),
                       capture_output=True, text=True)
    T('⑤真跑：推闸未跑时 rc=0', p.returncode == 0 or 推闸在跑() is not None)
    try:
        st = json.load(open(os.path.join(ROOT, '.claude', 'settings.json'), encoding='utf-8'))
        钩 = [e for e in (st.get('hooks') or {}).get('PreToolUse', []) for h in e.get('hooks', []) if '推闸中' in h.get('command', '')]
        T('⑥settings 之 PreToolUse 挂本器，matcher 中 Edit、Write、Bash', bool(钩) and all(re.search(钩[0]['matcher'], n) for n in ('Edit', 'Write', 'Bash')))
        hk = open(os.path.join(ROOT, '工具', 'githooks', 'pre-push'), encoding='utf-8').read()
        T('⑥之二 pre-push 起时写 推闸中.pid、毕即删', '推闸中.pid' in hk and 'trap' in hk)
    except Exception as e:
        T('⑥settings／pre-push 读不出：%s' % e, False)
    ok = sum(r)
    print('── 负测·推闸中 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


if __name__ == '__main__':
    if '--自测' in sys.argv[1:]:
        sys.exit(0 if 自测() else 1)
    try:
        入 = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                      # 入坏⛔拦（本钩只防留字，非安全之闸）
    拦, 由 = 判(入)
    if 拦:
        print(由, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)
