#!/usr/bin/env python3
"""链之检（1013 立·坑⑰复踩之守；1027 扩·坑⑤与绕钩之禁）——PreToolUse 钩：主环之 Bash 命令里诸确定失效／违律之形，拦。

为何立：`A | tail && B` 之 && 判的是 tail 之返回码，不是 A 的——A 败了 B 照跑。
  1013 实踩：381 封版，主环写 `python3 工具/封版.py 381 --後 2>&1 | tail -40 && python3 工具/推.py`，
  封版若败，推照推（幸 pre-push 之全测仍拦）。坑⑰（1009）之治只写在法典「以 && 相连或 set -e」，
  而 && 遇管道即失效——只写在纸上之治不算治，故立此钩（坑⑰之计：「主环之链若再踩，立 PreToolUse 钩」）。
判：先剔 heredoc 之体与引号中之字（坑㉑：码里、话里之字⛔认）；见 `python3 工具/…py … | … &&` 且全命令无 `pipefail` → 拦（rc=2，理由入 stderr）。
⛔只拦确定失效、或总章明禁之形；`grep | head && echo` 之类不拦（⛔为一个钩多拦一回空活）。
1027 执行之核（作者令「要避之坑须全部执行起来」·线 B）添：
  ①坑⑤（1007、1009、1017 三踩）：等推以 pgrep／`ps … | grep`（git push／推.py／全测）猜进程 → 拦，指 `推.py --等｜--候`（flock）。
  ②总章§五「⛔--no-verify、ZM_SKIP_HOOK」：git 之令带 --no-verify（commit 之 -n 同）、`ZM_SKIP_HOOK=` 之设、`-c core.hooksPath=` → 拦；
    唯 git push 之 refspec 俱係 备份/* 者放（存底、心跳之备份枝本即免闸；⛔误拦）。
  ③写者唯一（主枝唯 GitHub autopush 写；`推.py --直` 在 python 内调 git、⛔经此钩，係唯一之审计之例外）：
    Bash 之 git push 其靶及主枝（含 --all／--mirror、无 refspec 而当前枝即主枝）→ 拦。
  放行之反例（丝滑·⛔误拦）：echo 'pgrep'、heredoc 里之字、grep ZM_SKIP_HOOK 某档、git push origin HEAD:refs/heads/治-x、
    git push --no-verify origin x:refs/heads/备份/存底、git config core.hooksPath 工具/githooks（复原钩，⛔-c 之绕）。

用法（钩自调：stdin 为 {"tool_name":"Bash","tool_input":{"command":…}}）：
  python3 工具/链之检.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
主枝 = 'claude/the-novel-review-4dtuit'          # 与 推.枝、推报.主枝 同（自测对之）
形 = re.compile(r'python3\s+\S*工具/\S+\.py[^|&;\n]*\|(?!\|)[^&;\n]*&&')


def _剔(c):
    c = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", '', c, flags=re.S)
    c = re.sub(r'"(?:[^"\\]|\\.)*"', '""', c)
    c = re.sub(r"'[^']*'", "''", c)
    return re.sub(r'\d*>&\d*|&>', ' ', c)          # 2>&1、&> 是转向，⛔认作 && 之 &（1013 自测逮）


def _剔体(c):
    """只剔 heredoc 之体（引号中之字留：`grep "git push"` 之「git push」须见）。"""
    return re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", '', c or '', flags=re.S)


伪停 = re.compile(r'(^|[;&|\n]\s*)set\s+-[a-z]*e[a-z]*\b')
令首 = r'(?:^|[;&|(\n`]|\$\()\s*(?:(?:while|until|if|then|do|else|elif|!|time|sudo|nohup|exec|command|timeout\s+\S+)\s+)*'
pgrep式 = re.compile(令首 + r'pgrep\b')
ps管式 = re.compile(令首 + r'ps\b[^|;&\n]*\|\s*(?:grep|egrep|awk)\b([^;&\n|]*)')
推之字 = re.compile(r'git\s+push|推\.py|全测|push|pre-push')


def _段(c):
    """剔後之命令 → 诸简单命令之词（以 ; && || | 换行 ( ) 分）。引号之字已作 ''。"""
    出 = []
    for 段 in re.split(r'&&|\|\||[;|\n()&]', c):
        w = 段.split()
        if w:
            出.append(w)
    return 出


def _git之令(w):
    """词 → (设之变量［］, git 之全局之旗［］, 子令, 子令之参［］) 或 None（非 git 之令）。"""
    设 = []
    i = 0
    while i < len(w) and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', w[i]):
        设.append(w[i]); i += 1
    while i < len(w) and w[i] in ('env', 'sudo', 'command', 'nohup', 'exec', 'time'):
        i += 1
        while i < len(w) and re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', w[i]):
            设.append(w[i]); i += 1
    if i >= len(w) or not (w[i] == 'git' or w[i].endswith('/git')):
        return None
    i += 1
    全 = []
    while i < len(w):
        v = w[i]
        if v in ('-C', '-c', '--git-dir', '--work-tree', '--namespace', '--exec-path', '--config-env'):
            全 += w[i:i + 2]; i += 2
        elif v.startswith('-'):
            全.append(v); i += 1
        else:
            break
    if i >= len(w):
        return 设, 全, '', []
    return 设, 全, w[i], w[i + 1:]


_推值旗 = ('-o', '--push-option', '--receive-pack', '--exec', '--repo')


def _推之靶(参):
    """git push 之参 → (诸靶之枝名［］, 全推否)。无 refspec → [None]（当前枝）。"""
    位, i, 全 = [], 0, False
    while i < len(参):
        v = 参[i]
        if v in _推值旗:
            i += 2; continue
        if v in ('--all', '--mirror', '--tags') and v != '--tags':
            全 = True
        if v.startswith('-'):
            i += 1; continue
        位.append(v); i += 1
    if len(位) <= 1:
        return [None], 全
    靶 = []
    for r in 位[1:]:
        r = r.lstrip('+')
        dst = r.split(':', 1)[1] if ':' in r else r
        dst = re.sub(r'^refs/heads/', '', dst)
        靶.append(dst or None)
    return 靶, 全


def _当前枝(root=ROOT):
    try:
        root = root if root and os.path.isdir(root) else ROOT
        return subprocess.run(['git', 'symbolic-ref', '-q', '--short', 'HEAD'], cwd=root, capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        return ''


def _俱备份(靶):
    return bool(靶) and all(t and t.startswith('备份/') for t in 靶)


def 绕之判(c, 当前=None, 目=ROOT):
    """→ 拦之由或 None：①绕钩（--no-verify、ZM_SKIP_HOOK=、-c core.hooksPath=）②git push 之靶及主枝。"""
    剔 = _剔(c or '')
    if re.search(r'(?:^|[\s;&|(])(?:export\s+)?ZM_SKIP_HOOK=', 剔):
        return ('⛔链之检（总章§五·⛔ZM_SKIP_HOOK）：设 ZM_SKIP_HOOK 即绕 pre-push 之闸——闸红即照其红治（`python3 工具/推.py` 交 GitHub 之闸），⛔绕。')
    for w in _段(剔):
        g = _git之令(w)
        if not g:
            continue
        设, 全, 子, 参 = g
        if any(x.startswith('ZM_SKIP_HOOK=') for x in 设):
            return '⛔链之检（总章§五·⛔ZM_SKIP_HOOK）：设 ZM_SKIP_HOOK 即绕 pre-push 之闸——⛔绕。'
        绕旗 = [全[k + 1] for k in range(len(全) - 1) if 全[k] == '-c' and re.match(r'(?i)core\.hookspath=', 全[k + 1])]
        无验 = '--no-verify' in 参 or (子 == 'commit' and any(re.fullmatch(r'-[A-Za-z]*n[A-Za-z]*', x) and not x.startswith('--') for x in 参))
        if 子 == 'push':
            靶, 全推 = _推之靶(参)
            if (绕旗 or 无验) and not (_俱备份(靶) and not 全推):
                return ('⛔链之检（总章§五·⛔--no-verify、⛔绕钩）：「%s」——git push 绕 pre-push 之闸；唯 refspec 俱係 备份/* 者许（存底、心跳）。'
                        '照闸之红治，再 `python3 工具/推.py`（交 GitHub）。' % ' '.join(w)[:120])
            当 = None
            if None in 靶 or 'HEAD' in 靶:
                当 = 当前 if 当前 is not None else _当前枝(目)
            及主 = 全推 or any(t == 主枝 or (t in (None, 'HEAD') and 当 == 主枝) for t in 靶)
            if 及主:
                return ('⛔链之检（写者唯一·坑51／53）：「%s」——Bash 之 git push 其靶及主枝 %s。主枝唯 GitHub autopush 一写者：'
                        '`python3 工具/推.py`（交 治-<sha>，GitHub 分片而闸、过即并入）；报「拒」或 GitHub 停摆方 `python3 工具/推.py --直`（审计之例外）。'
                        % (' '.join(w)[:120], 主枝))
            continue
        if 绕旗:
            return ('⛔链之检（总章§五·⛔绕钩）：「%s」——以 -c core.hooksPath= 绕钩。复原钩用 `git config core.hooksPath 工具/githooks`。' % ' '.join(w)[:120])
        if 无验:
            return ('⛔链之检（总章§五·⛔--no-verify）：「%s」——绕钩之令⛔用；钩红即照其红治。' % ' '.join(w)[:120])
    return None


def 等推之判(c):
    """坑⑤：等推以 pgrep／ps|grep 猜进程 → 拦之由或 None。"""
    剔 = _剔(c or '')
    if pgrep式.search(剔):
        return ('⛔链之检（坑⑤·三踩：pgrep 认不着汉字名之进程、又认中本命令自身）：等推一律 `python3 工具/推.py --等`（flock，推者一放即返）'
                '或 `python3 工具/推.py --候 <sha>`（候 GitHub 并入主枝）；⛔pgrep、⛔sleep 环轮询（坑⑮）。')
    for 行 in _剔体(c or '').split('\n'):
        # 剔後之行有 ps|grep 之形（⛔认话里之字）；其所 grep 之字或在引号中——取原行验之
        if ps管式.search(_剔(行)) and 推之字.search(行):
            return ('⛔链之检（坑⑤）：以 `ps … | grep` 猜推送／全测之进程——等推一律 `python3 工具/推.py --等｜--候 <sha>`（flock）；⛔猜进程。')
    return None


def 判(c, 当前=None, 目=ROOT):
    """→ 拦之由（字符串）或 None。目：命令所跑之目（钩入之 cwd；无 refspec 之推以其当前枝判）。"""
    if 伪停.search(_剔(c or '')):
        # ★1013 实测：本壳（Bash 工具）里 set -e 不生效——`set -e; false; echo x` 照印 x；python 之 heredoc 败了後几行照跑（改单 G1013-01 因此先结後改）
        return ('⛔链之检（坑⑰·复踩2）：本壳 set -e 不生效（1013 实测：set -e; false; echo 照印）——'
                '多步之命令一律以 && 相连（pipefail 生效，可留）；把 set -e 去掉、改链再发。')
    由 = 等推之判(c) or 绕之判(c, 当前, 目)
    if 由:
        return 由
    剔 = _剔(c or '')
    if re.search(r'set\s+-o\s+pipefail|set\s+-[a-z]*o\s+pipefail', 剔):   # ★1013：须在剔後之命令里认（旧认原文，heredoc 正文里写着 pipefail 即整条放行——W22 方案之文实逮）
        return None
    m = 形.search(剔)
    if not m:
        return None
    return ('⛔链之检（坑⑰）：「%s」——管道之後之 && 判的是管道末一个命令之码，前头工具败了下一步照跑。'
            '改：命令首加 `set -o pipefail;`，或先跑工具、再另取其印。' % m.group(0)[:120])


def 自测():
    ok = 共 = 0
    def T(c, 应拦, 当前='某枝'):
        nonlocal ok, 共
        共 += 1
        r = bool(判(c, 当前)) == 应拦
        ok += r
        if not r:
            print('  ✗ %s：%s' % ('应拦' if 应拦 else '应放', c[:80]))
    T('cd /x && python3 工具/封版.py 381 --後 2>&1 | tail -40 && python3 工具/推.py 2>&1 | tail -12', True)   # 1013 实踩之原命令
    T('set -o pipefail; python3 工具/封版.py 381 --後 | tail -40 && python3 工具/推.py', False)
    T('python3 工具/封版.py 381 --後 && python3 工具/推.py | tail -3', False)        # 管道在末，无下一步
    T('python3 工具/全测.py --快 | grep 红 || echo 无', False)                        # || 非 &&
    T("python3 - <<'EOF'\nprint('python3 工具/推.py | tail && b')\nEOF", False)       # heredoc 之体⛔认
    T('git commit -m "python3 工具/推.py | tail && b"', False)                          # 引号中之字⛔认
    T('grep -n x a.md | head -3 && echo ok', False)                                    # 非工具之管道不拦
    T('python3 /home/user/the-novel/工具/造式验.py 381 | tail -5 && git add a', True)
    T('set -eo pipefail; cd /x && python3 a.py', True)                                  # set -e 不生效，拦
    T('set -e\npython3 - <<EOF\nx\nEOF\ngit add a', True)
    T('set -o pipefail; python3 工具/封版.py 1 --後 | tail && python3 工具/推.py', False)  # pipefail 生效，不拦
    T("python3 - <<'EOF'\nprint('set -e')\nEOF", False)                                # heredoc 之体⛔认
    T("cat > a.md <<'EOF'\n用 set -o pipefail 相链\nEOF\npython3 工具/方案.py --验 W | tail -1 && python3 b.py", True)   # heredoc 里之 pipefail ⛔作数
    # ★1027 坑⑤（三踩）：等推以 pgrep／ps|grep 猜进程 → 拦；话里、heredoc 里之字 → 放
    T('while pgrep -f "git push" >/dev/null; do sleep 30; done; echo 推毕', True)       # 1017 W51 主环之原命令（其形）
    T('pgrep -f 推.py || python3 工具/推.py', True)
    T('if ! pgrep -f 全测 ; then echo 无; fi', True)
    T('ps aux | grep "git push" | grep -v grep', True)
    T('ps -eo pid,cmd | grep 全测.py', True)
    T("echo 'pgrep 已禁'", False)
    T("cat > a.md <<'EOF'\n⛔pgrep -f 推\nps aux | grep git push\nEOF", False)
    T('grep -n pgrep 工具/推.py', False)
    T('ps aux | grep node', False)                                                     # 非推之 ps|grep ⛔拦
    T('python3 工具/推.py --等', False)
    # ★1027 总章§五：⛔--no-verify、⛔ZM_SKIP_HOOK、⛔-c core.hooksPath=；refspec 俱 备份/* 者放
    T('git push --no-verify origin HEAD:refs/heads/治-abc', True)
    T('git commit --no-verify -m x', True)
    T('git commit -nm x', True)
    T('ZM_SKIP_HOOK=1 git push origin HEAD:refs/heads/治-abc', True)
    T('export ZM_SKIP_HOOK=1; git push', True)
    T('git -c core.hooksPath=/dev/null push origin HEAD:refs/heads/治-x', True)
    T('git -c core.hooksPath=/dev/null commit -m x', True)
    T('git push --no-verify origin HEAD:refs/heads/备份/存底', False)                   # 存底、心跳之备份枝放
    T('git push -q --no-verify origin x:备份/心跳 y:refs/heads/备份/报', False)
    T('git push --no-verify origin HEAD:refs/heads/备份/存底 HEAD:refs/heads/治-x', True)  # 混推 → 拦
    T('grep -n ZM_SKIP_HOOK 工具/githooks/pre-push', False)                             # 读其字 ⛔拦
    T('git commit -m "⛔--no-verify 之律"', False)
    T('git config core.hooksPath 工具/githooks', False)                                 # 复原钩 ⛔拦
    T('git log -n 3', False)                                                           # 他令之 -n ⛔认作 no-verify
    # ★1027 写者唯一：Bash 之 git push 靶主枝 → 拦；治枝、章标、备份 → 放；无 refspec 视当前枝
    T('git push origin HEAD:claude/the-novel-review-4dtuit', True)
    T('git push -u origin claude/the-novel-review-4dtuit', True)
    T('git push origin +HEAD:refs/heads/claude/the-novel-review-4dtuit', True)
    T('cd /x && git push --all origin', True)
    T('git push', True, 当前=主枝)
    T('git push origin', True, 当前=主枝)
    T('git push', False, 当前='zh/B')
    T('git push origin HEAD', True, 当前=主枝)
    T('git push origin HEAD', False, 当前='zh/B')
    T('ps aux | grep node; echo ok', False)
    T('git push origin HEAD:refs/heads/治-abc123', False)
    T('git push origin HEAD:refs/heads/章-411', False)
    T('git push -u origin zh/B', False, 当前='zh/B')
    T("git commit -m 'git push origin claude/the-novel-review-4dtuit 之禁'", False)
    T('python3 工具/推.py --直', False)                                                 # 审计之例外在 python 内（⛔经此钩）
    print('链之检·自测 %d/%d' % (ok, 共))
    # 主枝之名与 推.py、推报 同（⛔另起尺）
    try:
        src = open(os.path.join(ROOT, '工具', '推.py'), encoding='utf-8').read()
        同 = ("枝 = '%s'" % 主枝) in src
    except Exception:
        同 = False
    print('  %s 主枝之名与 推.py 同' % ('✓' if 同 else '✗'))
    return ok == 共 and 同


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    try:
        d = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                       # 读不出即放（钩⛔把正事弄挂）
    if d.get('tool_name') != 'Bash':
        sys.exit(0)
    由 = 判((d.get('tool_input') or {}).get('command') or '', 目=d.get('cwd') or ROOT)
    if 由:
        print(由, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)
