#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""接力——**三本账问的都是「上一件事办完没有」，本器只问一句：「下一件事起来没有。」**

【其立之由（2026-09-11·一次真停摆逼出来的·作者亲令「确保不停」）】
  0910 21:00 第312章封版撤锁，0911 01:28 第313章才起——**中间四个半钟头，一个字也没写。**
  ★而那一刻本仓三本账**一本也没响，而且三本都报得对**：
    · 心跳：312 已撤锁 → 「✓无人在跑」——**它报得对**；
    · 续跑：末一步「312·封版席毕」——**它记得对**；
    · 存底：东西一样没丢——**它也对**。
  ★★**三本账问的全是同一件事：上一件事办完没有。**
    **没有一本在问：下一件事起来没有。**
  ★★★**「办完了」与「接上了」是两件事**——而书停就停在这两件事的缝里。

【它怎么问·只看盘上看得见的东西，不猜】
  甲·**断流**（红）：末章已封版（其回执在），而**下一章一点动静也没有**
     （`版本/第N+1章/` 不在，或其最新一档逾 限断 分钟未动），**且心跳报无人在跑**
     ——★**即：上一棒交了，下一棒没人接。**
     ★1020 X21：其静自「交棒之刻」与下一章之新动二者之晚者起算——交棒之刻＝`版本/第N章/_十一轮.json` 之 mtime
     （封版 --後 之第十一轮所产，紧在其全测之前）。旧只看下一章之新动，而那多是记席先写之开镜卡：
     封版之全测（心跳 N 已逾时）遂撞断流（394 推拦 68 分）；⛔为此先跳 N+1——那是一把无席之空锁（W53 验席所逮）。
  乙·**空转**（黄）：心跳报有人在跑，**而那一章的 `版本/第N章/` 逾 限空 分钟一档未动**
     ——★**锁攥在手里而活没在动**：多半是那一坐挂了而心跳被别的器顺手续着，
     或是它卡在某一处。**只报不判，其裁在人。**
  丙·**将断**（黄）：断流未逾 限断 而已逾其半——**先出声，好过等它红。**

【它绝不做的两样】
  ①**不动手**：不派席、不改文、不推——**它只说「断了没有」**；
  ②**不猜**：一切判据皆自盘上取（回执在不在／版本目录之 mtime／心跳档），**不问任何人**。

用法：
    python3 工具/接力.py            # 三路全查（rc=1 即断流）
    python3 工具/接力.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记
except Exception:
    pass
import os
import re
import sys
import glob
import time
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
限断 = 25 * 60      # 下一章一点动静也没有，逾此即判断流（自走 Routine 每小时一坐，二坐错开则 ≤30 分）
限空 = 50 * 60      # 锁在手而那一章一档未动，逾此即报空转


def 末章():
    return len([x for x in os.listdir(os.path.join(ROOT, '正文')) if x.endswith('.md')])


def 有回执(n):
    # ⛔认三种，不只认作业单（限360·其详在 全测.py::_已封版）
    return any(glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章%s.md' % (n, k)))
               for k in ('作业单', '封版席'))  # ⛔0924 收回「案席」·见上注


def 新动(n):
    """第n章之版本目录里，最新一档几时动过（返 epoch；目录不在返 None）。"""
    d = os.path.join(ROOT, '版本', '第%d章' % n)
    if not os.path.isdir(d):
        return None
    ts = [os.path.getmtime(os.path.join(d, x)) for x in os.listdir(d)]
    return max(ts) if ts else None


def 交棒(n):
    """第n章交棒之刻：其 `_十一轮.json` 之 mtime（封版 --後 之第十一轮所产；不在返 None）。★1020 X21。"""
    p = os.path.join(ROOT, '版本', '第%d章' % n, '_十一轮.json')
    return os.path.getmtime(p) if os.path.exists(p) else None


def 续跑末步():
    """★★★0911 立器当日即被自己逮出一处假黄，故补此函**（其形须记下）**：
    乙路原只看 `版本/第N章/` 之 mtime，**而一章之头三四段（定位／三魂／起草之前）一个版也不存**——
    於是 313 开跑二十分钟，本器就报「空转 280 分钟」：**它量的是上一坐留下的开镜卡，不是这一坐的活。**
    ★**故乙路须取二者之晚者**：版本目录之动 **与** 续跑末一步之时。
    ★★**其理一句**：**「活在不在动」这一问，版本目录只答得出後半程；前半程是续跑在记。**
    """
    p = os.path.join(ROOT, '_任务流.json')
    try:
        d = json.load(open(p, encoding='utf-8'))
        步 = d.get('步') or []
        if not 步:
            return None
        import calendar
        return calendar.timegm(time.strptime(步[-1].get('时', ''), '%Y-%m-%d %H:%M:%S'))
    except Exception:
        return None


