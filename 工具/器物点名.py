# -*- coding: utf-8 -*-
"""器物点名（2026-09-03·295第6轮记欠、295第7轮之坐立）

★立此器之由（其红在哪一行，上磁盘核过）：
  ★令§三③写死「**器物须有来去，入、用、出，缺一即伤**」，并指名「**其主人是第6轮·资源庭**」；
  ★★而 `工具/一坐.py::逐轮之器` 只列 4、5、7、8、9、12 六轮——**第6轮空着**；
  ★★★故295第6轮实跑之时，一坐印「下一轮：第6轮」而**未印一件器**，
    那一轮之数只得自手打之 grep（见 版本/第295章/_轮记.md 第6轮·甲）。
  ★★★★**一条有主人的法，主人手上没有尺**——记为欠-295A，今兑。

★★而其判据（令§六④：写下判据的同时，写一行「它认哪几样，本书同类共几样」）：
  · **它认哪几样**：**只认本章自报之器物册** `版本/第N章/_器物.md`，逐器三格（入／用／出），
    **每一格须给一个拍号，且那一拍的白文里须真有这件器物之名**；
  · **本书同类共几样**：另有一路「未报之疑」，取本书手上之器之全集
    （下之 手器全集，九样；其取法：逐样 grep 全书正文，见档尾之数），
    **凡本章白文里占三拍以上而册上没有的，印⚠**——**它只提醒，不判**（器物之名千变，闭集判不了它）。

★★★其红得起来吗（令§十四③）：`工具/负测_器物点名.py` 逐条回灌——
  删一格「出」即红｜拍号指到一个没有该器物之名的拍即红｜册不在即红｜**三格之拍号倒了即红**。

★★★★★2026-09-04·299第6轮新立二事（其由见 版本/第299章/_器物.md 之二节）：
  ★**其一·序之验（判）**：**入≤用≤出，且入<出**——**令§三③「器物须有来去」，「来去」是有方向的**；
    ★★旧闸只验「那一格有没有拍号」「那一拍有没有其名」，**故一份写作「入=110｜用=50｜出=8」的册照绿**；
    ★★★二九八之册自记「当场逮出四格拍号错位」——**那四格逮得着只因为错到了没有其名的拍上**；
      **错到一个有其名的拍上，旧闸一个也逮不着。**
    ★★★★旧式回灌：295／296／297／298 四章之册共二十一行，逐行验其序，**二十一行全过**（故此验不冤旧章）。
  ★**其二·身上的尺之疑（只提醒，不判·开集）**：**上之「未报之疑」认的是一个写死的九样闭集**，
    ★★而299手上最要紧的那一样是「指甲」（占6拍），**九样里没有它，故那一章跑完旧闸⚠一条也不印**；
    ★★★**一个闭集只逮得住它自己列过的东西**；故今另开一路**由白文之型认之**（拿X比／拿X量／用X比／用X量／数（了）自己的X），
      **凡所认之X既不在册上，又不在册之全文里被「」提过一回，即印⚠**——**它不判，只逼这一章当场说一句话。**
"""
import io, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ★手器全集（九样）——**本书主角手上真正过过的器物之名**，其数见档尾。
#   ★★此集只作「未报之疑」之用，不作判据：**判据永远是本章自报之册。**
手器全集 = ['本子', '笔', '绳', '灯', '刀', '针', '布', '架子', '鞋']

# ★★身上的尺之型（2026-09-04·299第6轮立）——**开集**：它不列名字，只认白文之型。
#   ★其所以不列名字：**闭集只逮得住它自己列过的东西**（见档头★★★★★之二）。
尺之型 = [
    r'拿([一-鿿]{1,2}?)(?:比|量)',
    r'用([一-鿿]{1,2}?)(?:比|量)',
    r'数(?:了)?自己的([一-鿿]{1,2})',
]


def 正文(n):
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if not m:
            continue
        from importlib.util import spec_from_file_location, module_from_spec
        sp = spec_from_file_location('_yz', os.path.join(ROOT, '工具', '一坐.py'))
        mo = module_from_spec(sp)
        sp.loader.exec_module(mo)
        if mo.cn2i(m.group(1)) != n:
            continue
        t = io.open(f, encoding='utf-8').read().split('【本章亮点】')[0]
        return re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)
    return None


def 分拍(b):
    return [re.sub(r'\s', '', p) for p in b.split('＊') if p.strip()]


def 读册(n):
    """册之式（每器一行，四格以｜分）：  器物名｜入=拍号｜用=拍号｜出=拍号
    ★「出」一格若係有意留的开口，写 `出=拍号(开口:其由)`——**仍须给拍号**。"""
    p = os.path.join(ROOT, '版本', '第%d章' % n, '_器物.md')
    if not os.path.exists(p):
        return None, p, ''
    rows = []
    全文 = io.open(p, encoding='utf-8').read()
    for line in 全文.split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('★'):
            continue
        parts = [x.strip() for x in line.split('｜')]
        # ★★★★★不许以「格不够就跳过」处置一行：**那正是本闸要逮的伤**。
        #   ★2026-09-03·负测②当场逮出：删一格「出」之後此行只三格，
        #     旧写法 `len(parts) < 4: continue` 把它整行丢了，於是闸绿。
        #   ★★一道闸把「缺了一格的行」当成「没有这一行」，它就永远逮不着缺格。
        if len(parts) < 2:
            continue
        d = {'名': parts[0]}
        for x in parts[1:]:
            m = re.match(r'(入|用|出)\s*=\s*(\d+)', x)
            if m:
                d[m.group(1)] = int(m.group(2))
        rows.append(d)
    return rows, p, 全文


