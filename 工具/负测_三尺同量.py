# -*- coding: utf-8 -*-
"""负测 · 三尺同量（2026-09-24 立·守 `设定/裁_0924_365差四字.md` 之教）

⛔**其病（0924·365 回修之实）**：同一章之净重，三器报三个数——
　`跑轮.score` 报 **2349**，`小说检察官._weight_stats` 与 `净重对表.净重` 报 **2296**；
　差 53 字，全是换场符「＊」。**分量闸取的正是跑轮那一把，於是 365 在 2300 之下而闸假绿。**
★**其教**：**一个数若由三把尺量，三把尺须是一把**——⛔差一个字也是两本账，
　**而那一个字恰恰落在界上（2296／2300）时，判就翻了。**
★★裁档所立之「三器同尺（换场符「＊」不计字）」只写在纸上；本测把它变成闸。

局（⛔每一局皆验其反面）：
　①沙盘：一章含「＊」之稿，三尺所得同，且等於「去＊去空白」之实字数
　②旧式回灌：把「＊」算成字之旧尺（0924 前之跑轮）量同一稿 → ⛔须与三尺不同（证本测有牙）
　③沙盘：只含正文不含亮点段之截取三尺同认（【本章亮点】以後不计）
　④真盘：`正文/` 每一章，三尺逐章同数——⛔一章不同即红，并印其章与三数
"""
import io, os, re, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _三尺():
    import 跑轮 as _pl
    import 净重对表 as _dz
    import 小说检察官 as _jc

    def a(t):
        return _pl.score(t)[1]['净重']

    def b(t):
        return _jc._weight_stats(t)[0]

    def c(t):
        # 净重对表.净重 取路径；照其式量文本（⛔不另抄其式：写临时档交它量）
        import tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False,
                                         encoding='utf-8') as f:
            f.write(t)
            p = f.name
        try:
            return _dz.净重(p)
        finally:
            os.unlink(p)
    return a, b, c


def _旧尺(t):
    """0924 前跑轮之式：「＊」算字（⛔回灌用，不许回到任何一器里）。"""
    body = re.sub(r'^.*?第.+?章[^\n]*\n', '', t.split('【本章亮点】')[0], count=1, flags=re.S)
    return sum(len(re.sub(r'\s', '', x)) for x in body.split('\n'))


稿 = ('# 《镇冢秘术》\n\n第九百九十九章　沙盘\n\n'
      '他把尺条搁下。\n\n＊\n\n老头蹲着，没有回头。\n\n＊\n\n零。\n\n'
      '【本章亮点】\n这一段不计。\n')
实 = len('他把尺条搁下。') + len('老头蹲着，没有回头。') + len('零。')


def 跑():
    局 = []
    try:
        a, b, c = _三尺()
    except Exception as e:
        print('⛔三尺取不回来：%s' % e)
        return 1
    数 = (a(稿), b(稿), c(稿))
    局.append(('①沙盘·三尺同数且等於实字 %d（得 %s）' % (实, '／'.join(map(str, 数))),
              数[0] == 数[1] == 数[2] == 实))
    局.append(('②旧式回灌·「＊」算字之尺得 %d ≠ %d（⛔证本测有牙）' % (_旧尺(稿), 实),
              _旧尺(稿) != 实))
    局.append(('③沙盘·亮点段不计（三尺皆不含「这一段不计」之字）',
              all(x < 实 + len('这一段不计。') for x in 数)))
    不同 = []
    共 = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md'))):
        try:
            t = io.open(f, encoding='utf-8').read()
        except OSError:
            continue
        if '【本章亮点】' not in t:
            continue
        共 += 1
        x = (a(t), b(t), c(t))
        if not (x[0] == x[1] == x[2]):
            不同.append('%s %s' % (os.path.basename(f)[:24], '／'.join(map(str, x))))
    局.append(('④真盘·%d 章三尺逐章同数%s' % (共, ('；⛔不同：' + '｜'.join(不同[:5])) if 不同 else ''),
              共 > 0 and not 不同))

    红 = 0
    print('════ 负测 · 三尺同量（%d 局）════' % len(局))
    for 名, 果 in 局:
        print('  %s %s' % ('✓' if 果 else '⛔', 名))
        if not 果:
            红 += 1
    print('  ── %d/%d ──' % (len(局) - 红, len(局)))
    return 红


if __name__ == '__main__':
    sys.exit(1 if 跑() else 0)