def 心跳():
    """返 (有人在跑?, 第几章, 几秒前报到)。★自本地之心跳档读——
    ★★**本器不 fetch 远端**：它只在本坐跑，而本坐若有席在跑，其心跳正是本坐续的。"""
    p = os.path.join(ROOT, '_心跳.json')
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception:
        return False, None, None
    if d.get('章') is None:
        return False, None, None
    差 = int(time.time()) - int(d.get('时', 0))
    return (差 <= 45 * 60), d.get('章'), 差


_未注 = object()   # ★**须与 None 分得开**：负测要注的正是「下一章根本没动静」这一局，
                   #   而那一局之值就是 None；若拿 None 当「没注」，本器即回头去读真盘，
                   #   ★★**於是那一格永远测不着**——0911 立器当日实见，一立即犯。


def 暂停():
    try:
        import 暂停令
        return 暂停令.在()
    except Exception:
        return False, ''


def 查(印=True, now=None, 末=None, 回执=None, 动=_未注, 跳=None, 续跑=_未注, 停=None, 交=_未注):
    """★诸入皆可由外注（负测之用）：末章／有无回执／下一章之新动／心跳三样；停＝(在否, 由)，暂停令（1009）；交＝末章交棒之刻（1020 X21）。"""
    now = now if now is not None else time.time()
    n = 末 if 末 is not None else 末章()
    封 = 回执 if 回执 is not None else 有回执(n)
    有人, 章, 差 = 跳 if 跳 is not None else 心跳()
    下 = n + 1
    t下 = 动 if 动 is not _未注 else 新动(下)
    停在, 停由 = 停 if 停 is not None else 暂停()
    坏, 黄 = [], []

    # 乙·空转：锁在手而那一章不动
    if 有人 and 章:
        t本 = 动 if (动 is not _未注 and 章 == 下) else 新动(int(章))
        # ★取二者之晚者：版本目录只答得出後半程，前半程是续跑在记
        t续 = 续跑 if 续跑 is not _未注 else 续跑末步()
        if t续 and (t本 is None or t续 > t本):
            t本 = t续
        if t本 and (now - t本) > 限空:
            黄.append('乙·空转：心跳报第%s章在跑（%d 分钟前报到），'
                      '而 `版本/第%s章/` 已 **%d 分钟**一档未动——'
                      '**锁攥在手里而活没在动**；其裁在人，本器只报。'
                      % (章, (差 or 0) // 60, 章, (now - t本) // 60))

    # 甲·断流：上一棒交了，下一棒没人接
    if 封 and not 有人:
        t交 = 交 if 交 is not _未注 else 交棒(n)
        t起 = max([t for t in (t下, t交) if t] or [None])     # ★1020 X21：交棒之刻与下一章之新动，取其晚者
        静 = (now - t起) if t起 else None
        if (t起 is None or 静 > 限断) and 停在:
            # ★1009：作者之暂停令在盘上（`工具/暂停令.py` 验其引作者原话、其据真在）——下一章不动是令，不是断
            黄.append('⏸ %s——第%d章不动是作者之令，⛔判断流；作者令下即 `python3 工具/暂停令.py --解 "作者令：……"`，本判即复。' % (停由, 下))
        elif t起 is None or 静 > 限断:
            几 = ('**`版本/第%d章/` 根本不在**' % 下) if t起 is None \
                 else ('自 `版本/第%d章/` 最新一档起算 **%d 分钟**' % (下, 静 // 60)) if t起 == t下 \
                 else ('自第%d章交棒（`_十一轮.json`）起算 **%d 分钟**%s' % (n, 静 // 60, '' if t下 else '；`版本/第%d章/` 不在' % 下))
            坏.append('甲·**断流**：第%d章已封版（回执在），而第%d章一点动静也没有（%s），'
                      '**且心跳报无人在跑**——★**上一棒交了，下一棒没人接。**'
                      % (n, 下, 几))
        elif 静 > 限断 / 2:
            黄.append('丙·将断：第%d章已封版而第%d章已静 **%d 分钟**（限 %d 分钟）——**先出声，好过等它红。**'
                      % (n, 下, 静 // 60, 限断 // 60))

    if 印:
        print('════ 接力 ════（只问一句：**下一件事起来没有**）')
        print('  末章 第%d章｜其回执 %s｜心跳 %s'
              % (n, '在' if 封 else '不在',
                 ('第%s章·%d 分钟前' % (章, (差 or 0) // 60)) if 有人 else '无人在跑'))
        for x in 坏:
            print('  ⛔ ' + x)
        for x in 黄:
            print('  ⚠ ' + x)
        if not 坏 and not 黄:
            print('  ✓ 接上了。')
        # ★★★★★2026-09-13 焊入（作者当面点名「不要再停」那一日）：
        #   ⛔**常令在此之前只在会话里，没有在盘上**——**每一次重启、每一次接手，
        #   它都得靠人记得**；★**故每跑一回接力，即把不停之律当面印一遍。**
        print('  ★★★⛔头一件事不是读这几条，是跑：python3 工具/自走.py')
        print('     （它只答「此刻该干哪一件」，并印出那一条可照抄之命令；跑完再跑一回它。）')
        print('  ── 不停之律（`设定/00_作者常令_不停之律.md`·⛔每次接手当面印）──')
        print('     ①一章写完接着下一章，⛔不为请示而停。')
        print('     ②⛔「派完席就回话」不算干活——**席在跑时手上须同时有另一件真活**。')
        print('     ③⛔回合末须有正在跑的席，或已排好的唤醒；两样都没有＝停了。')
        print('     ④⛔先干活再看闸；活干完闸还红→闸错了，改它并同日立负测。')
        print('     ⑤⛔而权再大也不许的一样：把闸放松以让自己这一章过。')
        if 坏:
            print('     ★**其治只有一条**：**当场派下一席**（照 `python3 工具/自走.py` 所印之令——二代 造章.js；第 %d 章），'
                  '**并验它真起来了（回了 Run ID，不是回了解析错）**。' % 下)
            print('     ⛔**派席之前先跑 `python3 工具/席法.py`**——'
                  '0911 那四个半钟头，正是因为那把钥匙断了而每一坐都白起。')
    return 坏, 黄


def 自测():
    global ROOT        # ⑯改 ROOT 指 tempdir（读盘之路），finally 还原
    ok, bad = 0, []

    def T(x, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(x + ('（%s）' % note if note else ''))

    now = 1_000_000_000.0

    # ①★**拿 0911 那一次真停摆回灌**：312 已封版、313 目录不在、心跳无人在跑
    坏, _ = 查(印=False, now=now, 末=312, 回执=True, 动=None, 跳=(False, None, None), 停=(False, ''), 交=None)
    T('①0911 真局回灌·上一棒交了而下一棒没人接 → 须断流', any('断流' in x for x in 坏))
    # ①之二·同一局而**三本账皆报得对**——故非本器不可（其证：三者之判各自为真）
    T('①之二 同一局之下「末章已封版」为真（续跑之判）', True)

    # ②下一章正在写（半分钟前动过）→ 不许红
    坏2, 黄2 = 查(印=False, now=now, 末=312, 回执=True, 动=now - 30, 跳=(False, None, None), 交=None)
    T('②下一章正在动（30 秒前）→ 不许断流', not 坏2)
    # ②之二·将断（逾限之半而未逾限）→ 须黄不红
    坏3, 黄3 = 查(印=False, now=now, 末=312, 回执=True, 动=now - 限断 * 0.8, 跳=(False, None, None), 交=None)
    T('②之二 逾限之半而未逾限 → 黄不红', not 坏3 and any('将断' in x for x in 黄3))

    # ③心跳报有人在跑 → 不许判断流（那是别人在写，不是断了）
    坏4, _ = 查(印=False, now=now, 末=312, 回执=True, 动=None, 跳=(True, 313, 60))
    T('③有人在跑 → 不许判断流', not 坏4)

    # ④末章尚未封版（回执不在）→ 不许判断流（那一章还在写）
    坏5, _ = 查(印=False, now=now, 末=312, 回执=False, 动=None, 跳=(False, None, None))
    T('④末章未封版 → 不许判断流', not 坏5)

    # ⑤空转：锁在手而那一章逾限不动 → 须报黄
    _, 黄6 = 查(印=False, now=now, 末=312, 回执=True, 动=now - 限空 - 60,
                跳=(True, 313, 60), 续跑=now - 限空 - 60)
    T('⑤锁在手而那一章逾 %d 分钟不动 → 须报空转' % (限空 // 60), any('空转' in x for x in 黄6))

    s = open(os.path.join(ROOT, '工具', '接力.py'), encoding='utf-8').read().split('def 自测')[0]
    # ⑥本器不许动手（它只说断没断）
    T('⑥本器不派席、不改文、不推（全码无 Workflow／git push／open(w)）',
      'subprocess' not in s and "'w'" not in s and 'git' not in s.replace('git push', ''))
    # ⑦其限之数只定义一处
    T('⑦限断／限空各只定义一处', s.count('限断 = ') == 1 and s.count('限空 = ') == 1)
    # ⑩★**立器当日之实败，钉在测里**：拿 None 当「没注」，则「下一章根本没动静」那一局
    #   永远注不进去（本器回头去读真盘，而真盘上那一章正在写）——**於是最要紧的那一格空测**。
    # ⑪★**立器当日之第二败**：乙路只看版本目录，而一章之头三四段一个版也不存——
    #   313 开跑二十分钟，本器即报「空转 280 分钟」：**它量的是上一坐留下的开镜卡，不是这一坐的活。**
    _, 黄11 = 查(印=False, now=now, 末=312, 回执=True, 动=now - 限空 - 60,
                跳=(True, 313, 60), 续跑=now - 120)
    T('⑪版本目录久未动而续跑两分钟前刚记过一步 → 不许报空转（前半程是续跑在记）',
      not any('空转' in x for x in 黄11))
    _, 黄12 = 查(印=False, now=now, 末=312, 回执=True, 动=now - 限空 - 60,
                跳=(True, 313, 60), 续跑=now - 限空 - 60)
    T('⑪之二 二者俱久未动 → 照旧报空转（不许因补了这一路就放松）',
      any('空转' in x for x in 黄12))
    T('⑩注入之「无」与「没注」分得开（不然最要紧的那一格是空测）',
      '_未注 = object()' in s and 'is not _未注' in s)
    # ⑧判据皆自盘上取，不问人
    T('⑧判据皆自盘上取（回执／版本目录 mtime／心跳档）',
      '有回执' in s and 'getmtime' in s and '_心跳.json' in s)
    # ⑨★其报须把「下一步该干什么」说出来（一个只会喊断的器，喊完还是没人接）
    T('⑨断流之报须带其治（派下一席＋先跑席法）', '当场派下一席' in s and '席法' in s)

    # ⑬1009·暂停令在（作者令、据真在）→ 不判断流，须报黄
    坏13, 黄13 = 查(印=False, now=now, 末=380, 回执=True, 动=None, 跳=(False, None, None), 停=(True, '暂停令在'), 交=None)
    T('⑬暂停令在 → 不判断流而报黄', not 坏13 and any('暂停令' in x for x in 黄13))
    # ⑭暂停令不在（已解或不认）→ 照旧断流
    坏14, _ = 查(印=False, now=now, 末=380, 回执=True, 动=None, 跳=(False, None, None), 停=(False, '已解'), 交=None)
    T('⑭暂停令已解或不认 → 照旧断流', any('断流' in x for x in 坏14))

    # ⑮★1020 X21（W53 验席之治法 a）：封版之全测之局——心跳 N 已逾时、下一章之卡係记席 68 分前所写、第十一轮 2 分前方过
    #   → ⛔断流（交棒之刻起算）；⛔为此先跳 N+1（空锁）。回灌旧判（静只自下一章之新动起算——即 交 不入）须红。
    坏15, _ = 查(印=False, now=now, 末=397, 回执=True, 动=now - 68 * 60, 跳=(False, None, None), 停=(False, ''), 交=now - 120)
    旧15, _ = 查(印=False, now=now, 末=397, 回执=True, 动=now - 68 * 60, 跳=(False, None, None), 停=(False, ''), 交=None)
    T('⑮X21 封版之全测：十一轮刚过、下一章之卡久 → ⛔断流（旧判只看卡 → 断流，即 394 之病）',
      not 坏15 and any('断流' in x for x in 旧15))
    # ⑮之二 交棒亦久（逾限断）且下一章不在 → 照旧断流，其报点名交棒之刻（⛔因补此路而放松 0911 之局）
    坏16, _ = 查(印=False, now=now, 末=397, 回执=True, 动=None, 跳=(False, None, None), 停=(False, ''), 交=now - 限断 - 60)
    T('⑮之二 交棒逾限而下一章不在 → 照旧断流（报交棒之刻、并点下一章不在）',
      any('断流' in x and '交棒' in x and '不在' in x for x in 坏16))
    # ⑮之三 交棒与下一章之新动取其晚者（⛔取早者）：卡 2 分前、交棒 3 时前 → ⛔断流
    坏17, _ = 查(印=False, now=now, 末=397, 回执=True, 动=now - 120, 跳=(False, None, None), 停=(False, ''), 交=now - 180 * 60)
    T('⑮之三 取晚者：下一章刚动而交棒久 → ⛔断流', not 坏17)

    # ⑯★W60·X33④（W53 验席所逮）：⑮诸格皆注入 交=…，**交棒() 读盘之一路无一格守**——
    #   变异「交棒读第 N+1 章之档」「交棒恒返 None」二式，旧测俱绿。今以 tempdir 造盘两局（_十一轮.json 有／无），
    #   改 ROOT 而⛔注 交、⛔注 动（交棒、新动皆自盘上读），验断流之有无。
    import tempfile
    _根 = ROOT
    try:
        with tempfile.TemporaryDirectory(prefix='接力自测_') as td:
            ROOT = td
            d97, d98 = (os.path.join(td, '版本', '第%d章' % k) for k in (397, 398))
            os.makedirs(d97)
            os.makedirs(d98)
            卡, 凭 = os.path.join(d98, '_开镜卡.md'), os.path.join(d97, '_十一轮.json')
            open(卡, 'w', encoding='utf-8').close()
            t0 = time.time()
            os.utime(卡, (t0 - 68 * 60, t0 - 68 * 60))

            def 盘(**k):
                return 查(印=False, now=t0, 末=397, 回执=True, 跳=(False, None, None), 停=(False, ''), 续跑=None, **k)
            # 有局：_十一轮.json 2 分前、下一章之卡 68 分前 → ⛔断流（交棒自盘上读得）
            open(凭, 'w', encoding='utf-8').write('{}')
            os.utime(凭, (t0 - 120, t0 - 120))
            坏有, _ = 盘()
            T('⑯盘·有局：_十一轮.json 2 分前、卡 68 分前 → 交棒自盘读得、⛔断流',
              交棒(397) == t0 - 120 and not 坏有, '交棒=%r 坏=%r' % (交棒(397), 坏有))
            # 有局之二：_十一轮.json 亦 68 分前 → 照旧断流（⛔因读盘之路而放松）
            os.utime(凭, (t0 - 68 * 60, t0 - 68 * 60))
            坏有2, _ = 盘()
            T('⑯之二 盘·有局：_十一轮.json 68 分前 → 照旧断流', any('断流' in x for x in 坏有2))
            # 无局：_十一轮.json 不在（而第 396 章之凭刚写、第 398 章亦无凭——只认第 N 章自己的）→ 断流
            os.remove(凭)
            os.makedirs(os.path.join(td, '版本', '第396章'))
            open(os.path.join(td, '版本', '第396章', '_十一轮.json'), 'w', encoding='utf-8').write('{}')
            坏无, _ = 盘()
            T('⑯之三 盘·无局：第397章之 _十一轮.json 不在（396 之凭刚写⛔认）→ 交棒 None、断流',
              交棒(397) is None and any('断流' in x for x in 坏无), '交棒=%r' % (交棒(397),))
            # 无局之二：下一章目录亦不在 → 断流，报「根本不在」（0911 之局，自盘读）
            import shutil
            shutil.rmtree(d98)
            坏无2, _ = 盘()
            T('⑯之四 盘·无局：第398章目录亦不在 → 断流、报其根本不在',
              any('断流' in x and '根本不在' in x for x in 坏无2))
    finally:
        ROOT = _根

    print('── 负测·接力 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    a = sys.argv
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    坏, _ = 查()
    sys.exit(1 if 坏 else 0)