def 跑(n):
    b = 正文(n)
    if b is None:
        print('⛔ 取不到第%d章正文' % n)
        return 2
    bs = 分拍(b)
    rows, p, 册文 = 读册(n)
    print('████ 器物点名 · 第%d章 ████' % n)
    print('  ★其判据：本章自报之器物册（%s）；★★另一路只提醒，不判。' % os.path.relpath(p, ROOT))
    print('  ★★★全章 %d 拍。' % len(bs))
    坏 = []
    if rows is None:
        print('  ⛔ 器物册不在：%s' % os.path.relpath(p, ROOT))
        print('     ★其式：器物名｜入=拍号｜用=拍号｜出=拍号（每器一行）')
        return 2
    if not rows:
        坏.append('★器物册在而一行也没有——一章之内一件器物也不过手，须当场答其由')
    print('  ── 逐件点名 ──')
    for d in rows:
        名 = d['名']
        line = '   %-8s' % 名
        for g in ('入', '用', '出'):
            if g not in d:
                line += ' %s=⛔缺' % g
                坏.append('★%s·缺「%s」——令§三③：入、用、出，缺一即伤' % (名, g))
                continue
            i = d[g]
            if not (1 <= i <= len(bs)):
                line += ' %s=⛔拍%d不在' % (g, i)
                坏.append('★%s·「%s」指拍%d，而全章只 %d 拍' % (名, g, i, len(bs)))
            elif 名 not in bs[i - 1]:
                line += ' %s=⛔拍%d无其名' % (g, i)
                坏.append('★%s·「%s」指拍%d，而那一拍的白文里没有「%s」三字——'
                          '拍号是抄的，不是数的' % (名, g, i, 名))
            else:
                line += ' %s=拍%-4d' % (g, i)
        # ★序之验（2026-09-04立）：入≤用≤出，且入<出——**「来去」是有方向的**。
        序 = [d[g] for g in ('入', '用', '出') if isinstance(d.get(g), int)]
        if len(序) == 3:
            # ★先验「入出同拍」再验「序倒」：**同拍是更准的一句话**，
            #   若先验序，一份「入=6｜用=91｜出=6」之册会被判作「倒」，而它真正的病是没动。
            if 序[0] == 序[2]:
                line += ' ⛔入出同拍'
                坏.append('★%s·「入」与「出」同指拍%d——'
                          '一件东西在同一拍上又进来又出去，那不是来去，是没动'
                          % (名, 序[0]))
            elif not (序[0] <= 序[1] <= 序[2]):
                line += ' ⛔序倒'
                坏.append('★%s·三格之拍号倒了（入=%d｜用=%d｜出=%d）——'
                          '令§三③「器物须有来去」，来去是有方向的：'
                          '一件东西不能先出后入' % (名, 序[0], 序[1], 序[2]))
        print(line)
    # ── 未报之疑（只提醒）──
    报了 = {d['名'] for d in rows}
    疑 = []
    for k in 手器全集:
        if k in 报了:
            continue
        c = sum(1 for x in bs if k in x)
        if c >= 3:
            疑.append((k, c))
    if 疑:
        print('  ── 未报之疑（只提醒，不判）──')
        for k, c in 疑:
            print('   ⚠「%s」占 %d 拍而册上没有——是它不过手，还是漏报了？' % (k, c))
    # ── 身上的尺之疑（开集·只提醒，不判）──
    尺 = {}
    for i, x in enumerate(bs, 1):
        for pat in 尺之型:
            for mm in re.finditer(pat, x):
                尺.setdefault(mm.group(1), []).append(i)
    尺疑 = [(k, v) for k, v in sorted(尺.items())
            if k not in 报了 and ('「%s」' % k) not in 册文]
    if 尺疑:
        print('  ── 身上的尺之疑（开集·只提醒，不判）──')
        for k, v in 尺疑:
            print('   ⚠本章有一把身上的尺「%s」（拍%s），而册上一字未提——'
                  '入不入册，须当场说一句' % (k, '、'.join(str(z) for z in v[:4])))
    if 坏:
        print('  ⛔ 器物点名 %d 处未过' % len(坏))
        for x in 坏:
            print('     ⛔ ' + x)
        return 1
    print('  ✓ 器物点名 %d 件俱全（入／用／出三格皆有拍号，且逐拍验过其名在）' % len(rows))
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        print(__doc__.strip())
        raise SystemExit(1)
    raise SystemExit(跑(int(sys.argv[1])))
