#!/usr/bin/env python3
"""对账预筛（1008 立·作者令「先确定方法绝对有效，再看效率；token 快用光了」）——零 token 之全书对账前置。

为何立：全书对账（`工具/席/全书对账.js`）若让各席自己 grep、自己读几百行，token 花在「找」上；
而「找」是机器的活。本器把「找」做完：按词 grep 正文全书，凡主案已引之章:行（含区间 263:145—161、
续列 263:145、189）一律滤去，只留**主案没管到的命中行**——席（或总编辑）只需判这几行。

用法：
  python3 工具/对账预筛.py 主案.md 词.json 出目录 [起章-止章] [引+闲屋,床上那]
    第五参（可缺）：只筛「主案引过之章」与「含所列词之章」——把与本题无涉之章剔出去
    词.json：{"组名": ["词1", "词2", ...], ...}
    出目录/预筛_组名.md：未引之命中行（章:行｜词｜原句）；末印各组命中数、已引数、未引数
  python3 工具/对账预筛.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def 章号(f):
    m = re.search(r'第([零〇一二三四五六七八九十百千]+)章', os.path.basename(f))
    if not m:
        return 0
    tot, cur = 0, 0
    for ch in m.group(1):
        if ch in CN:
            cur = CN[ch]
        elif ch == '十':
            tot += (cur or 1) * 10; cur = 0
        elif ch == '百':
            tot += (cur or 1) * 100; cur = 0
        elif ch == '千':
            tot += (cur or 1) * 1000; cur = 0
    return tot + cur


_汉 = r'(?:[一二三四五六七八九两]千)?(?:[一二三四五六七八九两]百)?零?(?:[一二三四五六七八九]?十)?[一二三四五六七八九]?'
_汉章行式 = re.compile(r'(?<![零〇一二三四五六七八九十百千两\d])(%s)(\s*[:：]\s*)(%s)((?:\s*(?:至|—|–|～|~)\s*%s)?)((?:、(?:%s)(?![零〇一二三四五六七八九十百千两天日章行号]|\s*[:：]))*)'
                    % (_汉, _汉, _汉, _汉))


def 汉数(t):
    """汉字之数（四百一十二、一百零三、十八、两千）→ int；空或不成数 → None。"""
    if not t:
        return None
    v = 章号('第%s章' % t.replace('两', '二'))
    return v or None


def 汉章行(s):
    """X84（1105·425 还账）：骨记以汉字写章行（「四百一十二：五十三」「四百一十三：五、七、十一」「三百九十二：一百一十九至一百二十三」）
    → 阿拉伯之「412：53」「413：5、：7、：11」「392：119至123」，冒号原样留；他文⛔动（⛔改骨记·只在器内换）。
    认之界：章行二段俱须成数、前一字⛔汉数；续列之「、N」其後⛔接 天／日／章／行／号（免把「五、七天」之类认作行）、⛔接冒号
    （X91①·434：「四百二十二：四十五、四百二十四：五」之「、四百二十四」係次一引之章、非前引之行——旧器析成 422:45、:424 而误印 390:422）。"""
    def 换(m):
        章, 行 = 汉数(m.group(1)), 汉数(m.group(3))
        if not 章 or not 行:
            return m.group(0)
        区 = m.group(4)
        if 区:
            k = re.match(r'(\s*(?:至|—|–|～|~)\s*)(.*)$', 区)
            v = 汉数(k.group(2))
            区 = k.group(1) + str(v) if v else 区
        # ★X100（450 封前）：续列之「、N」若是章号（N≥300 且远逾前行逾一百五十——今章之白文 ≤二百行）即止续、原样留：
        # 449 骨记「四百零三：三十五、四百四十一、四百四十五之日子」旧析成 403:441、403:445 而印假误
        续 = ''; 前 = max(行, v if 区 and (v := 汉数(re.match(r'\s*(?:至|—|–|～|~)\s*(.*)$', m.group(4)).group(1))) else 0)
        for k, x in enumerate(re.findall(r'、(%s)' % _汉, m.group(5) or '')):
            w = 汉数(x)
            if w and w >= 300 and w > 前 + 150:
                续 += ''.join('、' + y for y in re.findall(r'、(%s)' % _汉, m.group(5))[k:]); break
            续 += ('、：%d' % w) if w else '、' + x
            前 = max(前, w or 0)
        return '%d%s%d%s%s' % (章, m.group(2), 行, 区, 续)
    s = _汉章行式.sub(换, s)
    # 本章之引「（：三十九）」与续前之引「、：七」（冒号前无章）
    return re.sub(r'(?<=[（(、])([:：])(%s)(?![零〇一二三四五六七八九十百千两])' % _汉,
                  lambda x: x.group(1) + str(汉数(x.group(2))) if 汉数(x.group(2)) else x.group(0), s)


def 已引(案文):
    """→ {章: set(行)}：主案所引之章:行，含区间与「、」续列。"""
    引 = {}
    for m in re.finditer(r'(\d{1,3}):(\d{1,4})(?:[—–-](\d{1,4}))?((?:[、，,](?:\d{1,4})(?:[—–-]\d{1,4})?)*)', 案文):
        章 = int(m.group(1))
        段 = [(int(m.group(2)), int(m.group(3) or m.group(2)))]
        for x in re.findall(r'[、，,](\d{1,4})(?:[—–-](\d{1,4}))?', m.group(4) or ''):
            段.append((int(x[0]), int(x[1] or x[0])))
        s = 引.setdefault(章, set())
        for a, b in 段:
            if b < a or b - a > 600:
                b = a
            s.update(range(a, b + 1))
    return 引


def 筛(案, 词组, 出, 起=1, 止=9999, 正文=None, 章限=None):
    正文 = 正文 or os.path.join(ROOT, '正文')
    引 = 已引(open(案, encoding='utf-8').read())
    档 = sorted((章号(f), f) for f in glob.glob(os.path.join(正文, '*.md')))
    if 章限:
        档 = [(n, f) for n, f in 档 if n in 引 or any(w in open(f, encoding='utf-8', errors='replace').read() for w in 章限)]
    os.makedirs(出, exist_ok=True)
    报 = {}
    for 组, 词们 in 词组.items():
        命, 未 = 0, []
        见 = set()
        for n, f in 档:
            if not (起 <= n <= 止):
                continue
            for i, ln in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
                中 = [w for w in 词们 if w in ln]
                if not 中 or (n, i) in 见:
                    continue
                见.add((n, i)); 命 += 1
                if i not in 引.get(n, ()):
                    未.append((n, i, '、'.join(中), ln.strip()))
        with open(os.path.join(出, '预筛_%s.md' % 组), 'w', encoding='utf-8') as w:
            w.write('# 预筛·%s\n\n词：%s｜章 %d—%d｜命中 %d 行，主案已引 %d 行，**未引 %d 行**（下列）\n\n'
                    % (组, '、'.join(词们), 起, 止, 命, 命 - len(未), len(未)))
            for n, i, 中, ln in 未:
                w.write('- %d:%d｜%s｜%s\n' % (n, i, 中, ln[:160]))
        报[组] = (命, 命 - len(未), len(未))
    for 组, (a, b, c) in 报.items():
        print('%s：命中 %d｜已引 %d｜未引 %d' % (组, a, b, c))
    return 报


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '正文'))
        open(os.path.join(t, '正文', '镇冢秘术_第十二章_甲.md'), 'w', encoding='utf-8').write('一\n粮房里\n二\n粮房外\n她在粮房\n')
        open(os.path.join(t, '正文', '镇冢秘术_第三章_乙.md'), 'w', encoding='utf-8').write('粮房\n')
        open(os.path.join(t, '案.md'), 'w', encoding='utf-8').write('改 12:2；又 3:1—1、9\n')
        共 += 1; ok += (章号('镇冢秘术_第一百一十一章_后天.md') == 111 and 章号('第十二章') == 12)
        # ★X84：汉字之章行（420 骨记真句）——冒号原样、续列、区间；三百九十二：一百一十三两根之「两」⛔吞；「五、七天」之续⛔认；无冒号⛔动
        共 += 1; ok += (汉章行('是四百一十二：五十三那一截空') == '是412：53那一截空'
                        and 汉章行('看见的是四百一十三：五、七、十一她两夜') == '看见的是413：5、：7、：11她两夜'
                        and 汉章行('三百九十二：一百一十三两根指头') == '392：113两根指头'
                        and 汉章行('取三百九十：一百零三一句') == '取390：103一句'
                        and 汉章行('立十八：三十三之常') == '立18：33之常'
                        and 汉章行('三百九十二：一百一十九至一百二十三') == '392：119至123'
                        and 汉章行('四百一十三：五、七天') == '413：5、七天'
                        and 汉章行('起手接四百一十八收句与其一百零三行') == '起手接四百一十八收句与其一百零三行'
                        and 汉章行('412:53 与 第一百四十八天') == '412:53 与 第一百四十八天'
                        and 汉章行('（：三十九）「她」') == '（：39）「她」'
                        and 汉章行('四百二十二：四十五、四百二十四：五') == '422：45、424：5')   # X91①：「、N：M」係次一引⛔吞作前引之行
        引 = 已引('263:145—161、189、237—357 与 12:4')
        共 += 1; ok += (150 in 引[263] and 189 in 引[263] and 300 in 引[263] and 200 not in 引[263] and 引[12] == {4})
        报 = 筛(os.path.join(t, '案.md'), {'粮': ['粮房']}, os.path.join(t, '出'), 正文=os.path.join(t, '正文'))
        共 += 1; ok += (报['粮'] == (4, 2, 2))                      # 12:4、12:5 未引
        报 = 筛(os.path.join(t, '案.md'), {'粮': ['粮房']}, os.path.join(t, '出'), 起=10, 止=20, 正文=os.path.join(t, '正文'))
        共 += 1; ok += (报['粮'] == (3, 1, 2))                      # 章界
        报 = 筛(os.path.join(t, '案.md'), {'粮': ['粮房']}, os.path.join(t, '出'), 正文=os.path.join(t, '正文'), 章限=['无此词'])
        共 += 1; ok += (报['粮'] == (4, 2, 2))                      # 章限：引过之章留
    finally:
        shutil.rmtree(t)
    print('对账预筛·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) not in (3, 4, 5):
        print(__doc__); sys.exit(2)
    起, 止 = 1, 9999
    if len(a) >= 4:
        起, 止 = (int(x) for x in a[3].split('-'))
    章限 = a[4].split('+', 1)[1].split(',') if len(a) == 5 else None
    筛(a[0], json.load(open(a[1], encoding='utf-8')), a[2], 起, 止, 章限=章限)
