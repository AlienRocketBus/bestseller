# -*- coding: utf-8 -*-
"""自动.py —— 一条命令，把机械那一路走到底。

其序：一坐（查）→ 自修 --修（能修的自己修）→ 若十三轮已满则 收 --跑（封版）
     → 末了印出「下一件须人办的事」。

用法：
    python3 工具/自动.py
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def R(*a):
    try:
        p = subprocess.run(list(a), cwd=ROOT, capture_output=True,
                           text=True, timeout=900)
        return p.stdout
    except Exception as e:
        return 'ERR:%s' % e


def main():
    print('=' * 56)
    print('  自动 · 一条命令走完机械那一路')
    print('=' * 56)

    # 一·查
    o1 = R('python3', '工具/一坐.py')
    print(o1)

    m = re.search(r'该修者 (\d+) 处', o1)
    need_fix = int(m.group(1)) if m else 0
    full13 = ('十三轮已满' in o1)
    m2 = re.search(r'下一轮：第(\d+)轮', o1)
    nxt = int(m2.group(1)) if m2 else 0
    m3 = re.search(r'一坐 · 第(\d+)章', o1)
    n = int(m3.group(1)) if m3 else 0

    # 二·能修的自己修
    if need_fix:
        print('-' * 56)
        print('  自修（器自己动手）')
        print('-' * 56)
        print(R('python3', '工具/自修.py', '--修'))

    # 三·十三轮满则封版
    if full13:
        print('-' * 56)
        print('  收（封版之序）')
        print('-' * 56)
        print(R('python3', '工具/收.py', '--跑'))

    # 四·印下一件须人办的事
    print('=' * 56)
    print('  下一件（器办不了，须人办）')
    print('=' * 56)
    o2 = R('python3', '工具/一坐.py')
    if '尚未起草' in o2:
        print('  ▶ 起草第%d章。开镜卡：版本/第%d章/_开镜卡.md' % (n, n))
    elif '十三轮已满' in o2:
        print('  ▶ 封版之序已跑，看上面「收」停在哪一步。')
    elif nxt:
        print('  ▶ 跑第%d轮。先领轮：' % nxt)
        print('     python3 工具/跑轮.py --下一轮 %d' % n)
        print('     跑毕：python3 工具/跑轮.py --存版 %d "第%d轮·说明"' % (n, nxt))
    for l in o2.split('\n'):
        if '冷轮未执' in l or 'COLD' in l and '未执' in l:
            print('  ▶ ' + l.strip()[:96])
    print('')
    print('  ★做完任一件，再跑一次 python3 工具/自动.py')


if __name__ == '__main__':
    main()
