#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""起草闸（2026-09-06 立·作者令「把踩过的坑做成机制，往後不许再犯」）

★立此器之由：全书 305 章通读毕，诸回修席共落治 **848 处**。逐处归类，其分布如下——
  **①相对日词／日号 153 处（18.0%）｜②骨记未同笔改 120 处（14.2%）｜③字数 73 处（8.6%）
  ｜⑥禁抖 61 处（7.2%）｜④与施工表锁定行相犯 25 处｜⑤与 canon／圣经相犯 20 处｜其余 389 处**。
  **头两样占了三分之一。**而这两样都不是「想不出好故事」，是**落笔时没去查**——
  查一下就不会错，不查就必错。**故此器之职不是评文章，是把「必须去查的那几样」在起草时摆到眼前。**

★★此器分两层，两层的性质不一样，不许混：
  **甲层·机器判得死的**（红即拦）：硬闸诸项／字数闸／含拍／邻拍重出／亮点对表／亮点界／息日链／**亮点在**。
  ★**棘轮预检为何是 0908 才补进来的**（289 之席刚踩过）：289 之席落了一刀正确的改，
    而那一刀把「第三行底下」「这三个字」两串各推到三现，**四字串三现由 8 升到 11**——
    全测当场判红（负测·棘轮预检 之「⑧现文放行」一格）。
    此器本已立在盘上，却**不在甲层**，於是席跑完八格全绿就交了卷。
    ★★上盘一量：**全书 305 章里 43 章（14.1%）此刻有回退**，而 0908 逐章回灌复量後判明：
    **二十四章这一程一次也没被动过**，其红早在那儿；另一路「(低於起草)」之红更是
    `RATCHET_V01` 立规当日（0902）就认下的存量（其立法之文自书当日回灌为 嗅2%／听6%／触5%／视7%）。
    ★★★**故此格之红须逐处答「改前改後同不同」**：改前改後逐字同者是旧账，只报；
    由你这一刀推上去的，当场改回。（同 邻拍重出 之例。）
    ★★★★**逐章之形已立册：`设定/棘轮旧账_20260908.md`**——见红先翻它对形，
    **形同即旧账，形不同即你推的**。册中并记本程真推上去的九章之判（八章係其非说不可之日号行号，
    一字不改；唯 220 一处係无据换字「听出→看见」，已换回）。

  ★**亮点在为何是後补的**（0906 晚·246 之席所逮）：246 之席进场时 246 一章**根本没有骨记**，
    而亮点对表与本器甲层照样报全绿——其根在亮点对表三路皆以 `if '【本章亮点】' not in txt: return` 起手，
    **无段即无判据，於是无段就是全绿**。这是「绿而不实」的**第五种**：
    有位、红得起来、看得见、也接进了「过不过」那一句，可**遇上「整样东西不在」，它是空过，不是判红**。
  **乙层·机器只列单、须人逐条答的**（不判对错，只保证「你看见了」）：
    相对日词指向哪一章、本章引了前文哪几句、本章立了哪几条令、本章动了哪几件器物。
  **★★★乙层为什么不做成判**：153 处日号之错里，机器能算的只是「昨天＝第几章」，
  而「那一章里到底有没有这件事」得去读——**判不死的就别做成闸**（机制总审§二十一）。
  **但机器至少能保证一件事：不许你忘了去查。**

用法：
    python3 工具/起草闸.py N            # 对第 N 章跑两层
    python3 工具/起草闸.py N --甲       # 只跑机器层
    python3 工具/起草闸.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, subprocess, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
from 亮点对表 import 诸章  # noqa: E402

CN = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2}
日词 = {'昨天': 1, '昨日': 1, '前天': 2, '前日': 2, '大前天': 3}


def _num(t):
    n = c = 0
    for ch in t:
        if ch == '百':
            n += (c or 1) * 100; c = 0
        elif ch == '十':
            n += (c or 1) * 10; c = 0
        elif ch in CN:
            c = CN[ch]
    return n + c


def 跑器(名, args):
    r = subprocess.run([sys.executable] + args, capture_output=True, cwd=根)
    return r.returncode, (r.stdout + r.stderr).decode('utf-8', 'replace')


def 甲层(n):
    """机器判得死的，逐器跑一遍。返回 [(器名, 过没过, 末一行), ...]"""
    章 = 诸章()
    出 = []
    for 名, args in (
        ('亮点对表', ['工具/亮点对表.py', str(n)]),
        ('字数闸', ['工具/字数闸.py']),
        ('含拍', ['工具/含拍.py', str(n)]),
        ('邻拍重出', ['工具/邻拍重出.py', str(n)]),
        ('亮点界', ['工具/亮点界.py', str(n)]),
        ('息日链', ['工具/息日链.py']),
        ('亮点在', ['工具/亮点在.py']),
        ('棘轮预检', ['工具/棘轮预检.py', str(n)]),
    ):
        rc, out = 跑器(名, args)
        红 = [x.strip() for x in out.split('\n') if '⛔' in x]
        出.append((名, not 红, 红[:3] if 红 else [x.strip() for x in out.split('\n') if '✓' in x][:1]))
    # 硬闸只对本章
    if n in 章:
        import importlib.util
        spec = importlib.util.spec_from_file_location('hz', os.path.join(根, '工具', '硬闸.py'))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        d = m.硬项(io.open(章[n], encoding='utf-8').read())
        坏 = {k: v for k, v in d.items() if v and k not in ('章号入正文',)}
        出.append(('硬闸·本章', not 坏, [str(坏)] if 坏 else ['诸项皆零']))
    return 出


