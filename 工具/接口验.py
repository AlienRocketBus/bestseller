# -*- coding: utf-8 -*-
"""接口验 —— 圣经之锚所录「N-1之末句逐字」与 N-1 正文之真末句对不对（2026-09-05·机制总审·八路之起草庭审第8条／流程之缝审第1条）

★其红在哪一行：圣经每章立锚「第 N 章必须从N-1之末那一句接写（其末句逐字录於本条之尾，不许凭记忆抄）」——
  ★而验它的只有 开轮六检.check7「锚在不在／多长」；**末句逐字对不对、N 之首拍接没接，无一器读正文**。
  ★★而 N-1 一经回修（如今日 R0059/R0060），其末句可变而锚不变——锚成了一句凭记忆抄的话。
★★它认哪几样，本书同类共几样：只认圣经里「第 N 章必须从(N-1)之末那一句接写」之条中「(N-1)之末句逐字**：**X**」一格，
  与 正文 N-1 白文之末一行（去首尾空白）逐字比；全书有锚之章自 200 余起，逐条可比。
★★★其判：自 306 起（含 306 之锚，即 305 之末句）不合即⛔；旧锚之不合只报（一次说清，归回修专案）。

用法：
    python3 工具/接口验.py            # 印近十锚之对
    python3 工具/接口验.py --静       # 只印判
    python3 工具/接口验.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
圣经 = os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md')
新章起 = 306
CN = {'零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cn2i(t):
    v = 0
    m = re.match(r'([一二三四五六七八九])?百(.*)', t)
    if m:
        v = CN.get(m.group(1), 1) * 100
        t = m.group(2)
    m = re.match(r'([一二三四五六七八九])?十(.*)', t)
    if m:
        v += CN.get(m.group(1), 1) * 10
        t = m.group(2)
    for c in t:
        if c in CN:
            v += CN[c]
    return v


def 章号(p):
    m = re.search(r'第(.+?)章', os.path.basename(p))
    return cn2i(m.group(1)) if m else -1


def 真末句(n):
    fs = [p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if 章号(p) == n]
    if not fs:
        return None
    b = io.open(fs[0], encoding='utf-8').read().split('【本章亮点')[0]
    行 = [x.strip() for x in b.split('\n') if x.strip() and x.strip() != '＊']
    return 行[-1] if 行 else None


def 锚(text):
    """自圣经文取 {N: (N-1, 所录末句)}。"""
    out = {}
    for m in re.finditer(r'第\s*(\d+)\s*章必须从(\d+)之末那一句接写[^\n]*?\*\*(\d+)之末句逐字\*\*：\*\*(.+?)\*\*', text):
        n, prev, prev2, 句 = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4).strip()
        if prev == prev2:
            out[n] = (prev, 句)
    return out


def 净(s):
    return re.sub(r'[\s。！？，、；：「」『』（）《》*]', '', s or '')


def 对(锚表, 真=真末句, 近=10):
    """返回 [(N, prev, 所录, 真末句, 合否)]，只取最近 近 个锚。"""
    rows = []
    for n in sorted(锚表)[-近:]:
        prev, 句 = 锚表[n]
        真句 = 真(prev)
        rows.append((n, prev, 句, 真句, 真句 is not None and 净(句) == 净(真句)))
    return rows


def 报(quiet=False):
    text = io.open(圣经, encoding='utf-8', errors='replace').read()
    rows = 对(锚(text))
    犯 = [r for r in rows if not r[4] and r[0] >= 新章起]
    漂 = [r for r in rows if not r[4] and r[0] < 新章起]
    if not quiet:
        print('════ 接口验 · 圣经之锚所录末句 对 正文真末句（近 %d 锚）════' % len(rows))
        for n, prev, 句, 真句, ok in rows:
            print('  %s 第%d章之锚←%d末句：「%s」%s' % ('✓' if ok else '⛔', n, prev, 句[:30], '' if ok else ('　真末句：「%s」' % (真句 or '（无）')[:30])))
    if 犯:
        print('⛔ 接口验：%s' % '、'.join('第%d章之锚所录%d末句与正文不合' % (r[0], r[1]) for r in 犯))
        return 2
    if 漂 and not quiet:
        print('  ⚠ 旧锚不合 %d 处（只报·归回修专案）：%s' % (len(漂), '、'.join(str(r[0]) for r in 漂)))
    print('  ✓ 接口验：新章之锚逐字合正文末句%s' % ('（旧锚不合 %d 处只报）' % len(漂) if 漂 else ''))
    return 0


def 自测():
    R = []
    demo = ('第 306 章必须从305之末那一句接写（**其末句逐字录於本条之尾，不许凭记忆抄**）；★**305之末句逐字**：**十道白在纸里头，翻过去也在。**；★而306为**暗线**\n'
            '第 307 章必须从306之末那一句接写（**其末句逐字录於本条之尾**）；★**306之末句逐字**：**页边上剩一个字的地方。**；\n')
    a = 锚(demo)
    R.append(('①锚之式读得出（306←305、307←306）', a.get(306) == (305, '十道白在纸里头，翻过去也在。') and a.get(307, (0,))[0] == 306))
    真 = {305: '十道白在纸里头，翻过去也在。', 306: '页边上剩一个字。'}.get
    rows = 对(a, 真=真)
    R.append(('②合者✓、不合者⛔（307之锚所录与真末句不合）', [r[4] for r in rows] == [True, False]))
    R.append(('③净比：只去标点与空白，不去字（「翻过去也在」对「翻过去也在了」须不合）', 净('翻过去也在。') != 净('翻过去也在了。') and 净('十道白在纸里头，翻过去也在。') == 净('十道白在纸里头翻过去也在')))
    # ④磁盘之实：今圣经近十锚逐条对真末句，新章（≥306）之锚须合
    text = io.open(圣经, encoding='utf-8', errors='replace').read()
    rows = 对(锚(text))
    新不合 = [r for r in rows if not r[4] and r[0] >= 新章起]
    R.append(('④磁盘之实·近%d锚，新章之锚不合 %d（须0）；旧锚不合 %d（只报）' % (len(rows), len(新不合), sum(1 for r in rows if not r[4] and r[0] < 新章起)), len(rows) >= 5 and not 新不合))
    # ⑤旧式回灌：check7 只验锚在不在与其长——以一条末句抄错之锚喂之，旧式判✓（此处以「锚在」之判代旧式）
    demo_wrong = demo.replace('十道白在纸里头，翻过去也在。', '十道白在纸里，翻过去也在。')
    a2 = 锚(demo_wrong)
    R.append(('⑤旧式回灌·抄错一字之锚「在」（旧式✓），本器⛔', bool(a2.get(306)) and not 对(a2, 真=真)[0][4]))
    src = io.open(__file__, encoding='utf-8').read()
    R.append(('⑥自陈在册·它认哪几样／旧锚只报', '它认哪几样' in src and '旧锚之不合只报' in src))
    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·接口验 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '有败'))
    return 0 if not bad else 1


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(自测())
    sys.exit(报(quiet='--静' in sys.argv))
