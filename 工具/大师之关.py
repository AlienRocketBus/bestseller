#!/usr/bin/env python3
"""大师之关（0926·作者令立）：三执笔之构思、行家之审、创作记录、自我进化——**封了版的章，缺一样即红**。

⛔其立之由：作者令「必须得执行起来，别弄出来不执行」。席令里写了不等於席照做了；
  故凡自 `自章` 起封版之章，逐章亲查盘上之档，缺一样即红，推闸据此拦停。

查五样（第 N 章）：
  ①构思：版本/第N章/起草_甲／乙／丙_构思.md 三份俱在，各 ≥400 字，且各有「进化账所避」一行；
  ②行家评：版本/第N章/_行家评.md 在，含「小说家」「总编辑」二节与「## 合稿逐条回话」；
  ③创作记录：版本/第N章/_创作记录.md 在，一至六节俱全（「一、」…「六、」）；
  ④进化：设定/大师进化账.md 里有「[第N章]」之条；
  ⑤封版：以 版本/第N章/_十一轮.json 在为「已封」之据——未封之章不查（正在写的不拦）。

用法：python3 工具/大师之关.py          # 全书（自 自章 起）
      python3 工具/大师之关.py 377      # 只查一章
      python3 工具/大师之关.py --自测
      python3 工具/大师之关.py --标无稿 N 宽 稿号[,稿号]   # ★1118 写者（造章.js N≥464 选之先跑自调·零 token）：
            执笔被平台安全之检拦（造章.js 安全拒）而盘上缺档 → 於其构思书「无稿：…拦」一行；只印稿号（⛔泄执笔之名·蒙名）。
            ⛔代「缺档」：拦而无稿 照旧三条俱验（明标＋_创作记录.md 载缺档＋起草_稿 ≥3）——本器只书其一。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, re, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
自章 = 377   # 大师之制自 377 起生效；376 及以前用旧制，不追究


def 拦而无稿(d, t):
    """★1117：构思首有「无稿：…拦…」一行，且 _创作记录.md 载「缺档」、盘上起草_稿 ≥3 → 此席不查（席被拦非席之懒）；缺一即照查。"""
    import glob as _g
    if not re.search(r'^无稿[：:][^\n]*拦', t, re.M):
        return False
    记 = os.path.join(d, '_创作记录.md')
    return (os.path.exists(记) and '缺档' in open(记, encoding='utf-8', errors='replace').read()
            and len(_g.glob(os.path.join(d, '起草_稿*.md'))) >= 3)


干 = '甲乙丙丁戊己庚'                                          # 造章.js 功底之序
稿号们 = ('稿一', '稿二', '稿三', '稿四', '稿五', '稿六', '稿七')   # 造章.js 稿号


def 号之席(n, 宽, 号):
    """造章.js 蒙号(名)＝稿号[(干序+N) % 宽] 之逆：稿号 → 执笔之名（记料.py _胜嫁之构思 同式；负测_造章令 以真渲之令对之）。"""
    k = 稿号们.index(号)
    if not (3 <= 宽 <= 7 and k < 宽):
        raise ValueError('稿号 %s 不在宽 %d 之内' % (号, 宽))
    return 干[(k - n) % 宽]


def 标无稿(n, 宽, 号, root=ROOT):
    """★1118（a9e5cc5ee 根病②：459 丙、461 乙俱手补）：执笔被平台安全之检拦而盘上缺档者，於其构思书「无稿：…拦」一行。→ (名, 判)。
    其据：造章.js 之 安全拒（拒因含 safeguards／AUP／usage policy·X79）——只由 造章.js 选之先跑传入（⛔模型手传）。
    四条俱合方书（缺一⛔书、照红）：①稿档不在（选之先跑印「缺档」之同一判） ②起草_稿*.md ≥3 ③其构思今照 查() 即红（满者⛔书） ④未书过（⛔重书）；
    只书 甲乙丙（大师之关所查）。⛔代 _创作记录.md 之「缺档」——拦而无稿 照旧三条俱验，本器只书其一。"""
    import glob as _g
    名 = 号之席(n, 宽, 号)
    if 名 not in '甲乙丙':
        return 名, '⛔非大师之关所查之席——⛔书'
    d = os.path.join(root, '版本', '第%d章' % n)
    if os.path.exists(os.path.join(d, '起草_%s.md' % 号)):
        return 名, '⛔稿档在——非无稿，⛔书'
    if len(_g.glob(os.path.join(d, '起草_稿*.md'))) < 3:
        return 名, '⛔起草_稿 不足三——⛔书'
    f = os.path.join(d, '起草_%s_构思.md' % 名)
    t = open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else None
    if t is not None and re.search(r'^无稿[：:][^\n]*拦', t, re.M):
        return 名, '已书（⛔重书）'
    if not any(x.startswith('构思·%s ' % 名) for x in 查(n, root)):
        return 名, '⛔构思照查已全——⛔书'
    行 = '无稿：执笔被平台安全之检拦、未交（造章.js 拒因·安全之检·X79；%s 盘上缺档；大师之关.py --标无稿 自书）\n' % 号
    with open(f, 'a', encoding='utf-8') as o:
        o.write(('# 执笔·%s之构思（无稿）\n' % 名 if t is None else ('' if t.endswith('\n') or not t else '\n')) + 行)
    return 名, '已书'


def 查(n, root=ROOT):
    d = os.path.join(root, '版本', '第%d章' % n)
    缺 = []
    for 名 in '甲乙丙':
        f = os.path.join(d, '起草_%s_构思.md' % 名)
        if not os.path.exists(f):
            缺.append('构思·%s 不在' % 名); continue
        t = open(f, encoding='utf-8', errors='replace').read()
        if 拦而无稿(d, t):                    # ★1117（459 丙·X111）：执笔被平台之检拦、明标无稿而稿已足——⛔假红
            continue
        if len(re.sub(r'\s', '', t)) < 400:
            缺.append('构思·%s 不足 400 字' % 名)
        if '进化账所避' not in t:
            缺.append('构思·%s 无「进化账所避」' % 名)
        # 0927 作者令·完美主义（设定/反面教材.md）：自 380 章起构思须有「满分之问」
        if n >= 380 and '满分之问' not in t:
            缺.append('构思·%s 无「满分之问」（反面教材·一次到位）' % 名)
    f = os.path.join(d, '_行家评.md')
    if not os.path.exists(f):
        缺.append('_行家评.md 不在')
    else:
        t = open(f, encoding='utf-8', errors='replace').read()
        for k in ('小说家', '总编辑', '## 合稿逐条回话'):
            if k not in t:
                缺.append('_行家评.md 无「%s」' % k)
        # 0927 作者令·立得住之律（设定/立得住之律.md）：自 380 章起，行家须逐条过「因立不立得住」
        if n >= 380 and '## 立得住' not in t:
            缺.append('_行家评.md 无「## 立得住」（立得住之律）')
    f = os.path.join(d, '_创作记录.md')
    if not os.path.exists(f):
        缺.append('_创作记录.md 不在')
    else:
        t = open(f, encoding='utf-8', errors='replace').read()
        for k in '一二三四五六':
            if k + '、' not in t:
                缺.append('_创作记录.md 缺第%s节' % k)
    f = os.path.join(root, '设定', '大师进化账.md')
    t = open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else ''
    if '[第%d章]' % n not in t:
        缺.append('进化账无「[第%d章]」之条' % n)
    return 缺


def 已封诸章(root=ROOT):
    out = []
    vd = os.path.join(root, '版本')
    if not os.path.isdir(vd):
        return out
    for x in os.listdir(vd):
        m = re.match(r'第(\d+)章$', x)
        if m and int(m.group(1)) >= 自章 and os.path.exists(os.path.join(vd, x, '_十一轮.json')):
            out.append(int(m.group(1)))
    return sorted(out)


def 全(root=ROOT):
    红 = {}
    for n in 已封诸章(root):
        缺 = 查(n, root)
        if 缺:
            红[n] = 缺
    return 红


def 自测():
    ok = 0; 共 = 0
    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, '设定'))
        d = os.path.join(tmp, '版本', '第400章'); os.makedirs(d)
        open(os.path.join(tmp, '设定', '大师进化账.md'), 'w').write('# 账\n')
        # ①未封者不查
        共 += 1; ok += (全(tmp) == {})
        # ②已封而一样也没有 → 红
        open(os.path.join(d, '_十一轮.json'), 'w').write('{}')
        共 += 1; r = 全(tmp); ok += (400 in r and len(r[400]) >= 5)
        # ③五样俱全 → 绿
        for 名 in '甲乙丙':
            open(os.path.join(d, '起草_%s_构思.md' % 名), 'w').write('进化账所避：某条\n满分之问：三路\n' + '构' * 420)
        open(os.path.join(d, '_行家评.md'), 'w').write('【小说家】…\n【总编辑】…\n## 立得住\n无\n## 合稿逐条回话\n1. 改\n')
        open(os.path.join(d, '_创作记录.md'), 'w').write(''.join(k + '、x\n' for k in '一二三四五六'))
        open(os.path.join(tmp, '设定', '大师进化账.md'), 'a').write('- [第400章] 教训｜出处｜往后\n')
        共 += 1; ok += (全(tmp) == {})
        # ④构思缺「进化账所避」 → 红（不许只凑字数）
        open(os.path.join(d, '起草_乙_构思.md'), 'w').write('构' * 500)
        共 += 1; r = 全(tmp); ok += (400 in r and any('进化账所避' in x for x in r[400]))
        # ⑤行家评无合稿回话 → 红（行家之改法须逐条办）
        open(os.path.join(d, '起草_乙_构思.md'), 'w').write('进化账所避：某条\n满分之问：三路\n' + '构' * 420)
        open(os.path.join(d, '_行家评.md'), 'w').write('【小说家】…\n【总编辑】…\n')
        共 += 1; r = 全(tmp); ok += (400 in r and any('合稿逐条回话' in x for x in r[400]))
        # ⑥之一构思无「满分之问」 → 红
        open(os.path.join(d, '_行家评.md'), 'w').write('【小说家】…\n【总编辑】…\n## 立得住\n无\n## 合稿逐条回话\n1. 改\n')
        open(os.path.join(d, '起草_丙_构思.md'), 'w').write('进化账所避：某条\n' + '构' * 420)
        共 += 1; r = 全(tmp); ok += (400 in r and any('满分之问' in x for x in r[400]))
        # ⑥之二★1117：丙被拦而明标无稿——创作记录有缺档且稿 ≥3 → 不查；稿不足 → 照红；无标 → 照红
        open(os.path.join(d, '起草_丙_构思.md'), 'w').write('# 丙\n无稿：执笔被平台安全之检拦\n')
        共 += 1; ok += any('构思·丙' in x for x in 全(tmp).get(400, []))          # 记无缺档、无稿 → 照红
        open(os.path.join(d, '_创作记录.md'), 'a').write('稿五（缺档）\n')
        for k in '一二三':
            open(os.path.join(d, '起草_稿%s.md' % k), 'w').write('稿')
        共 += 1; ok += not any('构思·丙' in x for x in 全(tmp).get(400, []))      # 俱足 → 不查
        os.remove(os.path.join(d, '起草_稿三.md'))
        共 += 1; ok += any('构思·丙' in x for x in 全(tmp).get(400, []))          # 稿只二 → 照红
        open(os.path.join(d, '起草_丙_构思.md'), 'w').write('进化账所避：某条\n满分之问：三路\n' + '构' * 420)
        # ⑥无「立得住」 → 红
        open(os.path.join(d, '_行家评.md'), 'w').write('【小说家】…\n【总编辑】…\n## 合稿逐条回话\n1. 改\n')
        共 += 1; r = 全(tmp); ok += (400 in r and any('立得住' in x for x in r[400]))
        # ⑥自章之前者不查
        d2 = os.path.join(tmp, '版本', '第376章'); os.makedirs(d2)
        open(os.path.join(d2, '_十一轮.json'), 'w').write('{}')
        共 += 1; ok += (376 not in 全(tmp))
        # ⑦★1118 写者（标无稿·造章.js N≥464 选之先跑自调）——稿号之逆钉真例：461 稿三＝乙、459 稿二＝丙／稿五＝甲、464 稿一＝乙、宽三之 464 稿二＝丙
        共 += 1; ok += ([号之席(461, 5, '稿三'), 号之席(459, 5, '稿二'), 号之席(459, 5, '稿五'), 号之席(464, 5, '稿一'), 号之席(464, 3, '稿二')]
                       == ['乙', '丙', '甲', '乙', '丙'])
        d7 = os.path.join(tmp, '版本', '第461章'); os.makedirs(d7)
        open(os.path.join(d7, '_十一轮.json'), 'w').write('{}')
        for 名 in '甲丙':
            open(os.path.join(d7, '起草_%s_构思.md' % 名), 'w').write('进化账所避：某条\n满分之问：三路\n' + '构' * 420)
        题 = '# 执笔·乙之构思（咬合路）\n'
        open(os.path.join(d7, '起草_乙_构思.md'), 'w').write(题)                       # 461 之真形：只一题行（38 字节）
        open(os.path.join(d7, '_行家评.md'), 'w').write('【小说家】…\n【总编辑】…\n## 立得住\n无\n## 合稿逐条回话\n1. 改\n')
        open(os.path.join(d7, '_创作记录.md'), 'w').write(''.join(k + '、x\n' for k in '一二三四五六'))
        open(os.path.join(tmp, '设定', '大师进化账.md'), 'a').write('- [第461章] 教训｜出处｜往后\n')
        for k in '一二四':
            open(os.path.join(d7, '起草_稿%s.md' % k), 'w').write('稿')
        乙构 = lambda: open(os.path.join(d7, '起草_乙_构思.md'), encoding='utf-8').read()
        红乙 = lambda: any('构思·乙' in x for x in 全(tmp).get(461, []))
        # ⑦之二 稿档在（稿三在盘）→ ⛔书、构思一字不动
        open(os.path.join(d7, '起草_稿三.md'), 'w').write('稿')
        共 += 1; ok += (标无稿(461, 5, '稿三', tmp)[1].startswith('⛔稿档在') and 乙构() == 题)
        os.remove(os.path.join(d7, '起草_稿三.md'))
        # ⑦之三 稿不足三（只二）→ ⛔书
        os.remove(os.path.join(d7, '起草_稿四.md'))
        共 += 1; ok += (标无稿(461, 5, '稿三', tmp)[1].startswith('⛔起草_稿 不足三') and 乙构() == 题)
        open(os.path.join(d7, '起草_稿四.md'), 'w').write('稿')
        # ⑦之四 四条俱合 → 书；而创作记录未载缺档者照红（写者⛔代缺档）；载之即绿；再跑⛔重书
        共 += 1; ok += (标无稿(461, 5, '稿三', tmp) == ('乙', '已书') and 红乙())
        open(os.path.join(d7, '_创作记录.md'), 'a').write('| 稿三 | 乙 | 咬合 | 构思档只一题行，稿缺档 |\n')
        共 += 1; ok += (not 红乙() and 标无稿(461, 5, '稿三', tmp)[1].startswith('已书（') and 乙构().count('无稿：') == 1)
        # ⑦之五 构思已全者 → ⛔书（满者照内容查，⛔以标免之）；构思不在者 → 立档书之（造式 ② 之「在」亦合）
        open(os.path.join(d7, '起草_乙_构思.md'), 'w').write('进化账所避：某条\n满分之问：三路\n' + '构' * 420)
        共 += 1; ok += (标无稿(461, 5, '稿三', tmp)[1].startswith('⛔构思照查已全') and '无稿' not in 乙构())
        os.remove(os.path.join(d7, '起草_乙_构思.md'))
        共 += 1; ok += (红乙() and 标无稿(461, 5, '稿三', tmp) == ('乙', '已书') and 乙构().startswith('# 执笔·乙之构思') and not 红乙())
        # ⑦之六 稿号映於 丁（461 稿五＝丁·创作记录「稿五（丁·翻个儿）」）→ ⛔书（只 甲乙丙）
        共 += 1; ok += (号之席(461, 5, '稿五') == '丁' and 标无稿(461, 5, '稿五', tmp)[1].startswith('⛔非大师之关所查')
                       and not os.path.exists(os.path.join(d7, '起草_丁_构思.md')))
    finally:
        shutil.rmtree(tmp)
    print('大师之关·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--自测':
        sys.exit(0 if 自测() else 1)
    if a and a[0] == '--标无稿':                 # ★1118：造章.js（N≥464）选之先跑自调——只印稿号（蒙名）、恒返 0（⛔断选之先跑）
        for 号 in a[3].split(','):
            try:
                print('· 无稿之标·%s：%s' % (号, 标无稿(int(a[1]), int(a[2]), 号)[1]))
            except Exception as e:
                print('· 无稿之标·%s：⛔判不出（%s）' % (号, e))
        sys.exit(0)
    if a:
        缺 = 查(int(a[0]))
        print(('⛔ 大师之关·第%s章：' % a[0] + '｜'.join(缺)) if 缺 else '✓ 大师之关·第%s章：五样俱全' % a[0])
        sys.exit(1 if 缺 else 0)
    红 = 全()
    if 红:
        for n, 缺 in 红.items():
            print('⛔ 大师之关·第%d章：%s' % (n, '｜'.join(缺)))
        sys.exit(1)
    print('✓ 大师之关：自第%d章起已封诸章（%d 章），构思／行家评／创作记录／进化俱全' % (自章, len(已封诸章())))
