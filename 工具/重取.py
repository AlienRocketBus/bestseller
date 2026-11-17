#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重取（1024 立·盘坏之哨）——容器之盘生坏块时，立 <git 公目>/盘坏.flag 而众哨见之；本器只印重 clone 换目之步（⛔自跑）。

【其由·1024 实踩】容器之盘生坏块：git 读包与 版本/ 三千余档俱 Input/output error。`工具/存底守.py` 06:25 起每回 add 皆败，
  只记於 .git/存底守.log、无人见；直到建 worktree 时 git reset 死於 signal 7（SIGBUS）方觉——其间云端之底一回未更。已重 clone 换目。
【其法·零 token】存底.py 之 _跑（诸 git 之调俱经此）与 存底守 之一回，遇 Input/output error／signal 7／Bus error 即立旗
  （首见之时、档、语；已在即⛔覆——留首见者）。自走之前哨与 SessionStart 之钩（存底守 --起）见旗即印
  「⛔ 盘坏：…——照 python3 工具/重取.py 之法重 clone 换目」。新目之 .git 无此旗，换目即自清；误立者 `--清`。
用法：
  python3 工具/重取.py          # 印重 clone 换目之步（⛔自跑：盘坏之机，跑一半死於 signal 7 更糟——人照步逐条跑、逐条看）
  python3 工具/重取.py --查     # 旗在即印 ⛔ 一行、rc=1；否则 ✓
  python3 工具/重取.py --清     # 误立之旗除之
  python3 工具/重取.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
旗名 = '盘坏.flag'
主枝 = 'claude/the-novel-review-4dtuit'   # 读不出本枝时之退路（与 存底.主枝 同；⛔另起尺：自测对之）
泊式 = re.compile(r'^(章-\d+|治-[0-9a-f]{12})$')   # 推後之泊（1117·法用#停钩空转·与 推报.泊式 同：自测对之）——重取之仓⛔立於泊枝


def 本枝(当):
    """→ 重取之仓所检出之枝：读不出、游离、或泊於「章-N」／「治-<sha12>」者 → 主枝（泊枝无上游、其提交已在入主之途）；余照其枝。"""
    return 主枝 if (not 当 or 当 == 'HEAD' or 泊式.match(当)) else 当
_坏式 = re.compile(r'Input/output error|signal 7|Bus error|SIGBUS', re.I)


def 公目():
    """git 之公目（worktree 里 .git 係一档，⛔径接 ROOT/.git）。"""
    try:
        p = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if p:
            return p if os.path.isabs(p) else os.path.join(ROOT, p)
    except Exception:
        pass
    return os.path.join(ROOT, '.git')


def 迹(rc, 语=''):
    """⛔纯判：一调之 rc 与其错语有盘坏之迹否。-7 係 subprocess 死於 SIGBUS；135 係经 shell 者（128+7）。"""
    return rc in (-7, 135) or bool(_坏式.search(语 or ''))


def 立(档, 语, 目=None):
    """首见即立旗（时、档、语）；旗已在⛔覆（留首见者）。回 True 即此回新立。写不下⛔抛（盘坏之机，守⛔因此崩）。"""
    p = os.path.join(目 or 公目(), 旗名)
    if os.path.exists(p):
        return False
    行 = next((l for l in (语 or '').splitlines() if _坏式.search(l)), (语 or '').strip() or 'signal 7')
    try:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({'时': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()), '档': str(档)[:200],
                       '语': 行.strip()[:240]}, f, ensure_ascii=False)
        return True
    except Exception:
        return False


def 查迹(rc, 语, 档, 目=None):
    """诸器之调毕顺手一问：有迹即立。回 迹否。"""
    if 迹(rc, 语):
        立(档, 语, 目)
        return True
    return False


def 读(目=None):
    try:
        return json.load(open(os.path.join(目 or 公目(), 旗名), encoding='utf-8'))
    except FileNotFoundError:
        return None
    except Exception:
        return {'时': '?', '档': '?', '语': '旗在而读不出'}


