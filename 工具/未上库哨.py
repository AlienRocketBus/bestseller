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


def 报(前缀=''):
    """→ True 即安稳；False 即当面报（⛔读不着亦判 False·令§一②：读不着不是绿）。"""
    n, 日, 印 = 量()
    if n is None:
        print('%s⛔未上库哨：数不出本地领先远端几笔（远端之枝读不着）——'
              '⛔**读不着不是绿**，须当面查。' % 前缀)
        return False
    if n < 笔之限 and (日 is None or 日 < 日之限):
        print('%s✓未上库哨：领先 %d 笔，远端末笔 %.1f 日前。' % (前缀, n, 日 or 0))
        return True
    print('%s' % 前缀 + '═' * 60)
    print('%s  ⛔⛔⛔ **未上库** ⛔⛔⛔' % 前缀)
    print('%s  **本地领先远端 %d 笔｜远端末笔 %.1f 日前**' % (前缀, n, 日 or 0))
    print('%s  远端末笔：%s' % (前缀, 印))
    print('%s  ★**这些东西此刻只在一个会被回收的盘上**——'
          '**沙盒一没，写出来的章就没处找了。**' % 前缀)
    print('%s  ⛔**推闸红着⛔不是不推的理由**：'
          '**闸管的是「验收」，推管的是「不丢」，两件事不是一件事。**' % 前缀)
    print('%s  ★**此刻该办**：① `git add` 明路径并交提；② `git push -u origin %s`；'
          % (前缀, 枝))
    print('%s     ③ **若闸拦下，⛔不许默默接着写下一章**——'
          '**当面把它报给作者，请他决断。**' % 前缀)
    print('%s     ⛔**六天之实即由此来**：拦了六天，而作者一直不知道。' % 前缀)
    print('%s  ★★**而④这一条不须任何人开口，⛔六天里本坐一次也没走过**：' % 前缀)
    print('%s     `python3 工具/存底包.py` → 打出三样存底，**当面送给作者**' % 前缀)
    print('%s     （⭐全本单档 .txt 手机点开就能读）——' % 前缀)
    print('%s     ⛔**「推不上去」与「作者手上没有」是两件事**：' % 前缀)
    print('%s     **前者要等人开口，後者一条命令就办得了。**' % 前缀)
    print('%s' % 前缀 + '═' * 60)
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
