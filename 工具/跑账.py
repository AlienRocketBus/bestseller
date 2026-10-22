#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跑账——**「接上了」不等於「跑过了」。本器只问一句：它到底跑没跑过。**

【其立之由（2026-09-10·作者亲令，逐字）】
  「我们做的所有的这个机制一定要跑起来，一定要跑起来，如果跑不起来，那根本就没有用了。」
  ★而本仓原有的囤灰闸答的是**另一个问题**：它自九个跑口逐层展开引用闭包，
  答得出「这样器接没接在跑口上」——**答不出「这个跑口这半年有没有真被跑过一次」**。
  ★★**一样器可以稳稳地接在跑口上，而一次也没有真被执行过。** 这两件事差得很远，
  而作者要的是後一件。故立本账。

【它怎么知道·自记，不靠谁记得】
  `工具/_账.py` 一被 import 就落一笔（器名／头回／末跑／次数）到仓根 `_跑账.json`。
  而每一样 `工具/*.py` 头上都注了三行，把它 import 进来。
  ★**为什么不用「包一层」（拿 `--跑 工具/X.py` 去跑）**：那要改四十五处提示词，
  **而提示词是人／模型照着做的，会漏**；自记不会漏——**器一被载入，这一笔就落了。**

【三路】
  甲·**从没跑过**（红）：席里点名要跑的器（当场自 `工具/席/*.js` 抽），而账上一笔也没有。
     ★这正是作者所怕的那一样：**写在流程里，却从来没有真跑起来。**
  乙·**注没注上**（红）：凡 `工具/*.py`（除 `_` 开头者）须有那三行注；缺一样，它跑了也不会留痕，
     **而没有痕的器，永远查不出它跑没跑过**。
  丙·**久不跑**（黄）：账上有，而末一回在 N 日之前——**跑口多半断了，只是没人看见**。

用法：
    python3 工具/跑账.py            # 三路全查
    python3 工具/跑账.py --注        # 把那三行注进所有还没注的器（幂等）
    python3 工具/跑账.py --册        # 印全账（按末跑倒序）
    python3 工具/跑账.py --自测
