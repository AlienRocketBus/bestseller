#!/usr/bin/env python3
"""账限哨（1021 立·作者问「为什么到现在还是我自己发现之後告诉你，你才发现」）。

为何立：瑕疵总账诸条皆写了「限」（如「401 段前」「407 大审前」），而⛔一器读之——限到不到，全凭主环记得；
复盘之「B＋C 之候」写了七回、行了二回，亦无一处催。本哨零 token：读 设定/瑕疵总账.md 之未治诸行，取其限之章号，
与下一章比——到期即「欠」，自走.py 照「到期账」之欠一并印、⛔起笔；工作流账.py 会话开头亦印。
限之式：「NNN 段前／段开镜前／开镜前／大审前／前」→ 下一章 ≥ NNN 即到；「NNN 封版前／记席前」→ 下一章 > NNN 即到
（其活可於 NNN 一章之内办）；无章号之限（「W11 各该节」）不判。行中有「延：<由>」者只报⚠不拦（由须四字以上）。
用法：
  python3 工具/账限哨.py          # 印到期与将到（三章内）之条；有到期 rc=1
  python3 工具/账限哨.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
限式 = re.compile(r'(\d{3})\s*(段开镜前|段前|开镜前|大审前|封版前|记席前|前)')
延式 = re.compile(r'延[：:]\s*(?:\S\s*){4,}')


def 诸条(文):
    """返 [(号, 题, 限章, 限式, 有延)]——只取「## 未治」一节之 X 行。"""
    m = re.search(r'^## 未治[^\n]*\n(.*?)(?=^## |\Z)', 文, re.M | re.S)
    if not m:
        return []
    out = []
    for l in m.group(1).split('\n'):
        if not re.match(r'\|\s*X\d+\s*\|', l):
            continue
        格 = [c.strip() for c in l.strip().strip('|').split('|')]
        号, 题, 限 = 格[0], 格[1][:40], 格[-1]
        k = 限式.search(限)
        out.append((号, 题, int(k.group(1)) if k else None, k.group(2) if k else '', bool(延式.search(l))))
    return out


def 判(下, 文):
    """返 (到期, 将到)：到期 [(号, 题, 章, 式, 延)]；将到为三章内者。"""
    到, 将 = [], []
    for x in 诸条(文):
        号, 题, 章, 式, 延 = x
        if 章 is None:
            continue
        到期 = (下 > 章) if 式 in ('封版前', '记席前') else (下 >= 章)
        if 到期:
            到.append(x)
        elif 章 - 下 <= 3:
            将.append(x)
    return 到, 将


def 末章(root=ROOT):
    try:
        import 自走
        return 自走.末章()
    except Exception:
        return 0


def 印(root=ROOT, 下=None):
    try:
        文 = open(os.path.join(root, '设定', '瑕疵总账.md'), encoding='utf-8').read()
    except Exception as e:
        return False, ['账限哨：瑕疵总账读不得（%s）' % e]
    下 = 下 or 末章(root) + 1
    到, 将 = 判(下, 文)
    拦 = [x for x in 到 if not x[4]]
    L = ['%s 账限哨：下一章 %d——瑕疵总账到期 %d 条（延 %d）、三章内将到 %d 条' % ('⛔' if 拦 else '✓', 下, len(到), len(到) - len(拦), len(将))]
    for 号, 题, 章, 式, 延 in 到:
        L.append('   %s %s 限 %d %s：%s' % ('⚠延' if 延 else '⛔', 号, 章, 式, 题))
    for 号, 题, 章, 式, 延 in 将:
        L.append('   · %s 限 %d %s：%s' % (号, 章, 式, 题))
    return bool(拦), L


def 自测():
    r = []
    def T(名, 条):
        r.append((名, bool(条)))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)
    文 = '''# 账
## 未治
| 号 | 题 | 源 | 治 | 限 |
|---|---|---|---|---|
| X1 | 甲病 | s | t | 401 段开镜前（某裁） |
| X2 | 乙病 | s | t | 401 封版前 |
| X3 | 丙病 | s | t | W11 各该节 |
| X4 | 丁病 | s | t | 403 段前 |
| X5 | 戊病 | s | t | 401 段前（延：W59 落後即治，候其干跑） |
| X6 | 己病 | s | t | 420 前 |
## 已治
| Y1 | 旧 | s | t | 300 前 |
'''
    到, 将 = 判(401, 文)
    号到 = [x[0] for x in 到]
    T('①「401 段开镜前」下一章 401 即到', 'X1' in 号到)
    T('②「401 封版前」下一章 401 未到（可於 401 之内办）', 'X2' not in 号到)
    T('③「401 封版前」下一章 402 即到', 'X2' in [x[0] for x in 判(402, 文)[0]])
    T('④无章号之限不判', 'X3' not in 号到 and 'X3' not in [x[0] for x in 将])
    T('⑤三章内将到', 'X4' in [x[0] for x in 将])
    T('⑥有「延：」者到而只报', [x for x in 到 if x[0] == 'X5'][0][4] is True)
    T('⑦已治之节不读', 'Y1' not in 号到)
    T('⑧远者不报', 'X6' not in 号到 and 'X6' not in [x[0] for x in 将])
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, '设定'))
        open(os.path.join(d, '设定', '瑕疵总账.md'), 'w', encoding='utf-8').write(文)
        拦, L = 印(d, 401)
        T('⑨印：有未延之到期即拦', 拦 and L[0].startswith('⛔'))
    ok = sum(v for _, v in r)
    print('账限哨·自测 %d/%d%s' % (ok, len(r), ' 全通' if ok == len(r) else ' 未过'))
    return ok == len(r)


if __name__ == '__main__':
    if '--自测' in sys.argv[1:]:
        sys.exit(0 if 自测() else 1)
    拦, L = 印()
    print('\n'.join(L))
    sys.exit(1 if 拦 else 0)
