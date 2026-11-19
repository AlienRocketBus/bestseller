# -*- coding: utf-8 -*-
"""负测 · 书级体检（2026-09-24 立·令§一⑤）

⛔**其所以非有此测不可**：本器六检担着全书之判，而它係「赤手」——**至今无一份同名负测**；
  ★**而本坐今日刚动过它的⑦**（认「本章之失」之第二式）——
  **改过一处而无同名负测，正是最该补的那一处。**
★**本测所钉者係本器身上三处「被治过」的判**（⛔被治过一回的，最会被反回去）：
  ① `sig_of` **分子分母同源**（0820 之治：旧式分母含「＊」分隔行，均段被腰斩，全书尽判「短」）；
  ② `相对之型` **窗内不足八章者退回旧式**（⛔免拿三五个数去分四档）；
  ③ `check_endgame` **三判各管一样**（已逾终点／清不完／到期章逾终点）。
  另 ④ `check_type_chain` 连锁之限係写死之 12，⛔不由今日之数算出。
〔1119 死规之审·gates10/12〕⑥ 起钉新裁：①在场之距／②章型连锁 照旧侦得、只印 ⚠、⛔入「不过」；
  ③账之净额 照旧拦（净 >0 入「不过」·〔1119 更胜从前之筛〕gates11 退回原样）；⑤ 见下条。
〔1119 死规之审·gates漏2·终局之令〕⑤ 三判（已逾终点／清不完／到期章逾终点）照旧各管一样、照旧侦得，今亦只印 ⚠、⛔入「不过」
  （终点係今之估、由事定·作者 1119）；守牙仍红者：未见正文 → rc 2；任一检入 bad → 格照拦（rc 2·「不过」）。
⛔本负测一律造局，⛔**不读真盘一个字去下判**；末格方点一回真盘作注。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器():
    s = _u.spec_from_file_location('书级体检', os.path.join(ROOT, '工具', '书级体检.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _文(段, 星=False):
    """★造一章：头二行係书名与章名（`sig_of` 之 [2:] 即跳它们）。"""
    体 = ('\n\n＊\n\n' if 星 else '\n\n').join(段)
    return '《书》\n\n第九十九章　假\n\n%s\n' % 体


def 跑():
    m = _器()
    R = []

    # ①⛔0820 之治·**分子分母同源**：`＊` 分隔行不入分母
    段 = ['甲' * 30, '乙' * 30, '丙' * 30]
    k1, avg1, tot1 = m.sig_of(_文(段, 星=False))
    k2, avg2, tot2 = m.sig_of(_文(段, 星=True))
    R.append(('①⛔同一三段，夹不夹「＊」其均段须同（%.1f／%.1f）——0820 之治'
              % (avg1, avg2), abs(avg1 - avg2) < 1e-9 and tot1 == tot2))
    # ⛔旧式回灌：分母取 len(ps)（含星）者，均段当场被腰斩
    ps = [x.strip() for x in _文(段, 星=True).split('\n') if x.strip()][2:]
    旧均 = sum(m.net_len(x) for x in ps if x != '＊') / max(1, len(ps))
    R.append(('①之二·⛔旧式回灌：分母含星者，均段自 %.1f 落到 %.1f（腰斩）'
              % (avg2, 旧均), 旧均 < avg2 * 0.75))
    R.append(('①之三·总数只算实字（三段各30字，总须 90）', tot1 == 90))
    R.append(('①之四·空章不炸，判 None', m.sig_of('《书》\n\n第九十九章　假\n\n')[0] is None))

    # ②⛔`相对之型`·窗内不足八章者退回旧式（⛔免拿三五个数去分四档）
    少 = dict((n, 10.0 + n) for n in range(1, 8))          # 七章
    R.append(('②窗内七章（＜8）者退回旧式，判 None', m.相对之型(少, 7) is None))
    # ⛔**本坐头一版之局造错了**：**其窗只取「本章及其前」**——
    #   **故第 1—7 章窗内不足八章，一律判 None**，而本坐拿第 1 章去问「它是不是窄」。
    #   ★**改法**：**窗不动（十一章为底），只把本章之值在同一个窗里挪**——
    #     **四档到不到得齐，问的是这一件，不是章号。**
    底 = dict((n, 10.0 + n) for n in range(1, 12))          # 十一章·11.0—21.0
    def _档(v):
        d = dict(底)
        d[12] = v
        return m.相对之型(d, 12)
    R.append(('②之二·同一窗内，本章之值极低者判「窄」', _档(0.0) == '窄'))
    R.append(('②之三·极高者判「宽」', _档(99.0) == '宽'))
    诸 = {_档(v) for v in [0.0, 13.5, 16.5, 19.5, 99.0]}
    R.append(('②之四·四档各有其名且到得齐（%s）——⛔四档不许并作二档'
              % '／'.join(sorted(x for x in 诸 if x)),
              诸 == {'窄', '中', '中宽', '宽'}))
    # ②之五·⛔其窗只取本章及其前——**在後头添一章，今日之档一格不许动**
    窗 = dict(底)
    窗[12] = 16.0
    R.append(('②之五·⛔其窗只取本章及其前（在後头添第99章，第12章之档不动）',
              m.相对之型(dict(list(窗.items()) + [(99, 999.0)]), 12)
              == m.相对之型(窗, 12) is not None))

    # ③⛔`check_endgame` 三判各管一样（⛔不许一判吞三判）
    # 〔1119 死规之审·gates漏2·终局之令〕其第三项今係「信号」（main 只印 ⚠、⛔入「不过」）——三判各管一样之钉照留
    终 = m.END_CH
    R.append(('③甲·已逾终点（今章 %d）即报' % 终,
              any('终点' in x for x in m.check_endgame([], 终)[2])))
    R.append(('③乙·未清之账多於所余之章即报（10 笔 对 余 3 章）',
              any('清不完' in x for x in m.check_endgame(
                  [{'id': 'X%d' % i, '状态': 'open'} for i in range(10)], 终 - 3)[2])))
    R.append(('③丙·到期章逾终点者即报',
              any('逾终点' in x for x in m.check_endgame(
                  [{'id': 'X', '状态': 'open', '到期章': 终 + 1}], 300)[2])))
    R.append(('③丁·三样皆无者不报——⛔证本检不是一律判否',
              m.check_endgame([{'id': 'X', '状态': 'open', '到期章': 300}], 200)[2] == []))
    R.append(('③戊·已清之账不计入「清不完」之数',
              m.check_endgame([{'id': 'X%d' % i, '状态': 'done'} for i in range(99)],
                              终 - 1)[2] == []))

    # ④⛔连锁之限係写死之 12（⛔不由今日之数算出）
    src = io.open(os.path.join(ROOT, '工具', '书级体检.py'), encoding='utf-8').read()
    R.append(('④⛔TYPE_CHAIN_LIMIT == 12 且係码上常量（⛔不由今日之数算出）',
              m.TYPE_CHAIN_LIMIT == 12
              and re.search(r'^TYPE_CHAIN_LIMIT = 12$', src, re.M) is not None))
    R.append(('④之二·⛔END_CH 亦係常量（%d）' % 终,
              re.search(r'^END_CH = \d+$', src, re.M) is not None))

    # ⑥〔1119 死规之审·gates10/12〕造局：①② 俱逾而③⑤无事 → 侦得（⚠ 照印）而 rc 0；③ 净 >0 → rc 2（守牙仍红）
    import contextlib
    def _章(c):
        return _文(['甲' * 40, '乙' * 40, '丙' * 40])
    诸章 = dict((c, _章(c)) for c in range(200, 220))           # 二十章同纹理、六人之名一字不现
    账 = [{'id': 'A', '立账章': 219, '状态': 'open', '到期章': 300}]   # 近十章立一笔、清零笔 → 净 +1
    # 〔1119 更胜从前之筛·gates11 退回〕③ 照旧拦，故验 ①②⑤ 之局须净 ≤0：另清一笔（立於窗外）→ 立一清一、净 0
    账0 = 账 + [{'id': 'B', '立账章': 150, '状态': 'done', '清偿章': 219}]
    _p, _bp, _ = m.check_presence(诸章, 账)
    R.append(('⑥①逾限而无账：照旧侦得（其行 ok=False、印 ⚠）而⛔入 bad',
              any((not r[4]) and r[5].startswith('⚠') for r in _p) and _bp == []))
    _sq, _ch, _bt = m.check_type_chain(诸章)
    R.append(('⑥之二·②同型连 %d 章（限 %d）：照旧侦得而⛔入 bad' % (_ch[1], m.TYPE_CHAIN_LIMIT),
              _ch[1] > m.TYPE_CHAIN_LIMIT and _bt == []))
    # 〔1119 更胜从前之筛·gates11 退回〕钉还原：净 >0 → 入 bad（③守牙仍红）；净 ≤0 → 不入
    _rd, _net, _bd = m.check_due_net(账, 219)
    R.append(('⑥之三·⛔③近十章净 %+.1f（>0）→ 入 bad（守牙仍红）' % _net,
              _net > 0 and len(_bd) == 1 and '须 ≤0' in _bd[0]))
    _rd0, _net0, _bd0 = m.check_due_net(账0, 219)
    R.append(('⑥之三b·③立一清一、净 %+.1f → ⛔入 bad（⛔证本检不是一律判否）' % _net0,
              _net0 <= 0 and _bd0 == []))
    def _主(诸, 账_, 静=True):
        旧 = (m.load_chapters, m.load_due, sys.argv)
        m.load_chapters, m.load_due = (lambda: dict(诸)), (lambda: list(账_))
        sys.argv = ['书级体检.py'] + (['--静'] if 静 else [])
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = m.main()
        finally:
            m.load_chapters, m.load_due, sys.argv = 旧
        return rc, buf.getvalue()
    _rc0, _o0 = _主(诸章, 账0)
    R.append(('⑥之四·①② 俱逾而③⑤无事 → rc 0、「书级体检通过」（⛔再拦）', _rc0 == 0 and '书级体检通过' in _o0))
    _rc1, _o1 = _主(诸章, 账0, 静=False)
    R.append(('⑥之五·其详印里 ①② 各印 ⚠（信号照印，⛔印 ⛔）',
              _rc1 == 0 and _o1.count('⚠') >= 2 and '⛔逾限' not in _o1 and '已连锁' not in _o1))
    # 〔1119 更胜从前之筛·gates11 退回〕③守牙仍红：同局而净 +1 → rc 2、「不过」、详印 ③ 行印 ⛔
    _rc1b, _o1b = _主(诸章, 账)
    _rc1c, _o1c = _主(诸章, 账, 静=False)
    R.append(('⑥之五b·⛔③近十章净 +1 → rc 2、「不过」、其由「账之净额…须 ≤0」；详印 ③ 行印 ⛔',
              _rc1b == 2 and '不过' in _o1b and '账之净额 +1.0（须 ≤0）' in _o1b
              and _rc1c == 2 and re.search(r'★近十章净 \+1\.0.*⛔', _o1c) is not None))
    # 〔1119 死规之审·gates漏2·终局之令〕钉改：⑤ 三判今只印 ⚠、⛔入「不过」（原验「⑤到期章逾终点 → rc 2」今验「⚠ 而不红」）
    _账5 = 账0 + [{'id': 'Z', '状态': 'open', '到期章': 终 + 1}]   # 〔gates11 退回〕用净 0 之局，免 ③ 混入
    _rc2, _o2 = _主(诸章, _账5)
    _rc2b, _o2b = _主(诸章, _账5, 静=False)
    R.append(('⑥之六·⑤到期章逾终点（今之估）→ rc 0、「通过」；详印 ⚠ 照印、注「终点係估」（⛔印 ⛔）',
              _rc2 == 0 and '书级体检通过' in _o2 and _rc2b == 0
              and '⚠有 1 笔账之到期章逾终点' in _o2b and '终点係估' in _o2b and '⛔ 有' not in _o2b))
    _终章 = dict((c, _章(c)) for c in range(终 - 2, 终 + 3))             # 今章逾估之终
    _rc3, _o3 = _主(_终章, [], 静=False)
    _近章 = dict((c, _章(c)) for c in range(终 - 8, 终 - 2))             # 余 3 章、未清 10 笔
    _rc4, _o4 = _主(_近章, [{'id': 'X%d' % i, '状态': 'open', '到期章': 终 - 1} for i in range(10)], 静=False)
    R.append(('⑥之七·⑤已逾今之估终点／照估清不完 → 俱 rc 0、⚠ 照印（⛔逼收、⛔逼凑章数）',
              _rc3 == 0 and '⚠已达或逾终点' in _o3 and _rc4 == 0 and '⚠未清之账 10 笔' in _o4 and '清不完' in _o4))
    # ⛔守牙仍红：未见正文 → rc 2；格之拦照在——任一检入 bad 即 rc 2、「不过」（造局：借 ① 之口报一条）
    _rc5, _o5 = _主({}, 账)
    _旧p = m.check_presence
    m.check_presence = lambda c, d: (lambda r: (r[0], ['造局之守'], r[2]))(_旧p(c, d))
    try:
        _rc6, _o6 = _主(诸章, 账0)   # 〔gates11 退回〕用净 0 之局，令其红只出於造局之①
    finally:
        m.check_presence = _旧p
    R.append(('⑥之八·⛔守牙仍红：未见正文 → rc 2；任一检入 bad → rc 2、「不过」（书级体检之格留）',
              _rc5 == 2 and '未见正文' in _o5 and _rc6 == 2 and '不过' in _o6 and '造局之守' in _o6))

    # ⑤真盘（⛔只作注）：本器今日六检皆过
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '书级体检.py')],
                       capture_output=True, text=True)
    R.append(('⑤真盘·书级体检今日六检皆过（⛔此係今日之实，逐日会变，只作注）',
              r.returncode == 0))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·书级体检 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
