#!/usr/bin/env python3
"""链之检（1013 立·坑⑰复踩之守）——PreToolUse 钩：主环之 Bash 命令里「python3 工具/封版.py … | tail && python3 工具/推.py」这一形（工具之管道後接 &&）而无 pipefail 者，拦。

为何立：`A | tail && B` 之 && 判的是 tail 之返回码，不是 A 的——A 败了 B 照跑。
  1013 实踩：381 封版，主环写 `python3 工具/封版.py 381 --後 2>&1 | tail -40 && python3 工具/推.py`，
  封版若败，推照推（幸 pre-push 之全测仍拦）。坑⑰（1009）之治只写在法典「以 && 相连或 set -e」，
  而 && 遇管道即失效——只写在纸上之治不算治，故立此钩（坑⑰之计：「主环之链若再踩，立 PreToolUse 钩」）。
判：先剔 heredoc 之体与引号中之字（坑㉑：码里、话里之字⛔认）；见 `python3 工具/…py … | … &&` 且全命令无 `pipefail` → 拦（rc=2，理由入 stderr）。
⛔只拦此一形（工具之败要紧、且确定失效）；`grep | head && echo` 之类不拦（⛔为一个钩多拦一回空活）。

用法（钩自调：stdin 为 {"tool_name":"Bash","tool_input":{"command":…}}）：
  python3 工具/链之检.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import sys, re, json

形 = re.compile(r'python3\s+\S*工具/\S+\.py[^|&;\n]*\|(?!\|)[^&;\n]*&&')


def _剔(c):
    c = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", '', c, flags=re.S)
    c = re.sub(r'"(?:[^"\\]|\\.)*"', '""', c)
    c = re.sub(r"'[^']*'", "''", c)
    return re.sub(r'\d*>&\d*|&>', ' ', c)          # 2>&1、&> 是转向，⛔认作 && 之 &（1013 自测逮）


伪停 = re.compile(r'(^|[;&|\n]\s*)set\s+-[a-z]*e[a-z]*\b')


def 判(c):
    """→ 拦之由（字符串）或 None。"""
    if 伪停.search(_剔(c or '')):
        # ★1013 实测：本壳（Bash 工具）里 set -e 不生效——`set -e; false; echo x` 照印 x；python 之 heredoc 败了後几行照跑（改单 G1013-01 因此先结後改）
        return ('⛔链之检（坑⑰·复踩2）：本壳 set -e 不生效（1013 实测：set -e; false; echo 照印）——'
                '多步之命令一律以 && 相连（pipefail 生效，可留）；把 set -e 去掉、改链再发。')
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
    def T(c, 应拦):
        nonlocal ok, 共
        共 += 1; ok += (bool(判(c)) == 应拦)
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
    print('链之检·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    try:
        d = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                       # 读不出即放（钩⛔把正事弄挂）
    if d.get('tool_name') != 'Bash':
        sys.exit(0)
    由 = 判((d.get('tool_input') or {}).get('command') or '')
    if 由:
        print(由, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)
