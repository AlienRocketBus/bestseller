# -*- coding: utf-8 -*-
"""存底包 · 一条命令打出交给作者的三样存底（2026-09-24 立·作者当面令）

⛔**其所由来·0924 之实**：推闸自 345 章起挂着一条清不掉的红（`换型令`），
  **遂六天推不上去**；作者当面问「东西是不是都没了」之日，
  **本坐才想起还有一条不须任何人许可的路——把东西直接交到作者手上。**
★**其教**：⛔**「推不上去」与「作者手上没有」是两件事**——
  **前者要等人开口，後者一条命令就办得了**；**而本坐六天里没走过这一条。**
★★**故写成器**：下一坐不必临时想，**跑一句即得三样**。

用法：
    python3 工具/存底包.py            # 打包（落在临时处，其路印出来）
    python3 工具/存底包.py --自测

★**所出三样**（其序即其要紧之序）：
  ① **全本单档 .txt** ——⭐**手机点开就能读**，⛔不用解压、不用任何工具；
  ② **正文 .tar.gz** ——逐章之档；
  ③ **全仓 .bundle**（逾 30MB 者自分卷）——连历史，能 `git clone` 还原。
⛔**打完须当面把其路交给作者**（`SendUserFile`）——**打了而没送出去，等於没打。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, io, glob, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
      '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
卷之限 = 28 * 1024 * 1024          # ★送档之限係 30MB，留二兆余地


def cn(p):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(p))
    if not m:
        return -1
    t = n = 0
    for ch in m.group(1):
        if ch in CN and ch != '十':
            n = CN[ch]
        elif ch == '十':
            t += (n or 1) * 10
            n = 0
        elif ch == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


def 诸章():
    return sorted([p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if cn(p) > 0],
                  key=cn)


def 单档(到):
    """★①全本单档——⛔其所以排在头一样：**它是唯一一样不须任何工具就能读的**。"""
    fs =诸章()
    out = ['《镇冢秘术》全本 · 第1—%d章\n共 %d 篇\n' % (cn(fs[-1]), len(fs)), '=' * 60 + '\n']
    for p in fs:
        out.append('\n\n' + '=' * 60 + '\n')
        out.append(io.open(p, encoding='utf-8', errors='replace').read().rstrip() + '\n')
    t = ''.join(out)
    io.open(到, 'w', encoding='utf-8').write(t)
    return len(t), len(fs)


def 打(到处=None):
    到处 = 到处 or tempfile.mkdtemp(prefix='存底包_')
    os.makedirs(到处, exist_ok=True)
    日 = subprocess.run(['git', 'log', '-1', '--format=%cd', '--date=format:%Y%m%d'],
                        cwd=ROOT, capture_output=True, text=True).stdout.strip() or '今'
    末 = cn(诸章()[-1])
    出 = []

    p1 = os.path.join(到处, '镇冢秘术_全本单档_第1至%d章_%s.txt' % (末, 日))
    字, 篇 = 单档(p1)
    出.append(('①全本单档（⭐点开就能读）', p1, '%d 篇｜%d 字' % (篇, 字)))

    p2 = os.path.join(到处, '镇冢秘术_正文%d篇_%s.tar.gz' % (篇, 日))
    subprocess.run(['tar', 'czf', p2, '正文'], cwd=ROOT, capture_output=True)
    出.append(('②正文逐章', p2, ''))

    p3 = os.path.join(到处, '镇冢秘术_全仓存底_%s.bundle' % 日)
    subprocess.run(['git', 'bundle', 'create', p3, '--all'], cwd=ROOT, capture_output=True)
    v = subprocess.run(['git', 'bundle', 'verify', p3], cwd=ROOT,
                       capture_output=True, text=True).stdout
    出.append(('③全仓连历史', p3,
               '✓complete history' if 'complete history' in v else '⛔验不过'))

    # ★逾限者自分卷（⛔一个送不出去的档，等於没打）
    卷 = []
    if os.path.getsize(p3) > 卷之限:
        with open(p3, 'rb') as f:
            i = 1
            while True:
                b = f.read(卷之限)
                if not b:
                    break
                q = '%s.%03d' % (p3, i)
                open(q, 'wb').write(b)
                卷.append(q)
                i += 1
        出.append(('③之分卷（⛔送档之限 30MB）', '、'.join(os.path.basename(x) for x in 卷),
                   '%d 卷' % len(卷)))

    print('════ 存底包 ════')
    for 名, 路, 注 in 出:
        print('  %s\n     %s  %s' % (名, 路, 注))
    print('  ⛔**打完须当面把其路交给作者（SendUserFile）**——'
          '**打了而没送出去，等於没打。**')
    if 卷:
        print('  ★分卷之拼：`cat *.bundle.0?? > 全.bundle && git clone 全.bundle the-novel`')
    return [x[1] for x in 出[:3]] + 卷


def 自测():
    R = []
    fs = 诸章()
    R.append(('①数得着正文（今 %d 篇）' % len(fs), len(fs) > 0))
    R.append(('②章号解得出且有序（末章第%d章）' % cn(fs[-1]),
              cn(fs[0]) == 1 and cn(fs[-1]) >= len(fs)))
    d = tempfile.mkdtemp(prefix='存底包自测_')
    p = os.path.join(d, 't.txt')
    字, 篇 = 单档(p)
    R.append(('③单档打得出，且其字数逾百万（今 %d）' % 字, 字 > 1000000))
    R.append(('④单档所含之篇数＝正文之篇数（%d）' % 篇, 篇 == len(fs)))
    头 = io.open(p, encoding='utf-8').read(200)
    R.append(('⑤单档头一行写明其数（⛔一份存底须自己说清它有多少）',
              '共 %d 篇' % len(fs) in 头))
    尾 = io.open(p, encoding='utf-8').read()[-4000:]
    R.append(('⑥末章之文确在档尾（⛔不许打了一半就收）',
              io.open(fs[-1], encoding='utf-8').read().strip()[-40:] in 尾))
    R.append(('⑦⛔送档之限係写死之数（%d 兆），⛔不随今日之档大小挪' % (卷之限 // 1024 // 1024),
              卷之限 == 28 * 1024 * 1024))
    import shutil
    shutil.rmtree(d, ignore_errors=True)
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 存底包·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    打()
    sys.exit(0)
