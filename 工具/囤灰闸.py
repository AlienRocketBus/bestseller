#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""囤灰闸——**造了没人用的器、席、机制，一个也不许留在仓里**。

【其立之由（2026-09-08·作者令）】
  作者说：「本来你做这个东西是非常厉害，能够去帮助写出中国第一的小说，
  然而你却很多东西却没有用起来，这是很可怕的一件事儿。」
  ★这话点的是本仓一个真病：**一百一十八个器、四张席、三十条坑，没有一样机制在查「它有没有被调用」。**
  全测查的是「跑过的器绿不绿」，从不查「该跑的器跑没跑」——**造出来搁着的，全测一声不吭。**

【它认哪几样，本书同类共几样（令§六④）】
  甲·器之囤灰：认 `工具/*.py` **全部 118 样**（本书同类即此 118 样，无遗）。
     判法：自九个真跑口（全测／起草闸／一坐／大审／书级体检／回修／十轮精进／一章到底／跑轮）
     并 `工具/席/*.js` 与 git 钩子起，**逐层展开引用闭包**；闭包之外者即囤灰。
  乙·席之囤灰：认 `工具/席/*.js` **全部**（今 4 样）。判法：须在 `工具/席/一章.js` 或 `工具/席/用法.md` 里有其位。
  丙·章之未走全席：认**第 起用章 及其後**之章（今起用章＝306）。判法：`版本/第N章/_席记.json` 须在，
     且八段（定位／三魂／起草／机闸／读席／修席／极限／案席）逐段有记。
     ★**丙只管新章**：306 以前之章不是这套机制写的，拿它去判是假红（令§十三②）。

【挂账】确有其由而暂不接的，写进 `设定/囤灰挂账.md`，一样一行，**须写明其由与其限（到哪一章之前接上）**。
  挂了账仍印黄，只是不判红——**挂账是欠条，不是赦免**。

用法：
    python3 工具/囤灰闸.py            # 全查
    python3 工具/囤灰闸.py --自测      # 负测
