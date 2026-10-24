#!/usr/bin/env python3
"""稿差（1024 立·省 token 之审 seats②／failures②，二审俱许·零 token）——回写之後逻辑审·2 之窄审之门。

为何立：409、410 逻辑审·2 照第1回全审一遍（再读 N−5 至 N−3 章、六类重做），而回写只改一二行以销读误；
  第2回之 114K—161K 缓存建，大半是重读未动之行。今由机器量回写所动：只犯读误、改动小者窄审（只审所动、验读误之销），余照旧全审。
用法：
  python3 工具/稿差.py N --据   → 印「据 正文＝vNN」（正文与哪一版逐字同）；逻辑审·1 照抄其末行入轮记「## 造式·逻辑审·合後·第1回」之首行
  python3 工具/稿差.py N        → 底＝第1回轮记首行所据之版；比回写後之正文（只比白文：【本章亮点】以前），
                                 印 JSON {底,行变,字变,改行}、改行（各带上下两行），并汇料之所须入 .cache/稿差/第N章.md；
                                 末行「判：窄｜…」或「判：全｜由」
  python3 工具/稿差.py --自测
判全之由（任一即全）：轮记无第1回之节或其节无「据 正文＝vNN」｜底版之档不在｜正文与末版不一（回写未存版）｜白文无差｜行变逾 3｜字变逾 150。
⛔本器只读正文、版本/第N章/ 之 vNN 与 _轮记.md、_料.md；只写 .cache/稿差/（⛔写 版本/：免入封版之提交、惹囤灰闸与档肿哨）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, glob, difflib, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
行限, 字限 = 3, 150
据之式 = re.compile(r'据\s*正文\s*[＝=]\s*(v\d+)')
第一回之头 = '## 造式·逻辑审·合後·第1回'
# 窄席所须之料（seats② safeguard 三）：_料.md 之节头含此诸字者全录；开镜卡之下只取问三、问八、问九（含之二）
料之节 = ('〔段案·本章之行', '〔余章总案·下一章之行', '〔全员之账')
卡之问 = ('问三', '问八', '问九')


def 读(p):
    try:
        return open(p, encoding='utf-8').read()
    except OSError:
        return None


def 白文(文):
    return [l.rstrip() for l in 文.split('【本章亮点】')[0].split('\n')]


def 诸版(目):
    return sorted(glob.glob(os.path.join(目, 'v[0-9]*.md')), key=lambda p: int(re.sub(r'\D', '', os.path.basename(p)) or 0))


def 正文档(n, root):
    try:
        import 章料
        return 章料.章档(n, root=root)
    except Exception:
        return None


def 据(n, root=ROOT):
    """→ 与正文逐字同之版名（新者先），无则 None。"""
    f = 正文档(n, root)
    文 = 读(f) if f else None
    if 文 is None:
        return None
    for p in reversed(诸版(os.path.join(root, '版本', '第%d章' % n))):
        if 读(p) == 文:
            return os.path.basename(p)[:-3]
    return None


def 第一回之据(轮记):
    if not 轮记 or 第一回之头 not in 轮记:
        return None
    节 = 轮记.split(第一回之头, 1)[1]
    节 = re.split(r'^## ', 节, maxsplit=1, flags=re.M)[0]
    m = 据之式.search(节)
    return m.group(1) if m else None


def 量(旧, 新):
    """→ (行变, 字变, 诸块)：行变＝诸块 max(删行, 增行) 之和；字变＝诸块逐字之删＋增。"""
    sm = difflib.SequenceMatcher(None, 旧, 新, autojunk=False)
    行变 = 字变 = 0
    块 = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        行变 += max(i2 - i1, j2 - j1)
        a, b = ''.join(旧[i1:i2]), ''.join(新[j1:j2])
        c = difflib.SequenceMatcher(None, a, b, autojunk=False)
        字变 += sum((x2 - x1) + (y2 - y1) for o, x1, x2, y1, y2 in c.get_opcodes() if o != 'equal')
        块.append((i1, i2, j1, j2))
    return 行变, 字变, 块


def 料摘(料):
    if not 料:
        return '（_料.md 不在——料外 grep 核）'
    节们 = re.split(r'(?=^## )', 料, flags=re.M)
    出 = []
    for s in 节们:
        头 = s.split('\n', 1)[0]
        if any(k in 头 for k in 料之节) or (头.startswith('## ') and any(k in 头 for k in 卡之问) and '〔' not in 头):
            出.append(s.rstrip())
    return '\n\n'.join(出) or '（料中无所须之节）'


def 判(n, root=ROOT, 写=True):
    """→ (窄否, 由, 果dict)。"""
    目 = os.path.join(root, '版本', '第%d章' % n)
    果 = {'章': n}
    底 = 第一回之据(读(os.path.join(目, '_轮记.md')))
    if not 底:
        return False, '轮记无「%s」之节或其节无「据 正文＝vNN」' % 第一回之头, 果
    果['底'] = 底
    底文 = 读(os.path.join(目, 底 + '.md'))
    if 底文 is None:
        return False, '底版 %s 不在' % 底, 果
    f = 正文档(n, root)
    今 = 读(f) if f else None
    if 今 is None:
        return False, '正文不在', 果
    版 = 诸版(目)
    if not 版 or 读(版[-1]) != 今:
        return False, '正文与末版（%s）不一——回写未存版' % (os.path.basename(版[-1])[:-3] if 版 else '无'), 果
    果['今'] = os.path.basename(版[-1])[:-3]
    旧, 新 = 白文(底文), 白文(今)
    行变, 字变, 块 = 量(旧, 新)
    果.update(行变=行变, 字变=字变, 改行=[('%d—%d' % (j1 + 1, j2) if j2 > j1 + 1 else str(j1 + 1)) if j2 > j1 else '删於%d' % (j1 + 1) for _, _, j1, j2 in 块])
    if not 块:
        return False, '白文无差（底 %s 与正文同）' % 底, 果
    if 写:
        L = ['# 第%d章·稿差（工具/稿差.py 零 token 出；底 %s → 今 %s；行变 %d、字变 %d）' % (n, 底, 果['今'], 行变, 字变), '',
             '## 改行（新行号＝正文之行；各带上下两行；「-」底版之行、「+」今之行）']
        for i1, i2, j1, j2 in 块:
            L.append('')
            L.append('### 正文 %s' % ('%d—%d' % (j1 + 1, j2) if j2 > j1 else '删於 %d' % (j1 + 1)))
            for k in range(max(0, j1 - 2), j1):
                L.append('  %d: %s' % (k + 1, 新[k]))
            L += ['- %s' % x for x in 旧[i1:i2]]
            L += ['+ %d: %s' % (j1 + 1 + k, x) for k, x in enumerate(新[j1:j2])]
            for k in range(j2, min(len(新), j2 + 2)):
                L.append('  %d: %s' % (k + 1, 新[k]))
        L += ['', '## 料之所须（_料.md 摘：开镜卡问三问八问九、段案本章之行、余章总案下一章之行、全员之账）', '', 料摘(读(os.path.join(目, '_料.md')))]
        出 = os.path.join(root, '.cache', '稿差', '第%d章.md' % n)
        os.makedirs(os.path.dirname(出), exist_ok=True)
        open(出, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
        果['档'] = os.path.relpath(出, root)
    if 行变 > 行限 or 字变 > 字限:
        return False, '改动逾窄审之限（行变 %d／%d、字变 %d／%d）' % (行变, 行限, 字变, 字限), 果
    return True, '行变 %d、字变 %d；底 %s' % (行变, 字变, 底), 果


def 自测():
    import tempfile
    R = []
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, '正文')); 目 = os.path.join(t, '版本', '第9章'); os.makedirs(目)
        正 = os.path.join(t, '正文', '镇冢秘术_第九章_试.md')
        头 = '《镇冢秘术》\n\n第九章　试\n\n'
        原 = 头 + '\n'.join('第%d行她走过去。' % i for i in range(1, 21)) + '\n【本章亮点】骨\n'
        写 = lambda p, s: open(p, 'w', encoding='utf-8').write(s)
        写(os.path.join(目, 'v01.md'), 原); 写(正, 原)
        写(os.path.join(目, '_料.md'), '# 料\n## 〔开镜卡〕\n## ★★★问三·本章之一事\n一事\n## ★问五·本章之品\n品\n## 〔全员之账（生死）〕\n苏衍存\n## 〔前文·第8章白文〕\n长\n')
        R.append(('①--据：正文与 v01 同 → v01', 据(9, t) == 'v01'))
        R.append(('②轮记无第1回之节 → 全', not 判(9, t)[0] and '轮记无' in 判(9, t)[1]))
        写(os.path.join(目, '_轮记.md'), '# 轮记\n%s\n\n据 正文＝v01\n\n六类……\n## 防崩·合後回写\n' % 第一回之头)
        R.append(('③白文无差 → 全', not 判(9, t)[0] and '无差' in 判(9, t)[1]))
        小 = 原.replace('第5行她走过去。', '第5行她停了一下才走过去。')
        写(os.path.join(目, 'v02.md'), 小); 写(正, 小)
        ok, 由, 果 = 判(9, t)
        档 = 读(os.path.join(t, '.cache', '稿差', '第9章.md')) or ''
        R.append(('④一行小改 → 窄；行变 1、改行在正文第 9 行', ok and 果['行变'] == 1 and 果['改行'] == ['9'] and 0 < 果['字变'] <= 字限))
        R.append(('⑤差档在 .cache/稿差/（⛔版本/）、带上下文与料之摘（问三、全员之账；⛔前文、⛔问五）',
                  '+ 9: 第5行她停了一下' in 档 and '  8: 第4行' in 档 and '问三' in 档 and '苏衍存' in 档 and '前文' not in 档 and '问五' not in 档
                  and not os.path.exists(os.path.join(目, '_回写之差.md'))))
        写(正, 小.replace('第6行', '第6行改'))
        R.append(('⑥正文与末版不一（回写未存版）→ 全', not 判(9, t)[0] and '不一' in 判(9, t)[1]))
        大 = 原.replace('第5行她走过去。', '她' * 200 + '。')
        写(os.path.join(目, 'v03.md'), 大); 写(正, 大)
        R.append(('⑦字变逾 150 → 全', not 判(9, t)[0] and '逾窄审之限' in 判(9, t)[1]))
        多 = 原
        for i in (3, 7, 11, 15):
            多 = 多.replace('第%d行她走过去。' % i, '第%d行他走过去。' % i)
        写(os.path.join(目, 'v04.md'), 多); 写(正, 多)
        R.append(('⑧行变逾 3（四行各改一字）→ 全', not 判(9, t)[0] and 判(9, t)[2]['行变'] == 4))
        亮 = 小.replace('【本章亮点】骨', '【本章亮点】骨又添一注')
        写(os.path.join(目, 'v05.md'), 亮); 写(正, 亮)
        R.append(('⑨只比白文：亮点之改⛔计', 判(9, t)[2]['行变'] == 1))
        写(os.path.join(目, '_轮记.md'), '# 轮记\n%s\n\n据 正文＝v77\n' % 第一回之头)
        R.append(('⑩底版不在 → 全', not 判(9, t)[0] and '不在' in 判(9, t)[1]))
        写(os.path.join(目, '_轮记.md'), '# 轮记\n%s\n\n六类\n## 造式·逻辑审·合後·第2回\n据 正文＝v01\n' % 第一回之头)
        R.append(('⑪「据」须在第1回之节内（第2回之据⛔认）→ 全', not 判(9, t)[0] and '轮记无' in 判(9, t)[1]))
    for k, ok in R:
        print('  %s %s' % ('✓' if ok else '⛔', k))
    过 = sum(1 for _, o in R if o)
    print('── 稿差·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


def main():
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if not a or not a[0].isdigit():
        print(__doc__)
        sys.exit(2)
    n = int(a[0])
    if '--据' in a:
        v = 据(n)
        print('据 正文＝%s' % v if v else '据 正文＝未存（正文与诸版俱不一——先 python3 工具/跑轮.py --存 %d 存一版）' % n)
        sys.exit(0 if v else 1)
    窄, 由, 果 = 判(n)
    print(json.dumps(果, ensure_ascii=False))
    if 果.get('档'):
        print('差档：%s（改行各带上下两行、料之所须）' % 果['档'])
    print('判：%s｜%s' % ('窄' if 窄 else '全', 由))


if __name__ == '__main__':
    main()