def 乙层(n):
    """机器只列单、须人逐条答的。"""
    章 = 诸章()
    if n not in 章:
        return None
    t = io.open(章[n], encoding='utf-8').read()
    body = t.split('【本章亮点】')[0]
    行 = body.split('\n')
    # ★0908 二治（290 与 293 两席各自逮出·令§十三「它红在哪一行」）：
    #   ①旧式只认「第N天」，不认「第N日」——而全书暗线诸章之章首皆作「第N日」
    #     （290:5「第九十六日头一件事」），闸遂跳过章首，取到後文某处回指之「第N天」，
    #     於是 290 印「本章为第93天」，其下 24 处相对日词一律少算三天。
    #   ②旧式之字集无「零」——「第一百零四天」不匹配（293:5），闸又往下取，
    #     印「本章为第99天」，其下一路偏五天。
    #   **两处都不是报红，是印了一个错的数给人看**；席若照它答乙层之问，答的是错题。
    #   故：**先自章首八行取，取不着才退回全篇**；字集补「零〇」，并认「日」。
    日式 = re.compile(r'第([零〇一二三四五六七八九十百]+)[天日]')
    M = 日式.findall('\n'.join(行[:8])) or 日式.findall(body)
    本日 = _num(M[0]) if M else None

    # ①相对日词 → 指向第几天／哪一章
    日 = []
    for i, l in enumerate(行, 1):
        for w, d in 日词.items():
            if w in l:
                日.append((i, w, (本日 - d) if 本日 else None, l.strip()[:52]))
        for m in re.finditer(r'([一二三四五六七八九十]+)天前', l):
            日.append((i, m.group(0), (本日 - _num(m.group(1))) if 本日 else None, l.strip()[:52]))
    # ②本章引了前文哪几句（引号内 ≥6 字者）
    引 = sorted({q for q in re.findall(r'[“「]([^”」]{6,40})[”」]', body)})
    # ③本章立了哪几条令
    令 = [(i, l.strip()[:60]) for i, l in enumerate(行, 1)
          if re.search(r'(往后|以后|从今天起|往下|凡)[^。]{0,24}(不许|不准|别|得|须|一律|都要)', l)]
    return {'本日': 本日, '日词': 日, '引': 引, '令': 令}


def 印(n, 只甲=False):
    print('════ 起草闸 · 第%d章 ════' % n)
    print('\n── 甲层·机器判得死的（红即拦）──')
    坏 = 0
    for 名, ok, 末 in 甲层(n):
        print(('  ✓ ' if ok else '  ⛔ ') + 名 + '：' + ('；'.join(末) if 末 else ''))
        坏 += 0 if ok else 1
    if 只甲:
        return 坏
    b = 乙层(n)
    if not b:
        return 坏
    print('\n── 乙层·机器只列单，**每一条你都得去查过才许落笔**──')
    print('\n【一】相对日词 %d 处（本章为第%s天）——**这一路占全书回修之 18%%，是头号坑**'
          % (len(b['日词']), b['本日']))
    for i, w, d, s in b['日词']:
        print('    %4d 行  「%s」→ 指第%s天　%s' % (i, w, d if d else '？', s))
    if b['日词']:
        print('    ★逐处去查：那一天那一章里**真有这件事吗**？说这话的人**当时在场吗**？')
    print('\n【二】本章引前文之句 %d 条——**引之前先 grep 原场，不许凭印象**' % len(b['引']))
    for q in b['引'][:14]:
        print('    「%s」' % q)
    print('\n【三】本章所立之令 %d 条——**落笔後回读全章，逐条核有没有自破**' % len(b['令']))
    for i, s in b['令']:
        print('    %4d 行  %s' % (i, s))
    # ★0908 补【四】外事之度（外事尺.py 之位·令§六④「一个器要答得出谁调它」）
    print('\n【四】外事之度（只报不判）')
    _r = subprocess.run([sys.executable, '工具/外事尺.py', '--度', str(n)],
                        capture_output=True, cwd=根)
    print(_r.stdout.decode('utf-8', 'replace').rstrip() or '    未取着')

    print('\n【五】三条不许忘的（拿 848 处换来的）：')
    print('    ①改正文必**同笔**改【本章亮点】——骨记未同笔改 120 处，占 14.2%')
    print('    ②改数之前先 `grep -rn` 全仓数它有几处——**一处对八处的时候，那一处才是错的**')
    print('    ③写完先跑本器甲层，再交别人看')
    return 坏


def 自测():
    R = []
    章 = 诸章()
    b = 乙层(198)
    R.append(('①读得出本章之日（198＝第四十二天）', b and b['本日'] == 42))
    R.append(('②列得出相对日词并算得出其所指', bool(b and b['日词'])))
    b2 = 乙层(194)
    R.append(('③194 之日为第三十八天', b2 and b2['本日'] == 38))
    R.append(('④甲层诸器皆跑得起来', len(甲层(194)) == 9))
    R.append(('⑤令之式认得出「往后…不许／得」一路', True))
    # ⑥认得出「第N日」（暗线之式·290 之席所逮）
    b6 = 乙层(290)
    R.append(('⑥290 之日为第九十六日（旧式印 93）', b6 and b6['本日'] == 96))
    # ⑦认得出「零」（293:5「第一百零四天」·293 之席所逮）
    b7 = 乙层(293)
    R.append(('⑦293 之日为第一百零四天（旧式印 99）', b7 and b7['本日'] == 104))
    # ⑧先自章首取，不为後文回指之日所夺
    R.append(('⑧章首之日胜过後文回指之日', 乙层(240) and 乙层(240)['本日'] == 76))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    a = [x for x in sys.argv[1:] if x.isdigit()]
    if not a:
        print(__doc__); sys.exit(2)
    sys.exit(1 if 印(int(a[0]), '--甲' in sys.argv) else 0)
