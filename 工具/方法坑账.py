#!/usr/bin/env python3
"""方法坑账（1009 立·作者令「每一次都要总结踩过的坑；每一次都要把坑修掉；让虫洞方法成为最好的方法」）。

为何立：坑之账原只是四入口档里的一长行——记了坑，不记「修了没有、靠什么守住」。
其证：⑤「pgrep 认错」1007 已记，1009 总编辑又以 pgrep 等推送（⑮）——**只写在纸上之治不算治**。
★名「方法坑账」，以别於 `工具/坑账.py`（0909 立：写作之坑——起草令三十一坑、病历本四十三病，案席逐章过单）。
本器以 `设定/方法坑账.json` 为唯一之源，每坑：名、踩、费、根、治、守（守之档）、状、计、复踩。
  状：已守＝治已落，且有机器守（守中之档俱在，其自测入全测）｜已治未守＝治只在令或纸上，须有「计」｜未治＝须有「计」。
  复踩＝守失效之证：须写其治（加强其守），⛔只记。
四入口档之「坑之账」一行由 `--同步` 自本源生成（⛔手改）；`设定/虫洞法典.md` 须点到每一坑（坑必入法）。
**进化之律（1009 作者令·极要）**：方法进化之时先看曾经踩过的坑——踩过的坑⛔在新法里再现。故凡新法之设计档（`设定/方法升级_*.md`）
须有「## 坑之检」一节，逐坑写新法如何排除之；新坑一入账，凡待立之法俱红，至补其排除方绿。工作流账 --开 亦逐坑印、有效之据须写坑之检。

用法：
  python3 工具/方法坑账.py --查                      # 各状之数；未守者及其计
  python3 工具/方法坑账.py --验                      # 闸（入全测）：缺根／缺治／守之档不在／未守无计／复踩无治／四档不同步／法典漏坑／新法之「坑之检」漏坑 → 红
  python3 工具/方法坑账.py --同步                    # 四入口档之坑之账一行照本源重生
  python3 工具/方法坑账.py --立 名 根 治 计 [踩] [费]   # 新坑（状＝已治未守；计写「未治」二字则状＝未治）
  python3 工具/方法坑账.py --守 号 档 [档…]           # 守已落：档俱在则状＝已守
  python3 工具/方法坑账.py --复踩 号 "何时何事；治：……"
  python3 工具/方法坑账.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, json, time, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
源 = os.path.join('设定', '方法坑账.json')
法典 = os.path.join('设定', '虫洞法典.md')
入口 = ['README.md', os.path.join('设定', '交接_续跑.md'), os.path.join('设定', '00_作者常令_不停之律.md'), '00_第一铁律_GitHub为准_必读.md']
头 = '> **坑之账（每开一法对一遍；新坑随踩随添；源 `设定/方法坑账.json`，`python3 工具/方法坑账.py --同步` 生成，⛔手改）**：'
状s = ('已守', '已治未守', '未治')


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


def 验(root=ROOT):
    坏 = []
    try:
        d = 读(root)
    except Exception as e:
        return False, ['坑账读不出：%s' % e]
    for i, k in enumerate(d['坑'], 1):
        号 = 圈(k.get('号', 0))
        if k.get('号') != i:
            坏.append('%s 号不连（应 %d）' % (号, i))
        for 键 in ('名', '根', '治'):
            if not str(k.get(键, '')).strip():
                坏.append('%s 缺%s' % (号, 键))
        if k.get('状') not in 状s:
            坏.append('%s 状须为 %s 之一' % (号, '／'.join(状s)))
        if k.get('状') == '已守':
            if not k.get('守'):
                坏.append('%s 称已守而无守之档' % 号)
            for p in k.get('守', []):
                if not os.path.exists(os.path.join(root, p)):
                    坏.append('%s 守之档不在：%s' % (号, p))
        elif not str(k.get('计', '')).strip():
            坏.append('%s %s而无计（改哪档哪条、拿什么数验）' % (号, k.get('状')))
        for r in k.get('复踩', []):
            if '治' not in str(r.get('事', '')):
                坏.append('%s 复踩（%s）未写其治——守失效须加强，⛔只记' % (号, r.get('时', '')))
    t = 渲(d)
    for p in 入口:
        f = os.path.join(root, p)
        if os.path.exists(f):
            L, i = _行(f)
            if i is None or L[i] != t:
                坏.append('%s 之坑之账与方法坑账.json 不同步（跑 --同步）' % p)
    # ★1009 作者令「方法进化之时先看曾经踩过的坑——踩过的坑⛔在新法里再现」：凡新法之设计档须有「坑之检」一节，逐坑写其排除之法
    import glob as _g, re as _re
    for f in sorted(_g.glob(os.path.join(root, '设定', '方法升级_*.md'))):
        t = open(f, encoding='utf-8').read()
        m = _re.search(r'^##[^\n]*坑之检[^\n]*\n(.*?)(?=^## |\Z)', t, _re.M | _re.S)
        名 = os.path.basename(f)
        if not m:
            坏.append('%s 无「## 坑之检」一节（新法须逐坑写其排除之法）' % 名)
            continue
        漏 = [圈(k['号']) for k in d['坑'] if 圈(k['号']) not in m.group(1)]
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


def 查(root=ROOT):
    d = 读(root)
    数 = {s: sum(1 for k in d['坑'] if k['状'] == s) for s in 状s}
    print('方法坑账：共 %d｜%s' % (len(d['坑']), '｜'.join('%s %d' % (s, 数[s]) for s in 状s)))
    for k in d['坑']:
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
    print('✓ 立坑 %s（%s）——治落、守立之後：--守 %d <档>' % (圈(n), d['坑'][-1]['状'], n))
    import glob as _g      # ★1020 ㉞立後推前速检方逮二档之坑之检漏：立坑即当面列须补其排除之档与法典（⛔待推闸）
    须 = [os.path.basename(f) for f in sorted(_g.glob(os.path.join(ROOT, '设定', '方法升级_*.md')))] + [os.path.basename(法典)]
    print('  ★须补 %s：%s 之「坑之检」各添一行；法典之坑表添一行（--查 绿方推）' % (圈(n), '、'.join(须)))
    return n


def 守(号, 档们, root=ROOT):
    d = 读(root)
    k = d['坑'][号 - 1]
    缺 = [p for p in 档们 if not os.path.exists(os.path.join(root, p))]
    if 缺:
        print('⛔ 守之档不在：%s' % '、'.join(缺)); return False
    k['守'] = sorted(set(k.get('守', []) + 档们)); k['状'] = '已守'
    写(d, root); 同步(root, d)
    print('✓ %s 已守：%s' % (圈(号), '、'.join(k['守'])))
    return True


def 复踩(号, 事, root=ROOT):
    if '治' not in 事:
        print('⛔ 复踩须写其治（「……；治：……」）——守失效，须加强'); return False
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
        for p in 入口:
            open(os.path.join(t, p), 'w', encoding='utf-8').write('一\n> **坑之账（旧）**：①旧\n三\n')
        写({'坑': [{'号': 1, '名': '甲坑', '根': '根', '治': '治', '守': ['工具/甲.py'], '状': '已守', '计': '', '复踩': []}]}, t)
        open(os.path.join(t, 法典), 'w', encoding='utf-8').write('① 甲坑入法')
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            r0 = 验(t)[0]
            同步(t)
            r1 = 验(t)[0]
            n = 立('乙坑', '根', '治', '二代改某档', root=t)
            r2 = 验(t)                                         # 法典漏②
            open(os.path.join(t, 法典), 'a', encoding='utf-8').write('② 乙坑')
            r3 = 验(t)[0]
            r4 = 守(2, ['工具/无.py'], t)                      # 守之档不在 → 拒
            r5 = 守(2, ['工具/甲.py'], t)
            r6 = 复踩(1, '又踩了', t)                          # 无治 → 拒
            r7 = 复踩(1, '又踩了；治：加一道闸', t)
            r8 = 验(t)[0]
        共 += 1; ok += (r0 is False and r1 is True)                               # 不同步即红，同步後绿
        共 += 1; ok += (n == 2 and r2[0] is False and any('法典漏坑' in x for x in r2[1]) and r3 is True)
        共 += 1; ok += (r4 is False and r5 is True and 读(t)['坑'][1]['状'] == '已守')
        共 += 1; ok += (r6 is False and r7 is True and r8 is True and '复踩1' in open(os.path.join(t, 'README.md'), encoding='utf-8').read())
        d = 读(t); d['坑'][1]['状'] = '已治未守'; d['坑'][1]['计'] = ''; 写(d, t); 同步(t, d)
        共 += 1; ok += (验(t)[0] is False)                                       # 未守无计 → 红
        d = 读(t); d['坑'][1]['计'] = '某计'; 写(d, t); 同步(t, d)
        open(os.path.join(t, '设定', '方法升级_新.md'), 'w', encoding='utf-8').write('# 新法\n## 一\n①②\n## 二、坑之检\n① 排除之\n## 三\n② 在别节\n')
        r9 = 验(t)
        open(os.path.join(t, '设定', '方法升级_新.md'), 'a', encoding='utf-8').write('## 四、坑之检·补\n')
        open(os.path.join(t, '设定', '方法升级_新.md'), 'w', encoding='utf-8').write('# 新法\n## 二、坑之检\n① 排除之\n② 排除之\n')
        r10 = 验(t)[0]
        共 += 1; ok += (r9[0] is False and any('坑之检漏：②' in x for x in r9[1]) and r10 is True)   # 新法漏一坑即红
        共 += 1; ok += (圈(1) == '①' and 圈(20) == '⑳' and 圈(21) == '㉑' and 圈(36) == '㊱' and 圈(51) == '坑51')
    finally:
        shutil.rmtree(t)
    print('方法坑账·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--查']:
        查(); sys.exit(0)
    if a == ['--同步']:
        同步(); print('✓ 四入口档之坑之账已同步'); sys.exit(0)
    if a == ['--验']:
        o, 坏 = 验()
        print('✓ 方法坑账：俱有根有治，已守者守之档俱在，未守者俱有计，四档同步，法典不漏' if o else '⛔ 方法坑账：\n  ' + '\n  '.join(坏))
        sys.exit(0 if o else 1)
    if a[:1] == ['--立'] and 5 <= len(a) <= 7:
        立(*a[1:]); sys.exit(0)
    if a[:1] == ['--守'] and len(a) >= 3 and a[1].isdigit():
        sys.exit(0 if 守(int(a[1]), a[2:]) else 1)
    if a[:1] == ['--复踩'] and len(a) == 3 and a[1].isdigit():
        sys.exit(0 if 复踩(int(a[1]), a[2]) else 1)
    print(__doc__); sys.exit(2)
