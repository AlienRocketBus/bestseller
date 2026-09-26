#!/usr/bin/env python3
"""大师之关（0926·作者令立）：三执笔之构思、行家之审、创作记录、自我进化——**封了版的章，缺一样即红**。

⛔其立之由：作者令「必须得执行起来，别弄出来不执行」。席令里写了不等於席照做了；
  故凡自 `自章` 起封版之章，逐章亲查盘上之档，缺一样即红，推闸据此拦停。

查五样（第 N 章）：
  ①构思：版本/第N章/起草_甲／乙／丙_构思.md 三份俱在，各 ≥400 字，且各有「进化账所避」一行；
  ②行家评：版本/第N章/_行家评.md 在，含「小说家」「总编辑」二节与「## 合稿逐条回话」；
  ③创作记录：版本/第N章/_创作记录.md 在，一至六节俱全（「一、」…「六、」）；
  ④进化：设定/大师进化账.md 里有「[第N章]」之条；
  ⑤封版：以 版本/第N章/_十一轮.json 在为「已封」之据——未封之章不查（正在写的不拦）。

用法：python3 工具/大师之关.py          # 全书（自 自章 起）
      python3 工具/大师之关.py 377      # 只查一章
      python3 工具/大师之关.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, re, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
自章 = 377   # 大师之制自 377 起生效；376 及以前用旧制，不追究


def 查(n, root=ROOT):
    d = os.path.join(root, '版本', '第%d章' % n)
    缺 = []
    for 名 in '甲乙丙':
        f = os.path.join(d, '起草_%s_构思.md' % 名)
        if not os.path.exists(f):
            缺.append('构思·%s 不在' % 名); continue
        t = open(f, encoding='utf-8', errors='replace').read()
        if len(re.sub(r'\s', '', t)) < 400:
            缺.append('构思·%s 不足 400 字' % 名)
        if '进化账所避' not in t:
            缺.append('构思·%s 无「进化账所避」' % 名)
    f = os.path.join(d, '_行家评.md')
    if not os.path.exists(f):
        缺.append('_行家评.md 不在')
    else:
        t = open(f, encoding='utf-8', errors='replace').read()
        for k in ('小说家', '总编辑', '## 合稿逐条回话'):
            if k not in t:
                缺.append('_行家评.md 无「%s」' % k)
    f = os.path.join(d, '_创作记录.md')
    if not os.path.exists(f):
        缺.append('_创作记录.md 不在')
    else:
        t = open(f, encoding='utf-8', errors='replace').read()
        for k in '一二三四五六':
            if k + '、' not in t:
                缺.append('_创作记录.md 缺第%s节' % k)
    f = os.path.join(root, '设定', '大师进化账.md')
    t = open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''
    if '[第%d章]' % n not in t:
        缺.append('进化账无「[第%d章]」之条' % n)
    return 缺


def 已封诸章(root=ROOT):
    out = []
    vd = os.path.join(root, '版本')
    if not os.path.isdir(vd):
        return out
    for x in os.listdir(vd):
        m = re.match(r'第(\d+)章$', x)
        if m and int(m.group(1)) >= 自章 and os.path.exists(os.path.join(vd, x, '_十一轮.json')):
            out.append(int(m.group(1)))
    return sorted(out)


def 全(root=ROOT):
    红 = {}
    for n in 已封诸章(root):
        缺 = 查(n, root)
        if 缺:
            红[n] = 缺
    return 红


def 自测():
    ok = 0; 共 = 0
    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, '设定'))
        d = os.path.join(tmp, '版本', '第400章'); os.makedirs(d)
        open(os.path.join(tmp, '设定', '大师进化账.md'), 'w').write('# 账\n')
        # ①未封者不查
        共 += 1; ok += (全(tmp) == {})
        # ②已封而一样也没有 → 红
        open(os.path.join(d, '_十一轮.json'), 'w').write('{}')
        共 += 1; r = 全(tmp); ok += (400 in r and len(r[400]) >= 5)
        # ③五样俱全 → 绿
        for 名 in '甲乙丙':
            open(os.path.join(d, '起草_%s_构思.md' % 名), 'w').write('进化账所避：某条\n' + '构' * 420)
        open(os.path.join(d, '_行家评.md'), 'w').write('【小说家】…\n【总编辑】…\n## 合稿逐条回话\n1. 改\n')
        open(os.path.join(d, '_创作记录.md'), 'w').write(''.join(k + '、x\n' for k in '一二三四五六'))
        open(os.path.join(tmp, '设定', '大师进化账.md'), 'a').write('- [第400章] 教训｜出处｜往后\n')
        共 += 1; ok += (全(tmp) == {})
        # ④构思缺「进化账所避」 → 红（不许只凑字数）
        open(os.path.join(d, '起草_乙_构思.md'), 'w').write('构' * 500)
        共 += 1; r = 全(tmp); ok += (400 in r and any('进化账所避' in x for x in r[400]))
        # ⑤行家评无合稿回话 → 红（行家之改法须逐条办）
        open(os.path.join(d, '起草_乙_构思.md'), 'w').write('进化账所避：某条\n' + '构' * 420)
        open(os.path.join(d, '_行家评.md'), 'w').write('【小说家】…\n【总编辑】…\n')
        共 += 1; r = 全(tmp); ok += (400 in r and any('合稿逐条回话' in x for x in r[400]))
        # ⑥自章之前者不查
        d2 = os.path.join(tmp, '版本', '第376章'); os.makedirs(d2)
        open(os.path.join(d2, '_十一轮.json'), 'w').write('{}')
        共 += 1; ok += (376 not in 全(tmp))
    finally:
        shutil.rmtree(tmp)
    print('大师之关·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--自测':
        sys.exit(0 if 自测() else 1)
    if a:
        缺 = 查(int(a[0]))
        print(('⛔ 大师之关·第%s章：' % a[0] + '｜'.join(缺)) if 缺 else '✓ 大师之关·第%s章：五样俱全' % a[0])
        sys.exit(1 if 缺 else 0)
    红 = 全()
    if 红:
        for n, 缺 in 红.items():
            print('⛔ 大师之关·第%d章：%s' % (n, '｜'.join(缺)))
        sys.exit(1)
    print('✓ 大师之关：自第%d章起已封诸章（%d 章），构思／行家评／创作记录／进化俱全' % (自章, len(已封诸章())))