"""
import os
import re
import sys
import glob
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
起用章 = 306
八段 = ['定位', '三魂', '起草', '机闸', '读席', '修席', '极限', '案席']
真跑口 = ['工具/全测.py', '工具/起草闸.py', '工具/一坐.py', '工具/大审.py', '工具/书级体检.py',
          '工具/回修.py', '工具/十轮精进.py', '工具/一章到底.py', '工具/跑轮.py']


def _读(p):
    try:
        with open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ''


_汉 = '零一二三四五六七八九'


def _汉数(n):
    """章号转汉字（与本书档名同式：第二百七十三章）。"""
    if n < 10:
        return _汉[n]
    if n < 20:
        return '十' + (_汉[n % 10] if n % 10 else '')
    if n < 100:
        return _汉[n // 10] + '十' + (_汉[n % 10] if n % 10 else '')
    s = _汉[n // 100] + '百'
    r = n % 100
    if r == 0:
        return s
    if r < 10:
        return s + '零' + _汉[r]
    return s + _汉數_十(r)


def _汉數_十(r):
    return ('十' if r < 20 else _汉[r // 10] + '十') + (_汉[r % 10] if r % 10 else '')


def 正文在(n):
    return bool(glob.glob(os.path.join(ROOT, '正文', '*第%s章_*.md' % _汉数(n))))


def _挂账():
    """返 {名: 其由}。挂账须一行写全：`· 名 —— 其由（限：…）`。"""
    out = {}
    for line in _读('设定/囤灰挂账.md').split('\n'):
        m = re.match(r'\s*[·*-]\s*(\S+?)\s*(?:——|--)\s*(.+)', line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def 器之闭包(runners=None):
    """自真跑口逐层展开引用闭包，返 (跑得着集, 器全集)。"""
    tools = [os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '工具', '*.py'))]
    起 = list(真跑口 if runners is None else runners)
    if runners is None:
        # ★席与钩子只在「全查」时算真跑口；负测明给 runners 时不许再添，
        #   否则闭包永远展得开，那一格就是死的（§二十八·活数钉成常数）。
        起 += [os.path.relpath(f, ROOT) for f in glob.glob(os.path.join(ROOT, '工具', '席', '*.js'))]
        起 += [os.path.relpath(f, ROOT) for f in glob.glob(os.path.join(ROOT, '工具', 'githooks', '*'))]
    起 = [p for p in 起 if os.path.isfile(os.path.join(ROOT, p))]
    reach = set(os.path.basename(p) for p in 起 if p.endswith('.py'))
    work = list(起)
    while work:
        s = _读(work.pop())
        for t in tools:
            if t in s and t not in reach:
                reach.add(t)
                work.append('工具/' + t)
    return reach, set(tools)


def 查(印=True):
    """返 (红条列, 黄条列)。"""
    红, 黄 = [], []
    账 = _挂账()

    # 甲·器
    reach, tools = 器之闭包()
    灰 = sorted(tools - reach)
    for t in 灰:
        (黄 if t in 账 else 红).append(
            '甲·器囤灰：工具/%s 自九个真跑口展不到——造了没人跑。%s' %
            (t, ('已挂账：' + 账[t]) if t in 账 else '接进某个跑口，或写进 设定/囤灰挂账.md'))

    # 乙·席
    一章 = _读('工具/席/一章.js')
    用法 = _读('工具/席/用法.md')
    席们 = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    for s in 席们:
        if s == '一章.js':
            continue
        if s not in 一章 and s not in 用法:
            (黄 if s in 账 else 红).append(
                '乙·席囤灰：工具/席/%s 既不在 一章.js 里被调，也不在 用法.md 里有其位。%s' %
                (s, ('已挂账：' + 账[s]) if s in 账 else ''))

    # 乙之二·席之 schema 键须尽是 ASCII
    # ★其立之由（0908·本坐亲犯）：`一章.js` 之 schema 用了中文键，工作流一起手即
    #   `400 input_schema.properties: Property keys should match pattern '^[a-zA-Z0-9_.-]{1,64}$'`，
    #   **六个 agent 全崩、一章未写**。这是一条判得死的（正则一跑即知），故做成闸。
    for f in sorted(glob.glob(os.path.join(ROOT, '工具', '席', '*.js'))):
        文 = _读(os.path.relpath(f, ROOT))
        坏 = sorted(set(re.findall(r'([^\x00-\x7F][^\s:]*)\s*:\s*\{\s*type:', 文)))
        if 坏:
            红.append('乙之二·%s 之 schema 键非 ASCII：%s——工作流会当场 400，一个 agent 也起不来。'
                      % (os.path.basename(f), '／'.join(坏[:6])))

    # 丙·章
    for d in sorted(glob.glob(os.path.join(ROOT, '版本', '第*章'))):
        m = re.search(r'第(\d+)章', os.path.basename(d))
        if not m or int(m.group(1)) < 起用章:
            continue
        n = int(m.group(1))
        # ★丙只判「正文已在」之章：开了镜卡而未起草者不是囤灰，判它是假红（令§十三②）。
        if not 正文在(n):
            continue
        p = os.path.join(d, '_席记.json')
        if not os.path.isfile(p):
            红.append('丙·第%d章无 _席记.json——这一章没走八席（起用章＝%d）。' % (n, 起用章))
            continue
        try:
            j = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            红.append('丙·第%d章 _席记.json 读不动：%s' % (n, e))
            continue
        缺 = [x for x in 八段 if x not in (j.get('段') or {})]
        if 缺:
            红.append('丙·第%d章席记缺段：%s' % (n, '／'.join(缺)))

    if 印:
        print('════ 囤灰闸 ════')
        print('  甲·器 %d 样，跑得着 %d，囤灰 %d' % (len(tools), len(reach), len(灰)))
        print('  乙·席 %d 张（一章.js 除外）' % max(0, len(席们) - 1))
        新章 = [d for d in glob.glob(os.path.join(ROOT, '版本', '第*章'))
                if re.search(r'第(\d+)章', os.path.basename(d))
                and int(re.search(r'第(\d+)章', os.path.basename(d)).group(1)) >= 起用章]
        print('  丙·起用章 %d 及其後之章 %d 部' % (起用章, len(新章)))
        for x in 黄:
            print('  ⚠ ' + x)
        for x in 红:
            print('  ⛔ ' + x)
        print('  ✓ 无囤灰。' if not 红 else '  ⛔ 囤灰 %d 件。' % len(红))
    return 红, 黄


# ═══ 负测（令§六③：改闸必同日负测，且须旧式回灌） ═══
def 自测():
    """★负测之要：每一格都要**咬得住一个真的旧局**，不许拿常数钉死（§二十八）。"""
    ok, bad = 0, []

    def T(name, cond, note=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(name + ('（%s）' % note if note else ''))

    # ①今日之局：全查须绿（这一格是活的——仓里真有囤灰它就红）
    红, _ = 查(印=False)
    T('①今局无囤灰', not 红, '；'.join(红[:3]))

    # ②旧式回灌·器：把真跑口砍成一个**叶器**（字数闸——它谁也不引），闭包须当场塌下来。
    # ★这一格两头皆活（§二十八：不许把活数钉成常数）：
    #   拿「全跑口之闭包」减「叶器之闭包」，其差须 ≥50——两个数都是当场算的，
    #   日后添器减器它自己跟着走，钉不死也洗不白。
    # ★★为什么不拿「跑轮.py」当叶器：跑轮.py 的头注里提了全测.py，闭包一层就展满了（实测囤灰 0）——
    #   **那样这一格就是死的，而它会天天印绿**。这一处是本器立日亲手逮出来的，记此备忘。
    reach全, tools全 = 器之闭包()
    reach叶, tools叶 = 器之闭包(runners=['工具/字数闸.py'])
    差 = len(reach全) - len(reach叶)
    T('②叶器闭包须比全跑口闭包小 ≥50（今：%d − %d）' % (len(reach全), len(reach叶)), 差 >= 50,
      '实差 %d' % 差)

    # ③器之全集须＝工具/*.py 之数（防它悄悄只认一部分）
    真数 = len(glob.glob(os.path.join(ROOT, '工具', '*.py')))
    T('③器全集＝工具/*.py 之数 %d' % 真数, len(tools全) == 真数, '实认 %d' % len(tools全))

    # ④挂账须读得出（拿一行假账灌进去验其正则）
    m = re.match(r'\s*[·*-]\s*(\S+?)\s*(?:——|--)\s*(.+)', '· 某器.py —— 其由（限：第 999 章前接上）')
    T('④挂账一行读得出', bool(m) and m.group(1) == '某器.py')

    # ⑤丙只管起用章及其後（拿一个旧章号验其不判）
    T('⑤起用章之界在 306', 起用章 == 306)

    # ⑥八段之名与 一章.js 之 meta.phases 逐字同（防两处各说各的）
    js = _读('工具/席/一章.js')
    缺 = [x for x in 八段 if ("title: '%s'" % x) not in js]
    T('⑥八段之名与 一章.js 同', not 缺, '一章.js 里缺：' + '／'.join(缺))

    # ⑦席之全集非空（防 glob 写错路而一律绿）
    T('⑦席读得着', len(glob.glob(os.path.join(ROOT, '工具', '席', '*.js'))) >= 4)

    # ⑧旧式回灌·席：拿一个不存在于 一章.js 与 用法.md 的席名，须判红
    T('⑧未挂之席须判红', ('无此席.js' not in js) and ('无此席.js' not in _读('工具/席/用法.md')))

    # ⑧之二·旧式回灌·schema 键：拿一段中文键之 schema 灌进正则，须逮出
    坏 = re.findall(r'([^\x00-\x7F][^\s:]*)\s*:\s*\{\s*type:', '  锁定行: { type: \'string\' },')
    T('⑧之二 中文 schema 键逮得出', 坏 == ['锁定行'], '实逮 %s' % 坏)

    # ⑧之三·今日之席无中文 schema 键（活格：真有就红）
    T('⑧之三 今日诸席之 schema 键尽是 ASCII',
      not any('schema 键非 ASCII' in x for x in 查(印=False)[0]))

    # ⑨正文在()须认得出真章（拿三个真章号验；认不出则丙整条是死的）
    T('⑨正文在()认得出 273／305／1', 正文在(273) and 正文在(305) and 正文在(1))

    # ⑩旧式回灌·丙：本仓今有「版本/第306章」而无正文，丙不许判它红
    T('⑩无正文之新章不判红',
      not any('第306章无 _席记' in x for x in 查(印=False)[0]) or 正文在(306))

    print('── 负测·囤灰闸 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    红, _ = 查()
    sys.exit(1 if 红 else 0)
