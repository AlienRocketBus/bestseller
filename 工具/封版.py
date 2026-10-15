#!/usr/bin/env python3
"""封版（1013 立·造式二代·设定/方法升级_造式二代.md §五之五）——封版诸件之跑器、核数、提交、备份，归脚本。

为何立：一代之案席与封版席两席（380：$19.65＋$31.88，来回 414 回）大半在跑器、核数、提交、备份——机器之活。
二代拆开（零 token 之检）：
  · 读懂了才写得出之档（回执之文、锁定行逐拍、创作记录、全书记忆、状态册、open_brief、下一章开镜卡）——记席（造章.js 之末席）；
  · 其余——存版对表、造式之实、锁定行之数、坑账之单、诸闸、第十一轮、全测、提交、双备份、存底包、撤锁——本器。

用法：
  python3 工具/封版.py N --前        # 记席先跑：对表（正文≠末版即存一版）、造式之实、锁定行之数、坑账之单、冷轮之担、前章回执与锁定行之样
  python3 工具/封版.py N --後        # 记席毕、主环跑：验记席之档俱在 → 诸闸 → 第十一轮 → 全测 → 提交 → 存底与存底包 → 撤锁（红即停、⛔提交）
  python3 工具/封版.py N --後 --试   # 只跑诸闸与第十一轮之验，⛔写、⛔提交、⛔存底（演练用）
  python3 工具/封版.py --自测         # 以已封版之 380 之真料核诸数（与其锁定行亲核之数逐个同）
次序之据：开轮六检於第十一轮之前跑——十一轮一过、回执在，章即「已封版」，开轮六检⑭即判「封版之章不得再跑十轮」（1013 实测）。
推送：本器⛔推；跑毕主环 `python3 工具/推.py`（後台）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob, time, hashlib, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
施工表 = os.path.join('设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')
总纲 = os.path.join('设定', '02_余章之势_总纲.md')
尾 = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016Hgfc2SSNvGktFmk2LX825'


def 正文档(n, root=ROOT):
    from 对账预筛 import 章号
    for f in glob.glob(os.path.join(root, '正文', '*.md')):
        if 章号(f) == n:
            return f
    return None


def 跑(a, root=ROOT, 限=900):
    t = time.time()
    try:
        r = subprocess.run([sys.executable] + a if a[0].endswith('.py') else a, cwd=root, capture_output=True, text=True, timeout=限)
        return r.returncode, r.stdout + r.stderr, time.time() - t
    except subprocess.TimeoutExpired:
        return 124, '（逾 %d 秒未毕）' % 限, time.time() - t


def 器(名):
    return os.path.join(ROOT, '工具', 名)


def 数(n, root=ROOT):
    """锁定行之机器之数（⛔凭空写一个数即是造数）。"""
    f = 正文档(n, root)
    if not f:
        return {'坏': '第%d章之正文不在' % n}
    文 = open(f, encoding='utf-8').read()
    L = 文.split('\n')
    亮 = next((i + 1 for i, l in enumerate(L) if '【本章亮点】' in l), None)
    白止 = (亮 - 1) if 亮 else len(L)
    while 白止 > 1 and not L[白止 - 1].strip():
        白止 -= 1
    星 = sum(1 for l in L[:白止] if l.strip() == '＊')
    import 净重对表
    d = {'正文': os.path.relpath(f, root), '白文': '1 至 %d 行' % 白止, '亮点行': 亮, '净重': 净重对表.净重(f),
         '＊': 星, '拍': 星 + 1, 'sha1': hashlib.sha1(文.encode('utf-8')).hexdigest()[:12]}
    台 = os.path.join(root, '版本', '第%d章' % n, '_台账.json')
    if os.path.exists(台):
        版们 = json.load(open(台, encoding='utf-8')).get('版本', [])
        if 版们:
            末 = 版们[-1]
            d['末版'] = 末.get('版')
            s = 末.get('soft')
            s = eval(s, {}) if isinstance(s, str) else (s or {})      # 台账之 soft 以 Python 字面存（跑轮所写）
            d['六数'] = '净重%s｜段数%s｜长段数%s｜嗅%s｜触%s｜四字串三现%s' % tuple(s.get(k, '?') for k in ('净重', '段数', '长段数', '嗅', '触', '四字串三现'))
            d['诸版'] = ['%s %s「%s」' % (v.get('版'), v.get('时', ''), str(v.get('说明', ''))[:40]) for v in 版们]
            末档 = os.path.join(root, '版本', '第%d章' % n, '%s.md' % 末.get('版'))
            d['与末版同'] = os.path.exists(末档) and open(末档, encoding='utf-8').read() == 文
    m = re.search(r'\|\s*%d\s*\|\s*([主暗]·\d+)\s*\|' % n, open(os.path.join(root, 总纲), encoding='utf-8').read())   # 两栏排，整行逐栏认
    d['总纲'] = '| %d | %s |' % (n, m.group(1)) if m else None
    return d


def 前(n, root=ROOT):
    print('════ 封版·前（第%d章）════' % n)
    d = 数(n, root)
    if d.get('坏'):
        print('⛔ ' + d['坏']); return False
    if d.get('与末版同') is False:
        rc, out, _ = 跑([器('跑轮.py'), '--存', str(n), '造式二代·定稿：正文与末版对齐（封版.py --前）'], root)
        print('· 正文与末版不一：已存一版（rc=%d）' % rc)
        d = 数(n, root)
    rc, out, _ = 跑([器('造式.py'), str(n)], root)
    print('· 造式之实：%s' % (out.strip().split('\n')[-1] if out.strip() else rc))
    print('· 锁定行之数（取此，⛔凭空写）：')
    for k in ('正文', '总纲', '白文', '亮点行', '净重', '六数', '＊', '拍', '末版', '与末版同', 'sha1'):
        print('    %s：%s' % (k, d.get(k)))
    for v in d.get('诸版', []):
        print('    版：' + v)
    rc, out, _ = 跑([器('层census.py'), str(n)], root)
    print('· 层（层census.py %d）：\n%s' % (n, '\n'.join('    ' + l for l in out.strip().split('\n')[-8:])))
    rc, out, _ = 跑([器('坑账.py'), '--逐章', str(n)], root)
    print('· 坑账之单（逐条答进回执「坑账之答」）：\n' + '\n'.join('    ' + l for l in out.strip().split('\n')))
    try:                                                     # ★1013：开轮十六检（除⑭）——384 记席未写「承前之判」（⑮），封版·後 方红；今於 --前 即印其红
        rc6, out6, _ = 跑([器('开轮六检.py'), str(n), '--静'], root)
        import 全测 as _全测
        余6 = _全测._六检之败(out6, True)
        print('· 开轮十六检（除⑭）：%s' % ('✓ 俱过' if not 余6 else '⛔ ' + '；'.join(余6)[:600] + '——记席须治（承前之判写进轮记，逐样点名落判：认／翻／搁下）'))
    except Exception as _e:
        print('· 开轮十六检：⛔判不出（%s）' % _e)
    try:                                                     # ★1013：六问（质量三闸①之e）——381 记席未答，封版之全测方红；今於 --前 即印
        import 质量三闸
        _名, _过, _语 = 质量三闸.gate1e(n)[0]
        print('· 六问：%s %s%s' % ('✓' if _过 else '⛔', _语, '' if _过 else '——记席须於轮记之首答六条（造章.js 记令 2之二）'))
    except Exception as _e:
        print('· 六问：⛔判不出（%s）' % _e)
    冷 = glob.glob(os.path.join(root, '设定', '冷轮_COLD*_於%d补执.md' % n))
    print('· 冷轮之担：%s' % ('、'.join(os.path.relpath(x, root) for x in 冷) or '无'))
    回 = sorted(glob.glob(os.path.join(root, '设定', '回执_*_第%d章封版席.md' % (n - 1))))
    print('· 前章回执之样：%s' % (os.path.relpath(回[-1], root) if 回 else '（无）'))
    t = open(os.path.join(root, 施工表), encoding='utf-8').read()
    样 = [l[:120] + '…' for l in t.split('\n') if l.startswith('| %d | 锁定 |' % (n - 1)) or l.startswith('| %d | 悬账 |' % (n - 1))]
    print('· 前章锁定行与悬账行之样（施工表）：\n' + '\n'.join('    ' + x for x in 样))
    return True


def 记之缺(n, root=ROOT):
    t = open(os.path.join(root, 施工表), encoding='utf-8').read()
    项 = [('回执', bool(glob.glob(os.path.join(root, '设定', '回执_*_第%d章封版席.md' % n)))),
         ('锁定行', ('| %d | 锁定 |' % n) in t), ('悬账行', ('| %d | 悬账 |' % n) in t),
         ('创作记录', os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_创作记录.md'))),
         ('全书记忆·章详记', os.path.exists(os.path.join(root, '设定', '全书记忆', '第%d章.md' % n))),
         ('下一章开镜卡', os.path.exists(os.path.join(root, '版本', '第%d章' % (n + 1), '_开镜卡.md'))),
         ('席记', os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_席记.json')))]
    return [k for k, ok in 项 if not ok]


def 可提交(n, 路们):
    """只收本章所及之处（⛔git add -A）：正文／本章与下一章之版本目录／设定／根之 .md 与 .html。"""
    # ★1013：记席按令改 工具/ 下二档（小说检察官之 OPEN_BRIEF_CARD_SCHEMA[N+1]、提示词系统之「--开拍 N+1」）——旧只收 设定/ 等，此二档永留未提交（381 实逮）
    前缀 = ('正文/', '版本/第%d章/' % n, '版本/第%d章/' % (n + 1), '设定/', '工具/小说检察官.py', '工具/镇冢秘术_防前后矛盾提示词系统.md',
          '阅读器/镇冢秘术_全本阅读器.html')        # ★1013：阅读器由本器同步，旧不收——381 实逮「不在本章所及之处」
    收 = [p for p in 路们 if p.startswith(前缀) or ('/' not in p and p.endswith(('.md', '.html')))]
    return 收, [p for p in 路们 if p not in 收]


def 十一轮已过(n, root=ROOT):
    """首回封版已跑过第十一轮（`版本/第N章/_十一轮.json` 在）——本器重跑之认据。"""
    return os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_十一轮.json'))


def 後(n, 试=False, root=ROOT):
    print('════ 封版·後（第%d章）%s════' % (n, '·试（⛔写、⛔提交）' if 试 else ''))
    缺 = 记之缺(n, root)
    if 缺 and not 试:
        print('⛔ 记席之档未齐：%s——回记席补（⛔本器代写）' % '、'.join(缺)); return False
    步 = []
    if not 试:
        步 += [('净重对表 --补', [器('净重对表.py'), '--补'], False), ('同步全本阅读器', [器('同步全本阅读器.py')], False),
              ('剧情链', [器('剧情链.py')], False)]      # ★1015 作者令：每章精读之详记串成从头到尾之链，封版即重生、随提交上 GitHub
    步 += [('回执对账', [器('回执对账.py')], True), ('开轮六检', [器('开轮六检.py'), str(n)], True),
          ('第零轮开镜庭', [器('第零轮开镜庭.py')], True), ('造式之实', [器('造式.py'), str(n)], True)]
    for 名, a, 必 in 步:
        rc, out, 秒 = 跑(a, root)
        末 = [l for l in out.split('\n') if l.strip()][-1:] or ['']
        if 名 == '开轮六检' and rc != 0 and 十一轮已过(n, root):
            # ★1013 重跑之实：首回已过第十一轮（_十一轮.json 在），章即「已封版」，⑭必红——那不是伤，是本器重跑；
            #   只免⑭，余检照判（拆法与全测同一把尺：全测._六检之败，⛔另写）
            import 全测
            r2, o2, _ = 跑([器('开轮六检.py'), str(n), '--静'], root)
            余 = 全测._六检之败(o2, True)
            if not 余:
                rc, 末 = 0, ['重跑：第十一轮已过，⑭（已封版）免；余检俱过']
            else:
                末 = ['；'.join(余)]
        print('  %s %-10s rc=%d %5.0fs  %s' % ('✓' if rc == 0 else '⛔', 名, rc, 秒, 末[0].strip()[:150]))
        if 必 and rc != 0:
            print('⛔ 停：%s 红——⛔提交；照其印治（记席之档或交总编辑）' % 名); return False
    if not 试:
        p = os.path.join(root, '版本', '第%d章' % n, '_席记.json')
        j = json.load(open(p, encoding='utf-8'))
        j.setdefault('段', {})['封版'] = '封版.py：净重对表补、阅读器同步、回执对账、开轮六检、开镜庭、造式之实、囤灰闸、第十一轮、全测俱过；提交、存底、撤锁（%s）' % time.strftime('%Y-%m-%d', time.gmtime())
        json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for 名, a in [('囤灰闸', [器('囤灰闸.py')]), ('第十一轮', [器('小说检察官.py'), '--十一轮', str(n)]), ('全测·快', [器('全测.py'), '--快'])]:
        if 试 and 名 == '第十一轮' and os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_十一轮.json')):
            print('  · 第十一轮：试·已有凭据（⛔重写）'); continue
        rc, out, 秒 = 跑(a, root)
        末 = [l for l in out.split('\n') if l.strip()][-1:] or ['']
        print('  %s %-10s rc=%d %5.0fs  %s' % ('✓' if rc == 0 else '⛔', 名, rc, 秒, 末[0].strip()[:150]))
        if rc != 0:
            print('⛔ 停：%s 红——⛔提交' % 名); return False
    if 试:
        print('✓ 试毕：诸闸俱过（⛔提交、⛔存底）'); return True
    st = subprocess.run(['git', '-c', 'core.quotepath=off', 'status', '--porcelain', '-uall'], cwd=root, capture_output=True, text=True).stdout
    路们 = [l[3:].strip().strip('"') for l in st.split('\n') if l.strip()]
    收, 弃 = 可提交(n, 路们)
    if 弃:
        print('  · 不在本章所及之处、⛔提交：%s' % '、'.join(弃))
    名 = re.sub(r'^.*?第.+?章_?', '', os.path.basename(正文档(n, root) or ''))[:-3]
    subprocess.run(['git', 'add', '--'] + 收, cwd=root, check=True)
    # ★1013：说明须标「封版#N」——改单闸认之为「新章封版之追记（係添不係改）」；缺之则推时改单红（381 实逮）
    msg = '第%d章《%s》封版（造式二代·封版#%d）：诸闸、第十一轮、全测俱过——记席之档（回执、锁定行、创作记录、全书记忆、状态册、open_brief、第%d章开镜卡）\n\n%s' % (n, 名, n, n + 1, 尾)
    r = subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=root, capture_output=True, text=True)
    print('  %s 提交 %s' % ('✓' if r.returncode == 0 else '⛔', subprocess.run(['git', 'log', '--oneline', '-1'], cwd=root, capture_output=True, text=True).stdout.strip()[:100]))
    if r.returncode != 0:
        print(r.stdout + r.stderr); return False
    for 名, a in [('存底 --存', [器('存底.py'), '--存', '第%d章封版' % n]), ('存底 --标', [器('存底.py'), '--标', str(n)]),
                 ('存底 --演', [器('存底.py'), '--演', str(n)]), ('云端验', [器('云端验.py')]), ('跑账', [器('跑账.py')]),
                 ('存底包', [器('存底包.py')]), ('撤锁', [器('心跳.py'), '--收', str(n)])]:
        rc, out, 秒 = 跑(a, root)
        末 = [l for l in out.split('\n') if l.strip()][-1:] or ['']
        print('  %s %-8s rc=%d %5.0fs  %s' % ('✓' if rc == 0 else '⚠', 名, rc, 秒, 末[0].strip()[:150]))
    print('✓ 封版毕。下一步（主环）：python3 工具/推.py（後台）')
    return True


def 自测():
    ok = 共 = 0
    d = 数(380)
    # 据 380 锁定行亲核之数（施工表 | 380 | 锁定 |）：白文 1 至 107 行、亮点 109、净重 2572、末版 v03、「＊」4 处（五拍）、sha1 a2f8fd36、与 v03 逐字同
    共 += 1; ok += (d.get('白文') == '1 至 107 行' and d.get('亮点行') == 109)
    共 += 1; ok += (d.get('净重') == 2572 and d.get('末版') == 'v03' and d.get('六数', '').startswith('净重2572｜段数48｜长段数7｜嗅0｜触8｜四字串三现4'))
    共 += 1; ok += (d.get('＊') == 4 and d.get('拍') == 5 and d.get('sha1', '').startswith('a2f8fd36') and d.get('与末版同') is True)
    共 += 1; ok += (d.get('总纲') == '| 380 | 主·148 |')
    收, 弃 = 可提交(381, ['正文/a.md', '版本/第381章/x', '版本/第382章/_开镜卡.md', '设定/y.json', 'README.md', '工具/z.py', '版本/第379章/v.md'])
    共 += 1; ok += (弃 == ['工具/z.py', '版本/第379章/v.md'] and len(收) == 5)
    共 += 1; ok += (记之缺(380) == [] and '下一章开镜卡' not in 记之缺(380))
    print('封版·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) >= 2 and a[0].isdigit() and a[1] in ('--前', '--後'):
        n = int(a[0])
        sys.exit(0 if (前(n) if a[1] == '--前' else 後(n, '--试' in a)) else 1)
    print(__doc__); sys.exit(2)
