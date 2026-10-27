# -*- coding: utf-8 -*-
"""总编辑复核——**规矩是死的，人是活的。总编辑逐条复核本仓之规：留、改、废，当场裁、当场生效。**

【其立之由（2026-09-25·作者令，逐字之意）】
  「你是总话事人，拥有对这本小说的至高决定权。规矩是死的，人是活的。之前设立的规则如果不利于这本小说写成
   中国第一，可以废除或修缮，完全由你自行决断，不需要我的指示。下面所有的东西都得听你的，由你来指导。
   把这个弄成一个机制，并且这个机制一定要行使起来。」
  ★本仓全测挂着近两百条规，**从来没有谁逐条问过一句：它让书更好了，还是在绑写的人的手？**

【唯一之问】对每一条规：**它护的是这本书的质量（让诸章合起来成中国第一），还是只在绑手、造数、逼刻意？**
  护质者留；护质而伤手者改；只绑手者废。**裁语须带实据**（它逮过哪一回真病／它逼出过哪一回凑字）。

【二路·机制之牙】（1027 执行之审 #28 #59 #70 #92 改）
  甲·**须行使·按章计**：末章 N 之前一章（N−1）封版以来，须至少有一裁 → 否则红。
     裁＝本账之裁，或 `设定/法用册.json`「废」之「废于」（汰一法即是一裁·同功⛔两处各记）。
     旧以 48 小时之钟计：停写之中钟照走、器红到限，拦下的恰是治它的那一推（丝滑主义所忌）——今只在写章时催。
  丙·**进度**：印已复核几条／共几条，并印下三条待复核者——每一坐至少裁一条。
  （旧乙路「裁废而仍挂全测」并入 `工具/法用之守.py` 之所废除尽：裁「废」者於法用册「废」添一条，去证 `{"无格": "<规名>"}`，
   法用之守 验其已除、并於废前之树验其真红——⛔两处各验。）

用法：
  python3 工具/总编辑复核.py                      # 印进度与下三条待复核
  python3 工具/总编辑复核.py --裁 <规名> 留|改|废 "<实据与其由>"
  python3 工具/总编辑复核.py --查                 # 甲乙两路（全测用）
  python3 工具/总编辑复核.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join(ROOT, '设定', '总编辑复核账.json')


def 规之册():
    s = open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read()
    # ★1017：并认起首之元组表（('检察官自测', chk_selftest) 一类八条——旧式只认 items.append，裁之亦不入册）
    名们 = re.findall(r"items\.append\(\('([^']+)'", s) + re.findall(r"\('([^']+)',\s*chk_\w+\)", s)
    seen, out = set(), []
    for n in 名们:
        if n not in seen:
            seen.add(n); out.append(n)
    return out


def 读账():
    try:
        return json.load(open(账档, encoding='utf-8'))
    except Exception:
        return {'裁': []}


def 写账(d):
    t = 账档 + '.tmp'
    json.dump(d, open(t, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(t, 账档)


def 裁(名, 判, 由):
    if 判 not in ('留', '改', '废'):
        print('⛔判只许 留／改／废'); return False
    if len(由) < 12:
        print('⛔裁语须带实据（它逮过哪一回真病／逼出过哪一回凑字），不许一句空话'); return False
    d = 读账()
    d['裁'].append({'规': 名, '判': 判, '由': 由, '时': time.strftime('%Y-%m-%d %H:%M:%S')})
    写账(d)
    print('✓总编辑裁：「%s」→ %s｜%s' % (名, 判, 由))
    if 判 == '废':
        print('  ⛔裁了废，须当场从 全测.py 与其所挂之处撤下，并於 设定/法用册.json「废」添一条（去证 {"无格": "%s"}、在＝废前之笔）'
              '——法用之守 验其除尽（裁了不废是纸上的裁）。' % 名)
    return True


def _末章():
    import glob
    from 对账预筛 import 章号
    ns = [章号(f) for f in glob.glob(os.path.join(ROOT, '正文', '*.md'))]
    ns = [n for n in ns if n]
    return max(ns) if ns else 0


def 封时(n):
    """第 n 章封版之时（epoch）：其正文档初入库之提交之时（封版#n 一提交载之）；寻不着 → None。"""
    import subprocess
    try:
        import 章料
        f = 章料.章档(n, ROOT)
        if not f:
            return None
        r = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%ct', '-1', '--', os.path.relpath(f, ROOT)],
                           cwd=ROOT, capture_output=True, text=True, timeout=60)
        return int(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


def 诸裁之时(d=None, 册=None):
    """→ [epoch]：本账之裁之时＋法用册「废」之「废于」（MMDD，作其日之末）。"""
    d = d if d is not None else 读账()
    时们 = []
    for x in d.get('裁', []):
        try:
            时们.append(time.mktime(time.strptime(x['时'], '%Y-%m-%d %H:%M:%S')))
        except (KeyError, ValueError):
            pass
    if 册 is None:
        try:
            册 = json.load(open(os.path.join(ROOT, '设定', '法用册.json'), encoding='utf-8'))
        except Exception:
            册 = {}
    年 = time.localtime().tm_year
    for x in 册.get('废') or []:
        m = re.fullmatch(r'(\d{2})(\d{2})', str(x.get('废于', '')).strip())
        if not m:
            continue
        try:
            t0 = time.mktime(time.strptime('%d-%s-%s 23:59:59' % (年, m.group(1), m.group(2)), '%Y-%m-%d %H:%M:%S'))
        except ValueError:
            continue
        if t0 > time.time() + 86400:          # 跨年：MMDD 在今日之後者係去年
            t0 = time.mktime(time.strptime('%d-%s-%s 23:59:59' % (年 - 1, m.group(1), m.group(2)), '%Y-%m-%d %H:%M:%S'))
        时们.append(t0)
    return 时们


def 甲之判(末=None, 封=None, 时们=None):
    """→ 红之由（''＝不红）。末章 N 之前一章封版以来须有一裁；前章封时寻不着 → 不判（⛔挡推於器病）。"""
    末 = 末 if 末 is not None else _末章()
    时们 = 时们 if 时们 is not None else 诸裁之时()
    if not 时们:
        return '甲·总编辑复核一条也没裁过（法用册亦无一废）——权不行使，等於没有'
    t0 = (封 or 封时)(末 - 1)
    if t0 is None:
        return ''
    if max(时们) < t0:
        return ('甲·第%d章封版（%s）以来无一裁——写第%d章须先裁一条（python3 工具/总编辑复核.py --裁 <规> 留|改|废 "<实据>"，'
                '或汰一法入法用册「废」）' % (末 - 1, time.strftime('%m-%d %H:%M', time.localtime(t0)), 末))
    return ''


def 查(印=True):
    坏 = []
    甲 = 甲之判()
    if 甲:
        坏.append(甲)
    if 印:
        for x in 坏:
            print('  ⛔ ' + x)
        if not 坏:
            print('  ✓ 总编辑复核：前章封版以来有裁，权在行使（裁废之除尽归 法用之守）。')
    return not 坏, 坏


def 进度():
    d = 读账(); 册 = 规之册()
    已 = {x['规'] for x in d['裁']}
    待 = [n for n in 册 if n not in 已]
    print('════ 总编辑复核 ════（规矩是死的，人是活的：留／改／废，由总编辑当场裁）')
    print('  已复核 %d 条｜全测挂规 %d 条｜待复核 %d 条' % (len(已 & set(册)), len(册), len(待)))
    for x in d['裁'][-3:]:
        print('  · 近裁：「%s」→ %s｜%s' % (x['规'], x['判'], x['由'][:60]))
    print('  ★下三条待复核（每一坐至少裁一条；只问：它护质，还是绑手？）：')
    for n in 待[:3]:
        print('     · %s' % n)
    查()


def 自测():
    import tempfile
    global 账档
    旧 = 账档
    账档 = os.path.join(tempfile.mkdtemp(), 'z.json')
    r = []
    try:
        r.append(('①空账且法用册无废即红（权不行使）', bool(甲之判(末=411, 封=lambda n: 1000.0, 时们=[]))))
        r.append(('②裁语太短不收', not 裁('x', '留', '好')))
        r.append(('③判只许留改废', not 裁('x', '毁', '这一条逼出过三回凑字，废之')))
        裁('爆窗', '留', '0924 逮过 363 之窗爆一回，护质')
        r.append(('④新裁入账，其时可读', len(诸裁之时(册={})) == 1))
        T封 = time.mktime(time.strptime('2026-10-24 05:16:00', '%Y-%m-%d %H:%M:%S'))
        前 = time.mktime(time.strptime('2026-10-22 14:00:00', '%Y-%m-%d %H:%M:%S'))
        後 = time.mktime(time.strptime('2026-10-24 09:00:00', '%Y-%m-%d %H:%M:%S'))
        r.append(('⑤按章计：写 411 而 410 封版以来无一裁 → 红；有一裁 → 过', bool(甲之判(411, lambda n: T封, [前]))
                  and 甲之判(411, lambda n: T封, [前, 後]) == ''))
        _册 = {'废': [{'id': 'x', '废于': '1027'}, {'id': 'y', '废于': '坏'}]}
        _时 = 诸裁之时({'裁': [{'时': '2026-10-22 14:00:00'}]}, _册)
        r.append(('⑥法用册「废」之「废于」亦算一裁（1027 汰旧即行使·同功⛔两处各记）', len(_时) == 2 and 甲之判(411, lambda n: T封, _时) == ''))
        r.append(('⑦停写之中⛔按时逾限（旧 48 时之钟：末裁 120 时前即红；今前章封後有裁即过）',
                  甲之判(411, lambda n: T封, [後]) == '' and time.time() - 後 > 48 * 3600))
        r.append(('⑧前章封时寻不着 → 不判（⛔挡推於器病）', 甲之判(411, lambda n: None, [前]) == ''))
        r.append(('⑨乙路已并入法用之守（⛔两处各验）：本器⛔再数全测之格', '乙·裁了「废」' not in open(__file__, encoding='utf-8').read().split('def 自测')[0]))
        import subprocess as _sp
        _浅 = _sp.run(['git', 'rev-parse', '--is-shallow-repository'], cwd=ROOT, capture_output=True, text=True).stdout.strip() == 'true'
        r.append(('⑩真读：410 之封时读得出（浅克隆无其史者免·⑧ 之不判）', isinstance(封时(410), int) or _浅))
        # ⑪复核补·回灌真账（⛔只靠造局）：db52f247 之复核账（末裁 1022）而法用册无废 → 写 411（410 封於 1024）即红；
        #   今之法用册（1027 汰旧之「废于」）算裁 → 过（放行之反例）
        _旧 = _sp.run(['git', 'show', 'db52f247:设定/总编辑复核账.json'], cwd=ROOT, capture_output=True, text=True)
        if _旧.returncode == 0 and 封时(410):
            _旧账 = json.loads(_旧.stdout)
            r.append(('⑪回灌真账：db52f247 之复核账、法用册无废 → 写 411 即红；今法用册「废于」算裁 → 过',
                      bool(甲之判(411, 封时, 诸裁之时(_旧账, {}))) and 甲之判(411, 封时, 诸裁之时(_旧账)) == ''))
        else:
            print('  · ⑪旧树或封时不在（浅克隆）——略')
    finally:
        账档 = 旧
    for n, v in r:
        print(('  ✓ ' if v else '  ⛔ ') + n)
    print('负测·总编辑复核 %d/%d' % (sum(v for _, v in r), len(r)))
    return all(v for _, v in r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--查' in a:
        sys.exit(0 if 查()[0] else 1)
    if '--裁' in a:
        i = a.index('--裁')
        sys.exit(0 if 裁(a[i + 1], a[i + 2], a[i + 3]) else 1)
    进度()