def 印(目=None):
    """→ '' 或 ⛔ 一行（自走前哨、SessionStart 之钩用）。"""
    d = 读(目)
    if not d:
        return ''
    return ('⛔ 盘坏：%s 首见於 %s（%s）——照 python3 工具/重取.py 之法重 clone 换目'   # ★档、语截短：自走默印每行截於 160 字，⛔截掉其法
            % (d.get('时', ''), str(d.get('档', ''))[:30], str(d.get('语', ''))[:50]))


def _读(*a):
    try:
        r = subprocess.run(list(a), cwd=ROOT, capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else ''
    except Exception:
        return ''


def 步(仓, 枝, 远, 名, 邮, 排=None):
    """⛔纯：重 clone 换目之步（1024 今所行之法）。只印，⛔自跑。"""
    新 = 仓 + '.new'
    排 = 排 or os.path.join(仓, '.git', 'info', 'exclude')
    坏 = 仓 + '.坏.' + time.strftime('%m%d%H%M', time.gmtime())
    return [
        '# 重取（盘坏·重 clone 换目）——逐条跑、逐条看；⛔整段贴而不看（盘坏之机，一步死於 signal 7 即须停下）',
        '# 〇 先存底一回：python3 %s/工具/存底.py --存 "盘坏·重取前"（败亦续——云端之底以末回成者为准）' % 仓,
        '# 一 clone 至新目',
        'git clone %s %s' % (远 or '<origin 之 url：git -C %s remote get-url origin>' % 仓, 新),
        '# 二 checkout 本枝',
        'git -C %s checkout %s' % (新, 枝),
        '# 三 本仓之 git 设',
        'git -C %s config core.hooksPath 工具/githooks' % 新,
        'git -C %s config gc.auto 0' % 新,
        "git -C %s config user.name '%s'" % (新, 名 or '<旧仓之 user.name>'),
        "git -C %s config user.email '%s'" % (新, 邮 or '<旧仓之 user.email>'),
        '# 四 拷 .git/info/exclude 与被忽之状态档（_跑账.json、_任务流.json、_心跳.json 等；读不出者跳过——存底枝 备份/存底 有其 add -f 之本）',
        'cp %s %s/.git/info/exclude' % (排, 新),
        "cd %s && git ls-files -z --others --ignored --exclude-standard | grep -zv -e '__pycache__' -e '^\\.claude/worktrees/'"
        ' | xargs -0 -r cp --parents -t %s' % (仓, 新),
        '# 五 换目（先停旧守：其锁与日志在旧 .git）',
        "pkill -f '工具/存底守.py --跑'; mv %s %s && mv %s %s" % (仓, 坏, 新, 仓),
        '# 六 重起存底守',
        'cd %s && python3 工具/存底守.py --起' % 仓,
        '# 毕：python3 工具/重取.py --查 印 ✓（新 .git 无旗）；旧目 %s 留待作者删（⛔即删：其中或有未存之档可救）' % 坏,
    ]


def 自测():
    import tempfile
    r = []

    def T(名, 条):
        r.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    T('①迹：Input/output error、signal 7、SIGBUS 之 rc（-7／135）俱认', 迹(1, 'error: read 版本/x: Input/output error')
      and 迹(1, 'fatal: died of signal 7') and 迹(-7) and 迹(135) and 迹(1, 'Bus error (core dumped)'))
    T('①之二 寻常之败（无此远端、拒推、rc=1）⛔认', not 迹(1, 'fatal: 无此远端') and not 迹(128, 'rejected') and not 迹(0, ''))
    with tempfile.TemporaryDirectory() as d:
        T('②无旗 → 印空、读 None', 印(d) == '' and 读(d) is None)
        查迹(0, '', 'git add -A', d)
        T('②之二 无迹之调⛔立旗', 读(d) is None)
        新1 = 查迹(1, 'warning: x\nerror: 版本/第9章/a.md: Input/output error\nfatal: 败', 'git add -A', d)
        x = 读(d)
        T('③有迹 → 立旗，记首见之时、档、语（语取含迹之那一行）', 新1 and x and x['档'] == 'git add -A'
          and 'Input/output error' in x['语'] and '版本/第9章' in x['语'] and x['时'])
        查迹(-7, '', 'git reset', d)
        T('③之二 旗已在 → ⛔覆（留首见者）', 读(d)['档'] == 'git add -A')
        l = 印(d)
        T('④印：⛔ 盘坏 一行，指 重取.py 之法', l.startswith('⛔ 盘坏：') and 'python3 工具/重取.py 之法重 clone 换目' in l)
    with tempfile.TemporaryDirectory() as d:
        立('git -C /home/user/the-novel add -A -- 版本 正文 设定', 'error: ' + '版本/第九章/很长之档名' * 20 + ': Input/output error', d)
        l = 印(d)
        T('④之二 档、语虽长，印⛔逾 160 字而其法在末（自走默印截於 160）', len(l) <= 160 and l.endswith('之法重 clone 换目'))
    s = 步('/home/u/仓', '枝甲', 'https://x/y.git', '名', 'a@b')
    i = lambda k: next((n for n, x in enumerate(s) if k in x and not x.startswith('#')), -1)
    序 = [i('git clone https://x/y.git /home/u/仓.new'), i('checkout 枝甲'), i('core.hooksPath 工具/githooks'),
          i('gc.auto 0'), i("user.name '名'"), i('info/exclude'), i('--others --ignored'), i('mv /home/u/仓 '),
          i('存底守.py --起')]
    T('⑤步之序：clone → checkout 本枝 → hooksPath、gc.auto 0、user → 拷忽档 → mv 换目 → 存底守 --起', -1 not in 序 and 序 == sorted(序))
    src = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    跑们 = re.findall(r"subprocess\.run\(([^\n]*)", src)
    T('⑥⛔自跑：本器之 subprocess 只读（rev-parse 与 _读）、clone／mv／config 只在印之文里',
      len(跑们) == 2 and all("'clone'" not in x and "'mv'" not in x for x in 跑们) and 'os.rename' not in src and 'shutil' not in src)
    try:
        import 存底
        T('⑦退路之枝与 存底.主枝 同（⛔两把尺）', 主枝 == 存底.主枝)
    except Exception as e:
        T('⑦存底导入不得：%s' % e, False)
    try:
        import 推报
        T('⑧（1117·法用#停钩空转）泊於章-N／治-<sha12>、游离、读不出 → 主枝；他枝照其枝；泊式与 推报.泊式 同（⛔两把尺）',
          本枝('章-459') == 主枝 and 本枝('治-0123456789ab') == 主枝 and 本枝('HEAD') == 主枝 and 本枝('') == 主枝
          and 本枝('枝甲') == '枝甲' and 本枝('治-xyz') == '治-xyz' and 泊式.pattern == 推报.泊式.pattern
          and "步(仓, 本枝(_读('git', 'rev-parse', '--abbrev-ref', 'HEAD'))" in open(os.path.abspath(__file__), encoding='utf-8').read())
    except Exception as e:
        T('⑧推报导入不得：%s' % e, False)
    ok = sum(r)
    print('── 负测·重取 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--查' in a:
        l = 印()
        print(l or '✓ 盘无坏之旗（%s）' % os.path.join(公目(), 旗名))
        sys.exit(1 if l else 0)
    if '--清' in a:
        p = os.path.join(公目(), 旗名)
        if os.path.exists(p):
            os.remove(p)
            print('✓ 盘坏之旗已除（%s）' % p)
        else:
            print('✓ 无旗')
        sys.exit(0)
    _公 = 公目()
    仓 = os.path.dirname(_公) if os.path.basename(_公) == '.git' else ROOT   # worktree 之中亦指主仓（盘坏者主仓也）
    l = 印()
    print(l or '（今无盘坏之旗——此步备用）')
    for x in 步(仓, 本枝(_读('git', 'rev-parse', '--abbrev-ref', 'HEAD')), _读('git', 'remote', 'get-url', 'origin'),
               _读('git', 'config', '--get', 'user.name'), _读('git', 'config', '--get', 'user.email'),
               os.path.join(_公, 'info', 'exclude')):
        print(x)
    sys.exit(0)
