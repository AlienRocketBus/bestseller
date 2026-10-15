#!/usr/bin/env python3
"""剧情链（1015 立·作者令「每章写完就精读、详记，整合成一条从头到尾的链，日後大改不必再从头读」）——零 token。

为何立：每章之详记（设定/全书记忆/第N章.md：按拍、要句、新知、悬线、一句之要）由记席随章精读而写，1—388 无一缺；
  而它们散在三百多档，总览③只一章一行。要「一看就从头到尾全知道」，须一条中等粒度之链：
  照章序、分站，每章一节——题、线与日、一句之要、（有则）亮点与读之得、其详在何处（详记、回执、大审之册）。
  链由机器从详记串成，⛔模型另写；每回封版重生（封版.py --後），随提交上 GitHub。
⛔限：只串、⛔改其文；详记缺「一句之要」者照实标缺。

用法：
  python3 工具/剧情链.py           # → 设定/全书记忆/剧情链.md
  python3 工具/剧情链.py --验      # 链与详记同不同（封版後须同；不同 rc=1）
  python3 工具/剧情链.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
记 = os.path.join('设定', '全书记忆')
链档 = os.path.join(记, '剧情链.md')


def 节之文(t, 名):
    m = re.search(r'^## %s[^\n]*\n+(.*?)(?=^## |\Z)' % re.escape(名), t, re.M | re.S)
    return m.group(1).strip() if m else ''


def 站们(root=ROOT):
    """总览「② 按站」之「### E? 名（第 a—b 章…）」→ [(a, b, 题)]"""
    t = open(os.path.join(root, 记, '总览.md'), encoding='utf-8').read()
    出 = []
    for m in re.finditer(r'^### (E\d[^\n]*?)（第 (\d+)—(\d+)', t, re.M):
        出.append((int(m.group(2)), int(m.group(3)), m.group(1).strip()))
    m = re.search(r'^### (E\d[^\n]*?)（第 (\d+) 章起', t, re.M)   # 「E5 贺兰（冀鼎）（第 331 章起」：题里可带括号
    if m:
        出.append((int(m.group(2)), 10 ** 6, m.group(1).strip()))
    return sorted(出)


def 索引(root=ROOT):
    """总览③：| 章 | 题 | 线与日 | 一行 |"""
    t = open(os.path.join(root, 记, '总览.md'), encoding='utf-8').read()
    出 = {}
    for l in t.split('\n'):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) >= 3 and c[0].isdigit():
            出[int(c[0])] = (c[1], c[2])
    return 出


def 生(root=ROOT):
    档们 = {}
    for f in glob.glob(os.path.join(root, 记, '第*章.md')):
        m = re.search(r'第(\d+)章\.md$', f)
        if m:
            档们[int(m.group(1))] = f
    引 = 索引(root)
    站 = 站们(root)
    回执们 = {}
    for f in glob.glob(os.path.join(root, '设定', '回执_*_第*章*.md')):
        m = re.search(r'第(\d+)章', os.path.basename(f))
        if m:
            回执们.setdefault(int(m.group(1)), []).append(os.path.relpath(f, root))
    大审们 = sorted(glob.glob(os.path.join(root, '设定', '大审_至第*章.md')))
    出 = ['# 剧情链（全书从头到尾·一章一节）', '',
          '> 零 token 所串（工具/剧情链.py）：每章取其详记（设定/全书记忆/第N章.md）之「一句之要」，有则并「亮点」「读之得」；'
          '每回封版重生。要细读某章，照「详」所指之档取；⛔凭此链改正文之字（字以正文为准）。', '',
          '> 粒度：最粗一层＝总览③（一章一行）；本链＝一章一节；最细＝各章详记（按拍、要句、新知、悬线）。', '']
    缺 = []
    当站 = None
    for n in sorted(档们):
        for a, b, 题 in 站:
            if a <= n <= b and 题 != 当站:
                当站 = 题
                出 += ['', '## %s（第 %d 章起）' % (题, a), '']
                break
        t = open(档们[n], encoding='utf-8').read()
        要 = 节之文(t, '一句之要')
        亮 = 节之文(t, '亮点')
        得 = 节之文(t, '读之得')
        题, 线 = 引.get(n, ('', ''))
        if not 要:
            缺.append(n)
        出.append('### %d　%s　〔%s〕' % (n, 题, 线))
        出.append(要 or '（详记无「一句之要」）')
        if 亮:
            出.append('- **亮点**：' + re.sub(r'\s*\n\s*', '；', 亮))
        if 得:
            出.append('- **读之得**：' + re.sub(r'\s*\n\s*', '；', 得))
        详 = ['`%s`' % os.path.relpath(档们[n], root)] + ['`%s`' % x for x in sorted(回执们.get(n, []))[:1]]
        审 = [os.path.relpath(x, root) for x in 大审们 if _界(x)[0] <= n <= _界(x)[1]]
        if 审:
            详.append('`%s`' % 审[-1])
        出.append('- 详：' + '｜'.join(详))
        出.append('')
    return '\n'.join(出), 缺


def _界(p):
    t = open(p, encoding='utf-8').read(400)
    m = re.search(r'第(\d+)—(\d+)章', t)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r'至第(\d+)章', p)
    return (int(m.group(1)) - 9, int(m.group(1))) if m else (0, -1)


def 自测():
    ok = 共 = 0
    共 += 1; ok += 节之文('## 甲\n\n一二\n\n## 一句之要\n\n三四\n', '一句之要') == '三四'
    共 += 1; ok += 节之文('## 一句之要\n\n五\n## 亮点\n六', '亮点') == '六'
    t, 缺 = 生()
    共 += 1; ok += ('### 1　' in t and '### 388　' in t and not 缺)
    共 += 1; ok += len(站们()) >= 5
    print('剧情链·自测 %d/%d（%d 字节、缺一句之要 %d 章）' % (ok, 共, len(t.encode()), len(缺)))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    t, 缺 = 生()
    p = os.path.join(ROOT, 链档)
    if a == ['--验']:
        旧 = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        同 = 旧 == t
        print('剧情链·验：%s' % ('✓ 与详记同' if 同 else '⛔ 与详记不同——跑 python3 工具/剧情链.py 重生'))
        sys.exit(0 if 同 else 1)
    open(p, 'w', encoding='utf-8').write(t)
    print('✓ 写 %s（%d 章、%d KB；缺一句之要 %d 章%s）' % (链档, t.count('\n### '), len(t.encode()) // 1024, len(缺), ('：' + str(缺[:10])) if 缺 else ''))