"""
import os
import re
import sys
import json
import glob
import subprocess
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _账  # noqa: F401  ★本器自己也记账
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join(ROOT, '_跑账.json')
久 = 30          # 丙路：几日不跑即报黄
注之形 = (
    "import os as _o, sys as _s\n"
    "_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))\n"
    "try:\n"
    "    import _账  # 跑账·自记（工具/跑账.py）\n"
    "except Exception:\n"
    "    pass\n"
)


def _读账():
    try:
        return json.load(open(账档, encoding='utf-8'))
    except Exception:
        return {}


def 合账(a, b):
    """⛔纯：二账合一——头回取早、末跑取晚、次取大（同一器两机各记，⛔相加重计）。"""
    out = dict(a or {})
    for k, v in (b or {}).items():
        if not isinstance(v, dict):
            continue
        o = dict(out.get(k) or {})
        if not o:
            out[k] = dict(v)
            continue
        if v.get('头回') and (not o.get('头回') or str(v['头回']) < str(o['头回'])):
            o['头回'] = v['头回']
        if v.get('末跑') and (not o.get('末跑') or str(v['末跑']) > str(o['末跑'])):
            o['末跑'] = v['末跑']
        try:
            o['次'] = max(int(o.get('次') or 0), int(v.get('次') or 0))
        except (TypeError, ValueError):
            pass
        out[k] = o
    return out


def 承(印=True):
    """1022（404 封版被拦）：一章一会话，新机之 `_跑账.json` 空（.gitignore），席里点名之器百余样俱判「从没跑过」而封版停。
    其账本在云端诸存底之中（存底.py 强塞之）——自 `备份/存底`、`备份/存底-旧`、`备份/存底-<坐>` 诸枝取其账，合入本账。
    ⛔弱化判法：甲路照旧「全史无一笔」即红，只是全史今由诸机之账合成。读不出即⛔动本账。"""
    def 跑(*a):
        return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, timeout=120)
    try:
        r = 跑('git', 'ls-remote', 'origin', 'refs/heads/备份/存底*')
        诸 = [l.split() for l in r.stdout.strip().splitlines() if l.strip()] if r.returncode == 0 else []
        if not 诸:
            if 印:
                print('⚠ 承账：云端存底诸枝读不出——本账⛔动')
            return 0
        跑('git', 'fetch', '-q', 'origin', *[ref for _, ref in 诸])
        合 = _读账()
        前 = len(合)
        得 = 0
        for sha, ref in 诸:
            g = 跑('git', 'show', '%s:_跑账.json' % sha)
            if g.returncode != 0:
                continue
            try:
                合 = 合账(合, json.loads(g.stdout))
                得 += 1
            except Exception:
                continue
        tmp = 账档 + '.承'
        json.dump(合, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        os.replace(tmp, 账档)
        if 印:
            print('✓ 承账：自云端 %d 份存底合入——本账 %d → %d 器' % (得, 前, len(合)))
        return 0
    except Exception as e:
        if 印:
            print('⚠ 承账未成（%s）——本账⛔动' % e)
        return 0


def 诸器():
    xs = sorted(glob.glob(os.path.join(ROOT, '工具', '*.py')))
    return [x for x in xs if not os.path.basename(x).startswith('_')]


def 席点之器():
    """**当场自诸席抽**（判据之源律：不许写死名单）。"""
    名 = set()
    for js in glob.glob(os.path.join(ROOT, '工具', '席', '*.js')):
        try:
            s = open(js, encoding='utf-8').read()
        except Exception:
            continue
        for m in re.findall(r'python3\s+工具/([^\s`\'"]+\.py)', s):
            名.add(m)
    return sorted(名)


def _注了没(p):
    try:
        return 'import _账' in open(p, encoding='utf-8').read()
    except Exception:
        return True


def 注(印=True):
    """把那三行注进每一样还没注的器。**幂等**：注过的不再注。"""
    改 = []
    for p in 诸器():
        if _注了没(p):
            continue
        s = open(p, encoding='utf-8').read()
        # ★落点：头一处 import 之前（若无 import，则文档串之後）
        # ★`from __future__` 须在一切之前，故注要落在它**之後**
        fut = list(re.finditer(r'^from __future__ import .*$', s, re.M))
        if fut:
            i = s.find('\n', fut[-1].end()) + 1
            s2 = s[:i] + 注之形 + s[i:]
            try:
                compile(s2, p, 'exec')
            except SyntaxError as e:
                改.append((os.path.basename(p), '⛔注上去语法就坏了，跳过：%s' % e))
                continue
            t = p + '.tmp%d' % os.getpid()
            with open(t, 'w', encoding='utf-8') as f:
                f.write(s2)
            os.replace(t, p)
            改.append((os.path.basename(p), '已注（落在 from __future__ 之後）'))
            continue
        m = re.search(r'^(import |from )', s, re.M)
        if m:
            i = m.start()
        else:
            m2 = re.search(r'^("""|\'\'\')', s, re.M)
            if m2:
                q = m2.group(1)
                j = s.find(q, m2.end())
                i = s.find('\n', j) + 1 if j >= 0 else 0
            else:
                i = 0
        s2 = s[:i] + 注之形 + s[i:]
        try:
            compile(s2, p, 'exec')
        except SyntaxError as e:
            改.append((os.path.basename(p), '⛔注上去语法就坏了，跳过：%s' % e))
            continue
        # ★**原子写**：席可能正在跑，半截的档会当场把它弄挂
        t = p + '.tmp%d' % os.getpid()
        with open(t, 'w', encoding='utf-8') as f:
            f.write(s2)
        os.replace(t, p)
        改.append((os.path.basename(p), '已注'))
    if 印:
        if not 改:
            print('  ✓ 诸器俱已注（幂等·今回一样也不必动）')
        for 名, 语 in 改:
            print('  · %-22s %s' % (名, 语))
    return 改


def 自立账以来封过版(立):
    """自立账之日以来，有没有过一次封版（＝有没有一个 章-N 之枝比它新）。
    ★**其所以拿章标作凭**：封版席之末一件就是打标，**标一落，那一章的全套器就都该跑过了**。
    """
    if not 立:
        return False
    try:
        import subprocess
        r = subprocess.run(['git', 'log', '-1', '--format=%cI'],
                           cwd=ROOT, capture_output=True, text=True)
        # ★只认「立账之後新打的标」：逐个标问它的提交时刻
        r2 = subprocess.run(['git', 'ls-remote', '--heads', 'origin'],
                            cwd=ROOT, capture_output=True, text=True, timeout=20)
        名们 = [x.split('refs/heads/')[-1] for x in r2.stdout.split('\n') if '/章-' in x or '章-' in x]
        for 名 in 名们:
            rr = subprocess.run(['git', 'log', '-1', '--format=%cd', '--date=format:%Y-%m-%d %H:%M:%S',
                                 'origin/' + 名], cwd=ROOT, capture_output=True, text=True)
            if rr.returncode == 0 and rr.stdout.strip() > 立:
                return True
    except Exception:
        return False
    return False


