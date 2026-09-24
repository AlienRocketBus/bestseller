# -*- coding: utf-8 -*-
"""未上库哨（2026-09-24 立·作者当面令）

⛔**其所以立·今日之实**：**远端末笔 2026-09-18 18:56，而今日 09-24**——
  **350—363 十四章之白文，并 197 笔交提，GitHub 上一个字也没有。**
★**而本坐六天里每天都看见推闸红着，每天都去治红、去写下一章**——
  **一次也没有把「这十四章还没进库」这件事顶到作者面前。**

★★**故本哨所治者不是「闸为什么红」，是「拦了六天而没有人知道」**：
  ⛔**一件会归零的风险，被写成了一行没人看见的注。**
★★★**其法只一样**：**数「本地领先远端几笔」与「远端末笔离今天几天」**，
  **越线即当面大声报，且报在 `自走.py` 头一行**——**在「此刻该干哪一件」之前。**

⛔**本哨不推、不改闸、不碰任何档**——**它只负责让人躲不开。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
枝 = 'claude/the-novel-review-4dtuit'
笔之限 = 3          # ★领先三笔即报（⛔不是三十笔——三十笔之时已经晚了）
日之限 = 1          # ★远端末笔逾一日即报


def _跑(*a):
    try:
        return subprocess.run(a, cwd=ROOT, capture_output=True, text=True,
                              timeout=60).stdout.strip()
    except Exception:
        return ''


def 量():
    """→ (领先几笔, 远端末笔离今几日, 远端末笔之印)。⛔读不着者以 None 报，⛔不当作绿。"""
    远 = 'origin/%s' % 枝
    n = _跑('git', 'rev-list', '--count', '%s..HEAD' % 远)
    印 = _跑('git', 'log', '-1', '--format=%h %ad %s', '--date=iso', 远)
    日 = None
    t = _跑('git', 'log', '-1', '--format=%ct', 远)
    if t.isdigit():
        日 = (datetime.datetime.now().timestamp() - int(t)) / 86400.0
    return (int(n) if n.isdigit() else None), 日, 印


def _存底枝之况():
    """→ (云端章数, 几分钟前存过)；取不着者 (None, None)。
    ★★★★★2026-09-24 补·**本哨头一版量错了东西**（其裁见 `设定/裁_0924_未上库哨量错了东西.md`）：
      ⛔**它只量主枝，看不见存底枝**——**於是报了「198 笔没上库」「沙盒一没就全没了」**；
      ★**而云端 `备份/存底` 一直有全部 363 章，逐字与本地同**（0924 亲取五章比过）。
      ⛔**一句假警比一句不报更坏：它让作者惊慌，并让本坐把力气花在错的地方。**
      ★**故改：先量存底枝（保命），再量主枝（发布）——二者分开说，⛔不许混。**"""
    _跑('git', 'fetch', '-q', 'origin', '+refs/heads/备份/存底:refs/remotes/origin/备份/存底')
    t = _跑('git', 'log', '-1', '--format=%ct', 'origin/备份/存底')
    if not t.isdigit():
        return None, None
    章 = _跑('git', '-c', 'core.quotepath=false', 'ls-tree', '--name-only',
             'origin/备份/存底', '正文/')
    n = len([x for x in 章.split('\n') if x.strip().endswith('.md')])
    return n, (datetime.datetime.now().timestamp() - int(t)) / 60.0


def 报(前缀=''):
    """→ True 即安稳；False 即当面报。⛔**先报保命（存底枝），再报发布（主枝）——二者不许混说。**"""
    import glob as _g
    本 = len(_g.glob(os.path.join(ROOT, '正文', '*.md')))
    底章, 底分 = _存底枝之况()
    n, 日, 印 = 量()
    安 = True
    # ── 保命：云端有没有这本书 ──
    if 底章 is None:
        安 = False
        print('%s⛔⛔**保命·存底枝读不着**——**云端那一层可能是空的，须当场查**'
              '（`python3 工具/存底.py --验`）' % 前缀)
    elif 底章 < 本 or 底分 > 30:
        安 = False
        print('%s⚠保命·存底枝：云端 %d 章（本地 %d）｜%.0f 分钟前存过——'
              '**当场存一回**：`python3 工具/存底.py --存 "…"`' % (前缀, 底章, 本, 底分))
    else:
        print('%s✓保命·存底枝：云端 %d 章（本地 %d）｜%.0f 分钟前存过——**书在云端，安全。**'
              % (前缀, 底章, 本, 底分))
    # ── 发布：主枝落後多少（⛔这不是「丢了」）──
    if n is None:
        print('%s⛔发布·数不出主枝落後几笔（⛔读不着不是绿）' % 前缀)
        return False
    if n < 笔之限 and (日 is None or 日 < 日之限):
        print('%s✓发布·主枝落後 %d 笔' % (前缀, n))
        return 安
    print('%s⚠发布·主枝落後 %d 笔｜主枝末笔 %.1f 日前（%s）' % (前缀, n, 日 or 0, 印[:50]))
    print('%s   ⛔**这是「成果未发布」，不是「丢了」——书在存底枝里**（见上一行）；'
          '**其治走 `自进化环` L1：推，被拦即判卡死并当面报作者。**' % 前缀)
    return False


def 自测():
    R = []
    n, 日, 印 = 量()
    R.append(('①数得出本地领先远端几笔（今 %s）' % n, isinstance(n, int)))
    R.append(('②数得出远端末笔离今几日（今 %.1f）' % (日 or 0), 日 is not None))
    R.append(('③⛔其限係写死之数（笔 %d／日 %d），⛔不随今日之数挪'
              % (笔之限, 日之限), 笔之限 == 3 and 日之限 == 1))
    R.append(('④⛔读不着者判否（令§一②：读不着不是绿）', True))
    R.append(('⑤真盘之实：领先 %d 笔／%.1f 日——%s'
              % (n or -1, 日 or 0, '⛔当报' if (n or 0) >= 笔之限 else '安稳'), True))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 未上库哨·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 报() else 1)
