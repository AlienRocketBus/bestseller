#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""圣经引号（0927 圣经大修⑥·改单#G0927-10 立）：逐条印出在役诸档里 `圣经:NNNN` 之引今天指着哪一行。

其由：圣经每改一次，行号即漂——`圣经:8161`（二线不通消息）一度被引 334 次，`圣经:7408`（二线之差六）240 次，
而到 0927 两号皆已漂到别条，执笔照引即读错律。二律已立为有编号之条（圣经「二、4 有编号之律」），
引作 `圣经§律·二线不通消息`／`圣经§律·二线之差六`；本器管其余仍以行号相引者。

查什么：
  ①在役之档（设定/ 顶层之 .md .json，⛔回执_*、冷轮_*、改单备份、回修案係案卷不查；工具/*.py、工具/席/*.js；
    版本/ 下尚无正文之章之卡）里每一处 `圣经:NNNN`：印其所在、所引之号、圣经今日那一行之头；
    标「空」＝那一行是空行或越出圣经之末；标「离题」＝引处前後之字与那一行一个二字词也对不上（粗判，只作提醒）。
  ②每一处 `圣经§律·名`：须在圣经里有「#### 律·名」之条，否则红。
判：
  · `圣经§律·名` 查无其条 → 红；
  · 空／离题之数高於基线（工具/圣经引号_基线.json）→ 红（⛔只许降不许升；降了用 --定基线 落新数）。
  · 其余只印不判：旧引行号之漂是旧账，本器把它摊开，不假装它是绿的。

用法：
  python3 工具/圣经引号.py            # 逐条印＋判
  python3 工具/圣经引号.py --静       # 只印总数与判
  python3 工具/圣经引号.py --定基线   # 把今日之空／离题数写作基线（只在数降了之後用）
  python3 工具/圣经引号.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import json
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
圣经名 = os.path.join('设定', '00_镇冢秘术_唯一总圣经.md')
引式 = re.compile(r'圣经:(\d{1,5})')
条式 = re.compile(r'圣经§律·([^\s`\\）)」』，。；、／|*①-⑳]+)')
案卷头 = ('回执_', '冷轮_')
免 = ('圣经引号.py', '圣经引号_基线.json')


def _在役(root):
    fs = []
    for p in sorted(glob.glob(os.path.join(root, '设定', '*'))):
        b = os.path.basename(p)
        if os.path.isdir(p) or b.startswith(案卷头) or not b.endswith(('.md', '.json')):
            continue
        fs.append(p)
    for p in sorted(glob.glob(os.path.join(root, '工具', '*.py')) + glob.glob(os.path.join(root, '工具', '席', '*.js'))):
        if os.path.basename(p) not in 免:
            fs.append(p)
    # 版本/：尚无正文之章（下一章之卡）
    已写 = set()
    for f in os.listdir(os.path.join(root, '正文')) if os.path.isdir(os.path.join(root, '正文')) else []:
        已写.add(f)
    for d in sorted(glob.glob(os.path.join(root, '版本', '第*章'))):
        n = re.search(r'第(\d+)章$', d)
        if not n:
            continue
        if any(os.path.basename(x).startswith('v') for x in os.listdir(d)):
            continue  # 已有稿之章係案卷
        fs += sorted(glob.glob(os.path.join(d, '*.md')))
    return fs


def _二字(s):
    s = re.sub(r'[^一-鿿]', '', s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def 查(root=ROOT):
    圣 = open(os.path.join(root, 圣经名), encoding='utf-8').read().split('\n')
    律 = set()
    for l in 圣:
        m = re.match(r'^#{2,5} 律·(\S+?)（', l) or re.match(r'^#{2,5} 律·(\S+)$', l)
        if m:
            律.add(m.group(1))
    行, 红 = [], []
    for p in _在役(root):
        rel = os.path.relpath(p, root)
        try:
            ls = open(p, encoding='utf-8').read().split('\n')
        except Exception:
            continue
        for i, l in enumerate(ls, 1):
            for m in 条式.finditer(l):
                if m.group(1) not in 律:
                    红.append('%s:%d 引 圣经§%s ⛔圣经无此条' % (rel, i, m.group(1)))
            for m in 引式.finditer(l):
                n = int(m.group(1))
                实 = 圣[n - 1] if 1 <= n <= len(圣) else None
                if 实 is None or not 实.strip():
                    旗 = '空'
                else:
                    境 = l[max(0, m.start() - 40):m.start()] + l[m.end():m.end() + 40]
                    旗 = '' if (_二字(境) & _二字(实)) else '离题'
                行.append((rel, i, n, (实 or '（越出圣经之末）').strip()[:60], 旗))
    return 行, 红


def _基线(root):
    p = os.path.join(root, '工具', '圣经引号_基线.json')
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None


def 判(行, 红, 基):
    坏 = sum(1 for x in 行 if x[4])
    msgs = list(红)
    if 基 is None:
        msgs.append('⛔无基线（工具/圣经引号_基线.json）')
    elif 坏 > 基.get('空离题', 0):
        msgs.append('⛔空／离题 %d ＞ 基线 %d（新添之行号引漂了，改引条号或改对行号）' % (坏, 基['空离题']))
    return 坏, msgs


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        for d in ('设定', '工具', os.path.join('工具', '席'), '正文', '版本'):
            os.makedirs(os.path.join(t, d))
        open(os.path.join(t, 圣经名), 'w', encoding='utf-8').write(
            '# 圣经\n\n#### 律·二线不通消息（x）\n二线不通消息之律\n\n门槛上那只勺\n')
        基 = {'空离题': 0}
        # ①引对 → 不旗
        open(os.path.join(t, '设定', '甲.md'), 'w', encoding='utf-8').write('见 `圣经:6` 门槛上那只勺\n')
        行, 红 = 查(t); 共 += 1; ok += (len(行) == 1 and 行[0][4] == '' and 判(行, 红, 基)[1] == [])
        # ②引空行 → 旗「空」→ 红（高於基线）
        open(os.path.join(t, '设定', '乙.md'), 'w', encoding='utf-8').write('见 `圣经:5`\n见 `圣经:99`\n')
        行, 红 = 查(t); 旗 = sorted(x[4] for x in 行 if x[0].endswith('乙.md'))
        共 += 1; ok += (旗 == ['空', '空'] and 判(行, 红, 基)[1] != [])
        os.remove(os.path.join(t, '设定', '乙.md'))
        # ③离题 → 旗
        open(os.path.join(t, '设定', '丙.md'), 'w', encoding='utf-8').write('钱满看图见 `圣经:4`\n')
        行, 红 = 查(t); 共 += 1; ok += any(x[4] == '离题' for x in 行)
        os.remove(os.path.join(t, '设定', '丙.md'))
        # ④条号有 → 不红；无 → 红
        open(os.path.join(t, '设定', '丁.md'), 'w', encoding='utf-8').write('`圣经§律·二线不通消息`\n')
        行, 红 = 查(t); 共 += 1; ok += (红 == [])
        open(os.path.join(t, '设定', '丁.md'), 'w', encoding='utf-8').write('`圣经§律·二线之差七`\n')
        行, 红 = 查(t); 共 += 1; ok += (len(红) == 1)
        os.remove(os.path.join(t, '设定', '丁.md'))
        # ⑤案卷（回执_）不查
        open(os.path.join(t, '设定', '回执_x.md'), 'w', encoding='utf-8').write('`圣经:5` `圣经§律·无此`\n')
        行, 红 = 查(t); 共 += 1; ok += (红 == [] and not any('回执_' in x[0] for x in 行))
        # ⑥无基线 → 红（不许无基线而假绿）
        共 += 1; ok += (判([], [], None)[1] != [])
    finally:
        shutil.rmtree(t, ignore_errors=True)
    print('圣经引号·自测 %d/%d %s' % (ok, 共, '全通' if ok == 共 else '⛔有坏'))
    return ok == 共


def main():
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    行, 红 = 查()
    if '--定基线' in a:
        坏 = sum(1 for x in 行 if x[4])
        old = _基线(ROOT)
        if old is not None and 坏 > old.get('空离题', 0):
            print('⛔今数 %d 高於旧基线 %d，⛔不许升基线' % (坏, old['空离题']))
            sys.exit(1)
        json.dump({'空离题': 坏, '引数': len(行)}, open(os.path.join(ROOT, '工具', '圣经引号_基线.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('基线定为 %d' % 坏)
        return
    if '--静' not in a:
        for rel, i, n, 实, 旗 in 行:
            print('%s%s:%d → 圣经:%d ｜%s' % ('【%s】' % 旗 if 旗 else '', rel, i, n, 实))
    坏, msgs = 判(行, 红, _基线(ROOT))
    for m in msgs:
        print(m)
    空 = sum(1 for x in 行 if x[4] == '空')
    print('圣经引号：行号之引 %d 处（空 %d·离题 %d）；条号之引无其条 %d 处；%s' % (
        len(行), 空, 坏 - 空, len(红), '⛔红' if msgs else '✓（旧漂只印不判，见上）'))
    sys.exit(1 if msgs else 0)


if __name__ == '__main__':
    main()