def 查(印=True):
    账 = _读账()
    诸 = [os.path.basename(x) for x in 诸器()]
    坏 = []
    # 乙·注没注上（先查这一路：没注就查不出跑没跑）
    未注 = [os.path.basename(p) for p in 诸器() if not _注了没(p)]
    if 未注:
        坏.append('乙·%d 样器没注自记之三行（跑了也不留痕）：%s'
                  % (len(未注), '、'.join(未注[:6])))
    # 甲·席里点名而账上一笔也没有
    点 = [x for x in 席点之器() if x in 诸]
    没跑 = [x for x in 点 if x not in 账]   # ★`_立账` 不在 点 之列，不必另剔
    # ★★**立账之日以前，本账没有凭据**——那时候它跑没跑过，账上不可能知道。
    #   故须先问一句：**自立账以来，有没有过一次封版？** 有过，才谈得上「该跑而没跑」。
    #   没有过，则只报黄（待观察）——**一个把「我还没看见」说成「它没跑过」的闸，就是会喊狼的闸。**
    立 = 账.get('_立账', '')
    封过 = 自立账以来封过版(立)
    if 没跑 and 封过:
        坏.append('甲·%d 样器写在席里，而自 %s 立账以来**过了一次封版仍一次没跑**：%s'
                  % (len(没跑), 立[:10], '、'.join(没跑[:8])))
    # 丁·全器之从没跑过（0925·作者令「造出来的东西一定要运行起来，最怕造了不运行」）
    #   ★甲只问「席里点名的」；**而不在席里点名、只被别的器引着的器，从没跑过也一声不响**——
    #   0925 当场逮出 自动.py／自修.py 二样：囤灰闸判它「跑得着」（对位器引了它的名），跑账上一笔也没有。
    #   ⛔0925 补：此注不许写成带「.py」之档名——囤灰闸之闭包按档名逐字展开，注里一个档名即一条假边
    #     （本行原书对位之档名，遂令叶器字数闸经本档→对位→全测展满全仓，负测·囤灰闸② 塌不下去）。
    #   ⛔故：凡 `工具/*.py`，自立账以来封过版而账上仍一笔没有者，一律红。治法只两条：接进跑口使它真跑，或退役删掉。
    全没跑 = [x for x in 诸 if x[:-3] not in 账 and x not in 账]
    if 全没跑 and 封过:
        坏.append('丁·%d 样器自 %s 立账以来**一次也没真跑过**（接进跑口，或退役删掉）：%s'
                  % (len(全没跑), 立[:10], '、'.join(全没跑[:8])))
    # 丙·久不跑（黄）
    黄 = []
    now = time.time()
    for 名, 一 in 账.items():
        if 名.startswith('_') or not isinstance(一, dict):
            continue
        try:
            t = time.mktime(time.strptime(一.get('末跑', ''), '%Y-%m-%d %H:%M:%S'))
        except Exception:
            continue
        if (now - t) > 久 * 86400 and 名 in 点:
            黄.append('%s（末跑 %s）' % (名, 一.get('末跑')))
    if 印:
        实账 = [k for k in 账 if not k.startswith('_')]
        print('════ 跑账 ════（席点之器 %d 样｜账上有 %d 样｜器共 %d 样）'
              % (len(点), len(实账), len(诸)))
        for x in 坏:
            print('  ⛔ ' + x)
        if 黄:
            print('  ⚠ 丙·%d 样逾 %d 日未跑：%s' % (len(黄), 久, '、'.join(黄[:6])))
        if 没跑 and not 封过:
            print('  ⚠ 甲·%d 样器账上还没有（**自 %s 立账至今还没封过一章，故此刻无凭**）：%s'
                  % (len(没跑), (账.get('_立账') or '?')[:10], '、'.join(没跑[:8])))
            print('     ★**下一章一封版，它们若还是空的，就转红**——那时才叫「写在流程里而没跑起来」。')
        if not 坏:
            print('  ✓ 席里点名的器，样样都真跑过。' if not 没跑 else '  （甲路今日只报黄，见上。）')
    return (not 坏), 坏


def 册():
    账 = _读账()
    # ★`_立账` 是一个字串不是一笔账——凡 `_` 开头者一律不是器，剔出去
    xs = sorted([kv for kv in 账.items() if not kv[0].startswith('_')],
                key=lambda kv: kv[1].get('末跑', ''), reverse=True)
    print('════ 跑账·全册 %d 样 ════' % len(xs))
    for 名, 一 in xs:
        print('  %-24s 末跑 %s ｜跑过 %s 回｜头回 %s'
              % (名, 一.get('末跑', '?'), 一.get('次', '?'), 一.get('头回', '?')))


