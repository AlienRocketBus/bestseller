#!/usr/bin/env python3
"""段案验（1013 立·造式二代 §四：段案之闭环，机器验）——段案取骨之後、交各章执笔之前跑；红即回取骨席只治红处。

验（段案之格见 工具/段料.py）：
  ①本段每章一节「## N」，八项俱全（重、魂路、叫绝之拍、种、知之变、物之动、日、钩），⛔空、⛔「（填）」；
  ②重 ∈ 轻／中／重；魂路两三条，俱是造章所认之名（翻个儿／不说／速度／换账／物证／咬合／回声）；
  ③叫绝之拍须注「对标拍库第N拍」；
  ④日与总纲逐章同（总纲两栏，整行逐栏认——坑㉒）；
  ⑤种：「埋「X」→收 NNN」者 NNN 须在本章之後、≤510；「收「X」（埋於 NNN）」者 NNN 须在本章之前；
     本段内所埋而收章落本段者，其收章之节须有「收「X」」——⛔埋了不收、收了无埋。
⛔限：知之阶、生死不逆、对账词之撞，本器不判（交逻辑闭环之审一回）；本器只判机器判得死的。

用法：
  python3 工具/段案验.py 设定/段案/390-399.md 390 399
  python3 工具/段案验.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
项 = ('重', '魂路', '叫绝之拍', '种', '知之变', '物之动', '日', '钩')
魂路名 = ('翻个儿', '不说', '速度', '换账', '物证', '咬合', '回声')
末章 = 510


def 节们(文):
    出 = {}
    for m in re.finditer(r'^## (\d{3})\s*$(.*?)(?=^## |\Z)', 文, re.M | re.S):
        d = {}
        for k in 项:
            x = re.search(r'^- %s：(.*)$' % k, m.group(2), re.M)
            d[k] = x.group(1).strip() if x else ''
        出[int(m.group(1))] = d
    return 出


def 验(文, a, b, 日=None):
    坏 = []
    n们 = 节们(文)
    for n in range(a, b + 1):
        if n not in n们:
            坏.append('第%d章无节' % n); continue
        d = n们[n]
        for k in 项:
            if not d[k] or d[k].startswith('（填'):
                坏.append('第%d章缺「%s」' % (n, k))
        if d['重'] and d['重'] not in ('轻', '中', '重'):
            坏.append('第%d章之重须为 轻／中／重（今「%s」）' % (n, d['重']))
        路 = [x.strip() for x in d['魂路'].split('｜') if x.strip()]
        if d['魂路'] and not (2 <= len(路) <= 3 and all(x in 魂路名 for x in 路)):
            坏.append('第%d章之魂路须两三条且俱是造章所认之名（今「%s」）' % (n, d['魂路']))
        if d['叫绝之拍'] and not re.search(r'对标拍库第\d+拍', d['叫绝之拍']):
            坏.append('第%d章之叫绝之拍未注「对标拍库第N拍」' % n)
        if 日 is not None and d['日'] and 日.get(n) and d['日'] != 日[n]:
            坏.append('第%d章之日「%s」≠ 总纲「%s」' % (n, d['日'], 日[n]))
        for x, k in re.findall(r'埋「([^」]+)」\s*→\s*收\s*(\d{3})', d['种']):
            k = int(k)
            if not (n < k <= 末章):
                坏.append('第%d章所埋「%s」之收章 %d 须在本章之後、≤%d' % (n, x, k, 末章))
            elif a <= k <= b and k in n们 and ('收「%s」' % x) not in n们[k]['种']:
                坏.append('第%d章所埋「%s」钉收於 %d，而第%d章之种无「收「%s」」——埋了不收' % (n, x, k, k, x))
        for x, k in re.findall(r'收「([^」]+)」（埋於\s*(\d{3})）', d['种']):
            if int(k) >= n:
                坏.append('第%d章所收「%s」之埋章 %s 须在本章之前' % (n, x, k))
    return 坏


def 自测():
    ok = 共 = 0
    def 节(n, 种='无', 日='暗·142', 路='翻个儿｜物证', 重='中'):
        return '## %d\n- 重：%s\n- 魂路：%s\n- 叫绝之拍：拇指之口（对标拍库第7拍）\n- 种：%s\n- 知之变：甲知乙\n- 物之动：笔到她手\n- 日：%s\n- 钩：门开了\n' % (n, 重, 路, 种, 日)
    好 = 节(381, '埋「斜口」→收 382') + 节(382, '收「斜口」（埋於 381）', 日='主·149')
    纲日 = {381: '暗·142', 382: '主·149'}
    共 += 1; ok += (验(好, 381, 382, 纲日) == [])
    共 += 1; ok += any('埋了不收' in x for x in 验(节(381, '埋「斜口」→收 382') + 节(382, 日='主·149'), 381, 382, 纲日))
    共 += 1; ok += any('须在本章之前' in x for x in 验(节(381, '收「甲」（埋於 390）'), 381, 381, 纲日))
    共 += 1; ok += any('≠ 总纲' in x for x in 验(节(381, 日='暗·141'), 381, 381, 纲日))
    共 += 1; ok += any('魂路' in x for x in 验(节(381, 路='翻个儿｜飞天'), 381, 381, 纲日)) and any('之重' in x for x in 验(节(381, 重='极'), 381, 381, 纲日))
    共 += 1; ok += any('无节' in x for x in 验(节(381), 381, 382, 纲日))
    print('段案验·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) == 3 and a[1].isdigit() and a[2].isdigit():
        import 段料
        纲 = open(os.path.join(ROOT, '设定', '02_余章之势_总纲.md'), encoding='utf-8').read()
        坏 = 验(open(a[0], encoding='utf-8').read(), int(a[1]), int(a[2]), 段料.总纲之日(纲, int(a[1]), int(a[2])))
        print('✓ 段案验：%s 闭环之机器诸项俱过' % a[0] if not 坏 else '⛔ 段案验 %d 处：\n  ' % len(坏) + '\n  '.join(坏))
        sys.exit(0 if not 坏 else 1)
    print(__doc__); sys.exit(2)
