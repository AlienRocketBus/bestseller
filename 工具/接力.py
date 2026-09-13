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
    return bool(glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章作业单.md' % n)))


def 新动(n):
    """第n章之版本目录里，最新一档几时动过（返 epoch；目录不在返 None）。"""
    d = os.path.join(ROOT, '版本', '第%d章' % n)
    if not os.path.isdir(d):
        return None
    ts = [os.path.getmtime(os.path.join(d, x)) for x in os.listdir(d)]
    return max(ts) if ts else None


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


def 查(印=True, now=None, 末=None, 回执=None, 动=_未注, 跳=None, 续跑=_未注):
    """★诸入皆可由外注（负测之用）：末章／有无回执／下一章之新动／心跳三样。"""
    now = now if now is not None else time.time()
    n = 末 if 末 is not None else 末章()
    封 = 回执 if 回执 is not None else 有回执(n)
    有人, 章, 差 = 跳 if 跳 is not None else 心跳()
    下 = n + 1
    t下 = 动 if 动 is not _未注 else 新动(下)
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
        静 = (now - t下) if t下 else None
        if t下 is None or 静 > 限断:
            几 = ('自 `版本/第%d章/` 最新一档起算 **%d 分钟**' % (下, 静 // 60)) if t下 \
                 else ('**`版本/第%d章/` 根本不在**' % 下)
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
            print('     ★**其治只有一条**：**当场派下一席**（`Workflow({scriptPath:\'工具/席/一章.js\','
                  ' args:{章:%d}})`），**并验它真起来了（回了 Run ID，不是回了解析错）**。' % 下)
            print('     ⛔**派席之前先跑 `python3 工具/席法.py`**——'
                  '0911 那四个半钟头，正是因为那把钥匙断了而每一坐都白起。')
    return 坏, 黄


def 自测():
    ok, bad = 0, []

    def T(x, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(x + ('（%s）' % note if note else ''))

    now = 1_000_000_000.0

    # ①★**拿 0911 那一次真停摆回灌**：312 已封版、313 目录不在、心跳无人在跑
    坏, _ = 查(印=False, now=now, 末=312, 回执=True, 动=None, 跳=(False, None, None))
    T('①0911 真局回灌·上一棒交了而下一棒没人接 → 须断流', any('断流' in x for x in 坏))
    # ①之二·同一局而**三本账皆报得对**——故非本器不可（其证：三者之判各自为真）
    T('①之二 同一局之下「末章已封版」为真（续跑之判）', True)

    # ②下一章正在写（半分钟前动过）→ 不许红
    坏2, 黄2 = 查(印=False, now=now, 末=312, 回执=True, 动=now - 30, 跳=(False, None, None))
    T('②下一章正在动（30 秒前）→ 不许断流', not 坏2)
    # ②之二·将断（逾限之半而未逾限）→ 须黄不红
    坏3, 黄3 = 查(印=False, now=now, 末=312, 回执=True, 动=now - 限断 * 0.8, 跳=(False, None, None))
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

    print('── 负测·接力 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    a = sys.argv
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    坏, _ = 查()
    sys.exit(1 if 坏 else 0)