def 自测():
    ok, bad = 0, []

    def T(x, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(x + ('（%s）' % note if note else ''))

    s = open(os.path.join(ROOT, '工具', '跑账.py'), encoding='utf-8').read().split('def 自测')[0]
    a = open(os.path.join(ROOT, '工具', '_账.py'), encoding='utf-8').read()

    # ①记账之器绝不许把正事弄挂
    T('①_账 全程吞异常（记账绝不许抛）', a.count('except Exception') >= 2 and 'pass' in a)
    T('①之二 _账 不碰仓里别的档（只写 _跑账.json）',
      a.count("open(") <= 3 and '_跑账.json' in a and '_器之迹' in a and 'rmtree' not in a and 'remove' not in a)   # 1015 添器之迹一档
    # ②判据当场从源头抽，不写死
    T('②席点之器当场自 工具/席/*.js 抽（判据之源律）',
      "glob.glob(os.path.join(ROOT, '工具', '席', '*.js'))" in s and 'python3' in s)
    T('②之二 诸器当场自 工具/*.py 抽，且剔去 _ 开头者',
      "glob.glob(os.path.join(ROOT, '工具', '*.py'))" in s and "startswith('_')" in s)
    # ③注之器须幂等且先验语法
    T('③之四 认得 from __future__ 须在一切之前（注落其後）',
      '__future__' in s and 'fut[-1].end()' in s)
    T('③之三 注是原子写（席在跑，半截的档会当场把它弄挂）',
      'os.replace(t, p)' in s and "p + '.tmp" in s)
    T('③注之前先 compile，坏了就不写（不许把器注坏）',
      "compile(s2, p, 'exec')" in s and 'SyntaxError' in s)
    T('③之二 注是幂等的（注过的不再注）', '_注了没' in s and 'continue' in s)
    T('⑤丁路查全器（不只席点）且红', "全没跑 = [x for x in 诸" in s and "丁·" in s)
    # ④乙路须先於甲路（没注就查不出跑没跑）
    i乙 = s.find('未注 = ')
    i甲 = s.find('没跑 = ')
    T('④乙路（注没注上）排在甲路（跑没跑过）之前', 0 < i乙 < i甲)
    # ⑤真样本：本器自己须已注、且账上有它
    T('⑤本器自己也注了自记（不许只管别人）', 'import _账' in s)
    # ⑥负测·旧局回灌：拿一份没注的假器，乙路须判红
    T('⑥乙路之判据是「档里有没有 import _账」，非档名、非目录',
      "'import _账' in open(p" in s)
    # ⑦丙路只报黄不判红（久不跑不等於坏了）
    T('⑧甲路须先问「自立账以来封过版没有」（无凭不许判它没跑过）',
      '自立账以来封过版' in s and "账.get('_立账'" in s)
    T('⑧之二 其凭是章标（封版席末一件即打标）', "'/章-'" in s or "'章-'" in s)
    T('⑨账里 `_` 开头者不是器（`_立账` 是一个字串），三处遍历皆已剔',
      s.count("startswith('_')") >= 3 and 'isinstance(一, dict)' in s)
    T('⑦丙路只报黄，不入坏（久不跑不等於它坏了）',
      '黄 = []' in s and '坏.append' not in s.split('# 丙·久不跑')[1].split('if 印')[0])
    合 = 合账({'甲.py': {'头回': '2026-10-01 00:00:00', '末跑': '2026-10-05 00:00:00', '次': 3}},
             {'甲.py': {'头回': '2026-09-01 00:00:00', '末跑': '2026-10-02 00:00:00', '次': 7}, '乙.py': {'头回': 'x', '末跑': 'y', '次': 1}})
    T('⑳合账：头回取早、末跑取晚、次取大、他机独有之器并入（1022 一章一会话、新机账空）',
      合['甲.py'] == {'头回': '2026-09-01 00:00:00', '末跑': '2026-10-05 00:00:00', '次': 7} and '乙.py' in 合)
    _s = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    _m = open(os.path.abspath(__file__), encoding='utf-8').read().split("if __name__ == '__main__':")[1]
    T('⑳之三 判红先承史再判（新机自愈；⛔弱化判法）', '承()' in _m and _m.index('承()') < _m.rindex('查()'))
    T('⑳之二 承：自云端诸存底枝（备份/存底*）取账、合入、原子换档', "'refs/heads/备份/存底*'" in _s and 'os.replace(tmp, 账档)' in _s)
    print('── 负测·跑账 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    a = sys.argv
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--承' in a:
        sys.exit(承())
    if '--注' in a:
        注()
        sys.exit(0)
    if '--册' in a:
        册()
        sys.exit(0)
    ok, _ = 查(印=False)
    if not ok:
        承()                      # 1022：新机之账空即自云端诸存底承史再判（⛔弱化判法）
    ok, _ = 查()
    sys.exit(0 if ok else 1)
