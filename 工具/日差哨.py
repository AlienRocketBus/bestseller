# -*- coding: utf-8 -*-
"""日差哨 —— 二线之日历对不对得上（2026-09-05·机制总审·八路之跨章连贯审第1条，本坐上磁盘坐实後立）

★其红在哪一行（上磁盘核，非设想）：
  · **第201章**：「而她不知道的是，这一日山那头也有一个人在数：他记的是第四十四天」——**她第四十四页、他第四十四天，同一日**。
  · **第272章（主线·第九十三天）**：他在水边遇见一个女人，她怀里托出一本比他的薄、比他的窄的册子，看他本子上的行数。
  · **第273章（暗线·第八十九日）**：「她走了三天……三天前那个人，她不知道他叫什么」「三天前有一个人隔着五步看她这一页」
    ——**同一次照面：他那本记第九十三天，她那本记第八十六日。差七日。**
  · 而全书无一处写她漏记过一天（`grep 少了几天|漏了几天|不知道躺了` 皆无）。
★★其形：**暗线每章进一日，主线每章进一天；而235至286之间主线之章多於暗线之章**——
  日差自232之0（231主71／232暗71）一路涨到286之6（285主100／286暗94），此後二线逐章交替，日差钉在6。
★★★它认哪几样，本书同类共几样：只认**章首四百字内之「第N天／第N日」**；线之判用与开镜庭同一尺（「我」之密度<3/千字为暗线）。
  ★暗线201／211／217／268／277首拍无日之标，印「?」不判（宁不判，不许拿邻章去补）。
★★★★其判：**日差本身不判**——**2026-09-05 作者授全权，canon 已裁**（圣经§七·2「二线之历」）：**她之「日」係册子之页，不写之日不翻页**，
  故差係两本账各自之算法，非错；**判的是「日差有没有变」**——自 306 起，凡暗线之章其日差与上一暗线之章不同即⛔，
  **除该章开镜卡写明「页差改为N·其由」**（即正文里她没翻页／留了空页）；旧章之漂只报，一次说清，不追。

用法：
    python3 工具/日差哨.py            # 印196章以来之表与判
    python3 工具/日差哨.py --静       # 只印判（供全测／一坐）
    python3 工具/日差哨.py --自测     # 负测
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
起 = 196          # 二线并行之起（201前後）
新章起 = 306      # 自此起日差之变即⛔（旧章只报）
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


def 线与日(body):
    """返回 (线, 日)。线：主／暗（「我」密度<3/千字为暗，与 第零轮开镜庭.is_dark 同尺）；日：章首四百字内之第N天／第N日，无则 None。"""
    净 = len(re.sub(r'\s', '', body)) or 1
    线 = '暗' if body.count('我') / 净 * 1000 < 3 else '主'
    m = re.search(r'第([零〇一二三四五六七八九十百]+)([天日])', body[:400])
    return 线, (cn2i(m.group(1)) if m else None)


def 表(章库):
    """章库：[(n, body)] 已排序。返回逐章 dict 列表，暗线之章带「日差」与「变」。"""
    out = []
    上主 = None
    上暗差 = None
    for n, body in 章库:
        线, 日 = 线与日(body)
        row = {'章': n, '线': 线, '日': 日, '日差': None, '变': False}
        if 线 == '主':
            if 日 is not None:
                上主 = 日
        else:
            if 日 is not None and 上主 is not None:
                row['日差'] = 上主 - 日
                if 上暗差 is not None and row['日差'] != 上暗差:
                    row['变'] = True
                上暗差 = row['日差']
        out.append(row)
    return out


def 读库():
    fs = sorted(glob.glob(os.path.join(ROOT, '正文', '*.md')), key=章号)
    库 = []
    for p in fs:
        n = 章号(p)
        if n < 起:
            continue
        库.append((n, io.open(p, encoding='utf-8').read().split('【本章亮点】')[0]))
    return 库


def 判(rows):
    """返回 (犯, 漂)。犯：新章（≥新章起）之日差有变者；漂：旧章之日差有变者（只报）。"""
    犯 = []
    for r in rows:
        if r['变'] and r['章'] >= 新章起:
            # ★canon 之出口：该章开镜卡写明「页差改为N·其由」且 N 即本章之差，方许变
            卡 = os.path.join(ROOT, '版本', '第%d章' % r['章'], '_开镜卡.md')
            允 = False
            if os.path.exists(卡):
                m = re.search(r'页差改为\s*(\d+)\s*·', io.open(卡, encoding='utf-8').read())
                允 = bool(m) and int(m.group(1)) == r['日差']
            if not 允:
                犯.append(r)
    漂 = [r for r in rows if r['变'] and r['章'] < 新章起]
    return 犯, 漂


def 报(quiet=False):
    rows = 表(读库())
    犯, 漂 = 判(rows)
    暗 = [r for r in rows if r['线'] == '暗']
    末差 = next((r['日差'] for r in reversed(暗) if r['日差'] is not None), None)
    if not quiet:
        print('════ 日差哨 · 二线之日历（自第%d章起）════' % 起)
        print('  【其律】暗线之日差＝其前一主线章之天 − 本章之日；哨只判「差有没有变」，差本身归 canon（作者点头）。')
        print('  ' + ' '.join('%d%s%s%s' % (r['章'], r['线'], r['日'] if r['日'] is not None else '?', (r['线'] == '暗' and r['日差'] is not None) and ('(差%d%s)' % (r['日差'], '★' if r['变'] else '')) or '') for r in rows))
        print('  ── 旧章之漂（只报·一次说清）──')
        if 漂:
            print('  ⚠ 日差有变之暗线章 %d 处：%s' % (len(漂), '、'.join('%d(→%d)' % (r['章'], r['日差']) for r in 漂)))
            print('     ★其锚：201章「他记的是第四十四天」与她第四十四页同一日（差0）；272主93天／273暗89日之照面係她三天前（86），差7。')
            print('     ★★此係 canon 之事（她漏记了几日，还是二线本就两本历），须作者点头，哨不落刀。')
        else:
            print('  ✓ 旧章无日差之变。')
        print('  ── 新章（≥%d）──' % 新章起)
    if 犯:
        if not quiet:
            for r in 犯:
                print('  ⛔ 第%d章（暗线·第%s日）日差 %d，与上一暗线章不同——二线之历又漂了一日。' % (r['章'], r['日'], r['日差']))
        else:
            print('⛔ 日差哨：%s' % '、'.join('第%d章日差→%d' % (r['章'], r['日差']) for r in 犯))
        return 2
    print('  ✓ 日差哨：新章无日差之变%s' % ('（今差 %d）' % 末差 if 末差 is not None else ''))
    return 0


def 自测():
    R = []
    def mk(n, 线, 日):
        body = ('第%s%s。\n' % (日, '天' if 线 == '主' else '日')) if 日 else '天亮。\n'
        body += ('我走。我看。我数。' * 30) if 线 == '主' else ('她走。她看。她数。' * 30)
        return (n, body)
    # ①稳：主天逐章加一，暗日逐章加一，差恒 → 无犯无漂
    库 = [mk(300, '主', '一百'), mk(301, '暗', '九十四'), mk(302, '主', '一百零一'), mk(303, '暗', '九十五'), mk(306, '主', '一百零二'), mk(307, '暗', '九十六')]
    犯, 漂 = 判(表(库))
    R.append(('①差恒（6）→ 无犯无漂', (犯, 漂) == ([], [])))
    # ②新章之漂 → 犯（307暗96而其前主已102，差6；改307为95，差7）
    库2 = 库[:-1] + [mk(307, '暗', '九十五')]
    犯2, 漂2 = 判(表(库2))
    R.append(('②新章（307）日差 6→7 → ⛔犯', [r['章'] for r in 犯2] == [307] and 漂2 == []))
    # ③旧章之漂 → 只报不犯（旧式回灌：改前无此哨，磁盘上 235—286 之漂无一处出过声）
    库3 = [mk(231, '主', '七十一'), mk(232, '暗', '七十一'), mk(234, '主', '七十三'), mk(235, '暗', '七十二')]
    犯3, 漂3 = 判(表(库3))
    R.append(('③旧章（235）日差 0→1 → 只入漂不入犯', 犯3 == [] and [r['章'] for r in 漂3] == [235]))
    # ④无日之标者不判（201／211／217之形）
    库4 = [mk(300, '主', '一百'), mk(301, '暗', None), mk(302, '主', '一百零一'), mk(303, '暗', '九十五')]
    犯4, 漂4 = 判(表(库4))
    R.append(('④暗线首拍无日之标 → 印?不判，亦不搅其後之差', (犯4, 漂4) == ([], []) and 表(库4)[1]['日'] is None))
    # ⑤磁盘之实：今日之表须印出旧章之漂≥1处而新章零犯（306尚未写）
    rows = 表(读库())
    犯5, 漂5 = 判(rows)
    R.append(('⑤磁盘之实·旧章之漂 %d 处（须≥1·235至286之漂是真的）、新章犯 %d（须0）' % (len(漂5), len(犯5)), len(漂5) >= 1 and len(犯5) == 0))
    # ⑥线之尺与开镜庭同（「我」密度<3/千字为暗）
    R.append(('⑥线之尺：我密度<3/千字为暗', 线与日('她走。' * 50)[0] == '暗' and 线与日('我走。' * 50)[0] == '主'))
    # ⑦自陈在册
    src = io.open(__file__, encoding='utf-8').read()
    R.append(('⑦自陈在册·它认哪几样／差归canon不落刀／旧章只报', '它认哪几样' in src and '须作者点头' in src and '旧章之漂只报' in src))
    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·日差哨 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '有败'))
    return 0 if not bad else 1


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(自测())
    sys.exit(报(quiet='--静' in sys.argv))
