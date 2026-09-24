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
