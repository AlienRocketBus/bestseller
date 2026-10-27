#!/usr/bin/env python3
"""方法坑账（1009 立·作者令「每一次都要总结踩过的坑；每一次都要把坑修掉；让虫洞方法成为最好的方法」）。

为何立：坑之账原只是诸入口档里的一长行——记了坑，不记「修了没有、靠什么守住」。
其证：⑤「pgrep 认错」1007 已记，1009 总编辑又以 pgrep 等推送（⑮）——**只写在纸上之治不算治**。
★名「方法坑账」，以别於 `工具/坑账.py`（0909 立：写作之坑——起草令三十一坑、病历本四十三病，案席逐章过单）。
本器以 `设定/方法坑账.json` 为唯一之源，每坑：名、踩、费、根、治、守（守之档）、状、计、复踩、格、级、汰。
  状：已守＝治已落，且有机器守（守中之档俱在、守它之全测之格在）｜已治未守＝治只在令或纸上，须有「计」且计带「限」｜
      未治＝须有计、计带限｜已汰＝其坑之境已不复存（须书「汰」：由与代之者——坑号或 法用#id；验免其守与格，--查 不列）。
  复踩＝守失效之证：须写其治（加强其守），⛔只记；1027 起之复踩须带「守：工具/…」或「格：<全测之格>」（其档在、其格在全测）。
三入口档（README、交接、作者常令）之「坑之账」一行由 `--同步` 自本源生成（⛔手改）；`设定/虫洞法典.md` 须点到每一坑（坑必入法）。
**进化之律（1009 作者令·极要）**：方法进化之时先看曾经踩过的坑——踩过的坑⛔在新法里再现。故凡待立之新法之设计档
（`设定/方法升级_*.md` 之档首书「状：待立」者；已立者档首书「状：已立」，其坑之检係史、⛔再验）须有「## 坑之检」一节，
逐坑写新法如何排除之；新坑一入账，凡待立之法俱红，至补其排除方绿。工作流账 --开 亦逐坑印、有效之据须写坑之检。
**1027 执行之核（作者令「要避之坑须全部执行起来，并核查执行没有」）**：
  ①坑必有格：已守之坑（不论号）须点名守它之全测之格；㊲起之坑已治未守亦须格；复踩 ≥2 之坑（不论状）须有格——同错⛔犯三回。
    格须在读者可见之闸（红即拦推）；唯「器红级」之坑（费审、方法之坑，⛔关稿、书停、推）许其格只在全测（器红入账、逾三章即拦）。
  ②已治未守／未治之计须带「限：NNN章」或「限：MMDD」——末章 ≥ 限、或今日 > 限 即红（⛔无期之计：纸上之治永不落）。
⛔一刀切：凡新律须同枝内把现存之违者治平（已守而有现成之格者 --格 回填；无格可配者降「已治未守」带限）。

用法：
  python3 工具/方法坑账.py --查                      # 各状之数；未守者及其计（已汰不列）
  python3 工具/方法坑账.py --验                      # 闸（入全测）：缺根／缺治／守之档不在／未守无计无限、逾限／缺格／复踩无治、无守格／三档不同步／法典漏坑／待立之新法之「坑之检」漏坑 → 红
  python3 工具/方法坑账.py --同步                    # 三入口档之坑之账一行照本源重生
  python3 工具/方法坑账.py --立 名 根 治 计 [踩] [费]   # 新坑（状＝已治未守；计写「未治」二字则状＝未治）——计须带「限：…」
  python3 工具/方法坑账.py --守 号 档 [档…]           # 守已落：档俱在则状＝已守
  python3 工具/方法坑账.py --格 号 格 [格…]           # 点名守它的全测之格（须在读者可见之闸；器红级之坑许只在全测）
  python3 工具/方法坑账.py --级 号 器红 "由"          # 器红级（费审、方法之坑：其格许不在读者可见之闸）；--级 号 读者 即去之
  python3 工具/方法坑账.py --计 号 "计（带 限：NNN章｜限：MMDD）"   # 改计（器施，⛔手改源）
  python3 工具/方法坑账.py --踩 号 日                # 改「踩」（初踩之日）
  python3 工具/方法坑账.py --汰 号 "由（书代之者：坑号或 法用#id）"   # 状＝已汰（验免其守与格，--查 不列）
  python3 工具/方法坑账.py --复踩 号 "何时何事；治：……；守：工具/…（或 格：<全测之格>）"
  python3 工具/方法坑账.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, time, tempfile, shutil, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
源 = os.path.join('设定', '方法坑账.json')
法典 = os.path.join('设定', '虫洞法典.md')
# 1027 线B（#48 #138）：「开卷第一读·GitHub 为准」之旧入口档已删（同功两处即废劣者：唯一入口係 00_总章.md）——四档改三档
入口 = ['README.md', os.path.join('设定', '交接_续跑.md'), os.path.join('设定', '00_作者常令_不停之律.md')]
头 = '> **坑之账（每开一法对一遍；新坑随踩随添；源 `设定/方法坑账.json`，`python3 工具/方法坑账.py --同步` 生成，⛔手改）**：'
状s = ('已守', '已治未守', '未治', '已汰')
限式 = re.compile(r'限[:：]\s*(?:(\d{3,4})\s*章|(\d{2})(\d{2})(?!\d))')
代之式 = re.compile(r'[①-⑳㉑-㉟㊱-㊿]|坑\s*\d+|法用#\S+')
新复踩之起 = '2026-10-27'       # 自此日起之复踩须带「守：工具/…」或「格：<格>」（#46·⛔比 git 末改之日）
守式 = re.compile(r'守[:：]\s*`?((?:工具|设定|\.claude|\.github)/[^\s`；;，,）)]+)')
格式 = re.compile(r'格[:：]\s*`?([^\s`；;，,）)]+)')


def 圈(n):
    if 1 <= n <= 20:
        return chr(0x2460 + n - 1)
    if 21 <= n <= 35:
        return chr(0x3251 + n - 21)
    if 36 <= n <= 50:
        return chr(0x32B1 + n - 36)
    return '坑%d' % n


def 读(root=ROOT):
    return json.load(open(os.path.join(root, 源), encoding='utf-8'))


def 写(d, root=ROOT):
    json.dump(d, open(os.path.join(root, 源), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def 渲(d):
    def 一(k):
        标 = k['状'] + ('·复踩%d' % len(k['复踩']) if k.get('复踩') else '')
        return '%s%s〔%s〕' % (圈(k['号']), k['名'], 标)
    return 头 + '｜'.join(一(k) for k in d['坑'])


def _行(p):
    L = open(p, encoding='utf-8').read().split('\n')
    for i, l in enumerate(L):
        if l.startswith('> **坑之账'):
            return L, i
    return L, None


def 同步(root=ROOT, d=None):
    d = d or 读(root)
    t = 渲(d)
    for p in 入口:
        f = os.path.join(root, p)
        if not os.path.exists(f):
            continue
        L, i = _行(f)
        if i is None:
            print('⛔ %s 无「坑之账」一行' % p); continue
        if L[i] != t:
            L[i] = t
            open(f, 'w', encoding='utf-8').write('\n'.join(L))
    return t


有格之起 = 37        # ㊲（402 之失）起：已治未守亦须格（已守者 1027 起不论号俱须格）


def _全测之格(root=ROOT):
    """→ (全测所列诸格之名, 读者可见之闸之名)——读 工具/全测.py 之源（⛔ import 之：全测.py 甚重）。"""
    try:
        src = open(os.path.join(root, '工具', '全测.py'), encoding='utf-8').read()
    except Exception:
        return set(), set()
    名们 = set(re.findall(r"items\.append\(\('([^']+)'", src)) | set(re.findall(r"\(\s*'([^']+)'\s*,\s*chk_\w+\s*\)", src))
    m = re.search(r'^读者可见之闸 = \{(.*?)^\}', src, re.M | re.S)
    拦们 = set(re.findall(r"'([^']+)'", re.sub(r'#[^\n]*', '', m.group(1)))) if m else set()
    return 名们, 拦们


def _格之器(root=ROOT):
    """→ {格名: {所跑之器之档}}：全测之格所调之函，其体中所点之「工具/x.py」。读不出者不在表（不判）。"""
    try:
        src = open(os.path.join(root, '工具', '全测.py'), encoding='utf-8').read()
    except Exception:
        return {}
    函之体 = {}
    for m in re.finditer(r'^def (chk_\w+)\(\):\n(.*?)(?=^def |\Z)', src, re.M | re.S):
        函之体[m.group(1)] = set(re.findall(r"工具/[^'\"\s]+?\.py", m.group(2)))
    表 = {}
    for 名, 函 in re.findall(r"items\.append\(\('([^']+)',\s*(chk_\w+)\)", src):
        if 函之体.get(函):
            表[名] = 函之体[函]
    return 表


def 末章(root=ROOT):
    """末一有正文之章（同 自走.末章 之尺：正文/ 之档名「第…章」）；读不出作 0（⛔判逾章限）。"""
    try:
        import 自走
        ns = [自走._num(m.group(1)) for f in glob.glob(os.path.join(root, '正文', '*.md'))
              for m in [re.search(r'第([零〇一二三四五六七八九十百千]+)章', os.path.basename(f))] if m]
        return max(ns) if ns else 0
    except Exception:
        return 0


def 限之判(计, 章, 今):
    """→ (有限否, 逾限之语 or '')。章：末章；今：'MMDD'。"""
    m = 限式.search(计 or '')
    if not m:
        return False, ''
    if m.group(1):
        n = int(m.group(1))
        return True, ('末章 %d ≥ 限 %d 章' % (章, n)) if 章 >= n else ''
    md = m.group(2) + m.group(3)
    return True, ('今 %s > 限 %s' % (今, md)) if 今 > md else ''


def 格(号, 格们, root=ROOT):
    d = 读(root)
    k = d['坑'][号 - 1]
    名们, 拦们 = _全测之格(root)
    缺 = [g for g in 格们 if g not in 名们]
    if 缺:
        print('⛔ 全测无此格：%s' % '、'.join(缺)); return False
    k['格'] = sorted(set(k.get('格', []) + 格们))
    写(d, root); 同步(root, d)
    print('✓ %s 之格：%s%s' % (圈(号), '、'.join(k['格']), '' if all(g in 拦们 for g in k['格']) or k.get('级') == '器红'
                                                     else '（⚠ 有格不在读者可见之闸——须 --级 %d 器红 "由"，或换读者可见之格）' % 号))
    return True


def 验(root=ROOT, 章=None, 今=None):
    坏 = []
    try:
        d = 读(root)
    except Exception as e:
        return False, ['坑账读不出：%s' % e]
    章 = 末章(root) if 章 is None else 章
    今 = 今 or time.strftime('%m%d', time.gmtime())
    名们, 拦们 = _全测之格(root)
    器之 = _格之器(root)
    for i, k in enumerate(d['坑'], 1):
        号 = 圈(k.get('号', 0))
        状 = k.get('状')
        if k.get('号') != i:
            坏.append('%s 号不连（应 %d）' % (号, i))
        for 键 in ('名', '根', '治'):
            if not str(k.get(键, '')).strip():
                坏.append('%s 缺%s' % (号, 键))
        if 状 not in 状s:
            坏.append('%s 状须为 %s 之一' % (号, '／'.join(状s)))
        if 状 == '已汰':
            # ★1027（#104 #106 #107）：已汰须书由与代之者（坑号或 法用#id）——⛔无由而汰（汰即免守免格，空汰即逃）
            if not 代之式.search(str(k.get('汰', ''))):
                坏.append('%s 已汰而「汰」未书代之者（坑号或 法用#id）：--汰 %d "由……代之以 ㉝／法用#…"' % (号, k.get('号', 0)))
            continue
        if 状 == '已守':
            if not k.get('守'):
                坏.append('%s 称已守而无守之档' % 号)
            for p in k.get('守', []):
                if not os.path.exists(os.path.join(root, p)):
                    坏.append('%s 守之档不在：%s' % (号, p))
        else:
            计 = str(k.get('计', '')).strip()
            if not 计:
                坏.append('%s %s而无计（改哪档哪条、拿什么数验、限）' % (号, 状))
            else:
                # ★1027（#39 #23）：已治未守之计须带限，逾即红——⛔无期之计（纸上之治永不落）
                有, 逾 = 限之判(计, 章, 今)
                if not 有:
                    坏.append('%s %s之计无限（须带「限：NNN章」或「限：MMDD」：--计 %d "…；限：…"）' % (号, 状, k.get('号', 0)))
                elif 逾:
                    坏.append('%s %s而逾限（%s）——照计治落、--守 %d <档>，或降其坑另立新计（⛔悄悄续期）' % (号, 状, 逾, k.get('号', 0)))
        # ★1022 坑必有格；1027 执行之核：已守之坑不论号须格（纸上之守⛔算守）；㊲起已治未守亦须格；复踩 ≥2 之坑须格——
        #   格须在读者可见之闸（红即拦推）；器红级（费审、方法之坑）许只在全测（器红入账、逾三章即拦）。
        复 = len(k.get('复踩') or [])
        须格 = (状 == '已守') or (k.get('号', 0) >= 有格之起 and 状 != '未治') or 复 >= 2
        格们 = k.get('格') or []
        if 须格 and not 格们:
            由 = '复踩 %d 回' % 复 if 复 >= 2 and 状 != '已守' else 状
            坏.append('%s %s而无格（坑必有格：--格 %d <全测之格名>）' % (号, 由, k.get('号', 0)))
        for g in 格们:
            if g not in 名们:
                坏.append('%s 之格「%s」不在全测' % (号, g))
            elif g not in 拦们 and k.get('级') != '器红':
                坏.append('%s 之格「%s」不在读者可见之闸（红不拦推，守可被悄悄改坏；费审、方法之坑可 --级 %d 器红 "由"）' % (号, g, k.get('号', 0)))
            elif 状 == '已守' and 器之.get(g) and not (器之[g] & set(k.get('守', []))):
                坏.append('%s 之格「%s」所验之器（%s）不在其守之档——格⛔借他坑之格充数' % (号, g, '、'.join(sorted(器之[g]))))
        if k.get('级') == '器红' and len(str(k.get('级由', '')).strip()) < 4:
            坏.append('%s 器红级而无由（--级 %d 器红 "由"）' % (号, k.get('号', 0)))
        for r in k.get('复踩', []):
            事 = str(r.get('事', ''))
            if '治' not in 事:
                坏.append('%s 复踩（%s）未写其治——守失效须加强，⛔只记' % (号, r.get('时', '')))
            if str(r.get('时', '')) >= 新复踩之起:
                守们 = 守式.findall(事)
                格们2 = 格式.findall(事)
                if not 守们 and not 格们2:
                    坏.append('%s 复踩（%s）无「守：工具/…」或「格：<全测之格>」——其治须落於器（1027·#46）' % (号, r.get('时', '')))
                for p in 守们:
                    if not os.path.exists(os.path.join(root, p)):
                        坏.append('%s 复踩（%s）之守不在：%s' % (号, r.get('时', ''), p))
                for g in 格们2:
                    if g not in 名们:
                        坏.append('%s 复踩（%s）之格不在全测：%s' % (号, r.get('时', ''), g))
    t = 渲(d)
    for p in 入口:
        f = os.path.join(root, p)
        if os.path.exists(f):
            L, i = _行(f)
            if i is None or L[i] != t:
                坏.append('%s 之坑之账与方法坑账.json 不同步（跑 --同步）' % p)
    # ★1009 作者令「方法进化之时先看曾经踩过的坑——踩过的坑⛔在新法里再现」：凡待立之新法之设计档须有「坑之检」一节，逐坑写其排除之法
    #   ★1027（#105）：只认档首书「状：待立」者——已立之档（状：已立）其坑之检係史，⛔逼旧档逐坑补行（纸上之活）
    for f in 待立之档(root):
        t = open(f, encoding='utf-8').read()
        m = re.search(r'^##[^\n]*坑之检[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
        名 = os.path.basename(f)
        if not m:
            坏.append('%s 无「## 坑之检」一节（待立之新法须逐坑写其排除之法）' % 名)
            continue
        漏 = [圈(k['号']) for k in d['坑'] if k.get('状') != '已汰' and 圈(k['号']) not in m.group(1)]
        if 漏:
            坏.append('%s 之坑之检漏：%s（新坑入账，凡待立之法俱须补其排除）' % (名, ''.join(漏)))
    fp = os.path.join(root, 法典)
    if os.path.exists(fp):
        法 = open(fp, encoding='utf-8').read()
        漏 = [圈(k['号']) for k in d['坑'] if 圈(k['号']) not in 法]
        if 漏:
            坏.append('法典漏坑（坑必入法）：%s' % ''.join(漏))
    else:
        坏.append('无 %s' % 法典)
    return not 坏, 坏


def 待立之档(root=ROOT):
    """设定/方法升级_*.md 之档首（首二十行）书「状：待立」者。"""
    出 = []
    for f in sorted(glob.glob(os.path.join(root, '设定', '方法升级_*.md'))):
        首 = '\n'.join(open(f, encoding='utf-8').read().split('\n')[:20])
        if re.search(r'状[:：]\s*待立', 首):
            出.append(f)
    return 出


def 查(root=ROOT):
    d = 读(root)
    数 = {s: sum(1 for k in d['坑'] if k['状'] == s) for s in 状s}
    print('方法坑账：共 %d｜%s' % (len(d['坑']), '｜'.join('%s %d' % (s, 数[s]) for s in 状s)))
    for k in d['坑']:
        if k['状'] == '已汰':
            continue
        if k['状'] != '已守':
            print('  %s〔%s〕根：%s｜计：%s' % (圈(k['号']), k['状'], k['根'][:40], k['计'][:90]))
        for r in k.get('复踩', []):
            print('  %s 复踩 %s：%s' % (圈(k['号']), r.get('时', ''), r.get('事', '')[:90]))


def 立(名, 根, 治, 计, 踩='', 费='', root=ROOT):
    d = 读(root)
    n = len(d['坑']) + 1
    d['坑'].append({'号': n, '名': 名, '踩': 踩 or time.strftime('%Y-%m-%d', time.gmtime()), '费': 费, '根': 根, '治': 治,
                   '守': [], '状': '未治' if 计.strip() == '未治' else '已治未守', '计': 计, '复踩': []})
    写(d, root); 同步(root, d)
    print('✓ 立坑 %s（%s）——治落、守立之後：--守 %d <档>、--格 %d <全测之格>' % (圈(n), d['坑'][-1]['状'], n, n))
    if not 限式.search(计):
        print('  ⛔ 计无限：--计 %d "…；限：NNN章"（无限之计 --验 即红）' % n)
    # ★1020 ㉞立後推前速检方逮二档之坑之检漏：立坑即当面列须补其排除之档与法典（⛔待推闸）；1027 只列待立之档
    须 = [os.path.basename(f) for f in 待立之档(root)] + [os.path.basename(法典)]
    print('  ★须补 %s：%s 之「坑之检」各添一行（待立之新法）；法典之坑表添一行（--查 绿方推）' % (圈(n), '、'.join(须)))
    return n


def 守(号, 档们, root=ROOT):
    d = 读(root)
    k = d['坑'][号 - 1]
    缺 = [p for p in 档们 if not os.path.exists(os.path.join(root, p))]
    if 缺:
        print('⛔ 守之档不在：%s' % '、'.join(缺)); return False
    k['守'] = sorted(set(k.get('守', []) + 档们)); k['状'] = '已守'
    写(d, root); 同步(root, d)
    print('✓ %s 已守：%s%s' % (圈(号), '、'.join(k['守']), '' if k.get('格') else '——须 --格 %d <全测之格>（已守必有格）' % 号))
    return True


def 改计(号, 计, root=ROOT):
    if not 限式.search(计 or ''):
        print('⛔ 计须带「限：NNN章」或「限：MMDD」'); return False
    d = 读(root)
    d['坑'][号 - 1]['计'] = 计
    写(d, root); 同步(root, d)
    print('✓ %s 之计：%s' % (圈(号), 计[:90]))
    return True


def 改踩(号, 日, root=ROOT):
    if not re.fullmatch(r'\d{4}(-\d{2}-\d{2})?|\d{4}-\d{2}-\d{2}', 日 or ''):
        print('⛔ 踩之日须作 MMDD 或 YYYY-MM-DD'); return False
    d = 读(root)
    d['坑'][号 - 1]['踩'] = 日
    写(d, root); 同步(root, d)
    print('✓ %s 之踩：%s' % (圈(号), 日))
    return True


def 汰(号, 由, root=ROOT):
    if not 代之式.search(由 or ''):
        print('⛔ 汰须书代之者（坑号如 ㉝，或 法用#id）'); return False
    d = 读(root)
    k = d['坑'][号 - 1]
    k['状'] = '已汰'; k['汰'] = 由
    写(d, root); 同步(root, d)
    print('✓ %s 已汰：%s' % (圈(号), 由[:90]))
    return True


def 级(号, 级名, 由='', root=ROOT):
    d = 读(root)
    k = d['坑'][号 - 1]
    if 级名 == '器红':
        if len((由 or '').strip()) < 4:
            print('⛔ 器红级须书由（≥四字：何以其坑⛔关稿、书停、推）'); return False
        k['级'], k['级由'] = '器红', 由
    else:
        k.pop('级', None); k.pop('级由', None)
    写(d, root); 同步(root, d)
    print('✓ %s 之级：%s' % (圈(号), k.get('级', '读者可见')))
    return True


def 复踩(号, 事, root=ROOT):
    if '治' not in 事:
        print('⛔ 复踩须写其治（「……；治：……」）——守失效，须加强'); return False
    if not (守式.search(事) or 格式.search(事)):
        print('⛔ 复踩须点其治所落之器（「；守：工具/…」或「；格：<全测之格>」）——1027·#46'); return False
    d = 读(root)
    d['坑'][号 - 1].setdefault('复踩', []).append({'时': time.strftime('%Y-%m-%d', time.gmtime()), '事': 事})
    写(d, root); 同步(root, d)
    print('✓ %s 复踩记毕' % 圈(号))
    return True


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '设定')); os.makedirs(os.path.join(t, '工具'))
        open(os.path.join(t, '工具', '甲.py'), 'w').write('')
        open(os.path.join(t, '工具', '全测.py'), 'w', encoding='utf-8').write(
            "读者可见之闸 = {\n    '负测·甲',\n}\ndef chk_a():\n    return _自测之项('负测·甲', '工具/甲.py')\n\nitems.append(('负测·甲', chk_a))\n")
        for p in 入口:
            open(os.path.join(t, p), 'w', encoding='utf-8').write('一\n> **坑之账（旧）**：①旧\n三\n')
        写({'坑': [{'号': 1, '名': '甲坑', '根': '根', '治': '治', '守': ['工具/甲.py'], '状': '已守', '计': '', '复踩': [], '格': ['负测·甲']}]}, t)
        open(os.path.join(t, 法典), 'w', encoding='utf-8').write('① 甲坑入法')
        import io, contextlib
        V = lambda: 验(t, 章=410, 今='1027')
        with contextlib.redirect_stdout(io.StringIO()):
            r0 = V()[0]
            同步(t)
            r1 = V()[0]
            n = 立('乙坑', '根', '治', '二代改某档；限：420章', root=t)
            r2 = V()                                           # 法典漏②
            open(os.path.join(t, 法典), 'a', encoding='utf-8').write('② 乙坑')
            r3 = V()[0]
            r4 = 守(2, ['工具/无.py'], t)                      # 守之档不在 → 拒
            r5 = 守(2, ['工具/甲.py'], t)
            格(2, ['负测·甲'], t)
            r6 = 复踩(1, '又踩了', t)                          # 无治 → 拒
            r6b = 复踩(1, '又踩了；治：加一道闸', t)            # 1027：无守／格 → 拒
            r7 = 复踩(1, '又踩了；治：加一道闸；守：工具/甲.py', t)
            r8 = V()[0]
        共 += 1; ok += (r0 is False and r1 is True)                               # 不同步即红，同步後绿
        共 += 1; ok += (n == 2 and r2[0] is False and any('法典漏坑' in x for x in r2[1]) and r3 is True)
        共 += 1; ok += (r4 is False and r5 is True and 读(t)['坑'][1]['状'] == '已守')
        共 += 1; ok += (r6 is False and r6b is False and r7 is True and r8 is True and '复踩1' in open(os.path.join(t, 'README.md'), encoding='utf-8').read())
        d = 读(t); d['坑'][1]['状'] = '已治未守'; d['坑'][1]['计'] = ''; 写(d, t); 同步(t, d)
        共 += 1; ok += (V()[0] is False)                                       # 未守无计 → 红
        d = 读(t); d['坑'][1]['计'] = '某计；限：420章'; 写(d, t); 同步(t, d)
        # ★1027（#105）：只认档首「状：待立」之设计档；已立者⛔验其坑之检
        open(os.path.join(t, '设定', '方法升级_新.md'), 'w', encoding='utf-8').write('# 新法\n> 状：待立\n## 一\n①②\n## 二、坑之检\n① 排除之\n## 三\n② 在别节\n')
        r9 = V()
        open(os.path.join(t, '设定', '方法升级_新.md'), 'w', encoding='utf-8').write('# 新法\n> 状：待立\n## 二、坑之检\n① 排除之\n② 排除之\n')
        r10 = V()[0]
        open(os.path.join(t, '设定', '方法升级_新.md'), 'w', encoding='utf-8').write('# 新法\n> 状：已立（1013）\n## 二、坑之检\n① 排除之\n')
        r10b = V()[0]
        共 += 1; ok += (r9[0] is False and any('坑之检漏：②' in x for x in r9[1]) and r10 is True and r10b is True)   # 待立漏一坑即红；已立免
        共 += 1; ok += (圈(1) == '①' and 圈(20) == '⑳' and 圈(21) == '㉑' and 圈(36) == '㊱' and 圈(51) == '坑51')
        # ★1022／1027 坑必有格：已守之坑（不论号）无格即红；格不在全测即红；格不在读者可见之闸即红（器红级免）；三者俱合方绿
        open(os.path.join(t, '工具', '全测.py'), 'w', encoding='utf-8').write(
            "读者可见之闸 = {\n    '负测·甲',   # '负测·注'\n}\ndef chk_a():\n    return _自测之项('负测·甲', '工具/甲.py')\n\n"
            "def chk_b():\n    return _自测之项('负测·乙', '工具/甲.py')\n\nitems.append(('负测·甲', chk_a))\nitems.append(('负测·乙', chk_b))\n")
        d = 读(t); d['坑'][1]['状'] = '已守'; d['坑'][1]['守'] = ['工具/甲.py']; d['坑'][1]['格'] = []; 写(d, t); 同步(t, d)
        with contextlib.redirect_stdout(io.StringIO()):
            g0 = V()                                           # 回灌：② 号 <37、已守而无格（旧律之免）→ 今即红
            g1 = 格(2, ['负测·无'], t)
            格(2, ['负测·乙'], t)
            g2 = V()                                           # 格不在读者可见之闸（注中之名⛔算）→ 红
            g2b = 级(2, '器红', '', t)                          # 器红级无由 → 拒
            级(2, '器红', '费审之坑·⛔关稿', t)
            g3 = V()[0]                                        # 器红级：其格许只在全测
            级(2, '读者', root=t)
            d = 读(t); d['坑'][1]['格'] = ['负测·甲']; 写(d, t); 同步(t, d)
            g4 = V()[0]
        共 += 1; ok += (g0[0] is False and any('② 已守而无格' in x for x in g0[1]) and g1 is False
                      and g2[0] is False and any('不在读者可见之闸' in x for x in g2[1]) and g2b is False and g3 is True and g4 is True)
        # 1022 复核：㊲起已治未守亦须格；格所验之器不在守之档即红（⛔借格）
        open(os.path.join(t, '工具', '全测.py'), 'w', encoding='utf-8').write(
            "读者可见之闸 = {\n    '负测·甲', '负测·丙',\n}\ndef chk_a():\n    return _自测之项('负测·甲', '工具/甲.py')\n\n"
            "def chk_c():\n    return _自测之项('负测·丙', '工具/丙.py')\n\nitems.append(('负测·甲', chk_a))\nitems.append(('负测·丙', chk_c))\n")
        global 有格之起
        旧起 = 有格之起
        try:
            有格之起 = 1
            d = 读(t); d['坑'][1]['状'] = '已治未守'; d['坑'][1]['计'] = '某计；限：420章'; d['坑'][1]['格'] = []; 写(d, t); 同步(t, d)
            with contextlib.redirect_stdout(io.StringIO()):
                h0 = V()
                d = 读(t); d['坑'][1]['状'] = '已守'; d['坑'][1]['格'] = ['负测·丙']; 写(d, t); 同步(t, d)
                h1 = V()
                d = 读(t); d['坑'][1]['格'] = ['负测·甲']; 写(d, t); 同步(t, d)
                h2 = V()[0]
            共 += 1; ok += (h0[0] is False and any('已治未守而无格' in x for x in h0[1])
                          and h1[0] is False and any('借他坑之格' in x for x in h1[1]) and h2 is True)
        finally:
            有格之起 = 旧起
        # ★1027（#39 #23）：已治未守之计须带限，逾即红（章限、日限）；放行之反例：限未到
        d = 读(t); d['坑'][1]['状'] = '已治未守'; d['坑'][1]['计'] = '某计'; 写(d, t); 同步(t, d)
        j0 = V()
        d['坑'][1]['计'] = '某计；限：410章'; 写(d, t); 同步(t, d)
        j1 = V()
        d['坑'][1]['计'] = '某计；限：1026'; 写(d, t); 同步(t, d)
        j2 = V()
        d['坑'][1]['计'] = '某计；限：1103'; 写(d, t); 同步(t, d)
        j3 = V()[0]
        d['坑'][1]['计'] = '某计；限：411章'; 写(d, t); 同步(t, d)
        j4 = V()[0]
        共 += 1; ok += (j0[0] is False and any('之计无限' in x for x in j0[1]) and j1[0] is False and any('逾限' in x and '410' in x for x in j1[1])
                      and j2[0] is False and any('逾限' in x and '1026' in x for x in j2[1]) and j3 is True and j4 is True)
        # ★1027（#69）：复踩 ≥2 之坑（不论状）须有格；（#46）1027 起之复踩须带守／格且其档在、其格在全测
        d = 读(t); d['坑'][1]['格'] = []
        d['坑'][1]['复踩'] = [{'时': '2026-10-15', '事': '甲；治：乙'}, {'时': '2026-10-16', '事': '丙；治：丁'}]
        写(d, t); 同步(t, d)
        k0 = V()
        d['坑'][1]['格'] = ['负测·甲']; 写(d, t); 同步(t, d)
        k1 = V()[0]
        d['坑'][1]['复踩'].append({'时': '2026-10-27', '事': '戊；治：己'}); 写(d, t); 同步(t, d)
        k2 = V()
        d['坑'][1]['复踩'][-1]['事'] = '戊；治：己；守：工具/无.py'; 写(d, t); 同步(t, d)
        k3 = V()
        d['坑'][1]['复踩'][-1]['事'] = '戊；治：己；格：负测·甲'; 写(d, t); 同步(t, d)
        k4 = V()[0]
        共 += 1; ok += (k0[0] is False and any('复踩 2 回而无格' in x for x in k0[1]) and k1 is True
                      and k2[0] is False and any('无「守：工具/…」' in x for x in k2[1]) and k3[0] is False and any('之守不在' in x for x in k3[1]) and k4 is True)
        # ★1027（#104 #106 #107）：--计／--踩／--汰 三口；已汰须书代之者，验免其守与格、--查 不列
        with contextlib.redirect_stdout(io.StringIO()):
            m0 = 改计(2, '无限之计', t)
            m1 = 改计(2, '新计；限：430章', t)
            m2 = 改踩(2, '1027', t)
            m3 = 汰(2, '随汰', t)
            m4 = 汰(2, '随汰（1027 推闸交 GitHub·代之以 法用#推闸交GitHub）', t)
        d = 读(t)
        d['坑'][1]['守'] = ['工具/无.py']; d['坑'][1]['格'] = ['负测·无']; 写(d, t); 同步(t, d)
        m5 = V()[0]
        d['坑'][1]['汰'] = '随汰'; 写(d, t); 同步(t, d)
        m6 = V()
        with contextlib.redirect_stdout(io.StringIO()) as _o:
            d['坑'][1]['汰'] = '代之以 ㉝'; 写(d, t); 同步(t, d)
            查(t)
        共 += 1; ok += (m0 is False and m1 is True and m2 is True and m3 is False and m4 is True and m5 is True
                      and m6[0] is False and any('未书代之者' in x for x in m6[1]) and '②' not in _o.getvalue()
                      and '已汰' in open(os.path.join(t, 'README.md'), encoding='utf-8').read())
        # ★1027（#48 #138）：入口三档（第一铁律之档已删）；回灌：旧之四档表即红
        共 += 1; ok += (len(入口) == 3 and not any('第一铁律' in p for p in 入口) and 'README.md' in 入口)
    finally:
        shutil.rmtree(t)
    # ★1027 回灌旧树：db52f247 之坑账照今之律验即红（① 已守而无格、② 计无限……）——⛔空验
    try:
        import subprocess
        旧 = subprocess.run(['git', 'show', 'db52f24740315a2abd535781fd39fda45e6b681b:设定/方法坑账.json'], cwd=ROOT,
                           capture_output=True, text=True, timeout=30)
        if 旧.returncode == 0:
            t2 = tempfile.mkdtemp()
            try:
                os.makedirs(os.path.join(t2, '工具')); os.makedirs(os.path.join(t2, '设定'))
                shutil.copy(os.path.join(ROOT, '工具', '全测.py'), os.path.join(t2, '工具', '全测.py'))
                open(os.path.join(t2, 源), 'w', encoding='utf-8').write(旧.stdout)
                for p in 入口 + [法典]:
                    if os.path.exists(os.path.join(ROOT, p)):
                        shutil.copy(os.path.join(ROOT, p), os.path.join(t2, p))
                同步(t2)
                o2, 坏2 = 验(t2, 章=410, 今='1027')
                共 += 1; ok += (o2 is False and any('① 已守而无格' in x for x in 坏2) and any('② 已治未守之计无限' in x for x in 坏2))
            finally:
                shutil.rmtree(t2, ignore_errors=True)
    except Exception:
        pass
    print('方法坑账·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--查']:
        查(); sys.exit(0)
    if a == ['--同步']:
        同步(); print('✓ 三入口档之坑之账已同步'); sys.exit(0)
    if a == ['--验']:
        o, 坏 = 验()
        print('✓ 方法坑账：俱有根有治，已守者守之档与格俱在，未守者计带限而未逾，复踩俱落於器，三档同步，法典不漏' if o else '⛔ 方法坑账：\n  ' + '\n  '.join(坏))
        sys.exit(0 if o else 1)
    if a[:1] == ['--立'] and 5 <= len(a) <= 7:
        立(*a[1:]); sys.exit(0)
    if a[:1] == ['--守'] and len(a) >= 3 and a[1].isdigit():
        sys.exit(0 if 守(int(a[1]), a[2:]) else 1)
    if a[:1] == ['--格'] and len(a) >= 3 and a[1].isdigit():
        sys.exit(0 if 格(int(a[1]), a[2:]) else 1)
    if a[:1] == ['--级'] and len(a) in (3, 4) and a[1].isdigit():
        sys.exit(0 if 级(int(a[1]), a[2], a[3] if len(a) > 3 else '') else 1)
    if a[:1] == ['--计'] and len(a) == 3 and a[1].isdigit():
        sys.exit(0 if 改计(int(a[1]), a[2]) else 1)
    if a[:1] == ['--踩'] and len(a) == 3 and a[1].isdigit():
        sys.exit(0 if 改踩(int(a[1]), a[2]) else 1)
    if a[:1] == ['--汰'] and len(a) == 3 and a[1].isdigit():
        sys.exit(0 if 汰(int(a[1]), a[2]) else 1)
    if a[:1] == ['--复踩'] and len(a) == 3 and a[1].isdigit():
        sys.exit(0 if 复踩(int(a[1]), a[2]) else 1)
    print(__doc__); sys.exit(2)
