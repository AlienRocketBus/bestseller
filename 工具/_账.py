# -*- coding: utf-8 -*-
"""_账——**每一样器，只要跑过一次，就自己在账上留一笔。**

【其立之由（2026-09-10·作者亲令）】
  作者说：「我们做的所有的这个机制一定要跑起来，一定要跑起来，如果跑不起来，那根本就没有用了。」
  ★而囤灰闸只答得出「它接没接上跑口」（静态可达），答不出「它到底跑没跑过」——
  **一样器可以稳稳地接在跑口上，而一次也没有真被执行过。** 这两件事差得很远。
  ★★故立本账：**不问它接没接上，只问它跑没跑过、末一回是几时。**

【为什么是「自记」而不是「包一层」】
  包一层（拿 `跑账.py --跑 工具/X.py` 去跑）要改四十五处提示词，而**提示词是人／模型照着做的，会漏**。
  自记不会漏：**器一被 python 载入，这一笔就落了**——不靠谁记得。

【它绝不许做的三样】
  ①绝不许抛（任何一处出岔，一律吞掉——**一个记账的把正事弄挂了，比不记账坏得多**）；
  ②绝不许慢（只开一次档、只写一次，无网、无锁）；
  ③绝不许改仓里别的东西（它只碰 `_跑账.json` 一档）。
"""
import os
import sys
import json
import time

def _落():
    try:
        名 = os.path.basename(getattr(sys.modules.get('__main__'), '__file__', '') or '')
        if not 名 or 名.startswith('_'):
            return
        根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        档 = os.path.join(根, '_跑账.json')
        try:
            d = json.load(open(档, encoding='utf-8'))
        except Exception:
            d = {}
        今 = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        d.setdefault('_立账', 今)   # ★立账之日：此日之前无凭，不许拿来判谁没跑过
        一 = d.get(名) or {}
        一['末跑'] = 今
        一['次'] = int(一.get('次', 0)) + 1
        一.setdefault('头回', 今)
        d[名] = 一
        tmp = 档 + '.tmp%d' % os.getpid()
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(tmp, 档)
    except Exception:
        pass

_落()
